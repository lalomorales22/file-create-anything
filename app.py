import streamlit as st
import mimetypes
from PIL import Image
import pandas as pd
import docx2txt
from PyPDF2 import PdfReader
import csv
import json
import yaml
import xmltodict
import openpyxl
from io import BytesIO, StringIO
import base64
import time

# Set page config
st.set_page_config(page_title="File-Convert-Anything", layout="wide")

# Custom theme
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stSelectbox, .stTextInput {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .stButton>button {
        color: #1E1E1E;
        background-color: #4CAF50;
        border-radius: 20px;
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

def get_file_info(file):
    return {
        "Name": file.name,
        "Size": f"{file.size} bytes",
        "Type": file.type if file.type else mimetypes.guess_type(file.name)[0] or "application/octet-stream"
    }

def get_supported_conversions(file_type):
    conversions = {
        "text/plain": ["PDF", "DOCX", "HTML", "CSV", "JSON", "JSONL", "XML", "YAML"],
        "image/jpeg": ["PNG", "GIF", "BMP", "TIFF", "WEBP"],
        "image/png": ["JPEG", "GIF", "BMP", "TIFF", "WEBP"],
        "application/pdf": ["TXT", "DOCX", "HTML"],
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ["PDF", "TXT", "HTML"],
        "text/csv": ["JSON", "JSONL", "XML", "YAML", "XLSX", "HTML", "TSV"],
        "application/json": ["CSV", "JSONL", "XML", "YAML", "XLSX", "HTML", "TSV"],
        "application/x-ndjson": ["CSV", "JSON", "XML", "YAML", "XLSX", "HTML", "TSV"],
        "text/xml": ["JSON", "JSONL", "CSV", "YAML", "XLSX", "HTML", "TSV"],
        "text/yaml": ["JSON", "JSONL", "XML", "CSV", "XLSX", "HTML", "TSV"],
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ["CSV", "JSON", "JSONL", "XML", "YAML", "HTML", "TSV"]
    }
    return conversions.get(file_type, [])

def convert_file(file, file_type, target_format):
    content = file.getvalue()
    
    if file_type == "text/plain":
        if target_format.upper() == "PDF":
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            text = content.decode('utf-8')
            c.drawString(100, 750, text)
            c.save()
            return buffer.getvalue()
        elif target_format.upper() == "JSONL":
            # Convert plain text to JSONL
            lines = content.decode('utf-8').splitlines()
            jsonl_output = []
            for line in lines:
                jsonl_output.append(json.dumps({"text": line.strip()}))
            return '\n'.join(jsonl_output).encode('utf-8')
        elif target_format.upper() == "JSON":
            # Convert plain text to JSON
            lines = content.decode('utf-8').splitlines()
            json_output = [{"text": line.strip()} for line in lines]
            return json.dumps(json_output).encode('utf-8')
    
    elif file_type.startswith("image/") and target_format.upper() in ["PNG", "JPEG", "GIF", "BMP", "TIFF", "WEBP"]:
        img = Image.open(BytesIO(content))
        img_buffer = BytesIO()
        img.save(img_buffer, format=target_format.upper())
        return img_buffer.getvalue()
    
    elif file_type == "application/pdf" and target_format == "TXT":
        pdf = PdfReader(BytesIO(content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text.encode('utf-8')
    
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" and target_format == "TXT":
        text = docx2txt.process(BytesIO(content))
        return text.encode('utf-8')
    
    elif file_type in ["text/csv", "application/json", "application/x-ndjson", "text/xml", "text/yaml", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        # Load the data into a pandas DataFrame
        if file_type == "text/csv":
            df = pd.read_csv(BytesIO(content))
        elif file_type == "application/json":
            df = pd.read_json(BytesIO(content))
        elif file_type == "application/x-ndjson":
            df = pd.read_json(BytesIO(content), lines=True)
        elif file_type == "text/xml":
            df = pd.read_xml(BytesIO(content))
        elif file_type == "text/yaml":
            data = yaml.safe_load(BytesIO(content))
            df = pd.DataFrame(data)
        elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(BytesIO(content))
        
        # Convert the DataFrame to the target format
        if target_format.upper() == "CSV":
            output = df.to_csv(index=False).encode('utf-8')
        elif target_format.upper() == "JSON":
            output = df.to_json(orient="records").encode('utf-8')
        elif target_format.upper() == "JSONL":
            output = df.to_json(orient="records", lines=True).encode('utf-8')
        elif target_format.upper() == "XML":
            output = df.to_xml().encode('utf-8')
        elif target_format.upper() == "YAML":
            output = yaml.dump(json.loads(df.to_json(orient="records"))).encode('utf-8')
        elif target_format.upper() == "XLSX":
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            output = excel_buffer.getvalue()
        elif target_format.upper() == "HTML":
            output = df.to_html(index=False).encode('utf-8')
        elif target_format.upper() == "TSV":
            output = df.to_csv(index=False, sep='\t').encode('utf-8')
        else:
            raise ValueError(f"Conversion to {target_format} is not supported.")
        
        return output
    
    else:
        raise ValueError(f"Conversion from {file_type} to {target_format} is not supported.")

def get_file_preview(file, file_type):
    content = file.getvalue()
    if file_type.startswith('image/'):
        return content
    elif file_type in ['text/plain', 'text/csv', 'application/json', 'text/xml', 'text/yaml']:
        return content.decode('utf-8')[:1000] + '...' if len(content) > 1000 else content.decode('utf-8')
    else:
        return None

# Main app
st.title("File-Convert-Anything")
st.subheader("Your Ultimate File Conversion Tool")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=None)

if uploaded_file is not None:
    file_info = get_file_info(uploaded_file)
    
    # Display file information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", file_info["Name"])
    with col2:
        st.metric("File Size", file_info["Size"])
    with col3:
        st.metric("File Type", file_info["Type"])
    
    # File preview
    preview = get_file_preview(uploaded_file, file_info["Type"])
    if preview:
        if file_info["Type"].startswith('image/'):
            st.image(preview, caption="File Preview", use_column_width=True)
        else:
            st.text_area("File Preview", preview, height=200)
    
    supported_conversions = get_supported_conversions(file_info["Type"])
    
    if supported_conversions:
        target_format = st.selectbox("Convert to:", supported_conversions)
        
        # Additional options
        st.subheader("Additional Options")
        if target_format.upper() in ['CSV', 'TSV']:
            delimiter = st.text_input("Delimiter", value="," if target_format.upper() == 'CSV' else "\t")
        if target_format.upper() in ['JPEG', 'PNG', 'WEBP']:
            quality = st.slider("Image Quality", 1, 100, 85)
        
        if st.button("Convert"):
            try:
                # Show progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                converted_file = convert_file(uploaded_file, file_info["Type"], target_format)
                
                # Create download link
                b64 = base64.b64encode(converted_file).decode()
                href = f'<a href="data:application/{target_format.lower()};base64,{b64}" download="converted_file.{target_format.lower()}">Download converted {target_format} file</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                # Show success message
                st.success("Conversion completed successfully!")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"An error occurred during conversion: {str(e)}")
    else:
        st.warning("No supported conversions for this file type.")
else:
    st.info("Please upload a file to begin.")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ by Your Name")