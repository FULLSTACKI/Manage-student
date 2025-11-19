import seaborn as sns 

class ChartMapper: 
    @staticmethod
    def _get_chart_type(chart_type: str):
        map_chart = {
            "Line Chart": lambda data, x_col, y_col, ax: sns.lineplot(data=data, x=x_col, y=y_col, marker="o", ax=ax),
            "Bar Chart": lambda data, x_col, y_col, ax: sns.barplot(data=data, x=x_col, y=y_col, ax=ax),
            "Scatter Plot": lambda data, x_col, y_col, ax: sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax),
            "Pie Chart": lambda data, x_col, y_col, ax: data.groupby(x_col)[y_col].sum().plot.pie(
                autopct='%1.1f%%', startangle=90, ylabel='', ax=ax
            )
        }
        return map_chart.get(chart_type)