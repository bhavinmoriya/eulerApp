import streamlit as st
st.set_page_config(
    page_title="Kaprekar Constant Calculator",
    layout="wide"
)
def checkdigits(x):
    return len(set(str(x))) > 1

def KaprekarKonstant(x):
    if checkdigits(x) and len(str(x)) == 4:
        count = 0
        sortedNum = sorted([int(i) for i in list(str(x))])
        reverseNum = sortedNum[::-1]
        a, b = 0, 0
        for i in range(4):
            a += sortedNum[i] * (10 ** (3 - i))
            b += reverseNum[i] * (10 ** (3 - i))
        return b - a
    else:
        return None

st.title("Kaprekar Constant Calculator")
st.write("Enter a 4-digit number with at least two different digits.")

number = st.number_input(
    "Enter your 4-digit number:",
    min_value=1001,
    max_value=9998,
    step=1,
    format="%d"
)

if st.button("Calculate"):
    if checkdigits(number):
        count=1
        trajectory=[number]
        result = KaprekarKonstant(number)
        while result != 6174 and result != None:
            count+=1
            trajectory.append(result)
            result=KaprekarKonstant(result)
        if trajectory[-1] == 6174:
            st.success(f"Kaprekar operation result: {trajectory}")
        elif trajectory[-1] == 999:
            st.success(f"Kaprekar operation result: {trajectory}. The 999 does not lead to 6174. Choose another number.")
        else:
            st.error("Please enter a valid 4-digit number with at least two different digits.")
    else:
        st.error("All digits are the same. Please enter a number with at least two different digits.")
