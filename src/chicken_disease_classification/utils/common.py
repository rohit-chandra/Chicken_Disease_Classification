import os, yaml, json, joblib, base64
from box.exceptions import BoxValueError
from chicken_disease_classification import logger
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
from box import ConfigBox


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads yaml file and returns a ConfigBox object.
    
    Args:
        path_to_yaml (Path): path to yaml file
        
    Raises:
        ValueError: if yaml file is empty
        e: any other exception
    
    Returns:
        ConfigBox: ConfigBox object  
    
    """
    
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"yaml file: {path_to_yaml} is empty")
    except Exception as e:
        raise e




@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):
    """Creates directories if they do not exist.
    
    Args:
        path_to_directories (list): list of paths to directories
        ignore_log (bool, optional): ignore if mulitple dirs is to be created. Defaults to False.
    
    """
    
    for path in path_to_directories:
        os.makedirs(path, exist_ok = True)
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def save_json(path_to_json: Path, data: dict):
    """Saves data as json file.
    
    Args:
        path_to_json (Path): path to json file
        data (dict): data to be saved
    
    """
    
    with open(path_to_json, "w") as json_file:
        json.dump(data, json_file, indent = 4)
    
    logger.info(f"Saved json file at: {path_to_json}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())