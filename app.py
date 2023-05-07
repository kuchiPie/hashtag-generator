import streamlit as st

from get_image_caption import get_caption, get_hashtags 


# Set up the Streamlit application
st.title("Get Trendy Hashtags for your Image!")

# Allow the user to upload an image file
image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# If an image file was uploaded, display it and hashtag extraction on it
if image_file is not None:

    # hashtag extraction on the image
    caption = get_caption(image_file)
    
    hashtags = get_hashtags(caption)

    st.write("Related Top 10 Trendy Instagram Hashtags:")
    
    for i, hashtag in enumerate(hashtags):
        st.write(str(i+1) + '. '+ hashtag)
