# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import os

import llnl.util.tty as tty

import spack.config
import spack.environment as ev

from spack.util.editor import editor

description = "get and set configuration options"
section = "config"
level = "long"


def setup_parser(subparser):
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # User can only choose one
    subparser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        help="configuration scope to read/modify")

    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='config_command')

    get_parser = sp.add_parser('get', help='print configuration values')
    get_parser.add_argument('section',
                            help="configuration section to print. "
                                 "options: %(choices)s",
                            nargs='?',
                            metavar='SECTION',
                            choices=spack.config.section_schemas)

    blame_parser = sp.add_parser(
        'blame', help='print configuration annotated with source file:line')
    blame_parser.add_argument('section',
                              help="configuration section to print. "
                              "options: %(choices)s",
                              metavar='SECTION',
                              choices=spack.config.section_schemas)

    edit_parser = sp.add_parser('edit', help='edit configuration file')
    edit_parser.add_argument('section',
                             help="configuration section to edit. "
                                  "options: %(choices)s",
                             metavar='SECTION',
                             nargs='?',
                             choices=spack.config.section_schemas)
    edit_parser.add_argument(
        '--print-file', action='store_true',
        help="print the file name that would be edited")


def _get_scope_and_section(args, edit=True):
    """Extract config scope and section from arguments."""
    scope = args.scope
    section = args.section
    # w/no args and an active environment, point to env manifest
    if not args.section:
        env = ev.get_env(args, 'config edit')
        if env:
            scope = env.env_file_config_scope_name()

    # set scope defaults
    elif not args.scope:
        if edit:
            scope = spack.config.default_modify_scope(section)
        else:
            scope = spack.config.default_list_scope()

    return scope, section


def config_get(args):
    """Dump merged YAML configuration for a specific section.

    With no arguments and an active environment, print the contents of
    the environment's manifest file (spack.yaml).

    """
    scope, section = _get_scope_and_section(args, edit=False)

    if scope and scope.startswith('env:'):
        config_file = spack.config.config.get_config_filename(scope, section)
        if os.path.exists(config_file):
            with open(config_file) as f:
                print(f.read())
        else:
            tty.die('environment has no %s file' % ev.manifest_name)

    elif section is not None:
        spack.config.config.print_section(section)

    else:
        tty.die('`spack config get` requires a section argument '
                'or an active environment.')


def config_blame(args):
    """Print out line-by-line blame of merged YAML."""
    spack.config.config.print_section(args.section, blame=True)


def config_edit(args):
    """Edit the configuration file for a specific scope and config section.

    With no arguments and an active environment, edit the spack.yaml for
    the active environment.

    """
    scope, section = _get_scope_and_section(args)
    if not scope and not section:
        tty.die('`spack config edit` requires a section argument '
                'or an active environment.')

    config_file = spack.config.config.get_config_filename(scope, section)
    if args.print_file:
        print(config_file)
    else:
        editor(config_file)


def config(parser, args):
    action = {'get': config_get,
              'blame': config_blame,
              'edit': config_edit}
    action[args.config_command](args)
