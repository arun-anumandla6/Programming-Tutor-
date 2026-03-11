import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Programming Tutor", layout="wide")

st.markdown("""
<style>

body {
    background-color: #000000;
    color: white;
}

.stApp {
    background-color: #000000;
    color: white;
}

h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

label {
    color: white !important;
}

p {
    color: white !important;
}

span {
    color: white !important;
}

div {
    color: white;
}

textarea {
    background-color: #111111 !important;
    color: white !important;
}

input {
    background-color: #111111 !important;
    color: white !important;
}

.stTextArea textarea {
    border: 2px solid red;
}

.stButton button {
    background-color: red;
    color: white;
    border-radius: 6px;
}

.answer-box {
    border: 3px solid red;
    padding: 20px;
    margin-top: 20px;
    border-radius: 10px;
    background-color: #0b0b0b;
}

.course-box {
    border: 2px solid red;
    padding: 15px;
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: black !important;
    color: white !important;
    border: 2px solid red;
}

div[data-baseweb="select"] > div {
    background-color: black !important;
    color: white !important;
}

div[role="listbox"] {
    background-color: black !important;
}

div[role="option"] {
    background-color: black !important;
    color: white !important;
}

div[data-baseweb="popover"] {
    background-color: black !important;
}

ul {
    background-color: black !important;
}

li {
    background-color: black !important;
    color: white !important;
}

li:hover {
    background-color: #111111 !important;
}
pre {
    background-color: #000000 !important;
    color: white !important;
    border: 2px solid red;
}

code {
    background-color: #000000 !important;
    color: white !important;
}


div[data-testid="stSpinner"] * {
    stroke: orange !important;
    color: orange !important;
}

</style>
""", unsafe_allow_html=True)

st.title(" Welcome To Programming Tutor Agent ")

st.write("Lets solve Your problem together and learn from it :smile:")

st.divider()

left, right = st.columns([1,2])

with left:

    st.markdown('<div class="course-box">', unsafe_allow_html=True)

    st.subheader("Select Course")

    course = st.selectbox(
        "Course",
        ["Python", "Java", "Go"],
        label_visibility="collapsed"
    )

    code_input = st.text_area(
        "Paste Code",
        height=250
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.subheader("Ask Question")

    question = st.text_area(
        "Question",
        height=200,
        label_visibility="collapsed"
    )

    generate = st.button("Generate Answer")

if generate:

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:

        payload = {
            "question": question,
            "language": course.lower(),
            "code": code_input
        }

        try:

            with st.spinner("Be patience hero until i genrate ur answer..."):

                response = requests.post(
                    BACKEND_URL,
                    json=payload,
                    timeout=None
                )

            if response.status_code == 200:

                data = response.json()

                st.subheader("Answer")

                st.markdown(
                    f'<div class="answer-box">{data["answer"]}</div>',
                    unsafe_allow_html=True
                )

            else:

                st.error("Backend error")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Backend server not running")

        except Exception as e:
            st.error(str(e))