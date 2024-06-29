from datetime import datetime
import streamlit as st
from utils.ip_checker import get_remote_ip
from utils.chart_creator import create_chart
import json
import pandas as pd
import altair as alt


def app(session_state):
    ip = get_remote_ip()
    with st.sidebar:
        st.info(f"Ip address: {ip}")

    st.markdown(
        """
        Welcome to Sweephy  dashboard ! \n
        This dashboard shows 
            """
    )

    company = st.selectbox("Company", ["ABB", "SIEMENS"])

    f = open(f'tools/reports/{company}_general_report.json')
    f_stock = open(f'tools/financials/{company}_financialdata.json')
    f_news = open(f'tools/articles/{company}_news.json')
    data = json.load(f)
    yfinance_data = json.loads(json.load(f_stock))
    news_data = json.load(f_news)

    st.markdown(
        """  
        <style>  
        .small-font {  
            font-size:16px !important;  
        }  
        </style>  
        """,
        unsafe_allow_html=True,
    )

    # Overview Section
    with st.expander("Overview", expanded=True):
        st.markdown(
            '<p class="small-font"><strong>Business Summary</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(data['overview']['business_summary'])
        st.markdown(
            '<p class="small-font"><strong>Market Position</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(data['overview']['market_position'])
        st.markdown(
            '<p class="small-font"><strong>Recent Performance</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(data['overview']['recent_performance'])

    # =================================================================================

    # Stock Price Chart
    st.markdown(
        '<p class="medium-font"><strong>Stock Price (Last 3 Years) & News (Last 6 Months)</strong></p>',
        unsafe_allow_html=True,
    )
    create_chart(yfinance_data, news_data)

    # =================================================================================

    # Annual Report Key Points Section
    with st.expander(
        'Annual Report Key Points',
        expanded=False,
    ):
        # Prepare data for the
        '''
        st.markdown(
            '<p class="medium-font"><strong>Annual Report Key Points</strong></p>',
            unsafe_allow_html=True,
        )
        '''
        reports = data['mapping_annual_report_and_news']['key_points_annual_reports']
        years = [report['year'] for report in reports]
        max_points_len = max(len(report['points']) for report in reports)

        table_data = {year: [""] * max_points_len for year in years}

        for report in reports:
            for i, point in enumerate(report['points']):
                table_data[report['year']][i] = point

        # Convert to DataFrame
        df = pd.DataFrame(table_data)

        # Display the table
        st.table(df)

    # Financial Metrics Section
    with st.expander("Financial Metrics and KPIs", expanded=False):
        col1, col2, col3 = st.columns(3)
        for i, metric in enumerate(
            data['mapping_annual_report_and_financial_data']['financial_metrics_kpis']
        ):
            with [col1, col2, col3][i % 3]:
                st.markdown(
                    f'<p class="small-font"><strong>Year: {metric["year"]}</strong></p>',
                    unsafe_allow_html=True,
                )
                st.write(f"Revenue Growth: {metric['revenue_growth']}")
                st.write(f"Profit Margins: {metric['profit_margins']}")
                st.write(f"Return on Equity: {metric['return_on_equity']}")

    # Comparison with Historical Data Section
    with st.expander("Comparison with Historical Data", expanded=False):
        for comparison in data['mapping_annual_report_and_financial_data'][
            'comparison_with_historical_data'
        ]:
            st.markdown(
                f'<p class="small-font"><strong>{comparison["metric"]}</strong></p>',
                unsafe_allow_html=True,
            )
            st.write(f"Annual Report Value: {comparison['annual_report_value']}")
            st.write(f"Historical Value: {comparison['historical_value']}")
            st.write(f"Trend Analysis: {comparison['trend_analysis']}")

    # SWOT Analysis Section
    with st.expander("SWOT Analysis", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                '<p class="small-font"><strong>Strengths</strong></p>',
                unsafe_allow_html=True,
            )
            for strength in data['mapping_cross_checking_all_sources']['swot_analysis'][
                'strengths'
            ]:
                st.write(f"- {strength}")
        with col2:
            st.markdown(
                '<p class="small-font"><strong>Weaknesses</strong></p>',
                unsafe_allow_html=True,
            )
            for weakness in data['mapping_cross_checking_all_sources']['swot_analysis'][
                'weaknesses'
            ]:
                st.write(f"- {weakness}")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                '<p class="small-font"><strong>Opportunities</strong></p>',
                unsafe_allow_html=True,
            )
            for opportunity in data['mapping_cross_checking_all_sources'][
                'swot_analysis'
            ]['opportunities']:
                st.write(f"- {opportunity}")
        with col4:
            st.markdown(
                '<p class="small-font"><strong>Threats</strong></p>',
                unsafe_allow_html=True,
            )
            for threat in data['mapping_cross_checking_all_sources']['swot_analysis'][
                'threats'
            ]:
                st.write(f"- {threat}")

    # Long Term Strategy Insights Section
    with st.expander("Long Term Strategy Insights", expanded=False):
        st.write(
            data['mapping_cross_checking_all_sources']['long_term_strategy_insights']
        )

    # Conclusion Section
    with st.expander("Conclusion", expanded=False):
        st.markdown(
            '<p class="small-font"><strong>Summary of Findings</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(data['conclusion']['summary_findings'])
        st.markdown(
            '<p class="small-font"><strong>Strategic Outlook</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(data['conclusion']['strategic_outlook'])
        st.markdown(
            '<p class="small-font"><strong>Recommendations for Investors</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(data['conclusion']['recommendations_investors'])
