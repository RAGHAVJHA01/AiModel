# This is a sample Python script.
# Import necessary libraries
import streamlit as st
from DeepImageSearch import Load_Data, Search_Setup

def main():
    st.title("Deep Image Search")

    st.sidebar.header("Load Images")
    uploaded_files = st.sidebar.file_uploader("Upload Image(s)", accept_multiple_files=True)
    folder_path = st.sidebar.text_input("Folder Path (optional)")

    if folder_path:
        image_list = Load_Data().from_folder([folder_path])
    elif uploaded_files:
        image_list = [uploaded_file for uploaded_file in uploaded_files]
    else:
        st.sidebar.warning("Please upload image(s) or specify a folder path.")

    st.sidebar.header("Search Setup")
    model_name = st.sidebar.selectbox("Choose Model", ['vgg19', 'resnet50'])
    pretrained = st.sidebar.checkbox("Pretrained", value=True)
    image_count = st.sidebar.number_input("Number of Images", min_value=1, value=100)
    search_button = st.sidebar.button("Run Index")

    if search_button and image_list:
        st.write("Indexing images...")
        search_setup = Search_Setup(image_list=image_list, model_name=model_name, pretrained=pretrained, image_count=image_count)
        search_setup.run_index()
        st.write("Indexing completed.")

        metadata = search_setup.get_image_metadata_file()

    st.sidebar.header("Add Images to Index")
    additional_uploaded_files = st.sidebar.file_uploader("Upload Additional Image(s)", accept_multiple_files=True)
    add_button = st.sidebar.button("Add Images")

    if add_button and additional_uploaded_files:
        additional_image_paths = [uploaded_file for uploaded_file in additional_uploaded_files]
        st.write("Adding images to index...")
        search_setup.add_images_to_index(additional_image_paths)
        st.write("Images added to index.")

        metadata = search_setup.get_image_metadata_file()

    st.sidebar.header("Get Similar Images")
    image_path = st.sidebar.text_input("Enter Image Path")
    number_of_images = st.sidebar.number_input("Number of Similar Images", min_value=1, value=10)
    get_similar_button = st.sidebar.button("Get Similar Images")

    if get_similar_button and image_path:
        st.write("Searching for similar images...")
        similar_images = search_setup.get_similar_images(image_path=image_path, number_of_images=number_of_images)
        st.write(similar_images)
        st.write("Similar images retrieved.")

    st.sidebar.header("Plot Similar Images")
    plot_image_path = st.sidebar.text_input("Enter Image Path for Plot")
    plot_number_of_images = st.sidebar.number_input("Number of Similar Images for Plot", min_value=1, value=9)
    plot_button = st.sidebar.button("Plot Similar Images")

    if plot_button and plot_image_path:
        st.write("Plotting similar images...")
        search_setup.plot_similar_images(image_path=plot_image_path, number_of_images=plot_number_of_images)
        st.write("Similar images plotted.")

if __name__ == "__main__":
    main()
