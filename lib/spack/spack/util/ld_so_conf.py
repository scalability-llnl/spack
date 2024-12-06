# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re
import sys

from llnl.util.lang import dedupe

import spack.util.elf as elf_utils


def parse_ld_so_conf(conf_file="/etc/ld.so.conf"):
    """Parse glibc style ld.so.conf file, which specifies default search paths for the
    dynamic linker. This can in principle also be used for musl libc.

    Arguments:
        conf_file (str or bytes): Path to config file

    Returns:
        list: List of absolute search paths
    """
    # Parse in binary mode since it's faster
    is_bytes = isinstance(conf_file, bytes)
    if not is_bytes:
        conf_file = conf_file.encode("utf-8")

    # For globbing in Python2 we need to chdir.
    cwd = os.getcwd()
    try:
        paths = _process_ld_so_conf_queue([conf_file])
    finally:
        os.chdir(cwd)

    return list(paths) if is_bytes else [p.decode("utf-8") for p in paths]


def _process_ld_so_conf_queue(queue):
    include_regex = re.compile(b"include\\s")
    paths = []
    while queue:
        p = queue.pop(0)

        try:
            with open(p, "rb") as f:
                lines = f.readlines()
        except (IOError, OSError):
            continue

        for line in lines:
            # Strip comments
            comment = line.find(b"#")
            if comment != -1:
                line = line[:comment]

            # Skip empty lines
            line = line.strip()
            if not line:
                continue

            is_include = include_regex.match(line) is not None

            # If not an include, it's a literal path (no globbing here).
            if not is_include:
                # We only allow absolute search paths.
                if os.path.isabs(line):
                    paths.append(line)
                continue

            # Finally handle includes.
            include_path = line[8:].strip()
            if not include_path:
                continue

            cwd = os.path.dirname(p)
            os.chdir(cwd)
            queue.extend(os.path.join(cwd, p) for p in glob.glob(include_path))

    return dedupe(paths)


def get_conf_file_from_dynamic_linker(dynamic_linker_name):
    # We basically assume everything is glibc, except musl.
    if "ld-musl-" not in dynamic_linker_name:
        return "ld.so.conf"

    # Musl has a dynamic loader of the form ld-musl-<arch>.so.1
    # and a corresponding config file ld-musl-<arch>.path
    idx = dynamic_linker_name.find(".")
    if idx != -1:
        return dynamic_linker_name[:idx] + ".path"


def host_dynamic_linker_search_paths():
    """Retrieve the current host runtime search paths for shared libraries;
    for GNU and musl Linux we try to retrieve the dynamic linker from the
    current Python interpreter and then find the corresponding config file
    (e.g. ld.so.conf or ld-musl-<arch>.path). Similar can be done for
    BSD and others, but this is not implemented yet. The default paths
    are always returned. We don't check if the listed directories exist."""
    default_paths = ["/usr/lib", "/usr/lib64", "/lib", "/lib64"]

    # Currently only for Linux (gnu/musl)
    if not sys.platform.startswith("linux"):
        return default_paths

    # If everything fails, try this standard glibc path.
    conf_file = "/etc/ld.so.conf"

    # Try to improve on the default conf path by retrieving the location of the
    # dynamic linker from our current Python interpreter, and figure out the
    # config file location from there.
    try:
        with open(sys.executable, "rb") as f:
            elf = elf_utils.parse_elf(f, dynamic_section=False, interpreter=True)

        # If we have a dynamic linker, try to retrieve the config file relative
        # to its prefix.
        if elf.has_pt_interp:
            dynamic_linker = elf.pt_interp_str.decode("utf-8")
            dynamic_linker_name = os.path.basename(dynamic_linker)
            conf_name = get_conf_file_from_dynamic_linker(dynamic_linker_name)

            # Typically it is /lib/ld.so, but on Gentoo Prefix it is something
            # like <long glibc prefix>/lib/ld.so. And on Debian /lib64 is actually
            # a symlink to /usr/lib64. So, best effort attempt is to just strip
            # two path components and join with etc/ld.so.conf.
            possible_prefix = os.path.dirname(os.path.dirname(dynamic_linker))
            possible_conf = os.path.join(possible_prefix, "etc", conf_name)

            if os.path.exists(possible_conf):
                conf_file = possible_conf
    except (IOError, OSError, elf_utils.ElfParsingError):
        pass

    # Note: ld_so_conf doesn't error if the file does not exist.
    return list(dedupe(parse_ld_so_conf(conf_file) + default_paths))
