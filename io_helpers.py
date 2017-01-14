import os, json

home_directory = os.path.dirname(os.path.realpath(__file__))

def find_local_json(file_name):
    url_targets = open("/".join([home_directory,  file_name + ".json"]), "r").readlines()
    return  json.loads("".join(url_targets).replace("\n",""))

def write_input_to_file(input,file_name):
    file = open("/".join([home_directory,"routes",file_name + ".json"]), 'w')
    json.dump(input, file)
    file.close()

def find_local_file(file_name):
    file = open("/".join([home_directory,  file_name]), "r").readlines()
    return "".join(file)