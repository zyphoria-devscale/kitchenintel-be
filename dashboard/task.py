from typing import List

from huey import crontab

from shared.utils import graph_data
from dashboard.graph_generator import GraphGenerator
from dashboard.method import generate_insight
from dashboard.models import Dashboard, Graph, WEEKLY_DASHBOARD
import datetime
from huey.contrib.djhuey import periodic_task,task
from dashboard.queries import get_order_details

# For day-of-week, 0=Sunday and 6=Saturday.
# Time is in UTC.
@periodic_task(crontab(day_of_week=0,hour=17,minute=0),retries=2,retry_delay=60)
def weekly():
    print("start scheduler weekly task: weekly()")

    to_date = datetime.date.today()
    from_date = to_date - datetime.timedelta(days=7)
    data = get_order_details(from_date, to_date)

    generator = GraphGenerator(data=data)
    heat_map = generator.generate_hourly_sales_heatmap(save_path="media/weekly")
    total_sales_over_time = generator.generate_graph_total_sales_over_time_by_date(save_path="media/weekly")
    top_selling_menu = generator.generate_graph_top_selling_menu_item(save_path="media/weekly")
    top_category = generator.generate_graph_total_sales_by_category(save_path="media/weekly")

    data = [heat_map,total_sales_over_time,top_selling_menu,top_category]
    insight = generate_insight(data)
    insert_to_db(WEEKLY_DASHBOARD, data, insight, from_date, to_date)
    print("end scheduler weekly task: weekly()")


def insert_to_db(type_dashboard: str, data: List[graph_data], insight: str, from_date: datetime.date, to_date: datetime.date):
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
            dashboard=dashboard
        )
        graph.save()
