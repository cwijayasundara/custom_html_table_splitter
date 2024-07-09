import json

""" write a function to load the json file from docs/sales_sample.json """


def load_json_file(filename):
    with open(filename, "r") as file:
        json_data = json.load(file)
    return json_data


# file_name = "./docs/sales_sample.json"
#
# data = load_json_file(file_name)
#
# """ print doc_id from the json data"""
#
# print(data["doc_id"])
# print(data["content"])