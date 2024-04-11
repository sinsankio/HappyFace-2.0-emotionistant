import os

FILE_ROOT_DIR = "../tools/descriptions"


def get_description_text(tool_name: str = "HappyFaceSearchResultsTool") -> str | None:
    file_path = os.path.join(FILE_ROOT_DIR, tool_name + ".txt")
    try:
        with open(file_path, 'r') as desc_file:
            return desc_file.read()
    except FileNotFoundError:
        pass
