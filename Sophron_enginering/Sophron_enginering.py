import json
import sys
import os
from contextlib import suppress
import logging
import uuid
import requests
import yaml
import threading

logging.basicConfig(format="%(message)s", level=logging.INFO)


def print_title(func):
    """
    Decorator is printing function name
    """

    def inner(*args, **kwargs):
        logging.info(func.__name__[0].upper() + func.__name__[1:])
        res = func(*args, **kwargs)
        return res

    return inner


def read_json(json_file):
    """
    Read from JSON file

    """
    data = None
    try:
        with open(json_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("- JSON file not found:")
    except ValueError:
        logging.error("- Misconfigured JSON files:")
    return data


def write_yaml(json_name, yaml_name):
    """
    Write in YAML JSON file content
    """
    json_data = read_json(json_name)
    if json_data:
        with open(yaml_name + ".yaml", "w") as new_yaml:
            yaml.dump(json_data, new_yaml)
            logging.info("-Creating YAML from JSON Done:")


def make_dir(dir_name):
    """
    Creates a directory
    """
    with suppress(FileExistsError):
        os.makedirs(dir_name)


def del_dir(dir_name):
    """
    Delete a directory
    """
    web_images_folder_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.rmdir(web_images_folder_path)
    except FileNotFoundError:
        pass
    except OSError:
        logging.error("Can`t delete web_images. Folder isn`t empty:")


def save_image_by_url(image_url):
    """
    Creating random name for images
    Check if it image url
    Save images
    """
    initial_path = os.getcwd()
    file_name = uuid.uuid4().hex + ".jpg"
    image_formats = {"image/png", "image/jpeg", "image/jpg"}
    try:
        response = requests.get(image_url)
        if response.headers["content-type"] in image_formats:
            img_data = response.content
            file_destination = os.path.join(initial_path, "web_images", file_name)
            with open(file_destination, "wb") as handler:
                handler.write(img_data)
                logging.info(f"{file_name} image downloaded")
    except requests.exceptions.ConnectionError or requests.exceptions.MissingSchema:
        logging.error("Connection error:")


@print_title
def assignment_1(json_name, yaml_name):
    write_yaml(json_name, yaml_name)


@print_title
def assignment_2(json_name):
    threads = []
    make_dir("web_images")
    json_data = read_json(json_name)
    if json_data:
        for url in json_data["items"]:
            th = threading.Thread(target=save_image_by_url, args=(url["url"],))
            threads.append(th)
            th.start()
        for t in threads:
            t.join()
        logging.info("-Downloading completed:")
    del_dir("/web_images")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "assignment_1":
            if len(sys.argv) == 4:
                assignment_1(sys.argv[2], sys.argv[3])
            else:
                logging.warning("For using Assignment 1 method, you must input 2 arguments after script name.")
                logging.warning("example - assignment_1 task_urls.json yaml_1 ")
        elif sys.argv[1].lower() == "assignment_2":
            if len(sys.argv) == 3:
                assignment_2(sys.argv[2])
            else:
                logging.warning("For using Assignment 2 method, you must input 1 arguments after script name.")
                logging.warning("example - assignment_2 task_urls.json")
    else:
        logging.warning("You must enter method`s name after script name.")
else:
    json_file_name = "task_urls.json"
    yaml_file_name = "to_yaml"
    assignment_1(json_file_name, yaml_file_name)
    assignment_2(json_file_name)
