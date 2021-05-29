import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Covid Dashboard", page_icon="🕸", layout='wide', initial_sidebar_state='expanded')

st.header("Covid Dashboard")
st.subheader("Developed with ❤ by Heflin")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style,unsafe_allow_html=True)

@st.cache
def fetch_data(url):
    data = pd.read_csv(url)
    return data

covid_data = fetch_data("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
covid_death_data =fetch_data("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

last_updated__death_date=covid_death_data.columns[-1]
counrty_wise_death_cases = covid_death_data.groupby('Country/Region').agg({ last_updated__death_date:'sum'}).reset_index().sort_values(last_updated__death_date,ascending=False)

last_updated_date=covid_data.columns[-1]
counrty_wise_confirmed_cases = covid_data.groupby('Country/Region').agg({ last_updated_date:'sum'}).reset_index().sort_values(last_updated_date,ascending=False)

st.write(f"This data is obtained from [Johns Hopkins University.](https://github.com/CSSEGISandData/COVID-19) Last updated on {last_updated_date}")

no_of_coutires = st.slider("No. of countires", min_value=2, max_value=len(set(covid_data["Country/Region"])), value=50)

def bar_chart_countries(data,title,xaxis,yaxis,):
    last_updated_date=covid_data.columns[-1]
    fig = go.Figure(data=[
    go.Bar(
         x=data['Country/Region'][:no_of_coutires],
         y=data[last_updated_date][:no_of_coutires]
        )])
    fig.update_layout(
    title=title,
    xaxis_tickfont_size=12,
    xaxis=dict(title=xaxis,titlefont_size=16),
    yaxis=dict(title=yaxis,titlefont_size=16))
    return fig


col1,col2 = st.beta_columns(2)
col1.plotly_chart(bar_chart_countries(counrty_wise_confirmed_cases,title="Total Confirmed Cases",xaxis="Countries",yaxis="No. of people"))
col2.plotly_chart(bar_chart_countries(counrty_wise_death_cases,title="Total Death Cases",xaxis="Countries",yaxis="No. of people"))