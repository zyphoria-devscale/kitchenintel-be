import datetime
from typing import List

from huey import crontab
from huey.contrib.djhuey import periodic_task, task
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
    print("start scheduler weekly task: weekly()")

    to_date = datetime.date.today()
    from_date = to_date - datetime.timedelta(days=7)
    print(f"get order details from: {from_date} to: {to_date}")
    data = get_order_details(from_date, to_date)

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

    print("generate insight")
    data = [heat_map, total_sales_over_time, top_selling_menu, top_category]
    insight = generate_insight(data)

    insert_to_db(WEEKLY_DASHBOARD, data, insight, from_date, to_date)
    print("end scheduler weekly task: weekly()")


@periodic_task(crontab(day=1), retries=2, retry_delay=60)
def monthly():
    print("start scheduler monthly task: monthly()")
    to_date = datetime.date.today() - datetime.timedelta(days=1)
    from_date = datetime.date(to_date.year, to_date.month, 1)
    print(f"get order details from: {from_date} to: {to_date}")
    data = get_order_details(from_date, to_date)

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

    print("generate insight")
    data = [heat_map, total_sales_over_time, top_selling_menu, top_category]
    insight = generate_insight(data)

    insert_to_db(MONTHLY_DASHBOARD, data, insight, from_date, to_date)
    print("end scheduler monthly task: monthly()")


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
    print("start scheduler daily task: daily()")
    today = datetime.date.today()
    data = get_order_details(today, today)
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
    insert_to_chroma(graphs, "daily")
    print("end scheduler daily task: daily()")


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
