import streamlit as st
from PIL import Image
import easyocr
import re

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Function to extract text using EasyOCR
def extract_text(image):
    result = reader.readtext(image)
    return " ".join([item[1] for item in result])

# Function to extract invoice details using Regex
def extract_invoice_details(text):
    invoice_number = re.search(r"Invoice\s*Number:\s*(\S+)", text, re.IGNORECASE)
    date = re.search(r"Date:\s*([\d/.-]+)", text, re.IGNORECASE)
    total_amount = re.search(r"Total:\s*\$?([\d,]+\.\d{2})", text, re.IGNORECASE)

    return {
        "Invoice Number": invoice_number.group(1) if invoice_number else "Not found",
        "Date": date.group(1) if date else "Not found",
        "Total Amount": total_amount.group(1) if total_amount else "Not found"
    }

# Streamlit App
def main():
    st.title("Invoice Data Extractor")
    st.write("Upload an invoice image to extract key details.")

    # File uploader
    uploaded_file = st.file_uploader("Upload Invoice (Image)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Invoice", use_column_width=True)

        # Extract text
        with st.spinner("Extracting text..."):
            extracted_text = extract_text(uploaded_file)

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
