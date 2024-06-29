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
        Welcome to dashboard ! \n
            """
    )

    COMPANY_LIST = ['IBM', 'ABB', 'Raiffeisen', 'Siemens']
    company = st.selectbox("Company", COMPANY_LIST)

    f = open(f'tools/reports/{company}_general_report.json')
    f_stock = open(f'tools/financials/{company}_financialdata_4.json')
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
    with st.expander('Annual Report Key Points', expanded=False):
        reports = data['mapping_annual_report_and_news']['key_points_annual_reports']
        years = [report['year'] for report in reports]
        max_points_len = max(len(report['points']) for report in reports)
        table_data = {year: [""] * max_points_len for year in years}

        for report in reports:
            for i, point in enumerate(report['points']):
                table_data[report['year']][i] = f"{point['point']}: {point['details']}"

        # Convert to DataFrame
        df = pd.DataFrame(table_data)
        # Display the table
        st.table(df)

        # Cross Reference News Section
        if (
            'cross_reference_news' in data['mapping_annual_report_and_news']
            and data['mapping_annual_report_and_news']['cross_reference_news']
        ):
            st.markdown(
                '<p class="small-font"><strong>News Related to Annual Reports</strong></p>',
                unsafe_allow_html=True,
            )
            for news in data['mapping_annual_report_and_news']['cross_reference_news']:
                st.markdown(f"**Title:** [{news['title']}]({news['link']})")
                st.write(
                    f"**Related Annual Report Point:** {news['related_annual_report_point']}"
                )
                st.write(f"**Summary:** {news['summary']}")
                st.write(f"**Causalities/Reasons:** {news['causalities_reasons']}")
                st.write("---")

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
                for key, value in metric["metrics"].items():
                    st.write(
                        f"{key.replace('_', ' ').capitalize()}: {value['value']} ({value['details']})"
                    )

        # Comparison with Historical Data Section
        # with st.expander("Comparison with Historical Data", expanded=False):
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

    # Integrated Analysis Section
    with st.expander("Integrated Analysis", expanded=False):
        for analysis in data['mapping_cross_checking_all_sources'][
            'integrated_analysis'
        ]:
            st.markdown(
                f'<p class="small-font"><strong>Source: {analysis["source"]}</strong></p>',
                unsafe_allow_html=True,
            )
            st.write(f"Data: {analysis['data']}")
            st.write(f"Analysis: {analysis['analysis']}")
            st.write("---")

        st.markdown(
            '<p class="small-font"><strong>Long Term Strategy Insights</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(
            data['mapping_cross_checking_all_sources']['long_term_strategy_insights']
        )

        st.markdown(
            '<p class="small-font"><strong>Discrepancies/Inconsistencies</strong></p>',
            unsafe_allow_html=True,
        )
        st.write(
            data['mapping_cross_checking_all_sources']['discrepancies_inconsistencies']
        )

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
                st.write(f"- {strength['strength']}: {strength['reasons']}")

        with col2:
            st.markdown(
                '<p class="small-font"><strong>Weaknesses</strong></p>',
                unsafe_allow_html=True,
            )
            for weakness in data['mapping_cross_checking_all_sources']['swot_analysis'][
                'weaknesses'
            ]:
                st.write(f"- {weakness['weakness']}: {weakness['reasons']}")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                '<p class="small-font"><strong>Opportunities</strong></p>',
                unsafe_allow_html=True,
            )
            for opportunity in data['mapping_cross_checking_all_sources'][
                'swot_analysis'
            ]['opportunities']:
                st.write(f"- {opportunity['opportunity']}: {opportunity['reasons']}")

        with col4:
            st.markdown(
                '<p class="small-font"><strong>Threats</strong></p>',
                unsafe_allow_html=True,
            )
            for threat in data['mapping_cross_checking_all_sources']['swot_analysis'][
                'threats'
            ]:
                st.write(f"- {threat['threat']}: {threat['reasons']}")

    # PESTEL Analysis Section
    with st.expander("PESTEL Analysis", expanded=False):
        for factor, details in data['pestel_analysis'].items():
            st.markdown(
                f'<p class="small-font"><strong>{factor.replace("_", " ").capitalize()}</strong></p>',
                unsafe_allow_html=True,
            )
            st.write(f"{details['description']}: {details['details']}")

    # Regulatory Insights Section
    with st.expander("Regulatory Insights", expanded=False):
        st.write(data['regulatory_insights']['overview'])
        st.write(data['regulatory_insights']['details'])

    # Competitive Landscape Section
    with st.expander("Competitive Landscape", expanded=False):
        for force, details in data['competitive_landscape'][
            'porters_five_forces'
        ].items():
            st.markdown(
                f'<p class="small-font"><strong>{force.replace("_", " ").capitalize()}</strong></p>',
                unsafe_allow_html=True,
            )
            st.write(f"{details['description']}: {details['factors']}")

    # Conclusion Section
    with st.expander("Conclusion", expanded=True):
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
