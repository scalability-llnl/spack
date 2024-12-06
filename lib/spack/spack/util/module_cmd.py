# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module contains routines related to the module command for accessing and
parsing environment modules.
"""
import os
import re
import subprocess
from typing import MutableMapping, Optional

import llnl.util.tty as tty

# This list is not exhaustive. Currently we only use load and unload
# If we need another option that changes the environment, add it here.
module_change_commands = ["load", "swap", "unload", "purge", "use", "unuse"]

# This awk script is a posix alternative to `env -0`
awk_cmd = r"""awk 'BEGIN{for(name in ENVIRON)""" r"""printf("%s=%s%c", name, ENVIRON[name], 0)}'"""


def module(
    *args,
    module_template: Optional[str] = None,
    environb: Optional[MutableMapping[bytes, bytes]] = None,
):
    module_cmd = module_template or ("module " + " ".join(args))
    environb = environb or os.environb

    if args[0] in module_change_commands:
        # Suppress module output
        module_cmd += r" >/dev/null 2>&1; " + awk_cmd
        module_p = subprocess.Popen(
            module_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable="/bin/bash",
            env=environb,
        )

        new_environb = {}
        output = module_p.communicate()[0]

        # Loop over each environment variable key=value byte string
        for entry in output.strip(b"\0").split(b"\0"):
            # Split variable name and value
            parts = entry.split(b"=", 1)
            if len(parts) != 2:
                continue
            new_environb[parts[0]] = parts[1]

        # Update os.environ with new dict
        environb.clear()
        environb.update(new_environb)  # novermin

    else:
        # Simply execute commands that don't change state and return output
        module_p = subprocess.Popen(
            module_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable="/bin/bash",
        )
        # Decode and str to return a string object in both python 2 and 3
        return str(module_p.communicate()[0].decode())


def load_module(mod):
    """Takes a module name and removes modules until it is possible to
    load that module. It then loads the provided module. Depends on the
    modulecmd implementation of modules used in cray and lmod.
    """
    tty.debug("module_cmd.load_module: {0}".format(mod))
    # Read the module and remove any conflicting modules
    # We do this without checking that they are already installed
    # for ease of programming because unloading a module that is not
    # loaded does nothing.
    text = module("show", mod).split()
    for i, word in enumerate(text):
        if word == "conflict":
            module("unload", text[i + 1])

    # Load the module now that there are no conflicts
    # Some module systems use stdout and some use stderr
    module("load", mod)


def get_path_args_from_module_line(line):
    if "(" in line and ")" in line:
        # Determine which lua quote symbol is being used for the argument
        comma_index = line.index(",")
        cline = line[comma_index:]
        try:
            quote_index = min(cline.find(q) for q in ['"', "'"] if q in cline)
            lua_quote = cline[quote_index]
        except ValueError:
            # Change error text to describe what is going on.
            raise ValueError("No lua quote symbol found in lmod module line.")
        words_and_symbols = line.split(lua_quote)
        path_arg = words_and_symbols[-2]
    else:
        # The path arg is the 3rd "word" of the line in a Tcl module
        # OPERATION VAR_NAME PATH_ARG
        words = line.split()
        if len(words) > 2:
            path_arg = words[2]
        else:
            return []

    paths = path_arg.split(":")
    return paths


def path_from_modules(modules):
    """Inspect a list of Tcl modules for entries that indicate the absolute
    path at which the library supported by said module can be found.

    Args:
        modules (list): module files to be loaded to get an external package

    Returns:
        Guess of the prefix path where the package
    """
    assert isinstance(modules, list), 'the "modules" argument must be a list'

    best_choice = None
    for module_name in modules:
        # Read the current module and return a candidate path
        text = module("show", module_name).split("\n")
        candidate_path = get_path_from_module_contents(text, module_name)

        if candidate_path and not os.path.exists(candidate_path):
            msg = "Extracted path from module does not exist " "[module={0}, path={1}]"
            tty.warn(msg.format(module_name, candidate_path))

        # If anything is found, then it's the best choice. This means
        # that we give preference to the last module to be loaded
        # for packages requiring to load multiple modules in sequence
        best_choice = candidate_path or best_choice
    return best_choice


def get_path_from_module_contents(text, module_name):
    tty.debug("Module name: " + module_name)
    pkg_var_prefix = module_name.replace("-", "_").upper()
    components = pkg_var_prefix.split("/")
    # For modules with multiple components like foo/1.0.1, retrieve the package
    # name "foo" from the module name
    if len(components) > 1:
        pkg_var_prefix = components[-2]
    tty.debug("Package directory variable prefix: " + pkg_var_prefix)

    path_occurrences = {}

    def strip_path(path, endings):
        for ending in endings:
            if path.endswith(ending):
                return path[: -len(ending)]
            if path.endswith(ending + "/"):
                return path[: -(len(ending) + 1)]
        return path

    def match_pattern_and_strip(line, pattern, strip=[]):
        if re.search(pattern, line):
            paths = get_path_args_from_module_line(line)
            for path in paths:
                path = strip_path(path, strip)
                path_occurrences[path] = path_occurrences.get(path, 0) + 1

    def match_flag_and_strip(line, flag, strip=[]):
        flag_idx = line.find(flag)
        if flag_idx >= 0:
            # Search for the first occurence of any separator marking the end of
            # the path.
            separators = (" ", '"', "'")
            occurrences = [line.find(s, flag_idx) for s in separators]
            indices = [idx for idx in occurrences if idx >= 0]
            if indices:
                path = line[flag_idx + len(flag) : min(indices)]
            else:
                path = line[flag_idx + len(flag) :]
            path = strip_path(path, strip)
            path_occurrences[path] = path_occurrences.get(path, 0) + 1

    lib_endings = ["/lib64", "/lib"]
    bin_endings = ["/bin"]
    man_endings = ["/share/man", "/man"]

    for line in text:
        # Check entries of LD_LIBRARY_PATH and CRAY_LD_LIBRARY_PATH
        pattern = r"\W(CRAY_)?LD_LIBRARY_PATH"
        match_pattern_and_strip(line, pattern, lib_endings)

        # Check {name}_DIR entries
        pattern = r"\W{0}_DIR".format(pkg_var_prefix)
        match_pattern_and_strip(line, pattern)

        # Check {name}_ROOT entries
        pattern = r"\W{0}_ROOT".format(pkg_var_prefix)
        match_pattern_and_strip(line, pattern)

        # Check entries that update the PATH variable
        pattern = r"\WPATH"
        match_pattern_and_strip(line, pattern, bin_endings)

        # Check entries that update the MANPATH variable
        pattern = r"MANPATH"
        match_pattern_and_strip(line, pattern, man_endings)

        # Check entries that add a `-rpath` flag to a variable
        match_flag_and_strip(line, "-rpath", lib_endings)

        # Check entries that add a `-L` flag to a variable
        match_flag_and_strip(line, "-L", lib_endings)

    # Whichever path appeared most in the module, we assume is the correct path
    if len(path_occurrences) > 0:
        return max(path_occurrences.items(), key=lambda x: x[1])[0]

    # Unable to find path in module
    return None
