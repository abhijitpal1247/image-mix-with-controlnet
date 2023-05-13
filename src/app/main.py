import streamlit as st
from io import BytesIO
from PIL import Image


def upload_file():

    image_columns = st.columns((2, 1, 2), gap="medium")
    with image_columns[0]:
        content_file = st.file_uploader("Upload content file", type=['jpg', 'png', 'jpeg'])
        show_file_content = st.empty()
        if not content_file:
            show_file_content.info("Please Upload a file {}".format(' '.join(['jpg', 'png', 'jpeg'])))
        if content_file:
            content_image = content_file.getvalue()
            if isinstance(content_image, bytes):
                show_file_content.image(content_file)

    with image_columns[2]:
        style_file = st.file_uploader("Upload style file", type=['jpg', 'png', 'jpeg'])
        show_file_style = st.empty()
        if not style_file:
            show_file_style.info("Please Upload a file {}".format(' '.join(['jpg', 'png', 'jpeg'])))
        if style_file:
            style_image = style_file.getvalue()
            if isinstance(style_image, bytes):
                show_file_style.image(style_image)


if __name__ == '__main__':
    upload_file()
