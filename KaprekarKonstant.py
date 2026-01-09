import streamlit as st

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
    min_value=1000,
    max_value=9999,
    step=1,
    format="%d"
)

if st.button("Calculate"):
    if checkdigits(number):
        result = KaprekarKonstant(number)
        if result is not None:
            st.success(f"Kaprekar operation result: {result}")
        else:
            st.error("Please enter a valid 4-digit number with at least two different digits.")
    else:
        st.error("All digits are the same. Please enter a number with at least two different digits.")
