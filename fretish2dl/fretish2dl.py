import argparse
import json

from paramiko.kex_gss import c_MSG_KEXGSS_HOSTKEY

CHOOSE_ACTION_NAME = "RLChooseAction"
NO_ACTION_NAME = "RLNoChange"

SYSTEM_THRESHOLD_NAME = "SystemThreshold"
HCTHRESHOLD = "HCThreshold"

SYSTEM_RESILIENCE_NAME = "SystemResilience"
HCRESILIENCE1 = "HCResiliance1"
HCRESILIENCE2 = "HCResiliance2"

SYSTEM_RECOVERY_NAME = "SystemRecovery"
HCRECOVERY1 = "HCRecovery1"
HCRECOVERY2 = "HCRecovery2"


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

    if "system_resilience_condition" in extract_dict and extract_dict["system_resilience_condition"] is not None:
        threshold = extract_dict["system_resilience_condition"]
        dl_spec["system_property"] = threshold + " -> [" + system_name + "] " + threshold
        print("system property ::= " + dl_spec["system_property"])
    elif "system_threshold_postcondition" in extract_dict and extract_dict["system_threshold_postcondition"] is not None:
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

    clock_time = extract_dict["clock_time"]
    sample_time = extract_dict["sample_time"]

    dl_spec["alpha_continuous"] = clock_variable + "' = 1 & " +  clock_time + " <= " + sample_time

    print("alpha continuous ::= " + dl_spec["alpha_continuous"])

    #TODO this needs to deal with multiple HC elements, or multiple sources I suppose. They should all go into the list

    hc_concat = ""
    dl_spec["HC"] = []

    if "hc1_response" in extract_dict and extract_dict["hc1_response"] is not None and extract_dict["hc2_response"] is not None:
        dl_spec["HC"].append(extract_dict["hc1_response"])
        dl_spec["HC"].append(extract_dict["hc2_response"])

        print("HC :== " + dl_spec["HC"][0] + " && " + dl_spec["HC"][1])

    else:
        hc_trigger = extract_dict["hc_condition"]
        hc_threshold = extract_dict["hc_threshold"]
        hc_var =  extract_dict["hc_var"]
        hc_reaction =  extract_dict["hc_reaction_threshold"]

        dl_spec["HC"] = ["(" + hc_threshold + ")" + " -> " + hc_var + " + " + hc_reaction]

        print("HC :== " + dl_spec["HC"][0])



    return dl_spec





def parse_fret_project(project):
    """Parse the json FRET Project"""
    # TODO Check type of project is list
    print("+++ Parsing FRETISH Project +++")
    extract = {}

    # Call the relevant parsing method
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
        elif name == SYSTEM_RESILIENCE_NAME:
            parse_system_resilience(req, extract)
        elif name == HCRESILIENCE1:
            parse_hc_resilience1(req, extract)
        elif name == HCRESILIENCE2:
            parse_hc_resilience2(req, extract)
        elif name == SYSTEM_RECOVERY_NAME:
            parse_system_recovery(req, extract)
        elif name == HCRECOVERY1:
            parse_hc_recovery1(req, extract)
        elif name == HCRECOVERY2:
            parse_hc_recovery2(req, extract)
        else:
            print("+++ Unknown Requirement Name +++")
            print(req["reqid"])
            print("+++ +++")
            print("")


    print("+++ FRETISH Parsing Complete +++")
    return extract


def get_function_varlist(function_call):
    """Gets the variable list from an atomic function call"""
    print("+++ Getting Function's Variable List +++")

    # Find the brackets
    open_bracket = function_call.index("(")
    close_bracket = function_call.index(")")

    # Strip out the function call and brackets, and strip the outside whitespace
    stripped_function_call = function_call[open_bracket+1: close_bracket].strip()

    # Make it into a list, stripping the whitespace around the comma
    var_list = stripped_function_call.split(" , ")

    return var_list


def parse_choose_action(req, extract):
    """"parses the relevant information from an RLChooseAction requirement."""
    print("+++ Parsing Choose Action +++")
    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    extract["choose_action_condition"] = condition[3:-3]
    #extract["choose_action_postcondition"] = post_condition[1: -1]

    var_list = get_function_varlist(post_condition[1: -1])

    choose_action_variables = ""
    for var in var_list:
        choose_action_variables += "{0} := *; ".format(var)

    extract["choose_action_postcondition"] = choose_action_variables

    return

def parse_no_action(req, extract):
    """parses the relevant information from an RLNoChange requirement."""
    print("+++ Parsing No Action +++")
    condition = req["semantics"]["pre_condition"]
    variables = req["semantics"]["variables"]
    post_condition = req["semantics"]["post_condition"]

    extract["no_action_condition"] = condition[3:-3]
    extract["clock_time"], extract["sample_time"] = extract["no_action_condition"].split(" < ")
    extract["no_action_postcondition"] = post_condition[1: -1]


    print(extract["no_action_condition"])
    print( extract["no_action_postcondition"])

    var_list = get_function_varlist(post_condition[1: -1])

    no_action_variables = ""
    for var in var_list:
        no_action_variables += "{0} := {0}_old; ".format(var)

    extract["no_action_postcondition"] = no_action_variables

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

    print(extract["system_threshold_condition"] )
    print(extract["system_threshold_postcondition"])

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

def parse_system_resilience(req, extract):
    print("+++ Parsing System Resilience +++")

    condition = req["semantics"]["pre_condition"]
    post_condition = req["semantics"]["post_condition"]

    extract["system_resilience_condition"] = condition[1:-1]
    extract["system_resilience_postcondition"] = post_condition[1: -1]
    #TODO Check that the above are the same, or the contract template hasn't been obeyed

    print(extract["system_resilience_condition"])
    print(extract["system_resilience_postcondition"])

def parse_hc_resilience1(req, extract):
    print("+++ Parsing HC Resilience 1")
    condition = req["semantics"]["pre_condition"]
    post_condition = req["semantics"]["post_condition"]

    # ([threshold]) => ([var] + [worst case reaction] [thresholdComparison])

    extract["hc_r_condition"] = condition[3:-3]

    threshold, the_rest = post_condition.split(" => ")
    extract["hc_r_threshold"] = threshold[3:-2]
    var, the_rest = the_rest.split(" + ")
    extract["hc_r_var"] = var[2:]
    extract["hc_r_reaction_threshold"] = the_rest

    extract["hc1_response"] = post_condition.replace("=>", "->")

    return


def parse_hc_resilience2(req, extract):
    print("+++ Parsing HC Resilience 2")

    post_condition = req["semantics"]["post_condition"]

    extract["hc2_response"] = post_condition.replace("=>", "->")

    return


def parse_system_recovery(req, extract):
    pass


def parse_hc_recovery1(req, extract):
    pass


def parse_hc_recovery2(req, extract):
    pass

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
