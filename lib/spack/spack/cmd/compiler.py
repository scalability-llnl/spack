# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import sys
from six import iteritems

import llnl.util.tty as tty
import spack.cmd.common.deployment as deployment
import spack.compilers
import spack.config
import spack.spec
from llnl.util.lang import index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize
from spack.spec import CompilerSpec, ArchSpec

description = "manage compilers"
section = "system"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='compiler_command')

    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # Find
    find_parser = sp.add_parser(
        'find', aliases=['add'],
        help='search the system for compilers to add to Spack configuration')
    find_parser.add_argument('add_paths', nargs=argparse.REMAINDER)
    find_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope('compilers'),
        help="configuration scope to modify")

    # Remove
    remove_parser = sp.add_parser(
        'remove', aliases=['rm'], help='remove compiler by spec')
    remove_parser.add_argument(
        '-a', '--all', action='store_true',
        help='remove ALL compilers that match spec')
    remove_parser.add_argument('compiler_spec')
    remove_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope('compilers'),
        help="configuration scope to modify")

    # List
    list_parser = sp.add_parser('list', help='list available compilers')
    list_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_list_scope(),
        help="configuration scope to read from")

    # Info
    info_parser = sp.add_parser('info', help='show compiler paths')
    info_parser.add_argument('compiler_spec')
    info_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_list_scope(),
        help="configuration scope to read from")


def compiler_find(args):
    """Search either $PATH or a list of paths OR MODULES for compilers and
       add them to Spack's configuration.

    """
    deployment.die_if_deployment('compiler find')

    # None signals spack.compiler.find_compilers to use its default logic
    paths = args.add_paths or None

    # Don't initialize compilers config via compilers.get_compiler_config.
    # Just let compiler_find do the
    # entire process and return an empty config from all_compilers
    # Default for any other process is init_config=True
    compilers = [c for c in spack.compilers.find_compilers(paths)]
    new_compilers = []
    for c in compilers:
        arch_spec = ArchSpec((None, c.operating_system, c.target))
        same_specs = spack.compilers.compilers_for_spec(
            c.spec, arch_spec, init_config=False)

        if not same_specs:
            new_compilers.append(c)

    if new_compilers:
        spack.compilers.add_compilers_to_config(new_compilers,
                                                scope=args.scope,
                                                init_config=False)
        n = len(new_compilers)
        s = 's' if n > 1 else ''

        config = spack.config.config
        filename = config.get_config_filename(args.scope, 'compilers')
        tty.msg("Added %d new compiler%s to %s" % (n, s, filename))
        colify(reversed(sorted(c.spec for c in new_compilers)), indent=4)
    else:
        tty.msg("Found no new compilers")
    tty.msg("Compilers are defined in the following files:")
    colify(spack.compilers.compiler_config_files(), indent=4)


def compiler_remove(args):
    deployment.die_if_deployment('compiler remove')

    cspec = CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec, scope=args.scope)
    if not compilers:
        tty.die("No compilers match spec %s" % cspec)
    elif not args.all and len(compilers) > 1:
        tty.error("Multiple compilers match spec %s. Choose one:" % cspec)
        colify(reversed(sorted([c.spec for c in compilers])), indent=4)
        tty.msg("Or, use `spack compiler remove -a` to remove all of them.")
        sys.exit(1)

    for compiler in compilers:
        spack.compilers.remove_compiler_from_config(
            compiler.spec, scope=args.scope)
        tty.msg("Removed compiler %s" % compiler.spec)


def compiler_info(args):
    """Print info about all compilers matching a spec."""
    cspec = CompilerSpec(args.compiler_spec)
    compilers = spack.compilers.compilers_for_spec(cspec, scope=args.scope)

    if not compilers:
        tty.error("No compilers match spec %s" % cspec)
    else:
        for c in compilers:
            print(str(c.spec) + ":")
            print("\tpaths:")
            for cpath in ['cc', 'cxx', 'f77', 'fc']:
                print("\t\t%s = %s" % (cpath, getattr(c, cpath, None)))
            if c.flags:
                print("\tflags:")
                for flag, flag_value in iteritems(c.flags):
                    print("\t\t%s = %s" % (flag, flag_value))
            if len(c.environment) != 0:
                if len(c.environment.get('set', {})) != 0:
                    print("\tenvironment:")
                    print("\t    set:")
                    for key, value in iteritems(c.environment['set']):
                        print("\t        %s = %s" % (key, value))
            if c.extra_rpaths:
                print("\tExtra rpaths:")
                for extra_rpath in c.extra_rpaths:
                    print("\t\t%s" % extra_rpath)
            print("\tmodules  = %s" % c.modules)
            print("\toperating system  = %s" % c.operating_system)


def compiler_list(args):
    tty.msg("Available compilers")
    index = index_by(spack.compilers.all_compilers(scope=args.scope),
                     lambda c: (c.spec.name, c.operating_system, c.target))

    # For a container, take each element which does not evaluate to false and
    # convert it to a string. For elements which evaluate to False (e.g. None)
    # convert them to '' (in which case it still evaluates to False but is a
    # string type). Tuples produced by this are guaranteed to be comparable in
    # Python 3
    convert_str = (
        lambda tuple_container:
        tuple(str(x) if x else '' for x in tuple_container))

    index_str_keys = list(
        (convert_str(x), y) for x, y in index.items())
    ordered_sections = sorted(index_str_keys, key=lambda item: item[0])
    for i, (key, compilers) in enumerate(ordered_sections):
        if i >= 1:
            print()
        name, os, target = key
        os_str = os
        if target:
            os_str += "-%s" % target
        cname = "%s{%s} %s" % (spack.spec.compiler_color, name, os_str)
        tty.hline(colorize(cname), char='-')
        colify(reversed(sorted(c.spec for c in compilers)))


def compiler(parser, args):
    action = {'add': compiler_find,
              'find': compiler_find,
              'remove': compiler_remove,
              'rm': compiler_remove,
              'info': compiler_info,
              'list': compiler_list}
    action[args.compiler_command](args)
