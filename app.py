# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Define a function to generate a response from the API
def get_response(input_prompt, image):
    """
    Generate a response from the API.

    Args:
        input_prompt: The prompt to use for the API call.
        image: The input image.

    Returns:
        The response from the API.
    """

    # Create a Generative Model object
    model = genai.GenerativeModel('gemini-pro-vision')

    # Generate the response
    response = model.generate_content([input_prompt, image[0]])

    # Return the response text
    return response.text


# Define a function to prepare the input image
def input_image_setup(uploaded_file):
    """
    Prepare the input image for the API call.

    Args:
        uploaded_file: The uploaded image file.

    Returns:
        A list of image parts.
    """

    # Check if a file was uploaded
    if uploaded_file is not None:

        # Get the bytes of the image
        bytes_data = uploaded_file.getvalue()

        # Create a list of image parts
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]

        # Return the list of image parts
        return image_parts

    # If no file was uploaded, raise an error
    else:
        raise FileNotFoundError("No file uploaded")


# Set the page configuration
st.set_page_config(page_title="Gemini Health App")

# Create a header for the app
st.header("Gemini Health App")

# Create a file uploader for the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize the image variable
image = ""

# If an image was uploaded, display it
if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)

    # Display the image
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Create a button to submit the form
submit = st.button("Tell me the total calories")

# Define the input prompt for the API call
input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               
Finally, also mention whether the food is healthy or not and also mention the percentage splits of the ratio of 
carbohydrates, fats, fibres, sugar and other important things required in our diet.
"""

# If the submit button was clicked, call the API and display the response
if submit:

    # Prepare the input image
    image_data = input_image_setup(uploaded_file)

    # Get the response from the API
    response = get_response(input_prompt, image_data)

    # Create a subheader for the response
    st.subheader("The Response is")

    # Write the response to the page
    st.write(response)
