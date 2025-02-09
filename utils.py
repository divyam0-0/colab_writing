import os
import dropbox
import streamlit as st

# Configuration for Dropbox integration
EXCEL_FILE = "haiku_chains.xlsx"
DROPBOX_FILE_PATH = "/haiku_chains.xlsx"  # Dropbox path for your Excel file
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')

def download_excel_from_dropbox():
    """
    Download the Excel file from Dropbox and save it locally.
    If the file does not exist on Dropbox, returns False so you can initialize it.
    """
    if not DROPBOX_ACCESS_TOKEN:
        st.error("DROPBOX_ACCESS_TOKEN is not set in the environment.")
        return False

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    try:
        metadata, res = dbx.files_download(DROPBOX_FILE_PATH)
        with open(EXCEL_FILE, "wb") as f:
            f.write(res.content)
        # st.info("Excel file downloaded from Dropbox.")
        return True
    except dropbox.exceptions.ApiError as e:
        st.warning("Excel file not found on Dropbox. It will be initialized locally.")
        return False

def upload_excel_to_dropbox():
    """
    Upload the local Excel file to Dropbox, overwriting any existing file.
    Returns True if successful, False otherwise.
    """
    if not DROPBOX_ACCESS_TOKEN:
        st.error("DROPBOX_ACCESS_TOKEN is not set in the environment.")
        return False

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    try:
        with open(EXCEL_FILE, "rb") as f:
            dbx.files_upload(f.read(), DROPBOX_FILE_PATH, mode=dropbox.files.WriteMode.overwrite)
        # st.success("Excel file uploaded to Dropbox!")
        return True
    except Exception as e:
        st.error(f"Error uploading Excel file: {e}")
        return False

# For testing purposes: run this file directly
if __name__ == "__main__":
    if upload_excel_to_dropbox():
        print("Upload successful.")
    else:
        print("Upload failed.")

    if download_excel_from_dropbox():
        print("Download successful.")
    else:
        print("No file found; please initialize a new Excel file.")

