import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image, ExifTags

# 가장 먼저 set_page_config() 호출
st.set_page_config(page_title="Deepfake Prevention Filter (Test)", layout="wide")

# 나머지 Streamlit 코드
st.title("Deepfake Prevention Filter (Test)")
st.markdown("")
st.markdown("<span style='font-size: 18px;'>Hello! We are developing a solution to protect your photos from deepfakes.</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size: 18px;'>Our goal is to prevent personal photos posted online from being used in malicious deepfake videos. Before our official launch, we are conducting a simple test to gather your feedback.</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size: 18px;'>Recently, there have been daily reports of images uploaded to social media being misused for deepfakes. Therefore, we need your valuable opinions to find a solution.</span>", unsafe_allow_html=True)
st.markdown("")
st.markdown("<span style='font-size: 18px;'>Process 1. Upload a photo of yourself, and we will display the image with the applied prevention filter. (Your image will not be stored!)</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size: 18px;'>Process 2. Click the deepfake simulation button to view the results.</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size: 18px;'>Thank you for your participation!!</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size: 14px;'> *Prevention filter: A filter that makes subtle changes to the photo to hinder it from being learned by deepfake models.</span>", unsafe_allow_html=True)
st.markdown(
    """
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <style>
    /* 공통 스타일 */
    .stFileUploader label,
    .stRadio label,
    .stRadio div,
    .custom-caption-1,
    .custom-caption-2,
    .custom-caption-3,
    .button-container,
    .stButton button,
    .survey,
    .survey-1,
    .survey-2,
    .a-tag,
    a {
        transition: all 0.3s ease;
    }
    .stFileUploader label {
        font-size: 20px;
        font-weight: 500;
        color: #1f77b4;
    }
    .stRadio label {
        font-size: 20px;
        font-weight: 500;
        color: #1f77b4;
    }
    .stRadio div {
        display: flex;
        gap: 20px;
    }
    .custom-caption-1 {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        padding: 0 0 200px 0;
    }
    .custom-caption-2 {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        padding: 0 0 30px 0;
    }
    .custom-caption-3 {
        font-size: 30px;
        # font-weight: bold;
        text-align: center;
        margin-top: 10px;
        padding: 0 0 30px 0;
    }
    .button-container {
        text-align: center;
        margin-top: 30px;
    }
    .stButton button {
        width: 50%;
        font-size: 25px;
        padding: 10px 20px;
        background-color: #FFFFFF;
        font-weight: bold;
        color: black;
        opacity: 0.8;
        border: 3px solid black;
        border-radius: 5px;
        cursor: pointer;
        margin: 0 auto 50px auto;
        display: block;
    }
    .stButton button:hover {
        background-color: #FFFFFF;
        border: 3px solid #FF0080;
        color: #FF0080;
        opacity: 1;
    }
    .survey {
        text-align: center;
        margin-top: 10px
    }
    .survey-1 {
        font-size: 25px;
        text-align: center;
        margin-top: 10px
        font-weight: bold;
        color: #FF0080;
    }
    .survey-2 {
        text-align: center;
        margin-top: 10px
        font-weight: bold;
        padding 0 auto 50px auto
    }
    a:hover {
        color: #FF0080;
        text-decoration: none;
    }
    
    /* 스마트폰 화면 스타일 */
    @media only screen and (max-width: 600px) {
        .stFileUploader label,
        .stRadio label,
        .stButton button,
        .survey-1 {
            font-size: 16px;
        }
        .custom-caption-1,
        .custom-caption-2 {
            font-size: 24px;
            padding: 0 0 20px 0;
        }
        .custom-caption-3 {
            font-size: 20px;
            padding: 0 0 20px 0;
        }
        .stButton button {
            width: 100%;
            font-size: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def change_hair_to_blonde(image):
    # Convert to OpenCV format
    image = np.array(image)
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Define the range for hair color (dark colors)
    lower_hair = np.array([0, 0, 0])
    upper_hair = np.array([180, 255, 30])

    # Create a mask for hair
    mask = cv2.inRange(hsv, lower_hair, upper_hair)

    # Change hair color to blonde (light yellow)
    hsv[mask > 0] = (30, 255, 200)

    # Convert back to RGB color space
    image_blonde = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return image_blonde

def add_noise(image):
    # Convert to OpenCV format
    image_np = np.array(image)
    # Generate random noise
    noise = np.random.normal(0, 25, image_np.shape).astype(np.uint8)
    # Add noise to the image
    noisy_image = cv2.add(image_np, noise)
    return noisy_image

def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation, 1)
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return image

uploaded_file = st.file_uploader("Upload your Image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = correct_image_orientation(image)
    
    st.write("Processing...")

    # Save the original image as a numpy array
    image_np = np.array(image)

    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, use_column_width=True)
        st.markdown('<div class="custom-caption-1">Original image uploaded</div>', unsafe_allow_html=True)

    with col2:
        st.image(image, use_column_width=True)
        st.markdown('<div class="custom-caption-1">Image with applied filter</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-caption-1">The image with the applied filter shows no significant difference to the naked eye.</div>', unsafe_allow_html=True)

    button_clicked = st.button("Apply Deepfake Model")
    
    col3, col4 = st.columns(2)
    
    if button_clicked:
        processed_image = change_hair_to_blonde(image)
        deepfake_image = add_noise(image)
    else:
        processed_image = None
        deepfake_image = None

    if processed_image is not None and deepfake_image is not None:
        with col3:
            st.image(processed_image, use_column_width=True)
            st.markdown('<div class="custom-caption-2">Deepfake created from original image</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-caption-3">To illustrate, a deepfake algorithm that applies a yellow tint to the photo has been used. The original image will turn yellow due to the effect of the deepfake algorithm.</div>', unsafe_allow_html=True)
        
        with col4:
            st.image(deepfake_image, use_column_width=True)
            st.markdown('<div class="custom-caption-2">Deepfake created from applied filter</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-caption-3">The image with the prevention filter applied is protected from deepfake effects and produces a photo that is difficult to recognize.</div>', unsafe_allow_html=True)
        
        st.markdown('<p class="survey">If you have used similar services or are interested in our technological principles, please contact us at the email address below. We would be very grateful!</p>', unsafe_allow_html=True)
        st.markdown('<p class="survey-1">alsghksdl2827@gmail.com</p>', unsafe_allow_html=True)
        st.markdown('<p class="survey-2">Thank you for using our service! Have a great day!</p>', unsafe_allow_html=True)
        
        # Clicky script integration using components.html
        clicky_code = """
        <a title="Web Analytics" href="https://clicky.com/101461208">
            <img alt="Clicky" src="//static.getclicky.com/media/links/badge.gif" border="0" />
        </a>
        <script async data-id="101461208" src="//static.getclicky.com/js"></script>
        """
        components.html(clicky_code, height=0)
