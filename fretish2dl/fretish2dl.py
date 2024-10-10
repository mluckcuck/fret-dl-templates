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

    dl_spec = {"system_property": None, "alpha_discrete": None, "alpha_continuous": None, "HC": None}

    with open(args.filename, mode="r") as fret_file:
        fretish = json.load(fret_file)
        extract = parse_fret_project(fretish)

    # TODO add system name to the args
    output = build_output(extract, dl_spec, args.project_name)


    print("\n+++ Writing to File +++")
    output_file_name = "dl_specification_"+args.project_name+".json"
    print("+++ Filename = " + output_file_name)

    with open(output_file_name, mode="w") as output_file:
        json.dump(output, output_file)

    print("\n+++ Translation Complete +++")

def build_output(extract_dict, dl_spec, system_name):
    """Builds the text of the output from the variables in the extract_dict."""

    print("\n+++ Output Preview +++\n")
    #pre → [System]post ::= T ≤ T MAX → [T mpCtrl] T ≤ T MAX
    #α discr ::= {?c S ≥ t S ; c S := 0; c := ∗; ?(HC); + +?c S < t S ; }
    #α cont ::= {c S ′ = 1 & c S ≤ t S })
    #HC ::= T ≤ T MAX → T + (h MAX − c) · t S ≤ T MAX

    threshold = extract_dict["system_threshold_postcondition"]
    dl_spec["system_property"] = threshold + " -> [" + system_name + "] " + threshold

    print("system property ::= " + dl_spec["system_property"])

    clock_var1, the_rest = extract_dict["no_action_condition"].split(" < ")
    clock_var2, the_rest = extract_dict["choose_action_condition"].split(" >= ")
    # clock_var3, the_rest = extract_dict["hc_condition"].split(" >= ")
    # TODO make this a) more robust by actually extracting hc_condition and b) putting into a pre-process method
    assert (clock_var1 == clock_var2)
    clock_variable = clock_var1

    choose_trigger = extract_dict["choose_action_condition"]
    choose_action = extract_dict["choose_action_postcondition"]
    no_action_trigger = extract_dict["no_action_condition"]
    dl_spec["alpha_discrete"] = "{? " + choose_trigger + "; " + clock_variable + " := 0 ; " + choose_action + "?(HC); " + "++? " +no_action_trigger + (";}"
                                                                                                                                               "")
    print("alpha discrete ::= " + dl_spec["alpha_discrete"])

    dl_spec["alpha_continuous"] = clock_variable + "' = 1 & " +  no_action_trigger

    print("alpha continuous ::= " + dl_spec["alpha_continuous"])

    #TODO this needs to deal with multiple HC elements, or multiple sources I suppose. They should all go into the list

    hc_trigger = extract_dict["hc_condition"]
    hc_var =  extract_dict["hc_var"]
    hc_reaction =  extract_dict["hc_reaction_threshold"]

    dl_spec["HC"] = [ hc_trigger + " -> " + hc_var + " + " + hc_reaction  ]

    print("HC :== " + dl_spec["HC"][0])

    return dl_spec



def parse_fret_project(project):
    """Parse the json FRET Project"""
    # TODO Check type of project is list
    print("+++ Parsing FRETISH Project +++")
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

    print("+++ FRETISH Parsing Complete +++")
    return extract


def parse_choose_action(req, extract):
    """"parses the relevant information from an RLChooseAction requirement."""
    print("+++ Parsing Choose Action +++")
    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    extract["choose_action_condition"] = condition[3:-3]
    extract["choose_action_postcondition"] = post_condition[1: -1]


    return

def parse_no_action(req, extract):
    """parses the relevant information from an RLNoChange requirement."""
    print("+++ Parsing No Action +++")
    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    extract["no_action_condition"] = condition[3:-3]
    extract["no_action_postcondition"] = post_condition[1: -1]

    return

def parse_system_threshold(req, extract):
    """parse the relevant information from a SystemThreshold requirement"""
    print ("+++ Parsing System Threshold +++")

    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    print(condition[1:-1])
    print(post_condition[1: -1])
    # TODO Check that these are the same (they're not right now because I wrote the contracts wrong)
   # TODO this check needs to happen after parsing, because there are some checks that need to be done between contracts

    extract["system_threshold_condition"] = condition[1:-1]
    extract["system_threshold_postcondition"] = post_condition[1: -1]

    return

def parse_hc_threshold(req, extract):
    """parses the relevant information from an HCThreshold requirement."""
    print("+++ Parsing HC Threshold")
    condition = req["semantics"]["pre_condition"]
    post_condition = req["semantics"]["post_condition"]

    # ([threshold]) => ([var] + [worst case reaction] [thresholdComparison])

    extract["hc_condition"] = condition[3:-3]

    threshold, the_rest = post_condition.split(" => ")
    extract["hc_threshold"] = threshold[3:-2]
    var, the_rest = the_rest.split(" + ")
    extract["hc_var"] = var[2:]
    extract["hc_reaction_threshold"] = the_rest

    return



if __name__ == "__main__":

    # PARSE THE ARGS
    parser = argparse.ArgumentParser(
        prog='FRETISH 2 dL',
        description='Converts a set of FRETISH requirements from a json file exported from FRET into dL.',
        epilog='')
    parser.add_argument('filename')  # positional argument
    parser.add_argument('project_name')
    parser.add_argument('-f', '--format')  # option that takes a value
    args = parser.parse_args()

    fretish2dl()
