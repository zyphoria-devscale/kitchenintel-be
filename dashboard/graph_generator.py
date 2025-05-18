from typing import Tuple, List, Any
import pandas as pd
import seaborn as sns
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from shared.utils import graph_data, generate_id, delete_file_graph, convert_numpy_for_json
from core.ai.bucket import Bucket
from core.ai.promt_manager import PromptManager
from core.ai.prompts import PROMPT_GRAPH_DESC, PROMPT_GRAPH_MENU_CHART_DESC


class GraphGenerator:
    def __init__(self, data: List[Tuple[Any, ...]]):
        columns = [
            "order_no", "menu_name", "category", "quantity",
            "price_at_order_time", "subtotal", "notes", "order_date"
        ]
        self.data = pd.DataFrame(data, columns=columns)
        self.unique_id = generate_id()
        self.bucket = Bucket()
        self.prompt_manager = PromptManager()

    def _finalize_graph(self, filename: str, title: str, prompt: str, user_prompt: str, raw_data):
        plt.tight_layout()
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        image_url = self.bucket.upload_file(filename)
        self.prompt_manager.add_system_message(prompt.format(VISUALIZATION_TYPE=title))
        self.prompt_manager.add_message_with_image('user', user_prompt.format(title=title), image_url)
        description = self.prompt_manager.generate()
        delete_file_graph(filename)
        return graph_data(title, image_url, description, raw_data=raw_data)

    def generate_graph_top_selling_menu_item(self, save_path) -> graph_data:
        filename = f"{save_path}/{self.unique_id}_top_selling_menu_item.png"
        title = "Top Twenty Selling Menu Item"
        plt.figure(figsize=(10, 6))

        top_items = self.data.groupby('menu_name')['quantity'].sum().sort_values(ascending=False)
        top_10 = top_items.iloc[:20]
        others_sum = top_items.iloc[20:].sum()

        plot_data = pd.DataFrame({
            'menu_name': list(top_10.index) + (['Others'] if others_sum else []),
            'quantity': list(top_10.values) + ([others_sum] if others_sum else [])
        })
        plot_data['is_others'] = plot_data['menu_name'] == 'Others'
        plot_data.sort_values(by=['is_others', 'quantity'], ascending=[True, False], inplace=True)

        colors = sns.color_palette('viridis', n_colors=len(plot_data) - 1) + [(0.7, 0.7, 0.7)]
        sns.barplot(x='quantity', y='menu_name', hue='menu_name',data=plot_data, palette=colors, dodge=False, legend=False)

        for i, v in enumerate(plot_data['quantity']):
            plt.text(v + 0.1, i, f"{int(v)}", va='center')

        plt.xlabel('Total Quantity Sold')
        plt.ylabel('Menu Item')
        plt.title(title)

        raw_data = {
            "top_10": top_10.to_dict(),
            "others": {"count": len(top_items) - 10, "total_quantity": others_sum},
            "all_data": top_items.to_dict()
        } if others_sum else top_items.to_dict()

        return self._finalize_graph(filename, title, PROMPT_GRAPH_MENU_CHART_DESC,
                                    'give me the report of {title}', convert_numpy_for_json(raw_data))

    def generate_graph_total_sales_by_category(self, save_path) -> graph_data:
        filename = f"{save_path}/{self.unique_id}_total_sales_by_category.png"
        title = "Total Sales by Category"
        plt.figure(figsize=(8, 5))

        category_sales = self.data.groupby('category')['subtotal'].sum().sort_values(ascending=False)
        sns.barplot(x=category_sales.values, y=category_sales.index,hue=category_sales.index, palette='magma', legend=False)

        plt.xlabel('Total Sales (Rp) in Millions')
        plt.ylabel('Category')
        plt.title(title)

        return self._finalize_graph(filename, title, PROMPT_GRAPH_DESC,
                                    "give me the report of {title}, exclude 'others'",
                                    category_sales.to_json())

    def generate_graph_total_sales_over_time_by_date(self, save_path) -> graph_data:
        filename = f"{save_path}/{self.unique_id}_total_sales_over_time_by_date.png"
        title = "Total Sales Over Time by Date"
        self.data['created_at_date'] = pd.to_datetime(self.data['order_date']).dt.date
        daily_sales = self.data.groupby('created_at_date')['subtotal'].sum()

        plt.figure(figsize=(11, 5))
        ax = sns.lineplot(x=daily_sales.index, y=daily_sales.values, marker='o')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Total Sales (Rp) in Millions')
        plt.title(title)

        return self._finalize_graph(filename, title, PROMPT_GRAPH_DESC,
                                    'give me the report of {title}', daily_sales.to_json())

    def generate_graph_total_sales_by_hour_time(self, save_path) -> graph_data:
        filename = f"{save_path}/{self.unique_id}_total_sales_by_hour_time.png"
        title = "Total Sales Over Time by Hour"
        self.data['hour'] = pd.to_datetime(self.data['order_date']).dt.hour
        hourly_sales = self.data.groupby('hour')['subtotal'].sum()

        plt.figure(figsize=(10, 5))
        sns.lineplot(x=hourly_sales.index, y=hourly_sales.values, marker='o')
        plt.xlabel('Hour')
        plt.ylabel('Total Sales (Rp) in Millions')
        plt.title(title)

        return self._finalize_graph(filename, title, PROMPT_GRAPH_DESC,
                                    'give me the report of {title}', hourly_sales.to_json())

    def generate_hourly_sales_heatmap(self, save_path) -> graph_data:
        filename = f"{save_path}/{self.unique_id}_hourly_sales_heatmap.png"
        title = "Hourly Sales Heatmap by Day of Week"

        self.data['order_date'] = pd.to_datetime(self.data['order_date'])
        self.data['hour'] = self.data['order_date'].dt.hour
        self.data['day'] = self.data['order_date'].dt.day_name()

        pivot = self.data.pivot_table(index='day', columns='hour', values='subtotal', aggfunc='sum', fill_value=0)
        pivot = pivot.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        pivot = pivot.loc[:, (pivot.sum() > 0)].astype(float)

        plt.figure(figsize=(max(10, min(20, int(len(pivot.columns) * 0.8))), 8))
        mask = pivot == 0
        ax = sns.heatmap(pivot, cmap='YlOrRd', annot=True, fmt='.0f', linewidths=0.5,
                         cbar_kws={'label': 'Total Sales (Rp)', 'shrink': 0.8}, mask=mask,
                         annot_kws={"size": 9})

        for t in ax.texts:
            if t.get_text() != '0':
                try:
                    t.set_text(f"{float(t.get_text()):,.0f}")
                except ValueError:
                    pass

        plt.title(title, fontsize=16, pad=20)
        plt.xlabel('Hour of Day (24-hour format)', fontsize=12)
        plt.ylabel('Day of Week', fontsize=12)

        plt.xticks(np.arange(0.5, len(pivot.columns) + 0.5), [f"{h:02d}:00" for h in pivot.columns], rotation=45)

        peak_hour = pivot.sum().idxmax()
        peak_day = pivot.sum(axis=1).idxmax()
        business_hours = f"{min(pivot.columns):02d}:00-{max(pivot.columns):02d}:00"

        plt.figtext(0.5, 0.01,
                    f"Peak sales hour: {peak_hour:02d}:00 | Peak sales day: {peak_day} | Business hours: {business_hours}",
                    ha="center", fontsize=12, bbox={"facecolor": "lightgray", "alpha": 0.5, "pad": 5})

        return self._finalize_graph(filename, title, PROMPT_GRAPH_DESC,
                                    'give me the report of {title}', convert_numpy_for_json(pivot.to_dict()))
