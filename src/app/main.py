import streamlit as st
from src.models.caption_retrieval import generate_captions
from src.models.controlnet_generator import generate_stylized_image
from PIL import Image


def run():
    image_columns = st.columns((1, 1), gap="medium")
    with image_columns[0]:
        content_file = st.file_uploader("Upload content file", type=['jpg', 'png', 'jpeg'])
        show_file_content = st.empty()
        if not content_file:
            show_file_content.info("Please Upload a file {}".format(' '.join(['jpg', 'png', 'jpeg'])))
        if content_file:
            content_image = content_file.getvalue()
            if isinstance(content_image, bytes):
                show_file_content.image(content_file)

    with image_columns[1]:
        style_file = st.file_uploader("Upload style file", type=['jpg', 'png', 'jpeg'])
        show_file_style = st.empty()
        if not style_file:
            show_file_style.info("Please Upload a file {}".format(' '.join(['jpg', 'png', 'jpeg'])))
            if "options" in st.session_state:
                del st.session_state.options
            if 'selected' in st.session_state:
                del st.session_state.selected
        if style_file:
            style_image = style_file.getvalue()
            if isinstance(style_image, bytes):
                show_file_style.image(style_image)
    show_gen_image = st.empty()
    with st.sidebar:
        if "options" not in st.session_state:
            st.session_state.options = []
        st.session_state.button_state = False
        caption_generate_button = st.button('Generate Captions/Styles', disabled=st.session_state.button_state)
        if caption_generate_button:
            with st.spinner('Generating Captions'):
                st.session_state.button_state = True
                st.session_state.options = generate_captions(style_file).split(',')
                st.session_state.button_state = False
        options_multiselect = st.multiselect('Please select the captions/styles', st.session_state.options,
                                             key='selected')
        generate_image_button = st.button('Generate stylized image')
        if generate_image_button and options_multiselect:
            with st.spinner('Generating Image'):
                generated_image = generate_stylized_image(', '.join(options_multiselect), content_file)
            show_gen_image.image(generated_image, caption='generated image')


if __name__ == '__main__':
    run()
