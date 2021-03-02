# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
import spack.config
import spack.error
import spack.util.path

_extension_regexp = re.compile(r'spack-(\w[-\w]*)$')


# TODO: For consistency we should use spack.cmd.python_name(), but
#       currently this would create a circular relationship between
#       spack.cmd and spack.extensions.
def _python_name(cmd_name):
    return cmd_name.replace('-', '_')


def extension_name(path):
    """Returns the name of the extension in the path passed as argument.

    Args:
        path (str): path where the extension resides

    Returns:
        The extension name.

    Raises:
         ExtensionNamingError: if path does not match the expected format
             for a Spack command extension.
    """
    regexp_match = re.search(_extension_regexp,
                             os.path.basename(os.path.normpath(path)))
    if not regexp_match:
        raise ExtensionNamingError(path)
    return regexp_match.group(1)


def load_command_extension(command, path):
    """Loads a command extension from the path passed as argument.

    Args:
        command (str): name of the command (contains ``-``, not ``_``).
        path (str): base path of the command extension

    Returns:
        A valid module if found and loadable; None if not found. Module
    loading exceptions are passed through.
    """
    extension = _python_name(extension_name(path))

    # Compute the name of the module we search, exit early if already imported
    cmd_package = '{0}.{1}.cmd'.format(__name__, extension)
    python_name = _python_name(command)
    module_name = '{0}.{1}'.format(cmd_package, python_name)
    if module_name in sys.modules:
        return sys.modules[module_name]

    # Compute the absolute path of the file to be loaded, along with the
    # name of the python module where it will be stored
    cmd_path = os.path.join(path, extension, 'cmd', python_name + '.py')

    # Short circuit if the command source file does not exist
    if not os.path.exists(cmd_path):
        return None

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

    # TODO: Upon removal of support for Python 2.6 substitute the call
    # TODO: below with importlib.import_module(module_name)
    module = llnl.util.lang.load_module_from_file(module_name, cmd_path)
    sys.modules[module_name] = module

    return module


def get_extension_paths():
    """Return the list of canonicalized extension paths from config:extensions.

    """
    extension_paths = spack.config.get('config:extensions') or []
    paths = [spack.util.path.canonicalize_path(p) for p in extension_paths]
    return paths


def get_command_paths():
    """Return the list of paths where to search for command files."""
    command_paths = []
    extension_paths = get_extension_paths()

    for path in extension_paths:
        extension = _python_name(extension_name(path))
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
    extensions = get_extension_paths()
    for folder in extensions:
        module = load_command_extension(cmd_name, folder)
        if module:
            return module
    else:
        raise CommandNotFoundError(cmd_name)


def get_template_dirs():
    """Returns the list of directories where to search for templates
    in extensions.
    """
    extension_dirs = get_extension_paths()
    extensions = [os.path.join(x, 'templates') for x in extension_dirs]
    return extensions


class CommandNotFoundError(spack.error.SpackError):
    """Exception class thrown when a requested command is not recognized as
    such.
    """
    def __init__(self, cmd_name):
        super(CommandNotFoundError, self).__init__(
            '{0} is not a recognized Spack command or extension command;'
            ' check with `spack commands`.'.format(cmd_name))


class ExtensionNamingError(spack.error.SpackError):
    """Exception class thrown when a configured extension does not follow
    the expected naming convention.
    """
    def __init__(self, path):
        super(ExtensionNamingError, self).__init__(
            '{0} does not match the format for a Spack extension path.'
            .format(path))
