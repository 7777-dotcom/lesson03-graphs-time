import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, dtype={"날짜": str})
    # 하이픈 없는 여덟 자리 숫자를 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

st.caption("데이터 출처: KOBIS 일별 박스오피스 (최근 1년, 상위 10위권)")

# ==============================================================
# 구역 1. 영화별 일별 관객수 추이
# ==============================================================
st.header("1. 영화별 일별 관객수 추이")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 일별 관객수 변화",
    labels={"날짜": "날짜", "일관객": "일일 관객수"},
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

st.info("📌 이 그래프로 알 수 있는 것: (여기에 문구를 입력하세요)")

# ==============================================================
# 구역 2. 누적 일관객 상위 5편 비교
# ==============================================================
st.header("2. 누적 일관객 상위 5편 비교")

# 기간 내 일관객 합계 기준 상위 5편 선정
top5_movies = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index.tolist()
)

top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="기간 내 일관객 합계 상위 5편의 날짜별 일관객 추이",
    labels={"날짜": "날짜", "일관객": "일일 관객수", "영화명": "영화명"},
)
fig2.update_traces(
    hovertemplate="%{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra></extra>"
)
fig2.update_layout(hovermode="x unified", legend_title_text="영화명 (클릭해서 켜고 끄기)")

st.plotly_chart(fig2, use_container_width=True)

st.info("📌 이 그래프로 알 수 있는 것: (여기에 문구를 입력하세요)")

# ==============================================================
# 구역 3. 날짜별 10위권 총 관객수
# ==============================================================
st.header("3. 날짜별 10위권 총 관객수")

daily_total = df.groupby("날짜")["일관객"].sum().reset_index()
daily_total.columns = ["날짜", "총관객"]

# 총관객이 가장 컸던 상위 3일
top3_days = daily_total.sort_values("총관객", ascending=False).head(3)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="총관객",
    title="날짜별 박스오피스 10위권 총 관객수",
    labels={"날짜": "날짜", "총관객": "10위권 총 관객수"},
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>총 관객수: %{y:,}명<extra></extra>"
)
fig3.update_layout(hovermode="x unified")

# 상위 3일 표시 (점 + 날짜 라벨)
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["총관객"],
    mode="markers+text",
    marker=dict(size=12, color="red", symbol="star"),
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    name="총관객 최고 3일",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>총 관객수: %{y:,}명<extra></extra>",
)

st.plotly_chart(fig3, use_container_width=True)

st.info("📌 이 그래프로 알 수 있는 것: (여기에 문구를 입력하세요)")
