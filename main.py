import streamlit as st
from pyjiit import Webportal
from pyjiit.default import CAPTCHA
import pandas as pd

def fetch_attendance(userid, passwd):
    try:
        w = Webportal()
        s = w.student_login(userid, passwd, CAPTCHA)
        
        meta = w.get_attendance_meta()
        header = meta.latest_header()
        sem = meta.latest_semester()

        attendance_data = w.get_attendance(header, sem)
        
        student_attendance = attendance_data['studentattendancelist']
        return student_attendance

    except Exception as e:
        return f"An error occurred: {e}"

st.title("get yo attendance")

username = st.text_input("Enter your User ID")
password = st.text_input("Enter your Password", type="password")

if st.button("Get Attendance"):
    if not username or not password:
        st.error("Please enter both User ID and Password")
    else:
        attendance = fetch_attendance(username, password)

        if isinstance(attendance, str):
            st.error(attendance)
        else:
            for subject in attendance:
                with st.expander(subject['subjectcode']):
                    if(subject['LTpercantage']):
                        st.write(f"**Overall Percentage:** {subject['LTpercantage']}%")
                    if(subject['Ltotalclass']):
                        st.write(f"**Total Lectures:** {subject['Ltotalclass']}")
                    if(subject['Ltotalpres']):
                        st.write(f"**Lectures Attended:** {subject['Ltotalpres']}")
                    if(subject['Tpercentage']):
                        st.write(f"**Tutorial Percentage:** {subject['Tpercentage']}%")
                    if(subject['Ppercentage']):
                        st.write(f"**Practical Percentage:** {subject['Ppercentage']}%")
                    if(subject['abseent']):
                        st.write(f"**Absent Classes:** {subject['abseent']}")

            avg_lecture_percentage = pd.DataFrame(attendance)['LTpercantage'].mean()
            st.write(f"### Average Lecture Attendance: {avg_lecture_percentage:.2f}%")

