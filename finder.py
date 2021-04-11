import os
import PyPDF2
import docx2txt
import datetime
import time

result = list()
error_files = list()

def search(search_path: str, output_path: str, keywords: list, first: bool, start_time = 0):

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
            search(search_path + "\\" + file, output_path, keywords, False)
            os.chdir(search_path)
            print(f"changed working directory to {search_path}")
        elif os.path.isfile(file):
            if file.endswith(".pdf"):
                try:
                    if search_pdf_file(search_path + "\\" + file, keywords):
                        result.append(search_path + "\\" + file)
                        print("saved pdf file path")
                except ValueError:
                    print("error with pdf file")
                    error_files.append(search_path + "\\" + file)
                    print("saved error pdf file path")
            elif file.endswith(".docx"):
                if search_word_file(search_path + "\\" + file, keywords):
                    result.append(search_path + "\\" + file)
                    print("saved docx file path")
            

    # --------------------- save result in output folder ------------------------------------------
    if first:
        save_file_path = output_path + "\\" + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + "-" + "result.txt"
        with open(save_file_path, "w") as output_file:
            output_file.write(f"used keywords: {keywords}\n")
            output_file.write(f"Found [{len(result)}] || Error [{len(error_files)}] \n\n")
            output_file.write("Found: \n")
            for path in result:
                output_file.write(path + "\n")
            output_file.write("\nError: \n")
            for error_file_path in error_files:
                output_file.write(error_file_path + "\n")
            print(f"\n\ndone [{round(time.time() - start_time)} seconds]")
            print(f"saved result in {save_file_path}")

def binary_to_string(binary):
    binary = str(binary)
    values = binary.split()
    string = ""
    for value in values:       
        
        integ = int(value)
        
        char = chr(integ)
        string += char
    return string


def binary_to_string_sentence(binary):
    text = ""
    for word in binary:
        text += binary_to_string(word)
    return text


def search_pdf_file(file: str, keywords: list) -> bool:
    print(f"searching in {file}")
    # ------------ extracting text from pdf ------------------------------------------
    with open(file, "rb") as pdfFile:
        pdfReader = PyPDF2.PdfFileReader(pdfFile)
        for page in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            text = pageObj.extractText().encode("utf-8")

            # cleaning extracted text ------------------------------------------------
            while text.find(b"\n") != -1:
                index = text.find(b"\n")
                text = text[:index] + text[index + 1:]

            # -------------------- convert binary to string ------------------------
            text = binary_to_string_sentence(text)
            # -------------------- search ------------------------------------------
            for word in text.split():
                if word.lower() in keywords:
                    print("found pdf with the given keywords")
                    return True
    print(f"keywords not in {file}")
    return False


def search_word_file(file: str, keywords: list) -> bool:
    print(f"searching in {file}")
    text = docx2txt.process(file)
    for word in text.split():
        if word.lower()in keywords:
            print("found docx with the given keywords")
            return True
    print(f"keywords not in {file}")
    return False
