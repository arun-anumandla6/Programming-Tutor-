import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/query"
ACCURACY_URL = "http://127.0.0.1:8000/accuracy"
st.set_page_config(page_title="Programming Tutor", layout="wide")


try:
    acc_response = requests.get(ACCURACY_URL)
    if acc_response.status_code == 200:
        acc_value = acc_response.json()["accuracy"]
    else:
        acc_value = 0
except:
    acc_value = 0


st.set_page_config(page_title="Programming Tutor", layout="wide")
import base64

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.jpg")

st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:15px;">
        <img src="data:image/png;base64,{logo_base64}" width="100" style="border-radius: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #87CEEB, #4682B4, #000000);
}

[data-testid="stHeader"] {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)
# st.markdown("""
# <style>

# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #87CEEB, #B0E0E6, #E0F7FF);
# }

# [data-testid="stHeader"] {
#     background: transparent;
# }

# </style>
# """, unsafe_allow_html=True)
st.markdown("""
<style>
* {
    font-family: "Times New Roman" !important;
}

/* Background */
body {
    background-color: #f5f7fa;
    color: #1f2937;
}

.stApp {
    background-color: #f5f7fa;
    color: #1f2937;
}

/* Headings */
h1, h2, h3 {
    color: #111827 !important;
}

textarea, .stTextArea textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 6px;
    font-family: "Times New Roman", serif;
}

/* Button */
.stButton button {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}

.stButton button:hover {
    background-color: #2563eb;
}

/* Answer box */
.answer-box {
    border: 2px solid #3b82f6;
    padding: 20px;
    margin-top: 20px;
    border-radius: 10px;
    background-color: #ffffff;
    color: #111827;
}

/* Course box */
.course-box {
    border: 2px solid #3b82f6;
    padding: 15px;
    border-radius: 10px;
    background-color: #ffffff;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 2px solid #3b82f6;
    border-radius: 8px;
}

/* Spinner */
div[data-testid="stSpinner"] * {
    color: #3b82f6 !important;
}
# .stApp {
#     background: linear-gradient(-45deg, #000000, #1a0000, #000000, #330000);
#     background-size: 400% 400%;
#     animation: gradientMove 10s ease infinite;
# }

# @keyframes gradientMove {
#     0% { background-position: 0% 50%; }
#     50% { background-position: 100% 50%; }
#     100% { background-position: 0% 50%; }
# }
}
</style>
""", unsafe_allow_html=True)

st.title(" Welcome To Programming Tutor Agent ")

st.write("Lets solve Your problem together and learn from it :smile:")

st.divider()

left, right = st.columns([1,2])

with left:

    
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

    if question.strip() == "" and code_input.strip() == "":
        st.warning("Please enter a question or code.")
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
                st.markdown(
                    f'<div class="answer-box">Semantic Accuracy: {data["accuracy"]}</div>',
                    unsafe_allow_html=True)
                

            else:

                st.error("Backend error")
                st.text(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Backend server not running")

        except Exception as e:
            st.error(str(e))
  