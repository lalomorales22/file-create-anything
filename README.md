# File-Convert-Anything

File-Convert-Anything is a versatile file conversion tool built with Streamlit. It allows users to convert various file formats with ease through a user-friendly web interface.

## Features

- Support for multiple file formats including:
  - Text files (TXT)
  - Images (JPEG, PNG, GIF, BMP, TIFF, WEBP)
  - PDFs
  - Microsoft Word documents (DOCX)
  - CSV files
  - JSON and JSONL files
  - XML files
  - YAML files
  - Excel spreadsheets (XLSX)
- File preview functionality
- Custom dark theme for better user experience
- Additional conversion options for specific formats (e.g., image quality, CSV delimiter)
- Progress bar for conversion process
- Easy-to-use file upload and download interface

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/file-convert-anything.git
   cd file-convert-anything
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install streamlit pillow pandas python-magic-bin docx2txt PyPDF2 openpyxl pyyaml xmltodict reportlab
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501` (or the URL provided in the terminal).

3. Use the file uploader to select a file for conversion.

4. Choose the desired output format from the dropdown menu.

5. Adjust any additional options if available for the selected conversion.

6. Click the "Convert" button to start the conversion process.

7. Once the conversion is complete, use the download link to get your converted file.

## Supported Conversions

- Text files (TXT) to: PDF, DOCX, HTML, CSV, JSON, JSONL, XML, YAML
- Images (JPEG, PNG) to: PNG, JPEG, GIF, BMP, TIFF, WEBP
- PDFs to: TXT, DOCX, HTML
- Microsoft Word documents (DOCX) to: PDF, TXT, HTML
- CSV files to: JSON, JSONL, XML, YAML, XLSX, HTML, TSV
- JSON files to: CSV, JSONL, XML, YAML, XLSX, HTML, TSV
- JSONL files to: CSV, JSON, XML, YAML, XLSX, HTML, TSV
- XML files to: JSON, JSONL, CSV, YAML, XLSX, HTML, TSV
- YAML files to: JSON, JSONL, XML, CSV, XLSX, HTML, TSV
- Excel spreadsheets (XLSX) to: CSV, JSON, JSONL, XML, YAML, HTML, TSV

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- All the open-source libraries used in this project

