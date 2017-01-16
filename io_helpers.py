from pathlib import Path

import os, json


home_directory = os.path.dirname(os.path.realpath(__file__))

def find_local_file(file_name):
    file = Path("/".join([home_directory,  file_name]))
    return file.is_file()

def find_local_route_json(file_name):
    file = Path("/".join([home_directory, "routes",file_name + ".json"]))
    return file.is_file()


def read_local_file(file_name):
    if not find_local_file(file_name):
        return None
    file = open("/".join([home_directory,  file_name]), "r").readlines()
    return "".join(file)

def read_local_route_json(file_name):
    file = "/".join([home_directory, "routes", file_name + ".json"])

    if not find_local_route_json(file_name):
        return None
    url_targets = open(file, "r").readlines()
    return  json.loads("".join(url_targets).replace("\n",""))

def write_local_route_json(input, file_name):
    file = open("/".join([home_directory, "routes", file_name + ".json"]), 'w')
    json.dump(input, file)
    file.close()
    return True


def delete_local_route_json(file_name):
    file = Path("/".join([home_directory, "routes", file_name + ".json"]))
    os.remove(file)