import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import base64


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return none
    return r.json()


right_draw = load_lottieurl(
    "https://assets5.lottiefiles.com/packages/lf20_27cgfczo.json")
st.set_page_config(
    page_title="Prompt Profile Picture",
    page_icon="✨🖌️")  # layout="wide")

st.title("Prompt Profile Picture")

canvas = Image.open("images\canvas cyborg.png")
st.image(canvas)

st.subheader(" 🎙️ Intro")
left, right = st.columns((2, 1))
with left:
    st.markdown(
        '**Here** we can generate our own profile pic, banner images, cover images...., created by an A.I.🤖 on our prompt.')

    st.write("The only thing which decides that how stylish or beautiful or Digitaly artistic our profile and banner can be, is our way of prompt")
    st.write("So what you are waiting for.... Let's prompt ")
with right:
    st_lottie(right_draw)
