import streamlit as st
from src.models.caption_retrieval import generate_captions
from src.models.controlnet_generator import generate_stylized_image
from PIL import Image


def run():
    image_columns = st.columns((1, 1), gap="medium")
    style_file_bool = False
    content_file_bool = False
    with image_columns[0]:
        content_file = st.file_uploader("Upload content file", type=['jpg', 'png', 'jpeg'])
        show_file_content = st.empty()
        if not content_file:
            show_file_content.info("Please Upload a file {}".format(' '.join(['jpg', 'png', 'jpeg'])))
        if content_file:
            content_image = content_file.getvalue()
            if isinstance(content_image, bytes):
                content_file_bool = True
                show_file_content.image(content_image)

    with image_columns[1]:
        style_file = st.file_uploader("Upload style file", type=['jpg', 'png', 'jpeg'])
        show_file_style = st.empty()
        if not style_file:
            show_file_style.info("Please Upload a file {}".format(' '.join(['jpg', 'png', 'jpeg'])))
        if style_file:
            style_image = style_file.getvalue()
            if isinstance(style_image, bytes):
                style_file_bool = True
                show_file_style.image(style_image)

    show_gen_image = st.empty()
    with st.sidebar:
        if "options" not in st.session_state:
            st.session_state.options = []
        st.session_state.tags_button_state = True
        st.session_state.generate_button_state = True
        caption_generate_button = st.button('Generate tags/styles', disabled=not(st.session_state.tags_button_state and style_file_bool))
        if caption_generate_button:
            with st.spinner('Generating tags/styles'):
                st.session_state.tags_button_state = False
                st.session_state.options = generate_captions(style_file).split(',')
                st.session_state.selected = st.session_state.options
                st.session_state.tags_button_state = True

        add_tag_text_box = st.text_input("Enter Function to be added to multiselect")
        add_tag_button = st.button('Add tag/style')
        if add_tag_text_box != "" and add_tag_button:
            if add_tag_text_box not in st.session_state.options:
                st.session_state.options.append(add_tag_text_box)
                if "selected" in st.session_state:
                    st.session_state.selected.append(add_tag_text_box)

        options_multiselect = st.multiselect('Please select the tags/styles', st.session_state.options,
                                             st.session_state.options if "selected" not in st.session_state else st.session_state.selected,
                                             key='selected')

        generate_image_button = st.button('Generate stylized image', disabled=not st.session_state.generate_button_state)
        if generate_image_button and options_multiselect and content_file_bool:
            with st.spinner('Generating Image'):
                st.session_state.generate_button_state = False
                generated_image = generate_stylized_image(', '.join(options_multiselect), content_file)
                st.session_state.generate_button_state = True
            show_gen_image.image(generated_image, caption='generated image')


if __name__ == '__main__':
    run()
