import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 1. 한글 폰트 설정
def set_korean_font():
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':
        plt.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.set_page_config(layout="wide") # 화면을 넓게 쓰도록 설정
st.title("📚 송내도서관 대출 데이터 상세 분석기")

# 2. 파일 읽기
file_path = "송내도서관_대출정보.csv"

@st.cache_data
def load_data(path):
    try:
        # 공공데이터용 cp949 인코딩 시도
        data = pd.read_csv(path, encoding='cp949')
    except:
        # 실패 시 utf-8 시도
        data = pd.read_csv(path, encoding='utf-8')
    
    # 날짜 데이터 변환
    data['대출일시'] = pd.to_datetime(data['대출일시'], errors='coerce')
    return data

try:
    df = load_data(file_path)
    st.success("데이터를 성공적으로 불러왔습니다! ✅")

    # 3. 데이터 요약 및 미리보기 (20개로 확대)
    st.subheader("📝 데이터 요약 및 미리보기 (상위 20개)")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("전체 대출 건수", f"{len(df):,} 건")
    with col_stat2:
        st.metric("등록된 도서 종수", f"{df['도서명'].nunique():,} 종")
    with col_stat3:
        st.metric("주요 카테고리 수", f"{df['카테고리'].nunique():,} 개")

    st.dataframe(df.head(20), use_container_width=True) # 20개 출력

    st.divider()

    # 4. 분석 설정 부분
    st.subheader("🔍 분석 설정")
    analysis_type = st.radio(
        "확인하고 싶은 분석 주제를 선택하세요:",
        ["가장 많이 읽은 도서 TOP 10", "카테고리별 인기 순위", "대출연령 분포", "월별 대출 추세"],
        horizontal=True # 가로로 배치
    )

    st.write(f"### 📊 결과: {analysis_type}")

    # 5. 주제별 분석 로직
    if analysis_type == "가장 많이 읽은 도서 TOP 10":
        # 책 제목 기준 상위 10개 추출
        top_books = df['도서명'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 7))
        # 가로 막대 그래프가 제목 읽기에 더 편합니다
        sns.barplot(x=top_books.values, y=top_books.index, ax=ax, palette='magma')
        ax.set_title("송내도서관 인기 도서 TOP 10", fontsize=18, pad=20)
        ax.set_xlabel("대출 횟수", fontsize=12)
        ax.set_ylabel("도서명", fontsize=12)
        
        # 그래프 옆에 표도 함께 보여주기
        col_chart, col_table = st.columns([2, 1])
        with col_chart:
            st.pyplot(fig)
        with col_table:
            st.write("📌 **상세 순위**")
            st.table(top_books.reset_index().rename(columns={'index': '도서명', '도서명': '대출횟수'}))

    elif analysis_type == "카테고리별 인기 순위":
        category_counts = df['카테고리'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=category_counts.values, y=category_counts.index, ax=ax, palette='viridis')
        ax.set_title("인기 카테고리 TOP 10", fontsize=15)
        st.pyplot(fig)

    elif analysis_type == "대출연령 분포":
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['대출연령'], bins=20, kde=True, ax=ax, color='skyblue')
        ax.set_title("이용자 연령대 분포", fontsize=15)
        st.pyplot(fig)

    elif analysis_type == "월별 대출 추세":
        df['월'] = df['대출일시'].dt.to_period('M').astype(str)
        monthly_counts = df.groupby('월').size()
        fig, ax = plt.subplots(figsize=(12, 5))
        monthly_counts.plot(kind='line', marker='o', color='orange', ax=ax, linewidth=2)
        ax.set_title("월별 대출 건수 변화", fontsize=15)
        plt.xticks(rotation=45)
        st.pyplot(fig)

except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다: '{file_path}'")
except Exception as e:
    st.error(f"❌ 분석 중 오류가 발생했습니다: {e}")