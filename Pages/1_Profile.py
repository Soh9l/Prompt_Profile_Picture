import streamlit as st
from craiyon import Craiyon
from PIL import Image  # pip install pillow
from io import BytesIO
import base64
from streamlit_image_select import image_select
import os
import openai
import requests
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return none
    return r.json()


prof_gif = load_lottieurl(
    "https://assets1.lottiefiles.com/packages/lf20_NODCLWy3iX.json")


st.set_page_config(layout="wide")

# title
st.title("Generate Profile images")


tab1, tab2 = st.tabs(['Banner', 'Varitions'])

if "sm_options" not in st.session_state:
    st.session_state.options = "sm"

if "dimension" not in st.session_state:
    st.session_state['dimension'] = (800, 800)

with st.sidebar:

    sm_options = st.selectbox(
        "Which Social Media?",
        ("Twitch", "Twitter"),
        label_visibility="visible",
        key="sm"
    )

    st_lottie(prof_gif)
    # Twitch

    if sm_options == "Twitch":
        options = st.selectbox(
            "Choose Graphics",
            ("Profile Photo", "Info Panels"),
            label_visibility="visible",
            key="twtich"
        )

        if options == "Profile Banner":
            st.session_state['dimension'] = (800, 800)
        if options == "Info Panels":
            st.session_state['dimension'] = (320, 200)

    # Twitter
    if sm_options == "Twitter":
        options = st.selectbox(
            "Choose GraphicsGraphics",
            ("Profile Photo", "Summary Card Image"),
            label_visibility="visible",
            key="twitter"
        )

        if options == "Profile Photo":
            st.session_state['dimension'] = (400, 400)
        if options == "Summary Card Image":
            st.session_state['dimension'] = (280, 150)
    Api_key = st.text_input("Enter API Key", "")


# input
# session state input

if "prof_images" not in st.session_state:
    st.session_state['prof_images'] = {}


if "cols" not in st.session_state:
    st.session_state['cols'] = []


if "image_varition" not in st.session_state:
    st.session_state['image_varition'] = {}


# Dall.E2 Generated image function:
# Load your API key from an environment variable or secret management service
openai.api_key = Api_key


def generation(prom):
    response = openai.Image.create(
        prompt=prom,
        n=4,
        size="256x256"
    )

    image_generated = response
    return image_generated


# Dall.E2 Variation Function
def variations(vari):
    image = vari
    width, height = 256, 256
    image = image.resize((width, height))

    # Convert the image to a BytesIO object
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()

    response = openai.Image.create_variation(
        image=byte_array,
        n=1,
        size="512x512"
    )

    # image_variation = [response['data'][0]['url'],response['data'][0]['url']]
    image_variation = response
    return image_variation


# input
# Profile Photo	800 × 800 px
with tab1:

    keywords = st.text_area("Please write to Generate Profie Pics", "")
    generate = st.button("Generate")
    try:
        if generate:
            # A list containing image data as base64 encoded strings
            st.session_state['prof_images'] = generation(keywords)

        n_cols = 4
        n_rows = 1 + len(st.session_state['prof_images']) // int(n_cols)
        rows = [st.container() for _ in range(n_rows)]
        cols_per_row = [r.columns(n_cols) for r in rows]
        st.session_state['cols'] = [
            column for row in cols_per_row for column in row]

        gen_im = st.session_state['prof_images']

        for i in range(0, 4, 1):
            v_i = gen_im['data'][i]['url']
            image = Image.open(requests.get(v_i, stream=True).raw)
            v_im = image.resize(st.session_state['dimension'])
            st.session_state['cols'][i].image(v_im)
            buf = BytesIO()
            v_im.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.session_state['cols'][i].download_button(
                label="Download",
                data=byte_im,
                file_name="generation.png",
                mime="image/png",
                key=str("Generated")+str(i)
            )
            # Variation Tab
            if st.session_state['cols'][i].button("Variations", key=str("varitions")+str(i)):
                with tab2:
                    st.session_state['image_varition'] = variations(
                        v_im)  # Calling Dall.E2 Variation Function
                    # 1st
                    v_i = st.session_state['image_varition']['data'][0]['url']

                    image = Image.open(requests.get(v_i, stream=True).raw)
                    v_im = image.resize(st.session_state['dimension'])
                    st.image(v_im)
    except:
        print("Try to write to Generate")
