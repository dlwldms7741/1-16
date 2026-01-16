import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 1. 한글 폰트 설정 함수
def set_korean_font():
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':
        plt.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.title("📊 산업통상자원부 수출입동향 분석기")

# 2. 파일 읽기 (인코딩 에러 방지 처리)
file_path = "산업통상부_수출입동향 정보_20241231.csv"

@st.cache_data # 데이터를 매번 새로 읽지 않도록 속도 최적화
def load_data(path):
    try:
        # 먼저 cp949로 시도 (공공데이터 표준)
        return pd.read_csv(path, encoding='cp949')
    except:
        # 실패하면 utf-8로 시도
        return pd.read_csv(path, encoding='utf-8')

try:
    df = load_data(file_path)
    st.success("데이터 로드 성공! 🚀")

    # 3. 분석 화면 구성
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 데이터 미리보기")
        st.dataframe(df.head(10))

    with col2:
        st.subheader("📉 분석 설정")
        # 숫자 데이터만 선택
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # '연도'는 X축으로 쓸 거니까 선택 목록에서 제외 (센스!)
        if '연도' in numeric_cols:
            numeric_cols.remove('연도')
            
        selected_col = st.selectbox("분석할 지표를 선택하세요", numeric_cols)

    # 4. 메인 그래프 (연도별 추세)
    st.divider()
    st.subheader(f"📅 연도별 {selected_col} 추세 확인")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x='연도', y=selected_col, ax=ax, marker='o', color='#0077b6', linewidth=2)
    
    ax.set_title(f"연도별 {selected_col} 변화", fontsize=16, pad=20)
    ax.grid(True, linestyle=':', alpha=0.7)
    
    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다: '{file_path}'")
    st.info("팁: 파이썬 파일(.py)과 CSV 파일이 '같은 폴더'에 있는지 확인해 보세요!")
except Exception as e:
    st.error(f"❌ 예상치 못한 오류 발생: {e}")

    