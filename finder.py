import json
import os
import sys
import PyPDF2

result = list()

def search(search_path: str, output_path: str, keywords: list):

    # -------------------- change working directory -------------------------------------
    try:
        os.chdir(search_path)
        print(f"changed working directory to {search_path}")
    except (FileNotFoundError, NotADirectoryError):
        print(f"{search_path} is not a directory. stop script.")
        return
    except PermissionError:
        print(f"Do not have the permission to search: {search_path}")
        return

    # ----------------------- loop through directory and subdirectories -----------------------------------
    for file in os.listdir(search_path):
        if os.path.isdir(file):
            search(search_path + "\\" + file, output_path, keywords)
        elif os.path.isfile(file):
            if file.endswith(".pdf"):
                if search_pdf_file(search_path + "\\" + file, keywords):
                    result.append(search_path + "\\" + file)
            elif file.endswith(".kuhlkjh"):
                pass

    print(result)


def search_pdf_file(file: str, keywords: list) -> bool:
    with open(file, "rb") as pdfFile:
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        for page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            text = pageObj.extractText().encode("utf-8")
            print(text)
    return False


def search_word_file(file: str, keywords: list) -> bool:
    pass
