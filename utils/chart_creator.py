import pandas as pd
import altair as alt
from datetime import datetime
import streamlit as st


def create_chart(yfinance_data, news_data):
    close_data = yfinance_data["Close"]
    df_close = pd.DataFrame(list(close_data.items()), columns=["Timestamp", "Close"])

    # Convert timestamps to datetime
    df_close["Date"] = pd.to_datetime(
        df_close["Timestamp"].astype(int), unit='ms'
    ).dt.strftime('%Y-%m-%d')
    df_close.set_index("Date", inplace=True)
    df_close.drop(columns=["Timestamp"], inplace=True)

    # Convert news JSON data to DataFrame
    df_news = pd.DataFrame(news_data)
    df_news["Date"] = pd.to_datetime(df_news["publishedAt"])
    df_news["publishedAt"] = pd.to_datetime(df_news["publishedAt"], errors='coerce')
    df_news = df_news.dropna(subset=['publishedAt'])

    def convert_datetime_to_string(dt):
        if isinstance(dt, datetime):
            return dt.strftime('%Y-%m-%d')
        return dt

    for i, row in df_news.iterrows():
        df_news.at[i, 'publishedAt'] = convert_datetime_to_string(row['publishedAt'])

    df_news["Date"] = df_news["publishedAt"]
    news_count = df_news.groupby("Date").size().reset_index(name='News Count')
    news_count["Date"] = pd.to_datetime(news_count["Date"])
    df_close.index = pd.to_datetime(df_close.index)

    # Merge stock prices and news count data
    df_combined = df_close.merge(
        news_count, how='left', left_index=True, right_on='Date'
    )
    df_combined.set_index("Date", inplace=True)
    df_combined['News Count'].fillna(0, inplace=True)

    # Aggregate data to reduce number of points (e.g., weekly)
    df_combined = (
        df_combined.resample('W')
        .agg({'Close': 'mean', 'News Count': 'sum'})
        .reset_index()
    )

    # Create selection for hover effect
    nearest = alt.selection_point(
        nearest=True, on='mouseover', fields=['Date'], empty='none'
    )

    # Base chart
    base = alt.Chart(df_combined).encode(
        alt.X('Date:T', title='Date', axis=alt.Axis(format='%Y-%m-%d'))
    )

    # Line chart for Close
    line = base.mark_line(color='blue').encode(
        alt.Y('Close:Q', title='Stock Close Price')
    )

    # Bar chart for News Count
    bar = base.mark_bar(color='orange', opacity=0.5).encode(
        alt.Y('News Count:Q', title='News Count')
    )

    # Add vertical line for tooltip
    rule = (
        base.mark_rule(color='gray')
        .encode(
            opacity=alt.condition(nearest, alt.value(0.5), alt.value(0)),
            size=alt.value(2),
            tooltip=[
                alt.Tooltip('Date:T', title='Date'),
                alt.Tooltip('Close:Q', title='Close Price'),
                alt.Tooltip('News Count:Q', title='News Count'),
            ],
        )
        .add_params(nearest)
    )

    chart = alt.layer(line, bar, rule).resolve_scale(y='independent').interactive()

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
