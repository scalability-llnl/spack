# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import contextlib
import os
import sys

import spack.cmd
import spack.config
import spack.extensions
import spack.main


class Extension:
    """Helper class to simplify the creation of simple command extension
    directory structures with a conventional format for testing.
    """
    def __init__(self, name, root):
        """Create a command extension.

        Args:
            name (str): The name of the command extension.
            root (path object): The temporary root for the command extension
                (e.g. from tmpdir.mkdir()).
        """
        self.name = name
        self.pname = spack.cmd.python_name(name)
        self.root = root
        self.main = self.root.ensure(self.pname, dir=True)
        self.cmd = self.main.ensure('cmd', dir=True)

    def add_command(self, command_name, contents):
        """Add a command to this command extension.

        Args:
            command_name (str): The name of the command.
            contents (str): the desired contents of the new command module
                file."""
        spack.cmd.require_cmd_name(command_name)
        python_name = spack.cmd.python_name(command_name)
        cmd = self.cmd.ensure(python_name + '.py')
        cmd.write(contents)


@pytest.fixture(scope='function')
def extension_creator(tmpdir, config):
    """Create a basic extension command directory structure"""
    @contextlib.contextmanager
    def _ce(extension_name='testcommand'):
        root = tmpdir.mkdir('spack-' + extension_name)
        extension = Extension(extension_name, root)
        with spack.config.override('config:extensions',
                                   [str(extension.root)]):
            yield extension
    list_of_modules = list(sys.modules.keys())
    yield _ce

    to_be_deleted = [x for x in sys.modules if x not in list_of_modules]
    for module_name in to_be_deleted:
        del sys.modules[module_name]


@pytest.fixture(scope='function')
def hello_world_extension(extension_creator):
    """Create an extension with a hello-world command."""
    with extension_creator() as extension:
        extension.add_command('hello-world', """
description = "hello world extension command"
section = "test command"
level = "long"

def setup_parser(subparser):
    pass


def hello_world(parser, args):
    print('Hello world!')
""")
        yield extension


@pytest.fixture(scope='function')
def hello_world_cmd(hello_world_extension):
    """Create and return an invokable "hello-world" extension command."""
    yield spack.main.SpackCommand('hello-world')


@pytest.fixture(scope='function')
def hello_world_with_module_in_root(extension_creator):
    """Create a "hello-world" extension command with additional code in the
    root folder.
    """
    @contextlib.contextmanager
    def _hwwmir(extension_name=None):
        with extension_creator(extension_name) \
            if extension_name else \
                extension_creator() as extension:
            # Note that the namespace of the extension is derived from the
            # fixture.
            extension.add_command('hello', """
# Test an absolute import
from spack.extensions.{ext_pname}.implementation import hello_world

# Test a relative import
from ..implementation import hello_folks

description = "hello world extension command"
section = "test command"
level = "long"

# Test setting a global variable in setup_parser and retrieving
# it in the command
global_message = 'foo'

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subcommand')
    global global_message
    sp.add_parser('world', help='Print Hello world!')
    sp.add_parser('folks', help='Print Hello folks!')
    sp.add_parser('global', help='Print Hello folks!')
    global_message = 'bar'

def hello(parser, args):
    if args.subcommand == 'world':
        hello_world()
    elif args.subcommand == 'folks':
        hello_folks()
    elif args.subcommand == 'global':
        print(global_message)
""".format(ext_pname=extension.pname))

            extension.main.ensure('__init__.py')
            implementation \
                = extension.main.ensure('implementation.py')
            implementation.write("""
def hello_world():
    print('Hello world!')

def hello_folks():
    print('Hello folks!')
""")
            yield spack.main.SpackCommand('hello')

    yield _hwwmir


def test_simple_command_extension(hello_world_cmd):
    """Basic test of a functioning command."""
    output = hello_world_cmd()
    assert 'Hello world!' in output


def test_multi_extension_search(hello_world_extension, tmpdir):
    """Ensure we can find an extension command even if it's not in the first
    place we look.
    """

    extra_ext_name = 'testcommand2'
    extra_ext = Extension(extra_ext_name,
                          tmpdir.mkdir('spack-' + extra_ext_name))
    with spack.config.override('config:extensions', [str(extra_ext.root)]):
        assert ('Hello world') in spack.main.SpackCommand('hello-world')()


def test_duplicate_module_load(hello_world_cmd):
    """Ensure duplicate module load attempts are successful.

    The command module will already have been loaded once by the
    hello_world_cmd fixture.
    """
    assert ('Hello world') in spack.main.SpackCommand('hello-world')()


@pytest.mark.parametrize('extension_name',
                         [None, 'hyphenated-extension'],
                         ids=['simple', 'hyphenated_extension_name'])
def test_command_with_import(extension_name, hello_world_with_module_in_root):
    """Ensure we can write a functioning command with multiple imported
    subcommands, including where the extension name contains a hyphen.
    """
    with hello_world_with_module_in_root(extension_name) as hello_world:
        output = hello_world('world')
        assert 'Hello world!' in output
        output = hello_world('folks')
        assert 'Hello folks!' in output
        output = hello_world('global')
        assert 'bar' in output


def test_missing_command():
    """Ensure that we raise the expected exception if the desired command is
    not present.
    """
    with pytest.raises(spack.extensions.CommandNotFoundError):
        spack.cmd.get_module("no-such-command")


@pytest.mark.\
    parametrize('extension_path,expected_exception',
                [('/my/bad/extension',
                  spack.extensions.ExtensionNamingError),
                 ('', spack.extensions.ExtensionNamingError),
                 ('/my/bad/spack--extra-hyphen',
                  spack.extensions.ExtensionNamingError),
                 ('/my/good/spack-extension',
                  spack.extensions.CommandNotFoundError),
                 ('/my/still/good/spack-extension/',
                  spack.extensions.CommandNotFoundError),
                 ('/my/spack-hyphenated-extension',
                  spack.extensions.CommandNotFoundError)],
                ids=['no_stem', 'vacuous', 'leading_hyphen',
                     'basic_good', 'trailing_slash', 'hyphenated'])
def test_extension_naming(extension_path, expected_exception, config):
    """Ensure that we are correctly validating configured extension paths
    for conformity with the rules: the basename should match
    ``spack-<name>``; <name> may have embedded hyphens but not begin with one.
    """
    with spack.config.override('config:extensions', [extension_path]):
        with pytest.raises(expected_exception):
            spack.cmd.get_module("no-such-command")


def test_missing_command_function(extension_creator, capsys):
    """Ensure we die as expected if a command module does not have the
    expected command function defined.
    """
    with extension_creator() as extension:
        extension.\
            add_command('bad-cmd',
                        """\ndescription = "Empty command implementation"\n""")
        with pytest.raises(SystemExit):
            spack.cmd.get_module('bad-cmd')
        capture = capsys.readouterr()
        assert "must define function 'bad_cmd'." in capture[1]


def test_get_command_paths(config):
    """Exercise the construction of extension command search paths."""
    extensions = ('extension-1', 'extension-2')
    ext_paths = []
    expected_cmd_paths = []
    for ext in extensions:
        ext_path = os.path.join('my', 'path', 'to', 'spack-' + ext)
        ext_paths.append(ext_path)
        expected_cmd_paths.append(os.path.join(ext_path,
                                               spack.cmd.python_name(ext),
                                               'cmd'))

    with spack.config.override('config:extensions', ext_paths):
        assert spack.extensions.get_command_paths() == expected_cmd_paths


@pytest.mark.parametrize('command_name,contents,exception',
                         [('bad-cmd', 'from oopsie.daisy import bad\n',
                           ImportError),
                          ('bad-cmd', """var = bad_function_call('blech')\n""",
                           NameError),
                          ('bad-cmd', ')\n', SyntaxError)],
                         ids=['ImportError', 'NameError', 'SyntaxError'])
def test_failing_command(command_name, contents, exception, extension_creator):
    """Ensure that the configured command fails to import with the specified
    error.
    """
    with extension_creator() as extension:
        extension.add_command(command_name, contents)
        with pytest.raises(exception):
            spack.extensions.get_module(command_name)
