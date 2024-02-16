import json

import pandas as pd
import plotly.express as px
import plotly.offline as offline


def load_graph() -> None:
    data = pd.read_excel(
        'data\\AE33-S09-01249\\2023_07_AE33-S09-01249.xlsx',
    )
    data['day'] = data['Datetime'].apply(
        lambda x: "-".join(
            x.split()[0].split('.')[::-1]
        ) + " " + x.split()[1]
    )
    data['day'] = pd.to_datetime(
        data['day'], format='%Y-%m-%d %H:%M',
    )
    m = max(data['day'])
    cols = list(
        set(data.columns.to_list()) - set(['Datetime', 'date'])
    )
    last_48_hours = [m.replace(day=(m.day - 2)), max(data['day'])]
    fig = px.line(
        data,
        x='day',
        y=cols,
        range_x=last_48_hours
    )
    fig.update_layout(
        legend_itemclick='toggle'
    )
    offline.plot(
        fig,
        filename='templates/graph.html',
        auto_open=False
    )


def preprocessing_file(path: str) -> None:
    device = path.split('\\')[-2]
    df = pd.read_csv(path, sep=None, engine='python')
    time_col = json.load(
        open('config_devices.json', 'r')
    )[device]['time_cols']
    if device == "AE33-S09-01249":
        df[time_col] = pd.to_datetime(
            df[time_col],
            format="%d.%m.%Y %H:%M"
        )
    if device == "LVS" or device == "PNS":
        col = list(df.columns)
        try:
            df = df.drop('Error', axis=1)
        except KeyError:
            pass
        try:
            col.remove("Time")
        except ValueError:
            pass
        df.columns = col
        df[time_col] = pd.to_datetime(
            df[time_col],
            format="%d.%m.%Y %H:%M:%S",
        )
    if device == "TCA08":
        df[time_col] = pd.to_datetime(
            df[time_col],
            format="%Y-%m-%d %H:%M:%S",
        )
    if device == "Web_MEM":
        df[time_col] = pd.to_datetime(
            df[time_col],
            format="%d.%m.%Y %H:%M",
        )
    cols_to_draw = json.load(
        open('config_devices.json', 'r')
    )[device]['cols']
    time_col = json.load(
        open('config_devices.json', 'r')
    )[device]['time_cols']
    df = df[cols_to_draw + [time_col]]
    df = df.map(
        lambda x: x.strip()
        if isinstance(x, str) else x
    )
    df.to_csv(path, index=False)
