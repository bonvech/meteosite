import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import plotly.offline as offline


async def load_graph() -> None:
    data = pd.read_excel('C:\\Users\\ivank\\PycharmProjects\\meteosite\\data\\AE33-S09-01249\\2023_07_AE33-S09-01249.xlsx')
    data['day'] = data['Datetime'].apply(lambda x: "-".join(x.split()[0].split('.')[::-1]) + " " + x.split()[1])
    data['day'] = pd.to_datetime(data['day'], format='%Y-%m-%d %H:%M')
    m = max(data['day'])
    cols = list(set(data.columns.to_list()) - set(['Datetime', 'date']))
    last_48_hours = [m.replace(day=(m.day - 2)), max(data['day'])]
    fig = px.line(data, x='day', y=cols, range_x=last_48_hours)
    fig.update_layout(legend_itemclick='toggle')
    offline.plot(fig, filename='templates/graph.html', auto_open=False)
