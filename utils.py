import os
import dropbox
import streamlit as st

# Configuration for Dropbox integration
EXCEL_FILE = "haiku_chains.xlsx"
DROPBOX_FILE_PATH = "/haiku_chains.xlsx"  # Dropbox path for your Excel file
DROPBOX_ACCESS_TOKEN = "sl.u.AFiWZNgmjzLyyR8z49mFwo3ct0jWpcs-Gi91fHXuFBlyTOgInvI9PHcJcqy2Zba3P4tYNV9BSqxBLfqhBpkkwDLtOVNmB6cBivHZk-kIAcWFpDr7MSXxIpxS4gOWyEsosD7V6A8eB34MgOzbsCU_22EN36PFp4N1Sv-t1W3yXHqBcPCL3lawllCDy73jac_KzKwfsz3OpW-JLOs_LFWK6WlPT5f1xmWo3utKNzYingjBALG3AGJhWXNwYab-emq5fr98oGtAVywrcFevbUWxmgGn2l5_I2VeF-AkUdu115FA80lVtmZpxtJ_S4jd3nE0ch9mq5206bXW-J3TP93KYOfDmxbRmgNfOZsqUewV4YC-NnxsmgaZygGGy7e_nOyOoe5telEHpbxHN8fglQGzxmXVnxmuZlYN8fGQnQu86AvXMHGCE-EIqsBYfmwcGa4N4Mr-M4ZWTlyRHvo4rwT_jjeJwFNBn09HrHra-CPVS-oMmY_ApKJfvOMbwbRAJahwGeI1_I_8zO9NGlhiP6ihq5l5aGMfDzHqFynai-sNFYDqUvtOInlGUQjxZIUfRvTS2PINye6y1V5IQO4bj00H-24ahyHbo3RoH0LtnyPZkb_pNReMhsWGi-ZJrZi1Xwe99uAyEw-nYsSqI49Nm27uxdvOlkSKrv8LaisqZugWo42wtsSYfu4mkdKUaSxCytULwlMHYaG55FcaqQGNjl2ErPuY7YANd98gXYmWjmXFmJxJxiceWEYa-6S8bnoU60Zg2tO3NHFsgIkIVSpQFQgoYfvIFxOlgstTWiVVIiP5Gexw0PBlbpR3xQMSUCVdqbA6goiAzUR10_yJzif1RJCKU7B9lZMHob9_mDJzrcZhMP-P3L2eaBv9u5ayEDVJWYvZNEkmgyKYAD9wFHc3qIsV5S1xizK76PP0Z53ct474szU9i8J7q9w9aOf7SB36nYDSaVn7fFtcZttjZH1SYK60pLUEtRzOzkSvYYQvaMX9BFERm4H1elAZ5XDoCbSr62lpTLJPxRm5ulrYuW0sbSednUkf5aJJv0p_bA0fzdJvL_NbKf0O3993U0NLRYcjz0jcRjfiMjIqUe1xAFUOIz886z42fXO7PAaHuDLXBIXNgOM--geadQh8OTYQgJXVmy5ehBK1wuGENVebqg-cOiEtjCksSukZBTpcnXR1bTycurB-KLrDUXGcdd18S8fERpQoF-64vi2pcMG-BTikXX2YzOvKk8LJr23PDuVfY7BRysQB0eW3Nucq0KYlOHQMK6nwdYtop-VI4OcmJQWhIJOzeMLy"

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

