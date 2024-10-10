# BizCardX: Extracting Business Card Data with OCR

This project provides a solution for extracting and managing data from business cards using OCR (Optical Character Recognition). The platform enables users to upload business card images, automatically extract text information, and store it in a database for further management. It includes features for reading, updating, and deleting extracted data via a user-friendly interface.

## Features

- **Business Card Upload & OCR:** Users can upload business card images, and the system uses OCR (via easyOCR) to extract relevant information such as names, phone numbers, emails, and company names.
- **Data Management:** Extracted information is stored in a database, allowing for efficient retrieval. Users can perform CRUD operations (Create, Read, Update, Delete) through the app interface.
- **Highlighted Text in Images:** Extracted text from the business card is visually highlighted using Pillow to enhance user understanding of OCR results.
- **Interactive UI:** Developed with Streamlit, providing an easy-to-use interface for uploading, viewing, and managing business card data.
- **Secure & Efficient:** Designed to ensure data privacy and performance, with scalable architecture for handling multiple cards and records.

## Workflow

The workflow of this project can be summarized as follows:

1. **Business Card Upload:** Users upload an image of a business card through the Streamlit application UI.
2. **OCR Processing:** The uploaded image is processed using easyOCR, which extracts text details like names, phone numbers, emails, and addresses.
3. **Text Highlighting:** The extracted text is highlighted on the business card image using the Pillow library for visual representation.
4. **Data Storage:** The extracted data is stored in a MySQL database for persistent storage and easy access.
5. **Data Management:** Users can manage the data (CRUD operations) directly from the Streamlit UI, allowing for updates, deletion, or reviewing the data associated with each business card.

## Technologies Used

- **Python:** Main programming language used for development and scripting.
- **Libraries:** easyOCR, Pillow, Pandas
- **Database:** MySQL for storing and managing the extracted business card data.
- **User Interface:** Streamlit for building an interactive web-based interface for users.

## References

- **Python:** [https://docs.python.org/3/](https://docs.python.org/3/)
- **easyOCR:** [https://github.com/JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR)
- **Pillow:** [https://pillow.readthedocs.io/en/stable/](https://pillow.readthedocs.io/en/stable/)
- **Pandas DataFrame:** [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)
- **MySQL Documentation:** [https://www.mysql.com/](https://www.mysql.com/)
- **Streamlit Documentation:** [https://docs.streamlit.io/library/api-reference](https://docs.streamlit.io/library/api-reference)
