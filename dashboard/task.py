import datetime
from typing import List

from huey import crontab
from huey.contrib.djhuey import periodic_task
from shared.utils import graph_data

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
    print("insert to db")
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
    print("insert to db")
    insert_to_db(MONTHLY_DASHBOARD, data, insight, from_date, to_date)
    print("end scheduler monthly task: monthly()")


def insert_to_db(
    type_dashboard: str,
    data: List[graph_data],
    insight: str,
    from_date: datetime.date,
    to_date: datetime.date,
):
    dashboard = Dashboard(type_dashboard=type_dashboard, insight=insight)
    dashboard.save()
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
