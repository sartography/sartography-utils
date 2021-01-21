#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path
from string import Template
from os.path import expandvars
import sys
import re


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    via https://code.activestate.com/recipes/577058/, MIT licence
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def calculate_ports(port_range_start, templatelines, skipcheck=False):
    if port_range_start < 1024 and not skipcheck:
        print("use of reserved ports is forbidden in dev environments")
        if not query_yes_no("Do you want to continue?"):
            exit(1)
        else:
            return calculate_ports(port_range_start, templatelines, skipcheck=True)
    else:
        file_vars = []
        portdict = {}
        i = 0
        for line in templatelines:
            result = re.findall('\${.*?}', line)
            for r in result:
                if r not in file_vars:
                    file_vars.append(r)
        for file_var in file_vars:
            if "_port" in file_var.lower() or file_var.lower() == "port":
                if (":" or ",") not in file_var:
                    portname = re.sub('[{}$]', '', file_var)
                    portdict[portname] = port_range_start + i
                    i = i + 1
        return portdict


def script_generator(outfile, scriptlines):
    with open(outfile, "w+") as file:
        file.write("#!/bin/bash\n")
        for line in scriptlines:
            file.write("%s\n" % line)
    exit()


def stdio_script(scriptlines):
    print("#!/bin/bash")
    for line in scriptlines:
        print(line)
    exit()


def docker_compose_generator(inlines, outfile, data):
    outlines = []
    for line in inlines:
        a_line = Template(line)
        result = a_line.safe_substitute(data)
        outlines.append(result)
    with open(outfile, "w+") as file:
        file.writelines(outlines)
    exit()


def template_reader(templatefile):
    with open(templatefile, "r+") as file:
        inlines = file.readlines()
    return inlines


def strings_to_classes(a_string):
    if a_string != "" and a_string is not None:
        return eval(a_string)
    else:
        return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build docker compose based on templates. '
                                                 'If no output file or format is specified, this program will print the'
                                                 ' contents for a script to standard out ')
    parser.add_argument("-F", "--folder", help="A folder with args.csv, defaults.csv, and a docker-compose.yml")
    parser.add_argument("-af", "--argfile", help="specify argfile", default="./args.csv")
    parser.add_argument("-df", "--defaults-file", help="specify defaults file", default="./defaults.csv")
    parser.add_argument("-s", "--script",
                        help="Specifies an output script filename.")
    parser.add_argument("-c", "--docker-compose",
                        help="Specifies an output docker compose filename")
    parser.add_argument("-D", "--defaults", help="use sane defaults everywhere, default true", action="store_true")
    parser.add_argument("-t", "--template", help="A template for docker compose", default="./docker-compose.yml")
    args = parser.parse_known_args()
    if args[0].folder:
        arg_file = "%s/args.csv" % args[0].folder
        defaults_file = "%s/defaults.csv" % args[0].folder
        template_file = "%s/docker-compose.yml" % args[0].folder
    else:
        arg_file = args[0].argfile
        defaults_file = args[0].defaults_file
        template_file = args[0].template
    with open(arg_file) as f:
        records = csv.DictReader(f)
        for row in records:
            if "type" in row.keys():
                row["type"] = strings_to_classes(row["type"])
            else:
                row.pop("type")
            if "choices" in row.keys():
                row["choices"] = strings_to_classes(row["choices"])
            else:
                row.pop("choices")
            parser.add_argument(row.pop("short"),
                                row.pop("long"),
                                **{k: v for k, v in row.items() if (v != "")})
    parser.usage = parser.format_help()
    args = parser.parse_args()
    settings = {}
    DEFAULTS = {}
    script_lines = []
    with open(defaults_file) as f:
        rows = csv.reader(f)
        for row in rows:
            DEFAULTS[row[0].upper()] = row[1]
    default_keys = {
        "script",
        "docker_compose",
        "argfile",
        "defaults_file",
        "defaults",
        "template",
        "folder",
    }
    use_defaults = False
    if len(vars(args)) > 1:
        argset = set()
        for k, v in vars(args).items():
            if v is not None and v != "":
                argset.add(k)
        if argset < default_keys:
            use_defaults = True
    if args.defaults or use_defaults:
        template_lines = template_reader(template_file)
        ports = calculate_ports(int(DEFAULTS["PORT_RANGE_START"]), template_lines)
        if not args.docker_compose:
		print("echo Defaults selected or no values given")
        script_lines.append("echo using the following ports:")
        settings.update(DEFAULTS)
    else:
        for k, v in vars(args).items():
            settings[k.upper()] = v
        template_lines = template_reader(templatefile=template_file)
        if args.port_range:
            script_lines.append("echo Using the following ports:")
            ports = calculate_ports(args.port_range, templatelines=template_lines)
        else:
            ports = calculate_ports(DEFAULTS["PORT_RANGE_START"], templatelines=template_lines)
        if "PORT_RANGE_START" in settings.keys():
            settings.pop("PORT_RANGE_START")
        for k, v in settings.items():
            if settings[k] is None:
                if k in DEFAULTS.keys():
                    settings[k] = DEFAULTS[k]
                else:
                    settings[k] = ""
        if args.path_base:
            settings["PATH_BASE"] = args.path_base
        else:
            if args.deployment_identifier:
                settings["PATH_BASE"] = "%s%s/" % (DEFAULTS["PATH_BASE"], args.deployment_identifier)
            else:
                settings["PATH_BASE"] = DEFAULTS["PATH_BASE"]
            settings["PATH_BASE"] = expandvars(settings["PATH_BASE"])
            Path(settings["PATH_BASE"]).mkdir(parents=True, exist_ok=True)
    for service, port in ports.items():
        script_lines.append("echo %s: %s" % (service, port))
        script_lines.append("export %s=%s" % (service, port))
    for name, value in settings.items():
        if value != "" and value is not None:
            if name.lower() not in default_keys:
                script_lines.append("echo %s: %s" % (name, value))
                script_lines.append("export %s=%s" % (name, value))
        elif name.lower() not in default_keys:
            script_lines.append("export %s=%s" % (name, ""))
    settings.update(ports)
    if args.script:
        if args.script == template_file:
            print("output would overwrite template, exiting")
            exit(1)
        else:
            script_generator(outfile=args.script, scriptlines=script_lines)
    elif args.docker_compose:
        if args.docker_compose == template_file:
            print("output would overwrite template, exiting")
            exit(1)
        else:
            docker_compose_generator(inlines=template_lines, outfile=args.docker_compose, data=settings)
    else:
        stdio_script(script_lines)
        exit()
