import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub # kagglehub 추가

# Streamlit 페이지 설정
st.set_page_config(
    page_title="COVID-19 Time Series Dashboard",
    page_icon=":earth_asia:",
    layout="wide"
)

st.title("COVID-19 국가별 시계열 분석 대시보드")

@st.cache_data
def load_data():
    # kagglehub를 사용하여 데이터셋 다운로드 및 경로 확보
    path = kagglehub.dataset_download("imdevskp/corona-virus-report")
    
    try:
        df = pd.read_csv(f"{path}/full_grouped.csv")
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. `full_grouped.csv` 파일이 지정된 경로에 있는지 확인해주세요.")
        st.stop()
    
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df_corona = load_data()


# 사이드바에 국가 선택 드롭다운 추가
countries = df_corona['Country/Region'].unique()
selected_country = st.sidebar.selectbox("국가를 선택하세요:", countries)

# 선택된 국가에 따라 데이터 필터링
df_country = df_corona[df_corona['Country/Region'] == selected_country].copy() # SettingWithCopyWarning 방지

# 'Active' 케이스 계산 (확진자 - 사망자 - 회복자)
df_country['Active'] = df_country['Confirmed'] - df_country['Deaths'] - df_country['Recovered']

st.subheader(f"{selected_country} COVID-19 현황")

# Plotly를 사용하여 시계열 그래프 생성
fig = px.line(df_country, x='Date', y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
              title=f'{selected_country} COVID-19 Cases Over Time',
              labels={'value': 'Cases', 'variable': 'Category'},
              color_discrete_map={
                  'Confirmed': 'blue',
                  'Deaths': 'red',
                  'Recovered': 'green',
                  'Active': 'orange'
              })

fig.update_layout(hovermode="x unified")
fig.update_xaxes(rangeselector_buttons=list([
    dict(count=1, label="1m", step="month", stepmode="backward"),
    dict(count=6, label="6m", step="month", stepmode="backward"),
    dict(count=1, label="YTD", step="year", stepmode="todate"),
    dict(count=1, label="1y", step="year", stepmode="backward"),
    dict(step="all")
]))

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
--- 
### 데이터 출처
이 대시보드는 [Kaggle COVID-19 Report Dataset](https://www.kaggle.com/datasets/imdevskp/corona-virus-report)을 사용합니다.
""")
