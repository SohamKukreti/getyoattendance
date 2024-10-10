import streamlit as st
from pyjiit import Webportal
from pyjiit.default import CAPTCHA
import pandas as pd
import requests

# Function to fetch random meme
def fetch_random_meme():
    try:
        response = requests.get("https://meme-api.com/gimme")
        response.raise_for_status()
        meme_data = response.json()
        return meme_data["url"], meme_data["title"]
    except Exception as e:
        return None, f"An error occurred while fetching meme: {e}"

# Function to log in and get attendance details
def fetch_attendance(userid, passwd):
    try:
        w = Webportal()
        s = w.student_login(userid, passwd, CAPTCHA)
        if not s:
            raise Exception("Login failed due to CAPTCHA or incorrect credentials.")
        
        meta = w.get_attendance_meta()
        if not meta:
            raise Exception("Failed to fetch attendance metadata.")
        header = meta.latest_header()
        sem = meta.latest_semester()

        attendance_data = w.get_attendance(header, sem)
        if 'studentattendancelist' not in attendance_data:
            raise Exception("Attendance data format incorrect or unavailable.")

        
        student_attendance = attendance_data['studentattendancelist']
        return student_attendance

    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI Layout
st.title("Get Yo Attendance")

# Input for username and password
username = st.text_input("Enter your User ID")
password = st.text_input("Enter your Password", type="password")

if st.button("Get Attendance"):
    if not username or not password:
        st.error("Please enter both User ID and Password")
    else:
        text_placeholder = st.empty()
        meme_placeholder = st.empty()

        meme_url, meme_title = fetch_random_meme()
        if meme_url:
            text_placeholder.subheader(" Here's a random meme while we get your attendance: ")
            meme_placeholder.image(meme_url, caption=meme_title, use_column_width=True)

        attendance = fetch_attendance(username, password)

        text_placeholder.empty()
        meme_placeholder.empty()

        if isinstance(attendance, str):
            st.error(attendance)
        else:
            for subject in attendance:
                with st.expander(subject['subjectcode']):
                    if subject.get('LTpercantage'):
                        st.write(f"**Overall Percentage:** {subject['LTpercantage']}%")
                    if subject['Ltotalclass']:
                        st.write(f"**Total Lectures:** {subject['Ltotalclass']}")
                    if subject['Ltotalpres']:
                        st.write(f"**Lectures Attended:** {subject['Ltotalpres']}")
                    if subject['Ttotalclass']:
                        st.write(f"**Total Tutorials:** {subject['Ttotalclass']}")
                    if subject['Ttotalpres']:
                        st.write(f"**Tutorials Attended:** {subject['Ttotalpres']}")
                    if subject['Tpercentage']:
                        st.write(f"**Tutorial Percentage:** {subject['Tpercentage']}%")
                    if subject['Ppercentage']:
                        st.write(f"**Practical Percentage:** {subject['Ppercentage']}%")
                    if subject['abseent']:
                        st.write(f"**Absent Classes:** {subject['abseent']}")


            avg_lecture_percentage = pd.DataFrame(attendance)['LTpercantage'].astype(float).mean()
            st.write(f"### Average Lecture Attendance: {avg_lecture_percentage:.2f}%")

st.write("Thank you codelif :trophy:")
