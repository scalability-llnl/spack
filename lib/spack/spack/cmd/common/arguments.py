# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import argparse

import spack.cmd
import spack.config
import spack.dependency as dep
import spack.environment as ev
import spack.modules
import spack.spec
import spack.store
from spack.util.pattern import Args

__all__ = ['add_common_arguments']

#: dictionary of argument-generating functions, keyed by name
_arguments = {}


def arg(fn):
    """Decorator for a function that generates a common argument.

    This ensures that argument bunches are created lazily. Decorate
    argument-generating functions below with @arg so that
    ``add_common_arguments()`` can find them.

    """
    _arguments[fn.__name__] = fn
    return fn


def add_common_arguments(parser, list_of_arguments):
    """Extend a parser with extra arguments

    Args:
        parser: parser to be extended
        list_of_arguments: arguments to be added to the parser
    """
    for argument in list_of_arguments:
        if argument not in _arguments:
            message = 'Trying to add non existing argument "{0}" to a command'
            raise KeyError(message.format(argument))

        x = _arguments[argument]()
        parser.add_argument(*x.flags, **x.kwargs)


class ConstraintAction(argparse.Action):
    """Constructs a list of specs based on constraints from the command line

    An instance of this class is supposed to be used as an argument action
    in a parser. It will read a constraint and will attach a function to the
    arguments that accepts optional keyword arguments.

    To obtain the specs from a command the function must be called.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        # Query specs from command line
        self.values = values
        namespace.constraint = values
        namespace.specs = self._specs

    def _specs(self, **kwargs):
        qspecs = spack.cmd.parse_specs(self.values)

        # If an environment is provided, we'll restrict the search to
        # only its installed packages.
        env = ev._active_environment
        if env:
            kwargs['hashes'] = set(env.all_hashes())

        # return everything for an empty query.
        if not qspecs:
            return spack.store.db.query(**kwargs)

        # Return only matching stuff otherwise.
        specs = {}
        for spec in qspecs:
            for s in spack.store.db.query(spec, **kwargs):
                # This is fast for already-concrete specs
                specs[s.dag_hash()] = s

        return sorted(specs.values())


class SetParallelJobs(argparse.Action):
    """Sets the correct value for parallel build jobs.

    The value is is set in the command line configuration scope so that
    it can be retrieved using the spack.config API.
    """
    def __call__(self, parser, namespace, jobs, option_string):
        # Jobs is a single integer, type conversion is already applied
        # see https://docs.python.org/3/library/argparse.html#action-classes
        if jobs < 1:
            msg = 'invalid value for argument "{0}" '\
                  '[expected a positive integer, got "{1}"]'
            raise ValueError(msg.format(option_string, jobs))

        spack.config.set('config:build_jobs', jobs, scope='command_line')

        setattr(namespace, 'jobs', jobs)


class DeptypeAction(argparse.Action):
    """Creates a tuple of valid dependency types from a deptype argument."""
    def __call__(self, parser, namespace, values, option_string=None):
        deptype = dep.all_deptypes
        if values:
            deptype = tuple(x.strip() for x in values.split(','))
            if deptype == ('all',):
                deptype = 'all'
            deptype = dep.canonical_deptype(deptype)

        setattr(namespace, self.dest, deptype)


# TODO: merge constraint and installed_specs
@arg
def constraint():
    return Args(
        'constraint', nargs=argparse.REMAINDER, action=ConstraintAction,
        help='constraint to select a subset of installed packages',
        metavar='installed_specs')


@arg
def package():
    return Args('package', help='package name')


@arg
def packages():
    return Args(
        'packages', nargs='+', help='one or more package names',
        metavar='package')


# Specs must use `nargs=argparse.REMAINDER` because a single spec can
# contain spaces, and contain variants like '-mpi' that argparse thinks
# are a collection of optional flags.
@arg
def spec():
    return Args('spec', nargs=argparse.REMAINDER, help='package spec')


@arg
def specs():
    return Args(
        'specs', nargs=argparse.REMAINDER, help='one or more package specs')


@arg
def installed_spec():
    return Args(
        'spec', nargs=argparse.REMAINDER, help='installed package spec',
        metavar='installed_spec')


@arg
def installed_specs():
    return Args(
        'specs', nargs=argparse.REMAINDER,
        help='one or more installed package specs', metavar='installed_specs')


@arg
def yes_to_all():
    return Args(
        '-y', '--yes-to-all', action='store_true', dest='yes_to_all',
        help='assume "yes" is the answer to every confirmation request')


@arg
def recurse_dependencies():
    return Args(
        '-r', '--dependencies', action='store_true',
        dest='recurse_dependencies',
        help='recursively traverse spec dependencies')


@arg
def recurse_dependents():
    return Args(
        '-R', '--dependents', action='store_true', dest='dependents',
        help='also uninstall any packages that depend on the ones given '
        'via command line')


@arg
def clean():
    return Args(
        '--clean',
        action='store_false',
        default=spack.config.get('config:dirty'),
        dest='dirty',
        help='unset harmful variables in the build environment (default)')


@arg
def deptype():
    return Args(
        '--deptype', action=DeptypeAction, default=dep.all_deptypes,
        help="comma-separated list of deptypes to traverse\ndefault=%s"
        % ','.join(dep.all_deptypes))


@arg
def dirty():
    return Args(
        '--dirty',
        action='store_true',
        default=spack.config.get('config:dirty'),
        dest='dirty',
        help="preserve user environment in spack's build environment (danger!)"
    )


@arg
def long():
    return Args(
        '-l', '--long', action='store_true',
        help='show dependency hashes as well as versions')


@arg
def very_long():
    return Args(
        '-L', '--very-long', action='store_true',
        help='show full dependency hashes as well as versions')


@arg
def tags():
    return Args(
        '-t', '--tag', action='append', dest='tags', metavar='TAG',
        help='filter a package query by tag (multiple use allowed)')


@arg
def jobs():
    return Args(
        '-j', '--jobs', action=SetParallelJobs, type=int, dest='jobs',
        help='explicitly set number of parallel jobs')


@arg
def install_status():
    return Args(
        '-I', '--install-status', action='store_true', default=False,
        help='show install status of packages. packages can be: '
        'installed [+], missing and needed by an installed package [-], '
        'or not installed (no annotation)')


@arg
def no_checksum():
    return Args(
        '-n', '--no-checksum', action='store_true', default=False,
        help="do not use checksums to verify downloaded files (unsafe)")


@arg
def deprecated():
    return Args(
        '--deprecated', action='store_true', default=False,
        help='fetch deprecated versions without warning')


def add_cdash_args(subparser, add_help):
    cdash_help = {}
    if add_help:
        cdash_help['upload-url'] = "CDash URL where reports will be uploaded"
        cdash_help['build'] = """The name of the build that will be reported to CDash.
Defaults to spec of the package to operate on."""
        cdash_help['site'] = """The site name that will be reported to CDash.
Defaults to current system hostname."""
        cdash_help['track'] = """Results will be reported to this group on CDash.
Defaults to Experimental."""
        cdash_help['buildstamp'] = """Instead of letting the CDash reporter prepare the
buildstamp which, when combined with build name, site and project,
uniquely identifies the build, provide this argument to identify
the build yourself.  Format: %%Y%%m%%d-%%H%%M-[cdash-track]"""
    else:
        cdash_help['upload-url'] = argparse.SUPPRESS
        cdash_help['build'] = argparse.SUPPRESS
        cdash_help['site'] = argparse.SUPPRESS
        cdash_help['track'] = argparse.SUPPRESS
        cdash_help['buildstamp'] = argparse.SUPPRESS

    subparser.add_argument(
        '--cdash-upload-url',
        default=None,
        help=cdash_help['upload-url']
    )
    subparser.add_argument(
        '--cdash-build',
        default=None,
        help=cdash_help['build']
    )
    subparser.add_argument(
        '--cdash-site',
        default=None,
        help=cdash_help['site']
    )

    cdash_subgroup = subparser.add_mutually_exclusive_group()
    cdash_subgroup.add_argument(
        '--cdash-track',
        default='Experimental',
        help=cdash_help['track']
    )
    cdash_subgroup.add_argument(
        '--cdash-buildstamp',
        default=None,
        help=cdash_help['buildstamp']
    )
