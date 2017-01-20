from pathlib import Path

import os, json


home_directory = os.path.dirname(os.path.realpath(__file__))
route_directory = "/".join([home_directory,"routes"])

def find_case_insensitive_file(directory, file_name):
    file = Path("/".join([directory, file_name.lower()]))
    return file.is_file()

def read_case_insensitive_file(directory, file_name):
    if not find_case_insensitive_file(directory, file_name):
        return None
    file = open("/".join([directory, file_name.lower()]), "r").readlines()
    return "".join(file)

def write_case_insensitive_file(input, directory, file_name):
    if find_case_insensitive_file(directory, file_name):
        return False
    file = open("/".join([route_directory, file_name.lower()]), "w")
    file.write(input)
    file.close()
    return True

def alter_case_insensitive_file(input, directory, file_name):
    if not find_case_insensitive_file(directory, file_name):
        return False
    file = open("/".join([route_directory, file_name.lower()]), "w")
    file.write(input)
    file.close()
    return True

def delete_case_insensitive_file(directory, file_name):
    if not find_case_insensitive_file(directory, file_name):
        return False
    file = Path("/".join([directory, file_name.lower()]))
    os.remove(file)
    return True



def find_local_file(file_name):
    return find_case_insensitive_file(home_directory, file_name)

def find_local_route_json(file_name):
    json_file = (file_name + ".json").lower()
    return find_case_insensitive_file(route_directory, json_file)


def read_local_file(file_name):
    return read_case_insensitive_file(home_directory, file_name)

def read_local_route_json(file_name):
    json_file = read_case_insensitive_file(route_directory, file_name + ".json")
    if json_file is None:
        return None
    return  json.loads("".join(json_file).replace("\n",""))

def write_local_route_json(input, file_name):
    return write_case_insensitive_file(json.dumps(input), route_directory, file_name + ".json")

def alter_local_route_json(input, file_name):
    return alter_case_insensitive_file(json.dumps(input), route_directory, file_name + ".json")

def delete_local_route_json(file_name):
    return delete_case_insensitive_file(route_directory, file_name + ".json")

def create_routes_folder():
    if not Path("/".join([home_directory,"routes"])).is_dir():
        os.makedirs(home_directory)