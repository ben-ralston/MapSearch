import streamlit as st
import streamlit.components.v1 as components


def viewLocationOnMap(place_id):
    pass

st.title("Map")

# num1 = st.number_input("First Number", value = 0.0)
# num2 = st.number_input("Second Number", value = 0.0)
#
# theSum = num1 + num2
#
# theString = "The sum of {} and {} is equal to {}.".format(num1, num2, theSum)

# map = components.iframe('<iframe src="https://www.google.com/maps/d/u/0/embed'
#                         '?mid=1NmhTJJR0x3OR7oUM-RSexZWurF1Qnxs8&ehbc=2E312F'
#                         '" width="640" height="480"></iframe>')

components.iframe('https://www.google.com/maps/d/u/0/embed?mid='
                  '1NmhTJJR0x3OR7oUM-RSexZWurF1Qnxs8&ehbc=2E312F', height=1000)

# st.markdown(theString)
