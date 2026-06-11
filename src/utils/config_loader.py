import yaml


def load_params(path="config/params.yaml"):

    with open(path, "r") as file:
        params = yaml.safe_load(file)

    return params