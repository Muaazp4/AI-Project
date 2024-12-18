import streamlit as st
from PIL import Image
import easyocr
import re
import numpy as np

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Function to extract text using EasyOCR
def extract_text(image):
    # Convert the image to a NumPy array for EasyOCR
    image_np = np.array(image)
    result = reader.readtext(image_np)
    
    # Join detected text into a single string
    text = " ".join([item[1] for item in result])
    
    # OCR cleanup: fix common misreads
    text = text.replace("o", "0")  # Replace lowercase 'o' with zero '0'
    text = text.replace("O", "0")  # Replace uppercase 'O' with zero '0'
    text = text.replace("l", "1")  # Replace lowercase 'l' with one '1'
    text = text.replace("I", "1")  # Replace uppercase 'I' with one '1'
    
    return text.upper()  # Return cleaned and uppercase text

# Function to extract invoice details using Regex
import re

def extract_invoice_details(text):
    # Improved regex for invoice details
    invoice_number = re.search(r"Invoice\s*#?\s*[:\-]?\s*([A-Za-z0-9\-]+)", text, re.IGNORECASE)

    # Flexible date matching: e.g., "05 Aug 2024", "2024-08-05", "08/05/2024"
    date = re.search(r"(\b\d{1,2}[\s/-][A-Za-z]{3}[\s/-]\d{4}\b|\b\d{4}[\s/-]\d{2}[\s/-]\d{2}\b)", text)

    # Match Total Amount with optional currency symbol
    total_amount = re.search(r"(?:Total\s*Amount|Balance\s*Due|Total)\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})", text, re.IGNORECASE)

    # Add currency to total amount if found
    total_amount_value = f"${total_amount.group(1)}" if total_amount else "Not found"

    return {
        "Invoice Number": invoice_number.group(1) if invoice_number else "Not found",
        "Date": date.group(1) if date else "Not found",
        "Total Amount": total_amount_value
    }


# Streamlit App
def main():
    st.title("Invoice Data Extractor")
    st.write("Upload an invoice image to extract key details.")

    # File uploader
    uploaded_file = st.file_uploader("Upload Invoice (Image)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Open the image using PIL
        image = Image.open(uploaded_file)

        # Display uploaded image
        st.image(image, caption="Uploaded Invoice", use_container_width=True)

        # Extract text
        with st.spinner("Extracting text..."):
            extracted_text = extract_text(image)

        # Display extracted text
        st.subheader("Extracted Text")
        st.text(extracted_text)

        # Extract key details
        details = extract_invoice_details(extracted_text)

        # Display extracted details
        st.subheader("Extracted Invoice Details")
        st.json(details)

if __name__ == "__main__":
    main()
