# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Service functions and classes to implement the hooks
for Spack's command extensions.
"""
import os
import re
import sys
import types

import llnl.util.lang
import llnl.util.tty as tty
import spack.config
from spack.util.path import canonicalize_path

extension_regexp = re.compile(r'spack-([\w]*)')


def extension_name(path):
    """Returns the name of the extension in the path passed as argument.

    Args:
        path (str): path where the extension resides

    Returns:
        The extension name or None if path doesn't match the format
        for Spack's extension.
    """
    regexp_match = re.search(extension_regexp, os.path.basename(path))
    if not regexp_match:
        msg = "[FOLDER NAMING]"
        msg += " {0} doesn't match the format for Spack's extensions"
        tty.warn(msg.format(path))
        return None
    return regexp_match.group(1)


def load_command_extension(command, path):
    """Loads a command extension from the path passed as argument.

    Args:
        command (str): name of the command
        path (str): base path of the command extension

    Returns:
        A valid module object if the command is found or None
    """
    extension = extension_name(path)
    if not extension:
        return None

    # Compute the name of the module we search, exit early if already imported
    cmd_package = '{0}.{1}.cmd'.format(__name__, extension)
    python_name = command.replace('-', '_')
    module_name = '{0}.{1}'.format(cmd_package, python_name)
    if module_name in sys.modules:
        return sys.modules[module_name]

    def ensure_package_creation(name):
        package_name = '{0}.{1}'.format(__name__, name)
        if package_name in sys.modules:
            return

        parts = [path] + name.split('.') + ['__init__.py']
        init_file = os.path.join(*parts)
        if os.path.exists(init_file):
            m = llnl.util.lang.load_module_from_file(package_name, init_file)
        else:
            m = types.ModuleType(package_name)

        # Setting __path__ to give spack extensions the
        # ability to import from their own tree, see:
        #
        # https://docs.python.org/3/reference/import.html#package-path-rules
        #
        m.__path__ = [os.path.dirname(init_file)]
        sys.modules[package_name] = m

    # Create a searchable package for both the root folder of the extension
    # and the subfolder containing the commands
    ensure_package_creation(extension)
    ensure_package_creation(extension + '.cmd')

    # Compute the absolute path of the file to be loaded, along with the
    # name of the python module where it will be stored
    cmd_path = os.path.join(path, extension, 'cmd', command + '.py')

    try:
        # TODO: Upon removal of support for Python 2.6 substitute the call
        # TODO: below with importlib.import_module(module_name)
        module = llnl.util.lang.load_module_from_file(module_name, cmd_path)
        sys.modules[module_name] = module
    except (ImportError, IOError):
        module = None

    return module


def get_command_paths():
    """Return the list of paths where to search for command files."""
    command_paths = []
    extension_paths = spack.config.get('config:extensions') or []

    for path in extension_paths:
        extension = extension_name(path)
        if extension:
            command_paths.append(os.path.join(path, extension, 'cmd'))

    return command_paths


def path_for_extension(target_name, *paths):
    """Return the test root dir for a given extension.

    Args:
        target_name (str): name of the extension to test
        *paths: paths where the extensions reside

    Returns:
        Root directory where tests should reside or None
    """
    for path in paths:
        name = extension_name(path)
        if name == target_name:
            return path
    else:
        raise IOError('extension "{0}" not found'.format(target_name))


def get_module(cmd_name):
    """Imports the extension module for a particular command name
    and returns it.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
    """
    # If built-in failed the import search the extension
    # directories in order
    extensions = spack.config.get('config:extensions') or []
    for folder in [canonicalize_path(e) for e in extensions]:
        module = load_command_extension(cmd_name, folder)
        if module:
            return module
    else:
        return None


def get_template_dirs():
    """Returns the list of directories where to search for templates
    in extensions.
    """
    extension_dirs = spack.config.get('config:extensions') or []
    extensions = [os.path.join(x, 'templates') for x in extension_dirs]
    return extensions
