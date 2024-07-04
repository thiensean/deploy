import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def resize_image(image, target_size):
    # Calculate the new size maintaining aspect ratio
    aspect_ratio = image.width / image.height
    if image.width < image.height:
        new_width = target_size
        new_height = int(target_size / aspect_ratio)
    else:
        new_height = target_size
        new_width = int(target_size * aspect_ratio)
    return image.resize((new_width, new_height))

st.title("AI Inference with Sean's API")

# Accept any image file type
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "bmp", "tiff"])

if uploaded_file is not None:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    
    # Resize the image to 480 pixels on the shorter side
    resized_image = resize_image(image, 480)
    
    # Display the resized image
    st.image(resized_image, caption='Resized Image.', use_column_width=True)
    
    # Convert the resized image to bytes
    byte_arr = BytesIO()
    resized_image.save(byte_arr, format='PNG')
    file_bytes = byte_arr.getvalue()
    
    # Send the resized image to the FastAPI server
    ngrok_url = "https://f077-35-221-222-158.ngrok-free.app"  # Replace with your actual Ngrok URL
    response = requests.post(f"{ngrok_url}/process-image/", files={"file": ("resized_image.png", file_bytes, "image/png")})
    
    if response.status_code == 200:
        response_json = response.json()
        text_result = response_json.get("result", "")
        st.write("Result:", text_result)
    else:
        st.error("Failed to process image. Status code: {}".format(response.status_code))
