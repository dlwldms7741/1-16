import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform  # OS 확인용

# ================= 폰트 설정 시작 =================
def set_korean_font():
    if platform.system() == 'Windows':
        # 윈도우용 맑은 고딕 설정
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':
        # 맥용 애플 고딕 설정
        plt.rc('font', family='AppleGothic')
    
    # 마이너스 기호(-) 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()
# ================= 폰트 설정 끝 =================

st.title("📊국세청 근로소득 데이터 분석기")

file_path = "한국고용정보원_직업별_임금정보_20230908.csv"

try:
    # 데이터 읽기
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("데이터가 성공적으로 로드되었습니다😊")

    # 데이터 미리보기
    st.subheader("📝데이터 미리보기")
    st.dataframe(df.head())

    # 데이터 분석 그래프 그리기
    st.subheader("📈항목별 분포 그래프")

    # [수정포인트 1] 숫자 데이터가 들어있는 열만 골라내기
    # 문자열 열로 그래프를 그리면 x축이 겹쳐서 오류가 납니다.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        selected_col = st.selectbox("분석할 항목(숫자 데이터)을 선택하세요", numeric_cols)

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # [수정포인트 2] 결측치(NaN)를 제거하고 그려야 오류가 없습니다.
        sns.histplot(df[selected_col].dropna(), ax=ax, color="#ccffff", kde=True)

        # 한글이 적용될 제목들
        ax.set_title(f"{selected_col} 분포 확인", fontsize=15)
        ax.set_xlabel(selected_col)
        ax.set_ylabel("빈도수")

        # 스트림릿 웹 화면에 그래프 표시
        st.pyplot(fig)
    else:
        st.warning("데이터프레임에 시각화할 수 있는 숫자 열이 없습니다.")

except FileNotFoundError:
    st.error(f"'{file_path}' 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"데이터를 로드하는 중에 오류가 발생했습니다: {e}")