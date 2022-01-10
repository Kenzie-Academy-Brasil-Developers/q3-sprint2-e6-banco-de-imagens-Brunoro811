import os
from flask import Flask, request, send_from_directory


from app.kenzie.image import get_all_paths_all_files, upload_image, check_extension_of_file, check_file_exist, get_path, download_dir_as_zip_image, check_extension_allowed_for_extension, get_files_for_path
app = Flask(__name__)
# Observação coloquei diretamente nas configurações do flask pois no .venv não funcionou
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000


def create_path_assets():
    #os.chdir("cd ../../")
    if not os.path.isdir("assets"):
        os.system("mkdir assets")


create_path_assets()


@app.get("/")
def home():
    return {"msg": "Bem vindo a entrega Entrega 6 - Banco de Imagens"}


@app.post("/upload")
def upload_file():
    try:
        files = request.files
        if(files):
            file = files['file']
            result = {"msg": "retorno obrigatorio"}
            if not check_extension_of_file(file):
                return {"msg": "formado não suportado"}, 415
            if check_file_exist(file):
                return {"msg": "Arquivo ja existe!"}, 409
            result = upload_image(file)
            return result
    except Exception:
        return {"msg": "Arquivo maior que 1MB!"}, 413


@app.get("/files")
def files():
    result = get_all_paths_all_files()
    if result:
        return result
    return {"msg": "listar todos os arquivos"}


@app.get("/files/<extension>")
def files_extension(extension):

    if not check_extension_allowed_for_extension(extension):
        return {"msg": "Formato invalido!"}, 404
    files = get_files_for_path(extension)
    return {
        "files": files
    }


@app.get("/download/<file_name>")
def download(file_name):
    try:
        if(file_name):
            FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
            path = get_path(file_name)
            return send_from_directory(
                directory=f"{FILES_DIRECTORY}/{path}",
                path=file_name,
                as_attachment=True
            ), 200
    except:
        # raise
        return {"msg": "Não encontrado"}, 404


@app.get("/download-zip")
def download_dir_as_zip():
    try:
        file_extension = request.args.get("file_extension")
        compression_ratio = request.args.get("compression_ratio")
        return download_dir_as_zip_image(file_extension, compression_ratio)
    except:
        return {"msg": "erro"}, 404
