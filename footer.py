# for now we aren't adding a footer


# Footer with background image using base64 encoding
def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    return base64.b64encode(data).decode()

# Local path to the image
image_path = "C:\\Users\\jonat\\Documents\\GitHub\\ihackf24-main\\background_wallpaper.jpg"
base64_image = get_base64_image(image_path)

# Footer with background image using base64 encoding
footer_html = f"""
    <style>
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        padding: 40px;
        text-align: center;
        color: white;
        font-size: 16px;
        z-index: 1;
    }}
    body {{
        margin-bottom: 200px; /* Ensure footer doesn't overlap with the content */
    }}
    </style>
    <div class="footer">
  
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
