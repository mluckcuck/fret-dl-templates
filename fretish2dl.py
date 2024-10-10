import argparse
import json

CHOOSE_ACTION_NAME = "RLChooseAction"
NO_ACTION_NAME = "RLNoChange"
SYSTEM_THRESHOLD_NAME = "SystemThreshold"
HCTHRESHOLD = "HCThreshold"

def fretish2dl():
    """Main Method for the translator.
    This calls the right translation code,
    based on the format argument"""
    print(args.filename, args.format)
    dl_spec = {"system_property": None, "alpha_discrete": None, "alpha_continuous": None, "HC": None}

    with open(args.filename, mode="r") as fret_file:
        fretish = json.load(fret_file)
        parse_fret_project(fretish)


def parse_fret_project(project):
    """Parse the json FRET Project"""
    # TODO Check type of project is list

    extract = {}
    # if args.format is None:
    for req in project:
        name = req["reqid"]
        if  name == CHOOSE_ACTION_NAME:
            parse_choose_action(req, extract)
        elif name == NO_ACTION_NAME:
            parse_no_action(req, extract)
        elif name == SYSTEM_THRESHOLD_NAME:
            parse_system_threshold(req, extract)
        elif name == HCTHRESHOLD:
            parse_hc_threshold(req, extract)


def parse_choose_action(req, extract):
    print("+++ Parsing Choose Action +++")
    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    extract["choose_action_condition"] = condition[3:-3]
    extract["choose_action_postcondition"] = post_condition[1: -1]

    return

def parse_no_action(req, extract):
    print("+++ Parsing No Action +++")
    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    extract["no_action_condition"] = condition[3:-3]
    extract["no_action_postcondition"] = post_condition[1: -1]

    return

def parse_system_threshold(req, extract):
    print ("+++ Parsing System Threshold +++")

    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    extract["system_threshold_condition"] = condition[3:-3]
    extract["system_threshold_postcondition"] = post_condition[1: -1]

    return

def parse_hc_threshold(req, extract):
    pass

if __name__ == "__main__":

    # PARSE THE ARGS
    parser = argparse.ArgumentParser(
        prog='FRETISH 2 dL',
        description='Converts a set of FRETISH requirements from a json file exported from FRET into dL.',
        epilog='')
    parser.add_argument('filename')  # positional argument
    parser.add_argument('-f', '--format')  # option that takes a value
    args = parser.parse_args()

    fretish2dl()
