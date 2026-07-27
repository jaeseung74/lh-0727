import streamlit as st

st.set_page_config(page_title="숫자 더하기 앱", page_icon=":heavy_plus_sign:")

st.title("두 숫자 더하기 앱")

st.write("두 개의 숫자를 입력하여 합계를 계산합니다.")

# 사용자로부터 숫자 입력 받기
num1 = st.number_input("첫 번째 숫자를 입력하세요:", value=0)
num2 = st.number_input("두 번째 숫자를 입력하세요:", value=0)

# 숫자 더하기
sum_result = num1 + num2

# 결과 출력
st.subheader("결과")
st.success(f"두 숫자의 합계는: {sum_result}")

st.write("이 앱은 Streamlit을 사용하여 만들어졌습니다.")
