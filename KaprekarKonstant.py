import streamlit as st

st.set_page_config(page_title="Kaprekar Constant Calculator", layout="wide")


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

def KaprekarKonstant3digit(x):
    if checkdigits(x) and len(str(x))==3:
        count =0
        sortedNum=sorted([int(i) for i in list(str(x))])
        reverseNum = sortedNum[::-1]
        a,b=sortedNum[0],reverseNum[0]
        for i in range(1,3):
            a+=(sortedNum[i]*(10**i))
            b+=(reverseNum[i]*(10**i))
        return a-b
    else:
        return None
st.title("Kaprekar Constant Calculator")
st.write("Enter a 4-digit number with at least two different digits.")

number = st.number_input(
    "Enter your a 4-digit number:", min_value=1001, max_value=9998, step=1, format="%d"
)

if st.button("Calculate", key="calc_btn_4digit"):
    if checkdigits(number):
        count = 1
        trajectory = [number]
        result = KaprekarKonstant(number)
        trajectory.append(result)
        while result != 6174 and result != None:
            count += 1
            result = KaprekarKonstant(result)
            trajectory.append(result)
        if trajectory[-1] == 6174:
            st.success(f"Kaprekar operation result: {trajectory}")
        else:
            if len(trajectory) == 1:
                st.error(
                    "Please enter a valid 4-digit number with at least two different digits."
                )
            else:
                if trajectory ==[number, 999, None]:
                    count=1
                    result=KaprekarKonstant(9990)
                    trajectory=[number, 999, result]
                    while result != 6174 and result != None:
                        count+=1
                        result=KaprekarKonstant(result)
                        trajectory.append(result)
                    st.success(f"Kaprekar operation result: {trajectory}")
    else:
        st.error(
            "All digits are the same. Please enter a number with at least two different digits."
        )

st.write("Enter a 3-digit number with at least two different digits.")

number = st.number_input(
    "Enter your a 3-digit number:", min_value=100, max_value=998, step=1, format="%d"
)

if st.button("Calculate", key="calc_btn_3digit"):
    if checkdigits(number):
        count = 1
        trajectory = [number]
        result = KaprekarKonstant3digit(number)
        trajectory.append(result)
        while result != 495 and result != None:
            count += 1
            result = KaprekarKonstant3digit(result)
            trajectory.append(result)
        if trajectory[-1] == 495:
            st.success(f"Kaprekar operation result: {trajectory}")
        else:
            if len(trajectory) == 1:
                st.error(
                    "Please enter a valid 3-digit number with at least two different digits."
                )
            else:
                if trajectory ==[number, 99, None]:
                    count=1
                    result=KaprekarKonstant3digit(990)
                    trajectory=[number, 99, result]
                    while result != 495 and result != None:
                        count+=1
                        result=KaprekarKonstant3digit(result)
                        trajectory.append(result)
                    st.success(f"Kaprekar operation result: {trajectory}")
    else:
        st.error(
            "All digits are the same. Please enter a number with at least two different digits."
        )
