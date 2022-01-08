import os
from flask import send_from_directory
import re

# functions assistant get


def get_extension_file(file):
    return file.filename.rsplit('.', 1)[1].lower()


def get_path(file):
    return file.rsplit(".")[1].lower()


def get_all_paths_all_files():
    FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
    pasta = f"{FILES_DIRECTORY}"
    files = []
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            files.append(arquivo)
    if files:
        return {"all_files": files}
    return "Not Found"


def get_files_for_path(path):
    FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
    pasta = f"{FILES_DIRECTORY}/{path}"
    files = []
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            files.append(arquivo)
    if files:
        return files
    return "Not Found"


def get_file_name_clear_of_save(file_name: str):
    file_name = re.sub("[(){,\}/|\s]", "", file_name)
    return file_name

# functions checks


def check_file_limit_size(file):
    size_limit_mb = 1
    size_file_bytes = file.seek(0, os.SEEK_END)
    size_file_mb = size_file_bytes / 1000000
    if size_file_mb >= size_limit_mb:
        return True
    return False


def check_file_exist(file):
    FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
    extension = get_extension_file(file)
    file_name = file.filename.replace(" ", "")
    status = os.path.isfile(f"{FILES_DIRECTORY}/{extension}/{file_name}")
    if status:
        return True
    else:
        return False


def check_extension_of_file(file):
    status = -1  # false for find()
    name_file = "None"
    name_file = file.filename
    extension_allowed = os.getenv("ALLOWED_EXTENSIONSS")

    if not extension_allowed:
        extension_allowed = ["jpg", "png", "gif"]
    for element in extension_allowed:
        status = name_file.find(element)
        if(status > -1):
            return True
    return False


def check_extension_allowed_for_extension(extension):
    extension_allowed = os.getenv("ALLOWED_EXTENSIONSS")
    if not extension_allowed:
        extension_allowed = ["jpg", "png", "gif"]
    for element in extension_allowed:
        status = extension.find(element)
        if(status > -1):
            return True
    return False

# functions the actions


def upload_image(file):
    try:
        extension = get_extension_file(file)
        st = os.path.isdir(f"../../assets/{extension}")
        if not st:
            os.mkdir(f"../../assets/{extension}")
        FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")

        file_name = get_file_name_clear_of_save(file.filename)
        file.save(
            f"../../assets/{extension}/{file_name}")

        return {"msg": "Sucesso ao enviar arquivo!"}, 201
    except:
        return {"msg": "Falha ao enviar arquivo!"}, 400


def download_dir_as_zip_image(file_extension, compression_ratio):
    try:

        if (os.path.isfile("/tmp/download.zip")):
            os.remove("/tmp/download.zip")
        path_tmp = f"/tmp/download.zip"
        FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
        files_for_path_list = get_files_for_path(file_extension)
        files_for_path_str = " ".join(files_for_path_list)
        os.chdir(f"../../assets/{file_extension}")
        os.system(
            f"zip {path_tmp} {files_for_path_str}")
        response = send_from_directory(
            directory="/tmp", path="download.zip", as_attachment=True)
        return response
    except Exception:
        raise
