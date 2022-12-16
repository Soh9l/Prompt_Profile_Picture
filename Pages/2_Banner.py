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


banner_gif = load_lottieurl(
    "https://assets1.lottiefiles.com/packages/lf20_mhkmlqef.json")

# Load your API key from an environment variable or secret management service
openai.api_key = "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"


# High quality 3d render synthwave style landscape where a futuristic cyborg wearing a headphone sitting in the middle drawing on a canvas.

# Space out the maps so the first one is 2x the size of the other three
# c1, c2, c3, c4, c5, c6, c7, c8 = st.columns((2, 1, 1, 1, 1, 1, 1, 1))
st.set_page_config(layout="wide")
# title
st.title("Generate Banner images")

tab1, tab2 = st.tabs(['Banner', 'Varitions'])

if "sm_options" not in st.session_state:
    st.session_state.options = "sm"

if "dimension" not in st.session_state:
    st.session_state['dimension'] = (810, 312)

with st.sidebar:

    sm_options = st.selectbox(
        "Which Social Media?",
        ("Twitch", "Twitter"),
        label_visibility="visible",
        key="sm"
    )

    st_lottie(banner_gif)
    # Twitch

    if sm_options == "Twitch":
        options = st.selectbox(
            "Choose Graphics",
            ("Profile Banner", "Video Player Banner", "Cover Image"),
            label_visibility="visible",
            key="twtich"
        )

        if options == "Profile Banner":
            st.session_state['dimension'] = (1920, 480)
        if options == "Video Player Banner":
            st.session_state['dimension'] = (1920, 1080)
        if options == "Cover Image":
            st.session_state['dimension'] = (380, 1200)

    # Twitter
    if sm_options == "Twitter":
        options = st.selectbox(
            "Choose Graphics",
            ("Header Photo", "Cards Image", "Twitter Post"),
            label_visibility="visible",
            key="twitter"
        )

        if options == "Header Photo":
            st.session_state['dimension'] = (1500, 500)
        if options == "Cards Image":
            st.session_state['dimension'] = (800, 320)
        if options == "Twitter Post":
            st.session_state['dimension'] = (1024, 512)

    Api_key = st.text_input("Enter API Key", "")

# input
# session state input

if "images" not in st.session_state:
    st.session_state['images'] = []


if "image_varition" not in st.session_state:
    st.session_state['image_varition'] = []

# Dall.E2 Variation Function
# Load your API key from an environment variable or secret management service
openai.api_key = Api_key


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


with tab1:
    with st.form("Generate"):
        keywords = st.text_area("Please write to Generate Banner", "")
        generate = st.form_submit_button("Generate")

    if generate:
        generator = Craiyon()  # Instantiates the api wrapper
        result = generator.generate(
            keywords
        )  # Generates 9 images by default and you cannot change that
        # A list containing image data as base64 encoded strings
        st.session_state['images'] = result.images

    for image_index, i in enumerate(st.session_state['images']):
        image = Image.open(BytesIO(base64.decodebytes(i.encode("utf-8"))))
        im = image.resize(st.session_state['dimension'])
        st.image(im)
        buf = BytesIO()
        im.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download",
            data=byte_im,
            file_name="generation.png",
            mime="image/png",
            key=str(image_index)+str(i)
        )
        if st.button("Variations", key=str("varitions")+str(image_index)+str(i)):
            with tab2:
                st.session_state['image_varition'] = variations(
                    im)  # Calling Dall.E2 Variation Function
                # 1st
                v_i = st.session_state['image_varition']['data'][0]['url']

                image = Image.open(requests.get(v_i, stream=True).raw)
                v_im = image.resize(st.session_state['dimension'])
                st.image(v_im)
                # buf = BytesIO()
                # v_im = v_i.resize(st.session_state['dimension'])
                # v_im.save(buf, format="PNG")
                # byte_im1 = buf.getvalue()
                # btn = st.download_button(
                #           label="Download Variation",
                #          data=byte_im1,
                #         file_name="variation generation1.png",
                #        mime="image/png",
                #       key=str("Variation Generated")
                #      )


# for i in images:
    # st.image(img)
