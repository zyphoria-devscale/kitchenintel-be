import datetime
from typing import List

from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from django.core.cache import cache
from shared.utils import graph_data, date_to_string, date_to_timestamp
from core.ai.chromadb import chroma, openai_ef

from dashboard.graph_generator import GraphGenerator
from dashboard.method import generate_insight
from dashboard.models import MONTHLY_DASHBOARD, WEEKLY_DASHBOARD, Dashboard, Graph
from dashboard.queries import get_order_details


# For day-of-week, 0=Sunday and 6=Saturday.
# Time is in UTC.
@periodic_task(crontab(day_of_week=0, hour=17, minute=0), retries=2, retry_delay=60)
def weekly():
    # Create a lock key for the current week
    today = datetime.date.today()
    # Get the week number and year for a unique weekly key
    year, week_num, _ = today.isocalendar()
    lock_key = f'weekly_task_lock_{year}_week_{week_num}'
    
    # Check if the task has already run this week
    if cache.get(lock_key):
        print(f"Weekly task already ran successfully for week {week_num} of {year}. Skipping.")
        return
    
    try:
        print("start scheduler weekly task: weekly()")
        
        # Set a temporary lock to indicate we're running
        cache.set(lock_key + '_running', True, 7200)  # 2 hour timeout
        
        to_date = datetime.date.today()
        from_date = to_date - datetime.timedelta(days=7)
        print(f"get order details from: {from_date} to: {to_date}")
        
        # Get order details
        data = get_order_details(from_date, to_date)
        if not data:
            print("Warning: No order details found for the week")
            return

        # Generate graphs
        print("generate graph")
        generator = GraphGenerator(data=data)
        print("generate heatmap")
        heat_map = generator.generate_hourly_sales_heatmap(save_path="media/weekly")
        print("generate total sales over time")
        total_sales_over_time = generator.generate_graph_total_sales_over_time_by_date(
            save_path="media/weekly"
        )
        print("generate top selling menu")
        top_selling_menu = generator.generate_graph_top_selling_menu_item(
            save_path="media/weekly"
        )
        print("generate top category")
        top_category = generator.generate_graph_total_sales_by_category(
            save_path="media/weekly"
        )

        # Generate insight and save to DB
        print("generate insight")
        data = [heat_map, total_sales_over_time, top_selling_menu, top_category]
        insight = generate_insight(data)

        insert_to_db(WEEKLY_DASHBOARD, data, insight, from_date, to_date)
        
        # Set a lock that lasts until the end of the week (plus 1 day buffer)
        # This prevents the task from running again this week
        next_week = today + datetime.timedelta(days=7-today.weekday()+1)
        next_week = datetime.datetime.combine(next_week, datetime.time(0, 0))
        seconds_until_next_week = int((next_week - datetime.datetime.now()).total_seconds())
        cache.set(lock_key, True, seconds_until_next_week)
        
        print("end scheduler weekly task: weekly()")
    except Exception as e:
        print(f"Error in weekly task: {e}")
        # Don't set the completion lock if there was an error
        raise
    finally:
        # Always clear the running lock
        cache.delete(lock_key + '_running')


@periodic_task(crontab(day=1), retries=2, retry_delay=60)
def monthly():
    # Create a lock key for the current month
    today = datetime.date.today()
    lock_key = f'monthly_task_lock_{today.year}_{today.month}'
    
    # Check if the task has already run this month
    if cache.get(lock_key):
        print(f"Monthly task already ran successfully for {today.year}-{today.month}. Skipping.")
        return
    
    try:
        print("start scheduler monthly task: monthly()")
        
        # Set a temporary lock to indicate we're running
        cache.set(lock_key + '_running', True, 7200)  # 2 hour timeout
        
        to_date = datetime.date.today() - datetime.timedelta(days=1)
        from_date = datetime.date(to_date.year, to_date.month, 1)
        print(f"get order details from: {from_date} to: {to_date}")
        
        # Get order details
        data = get_order_details(from_date, to_date)
        if not data:
            print("Warning: No order details found for the month")
            return

        # Generate graphs
        print("generate graph")
        generator = GraphGenerator(data=data)
        print("generate heatmap")
        heat_map = generator.generate_hourly_sales_heatmap(save_path="media/monthly")
        print("generate total sales over time")
        total_sales_over_time = generator.generate_graph_total_sales_over_time_by_date(
            save_path="media/monthly"
        )
        print("generate top selling menu")
        top_selling_menu = generator.generate_graph_top_selling_menu_item(
            save_path="media/monthly"
        )
        print("generate top category")
        top_category = generator.generate_graph_total_sales_by_category(
            save_path="media/monthly"
        )

        # Generate insight and save to DB
        print("generate insight")
        data = [heat_map, total_sales_over_time, top_selling_menu, top_category]
        insight = generate_insight(data)

        insert_to_db(MONTHLY_DASHBOARD, data, insight, from_date, to_date)
        
        # Set a lock that lasts until the end of the month (plus 1 day buffer)
        if today.month == 12:
            next_month = datetime.date(today.year + 1, 1, 2)
        else:
            next_month = datetime.date(today.year, today.month + 1, 2)
        next_month = datetime.datetime.combine(next_month, datetime.time(0, 0))
        seconds_until_next_month = int((next_month - datetime.datetime.now()).total_seconds())
        cache.set(lock_key, True, seconds_until_next_month)
        
        print("end scheduler monthly task: monthly()")
    except Exception as e:
        print(f"Error in monthly task: {e}")
        # Don't set the completion lock if there was an error
        raise
    finally:
        # Always clear the running lock
        cache.delete(lock_key + '_running')


@task(retries=2, retry_delay=60)
def insert_to_db(
    type_dashboard: str,
    data: List[graph_data],
    insight: str,
    from_date: datetime.date,
    to_date: datetime.date,
):
    print("start insert to db graph: insert_to_db_graph()")
    dashboard = Dashboard(type_dashboard=type_dashboard, insight=insight)
    dashboard.save()
    graphs = []
    for i in data:
        graph = Graph(
            title=i.title,
            description=i.description,
            raw_data=i.raw_data,
            url=i.url,
            from_date=from_date,
            to_date=to_date,
            dashboard=dashboard,
        )
        graph.save()
        graphs.append(graph)
    insert_to_chroma(graphs, type_dashboard)
    print("end insert to db graph: insert_to_db_graph()")


@periodic_task(crontab(hour=17), retries=2, retry_delay=60)
def daily():
    # Create a lock key with today's date to ensure uniqueness per day
    today = datetime.date.today()
    lock_key = f'daily_task_lock_{today.isoformat()}'
    
    # Check if the task has already run today
    if cache.get(lock_key):
        print(f"Daily task already ran successfully today ({today}). Skipping.")
        return
    
    try:
        print("start scheduler daily task: daily()")
        
        # Set a temporary lock to indicate we're running
        # This will expire after 2 hours (7200 seconds) in case the task crashes
        cache.set(lock_key + '_running', True, 7200)
        
        # Get order details
        data = get_order_details(today, today)
        if not data:
            print("Warning: No order details found for today")
            return
            
        # Generate graphs
        generator = GraphGenerator(data=data)
        total_sales_hour_time = generator.generate_graph_total_sales_by_hour_time(
            save_path="media/daily"
        )
        top_selling_menu = generator.generate_graph_top_selling_menu_item(
            save_path="media/daily"
        )
        top_category = generator.generate_graph_total_sales_by_category(
            save_path="media/daily"
        )

        # Save to database
        data = [total_sales_hour_time, top_selling_menu, top_category]
        graphs = []
        for i in data:
            graph = Graph(
                title=i.title,
                description=i.description,
                raw_data=i.raw_data,
                url=i.url,
                from_date=today,
                to_date=today,
            )
            graph.save()
            graphs.append(graph)
            
        # Insert to ChromaDB
        if graphs:
            insert_to_chroma(graphs, "daily")
        
        # Set a lock that lasts until the end of the day (plus 1 hour buffer)
        # This prevents the task from running again today even if it completes successfully
        tomorrow = datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time(1, 0))
        seconds_until_tomorrow = int((tomorrow - datetime.datetime.now()).total_seconds())
        cache.set(lock_key, True, seconds_until_tomorrow)
        
        print("end scheduler daily task: daily()")
    except Exception as e:
        print(f"Error in daily task: {e}")
        # Don't set the completion lock if there was an error
        # This allows the task to be retried
        raise
    finally:
        # Always clear the running lock
        cache.delete(lock_key + '_running')


@task(retries=2, retry_delay=60)
def insert_to_chroma(data: List[Graph], type_dashboard: str):
    print("start insert to db graph: insert_to_db_graph()")
    metadatas = []
    for i in data:
        meta = {
            "title": i.title,
            "url": i.url,
            "from_date_string": date_to_string(i.from_date),
            "to_date_string": date_to_string(i.to_date),
            "from_date_timestamp": date_to_timestamp(i.from_date),
            "to_date_timestamp": date_to_timestamp(i.to_date),
            "dashboard": type_dashboard,
        }
        metadatas.append(meta)

    collection = chroma.get_or_create_collection(
        name="dashboard", embedding_function=openai_ef
    )

    collection.add(
        ids=[str(i.id) for i in data],
        documents=[i.description for i in data],
        metadatas=metadatas,
    )
    print("end insert to db graph: insert_to_db_graph()")
