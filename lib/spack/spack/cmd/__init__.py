# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import re
import sys
import argparse
import ruamel.yaml as yaml

import six

import llnl.util.tty as tty
from llnl.util.lang import attr_setdefault, index_by
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize
from llnl.util.filesystem import join_path

import spack.config
import spack.error
import spack.extensions
import spack.paths
import spack.spec
import spack.store
import spack.util.spack_json as sjson
import spack.util.string
from ruamel.yaml.error import MarkedYAMLError


# cmd has a submodule called "list" so preserve the python list module
python_list = list

# Patterns to ignore in the commands directory when looking for commands.
ignore_files = r'^\.|^__init__.py$|^#'

SETUP_PARSER = "setup_parser"
DESCRIPTION = "description"


def python_name(cmd_name):
    """Convert ``-`` to ``_`` in command name, to make a valid identifier."""
    return cmd_name.replace("-", "_")


def require_python_name(pname):
    """Require that the provided name is a valid python name (per
    python_name()). Useful for checking parameters for function
    prerequisites."""
    if python_name(pname) != pname:
        raise PythonNameError(pname)


def cmd_name(python_name):
    """Convert module name (with ``_``) to command name (with ``-``)."""
    return python_name.replace('_', '-')


def require_cmd_name(cname):
    """Require that the provided name is a valid command name (per
    cmd_name()). Useful for checking parameters for function
    prerequisites.
    """
    if cmd_name(cname) != cname:
        raise CommandNameError(cname)


#: global, cached list of all commands -- access through all_commands()
_all_commands = None


def all_commands():
    """Get a sorted list of all spack commands.

    This will list the lib/spack/spack/cmd directory and find the
    commands there to construct the list.  It does not actually import
    the python files -- just gets the names.
    """
    global _all_commands
    if _all_commands is None:
        _all_commands = []
        command_paths = [spack.paths.command_path]  # Built-in commands
        command_paths += spack.extensions.get_command_paths()  # Extensions
        for path in command_paths:
            for file in os.listdir(path):
                if file.endswith(".py") and not re.search(ignore_files, file):
                    cmd = re.sub(r'.py$', '', file)
                    _all_commands.append(cmd_name(cmd))

        _all_commands.sort()

    return _all_commands


def remove_options(parser, *options):
    """Remove some options from a parser."""
    for option in options:
        for action in parser._actions:
            if vars(action)['option_strings'][0] == option:
                parser._handle_conflict_resolve(None, [(option, action)])
                break


def get_module(cmd_name):
    """Imports the module for a particular command name and returns it.

    Args:
        cmd_name (str): name of the command for which to get a module
            (contains ``-``, not ``_``).
    """
    require_cmd_name(cmd_name)
    pname = python_name(cmd_name)

    try:
        # Try to import the command from the built-in directory
        module_name = "%s.%s" % (__name__, pname)
        module = __import__(module_name,
                            fromlist=[pname, SETUP_PARSER, DESCRIPTION],
                            level=0)
        tty.debug('Imported {0} from built-in commands'.format(pname))
    except ImportError:
        module = spack.extensions.get_module(cmd_name)

    attr_setdefault(module, SETUP_PARSER, lambda *args: None)  # null-op
    attr_setdefault(module, DESCRIPTION, "")

    if not hasattr(module, pname):
        tty.die("Command module %s (%s) must define function '%s'." %
                (module.__name__, module.__file__, pname))

    return module


def get_command(cmd_name):
    """Imports the command function associated with cmd_name.

    The function's name is derived from cmd_name using python_name().

    Args:
        cmd_name (str): name of the command (contains ``-``, not ``_``).
    """
    require_cmd_name(cmd_name)
    pname = python_name(cmd_name)
    return getattr(get_module(cmd_name), pname)


def parse_specs(args, **kwargs):
    """Convenience function for parsing arguments from specs.  Handles common
       exceptions and dies if there are errors.
    """
    concretize = kwargs.get('concretize', False)
    normalize = kwargs.get('normalize', False)
    tests = kwargs.get('tests', False)

    try:
        sargs = args
        if not isinstance(args, six.string_types):
            sargs = ' '.join(spack.util.string.quote(args))
        specs = spack.spec.parse(sargs)
        for spec in specs:
            if concretize:
                spec.concretize(tests=tests)  # implies normalize
            elif normalize:
                spec.normalize(tests=tests)

        return specs

    except spack.spec.SpecParseError as e:
        msg = e.message + "\n" + str(e.string) + "\n"
        msg += (e.pos + 2) * " " + "^"
        raise spack.error.SpackError(msg)

    except spack.error.SpecError as e:

        msg = e.message
        if e.long_message:
            msg += e.long_message

        raise spack.error.SpackError(msg)


def matching_spec_from_env(spec):
    """
    Returns a concrete spec, matching what is available in the environment.
    If no matching spec is found in the environment (or if no environment is
    active), this will return the given spec but concretized.
    """
    env = spack.environment.get_env({}, cmd_name)
    if env:
        return env.matching_spec(spec) or spec.concretized()
    else:
        return spec.concretized()


def elide_list(line_list, max_num=10):
    """Takes a long list and limits it to a smaller number of elements,
       replacing intervening elements with '...'.  For example::

           elide_list([1,2,3,4,5,6], 4)

       gives::

           [1, 2, 3, '...', 6]
    """
    if len(line_list) > max_num:
        return line_list[:max_num - 1] + ['...'] + line_list[-1:]
    else:
        return line_list


def disambiguate_spec(spec, env, local=False, installed=True, first=False):
    """Given a spec, figure out which installed package it refers to.

    Arguments:
        spec (spack.spec.Spec): a spec to disambiguate
        env (spack.environment.Environment): a spack environment,
            if one is active, or None if no environment is active
        local (boolean, default False): do not search chained spack instances
        installed (boolean or any, or spack.database.InstallStatus or iterable
            of spack.database.InstallStatus): install status argument passed to
            database query. See ``spack.database.Database._query`` for details.
    """
    hashes = env.all_hashes() if env else None
    return disambiguate_spec_from_hashes(spec, hashes, local, installed, first)


def disambiguate_spec_from_hashes(spec, hashes, local=False,
                                  installed=True, first=False):
    """Given a spec and a list of hashes, get concrete spec the spec refers to.

    Arguments:
        spec (spack.spec.Spec): a spec to disambiguate
        hashes (iterable): a set of hashes of specs among which to disambiguate
        local (boolean, default False): do not search chained spack instances
        installed (boolean or any, or spack.database.InstallStatus or iterable
            of spack.database.InstallStatus): install status argument passed to
            database query. See ``spack.database.Database._query`` for details.
    """
    if local:
        matching_specs = spack.store.db.query_local(spec, hashes=hashes,
                                                    installed=installed)
    else:
        matching_specs = spack.store.db.query(spec, hashes=hashes,
                                              installed=installed)
    if not matching_specs:
        tty.die("Spec '%s' matches no installed packages." % spec)

    elif first:
        return matching_specs[0]

    elif len(matching_specs) > 1:
        format_string = '{name}{@version}{%compiler}{arch=architecture}'
        args = ["%s matches multiple packages." % spec,
                "Matching packages:"]
        args += [colorize("  @K{%s} " % s.dag_hash(7)) +
                 s.cformat(format_string) for s in matching_specs]
        args += ["Use a more specific spec."]
        tty.die(*args)

    return matching_specs[0]


def gray_hash(spec, length):
    if not length:
        # default to maximum hash length
        length = 32
    h = spec.dag_hash(length) if spec.concrete else '-' * length
    return colorize('@K{%s}' % h)


def display_specs_as_json(specs, deps=False):
    """Convert specs to a list of json records."""
    seen = set()
    records = []
    for spec in specs:
        if spec.dag_hash() in seen:
            continue
        seen.add(spec.dag_hash())
        records.append(spec.to_record_dict())

        if deps:
            for dep in spec.traverse():
                if dep.dag_hash() in seen:
                    continue
                seen.add(dep.dag_hash())
                records.append(dep.to_record_dict())

    sjson.dump(records, sys.stdout)


def iter_groups(specs, indent, all_headers):
    """Break a list of specs into groups indexed by arch/compiler."""
    # Make a dict with specs keyed by architecture and compiler.
    index = index_by(specs, ('architecture', 'compiler'))
    ispace = indent * ' '

    # Traverse the index and print out each package
    for i, (architecture, compiler) in enumerate(sorted(index)):
        if i > 0:
            print()

        header = "%s{%s} / %s{%s}" % (
            spack.spec.architecture_color,
            architecture if architecture else 'no arch',
            spack.spec.compiler_color,
            compiler if compiler else 'no compiler')

        # Sometimes we want to display specs that are not yet concretized.
        # If they don't have a compiler / architecture attached to them,
        # then skip the header
        if all_headers or (architecture is not None or compiler is not None):
            sys.stdout.write(ispace)
            tty.hline(colorize(header), char='-')

        specs = index[(architecture, compiler)]
        specs.sort()
        yield specs


def display_specs(specs, args=None, **kwargs):
    """Display human readable specs with customizable formatting.

    Prints the supplied specs to the screen, formatted according to the
    arguments provided.

    Specs are grouped by architecture and compiler, and columnized if
    possible.

    Options can add more information to the default display. Options can
    be provided either as keyword arguments or as an argparse namespace.
    Keyword arguments take precedence over settings in the argparse
    namespace.

    Args:
        specs (list of spack.spec.Spec): the specs to display
        args (optional argparse.Namespace): namespace containing
            formatting arguments

    Keyword Args:
        paths (bool): Show paths with each displayed spec
        deps (bool): Display dependencies with specs
        long (bool): Display short hashes with specs
        very_long (bool): Display full hashes with specs (supersedes ``long``)
        namespace (bool): Print namespaces along with names
        show_flags (bool): Show compiler flags with specs
        variants (bool): Show variants with specs
        indent (int): indent each line this much
        groups (bool): display specs grouped by arch/compiler (default True)
        decorators (dict): dictionary mappng specs to decorators
        header_callback (function): called at start of arch/compiler groups
        all_headers (bool): show headers even when arch/compiler aren't defined
        output (stream): A file object to write to. Default is ``sys.stdout``

    """
    def get_arg(name, default=None):
        """Prefer kwargs, then args, then default."""
        if name in kwargs:
            return kwargs.get(name)
        elif args is not None:
            return getattr(args, name, default)
        else:
            return default

    paths         = get_arg('paths', False)
    deps          = get_arg('deps', False)
    hashes        = get_arg('long', False)
    namespace     = get_arg('namespace', False)
    flags         = get_arg('show_flags', False)
    full_compiler = get_arg('show_full_compiler', False)
    variants      = get_arg('variants', False)
    groups        = get_arg('groups', True)
    all_headers   = get_arg('all_headers', False)
    output        = get_arg('output', sys.stdout)

    decorator     = get_arg('decorator', None)
    if decorator is None:
        decorator = lambda s, f: f

    indent = get_arg('indent', 0)

    hlen = 7
    if get_arg('very_long', False):
        hashes = True
        hlen = None

    format_string = get_arg('format', None)
    if format_string is None:
        nfmt = '{fullname}' if namespace else '{name}'
        ffmt = ''
        if full_compiler or flags:
            ffmt += '{%compiler.name}'
            if full_compiler:
                ffmt += '{@compiler.version}'
            ffmt += ' {compiler_flags}'
        vfmt = '{variants}' if variants else ''
        format_string = nfmt + '{@version}' + ffmt + vfmt

    transform = {'package': decorator, 'fullpackage': decorator}

    def fmt(s, depth=0):
        """Formatter function for all output specs"""
        string = ""
        if hashes:
            string += gray_hash(s, hlen) + ' '
        string += depth * "    "
        string += s.cformat(format_string, transform=transform)
        return string

    def format_list(specs):
        """Display a single list of specs, with no groups"""
        # create the final, formatted versions of all specs
        formatted = []
        for spec in specs:
            formatted.append((fmt(spec), spec))
            if deps:
                for depth, dep in spec.traverse(root=False, depth=True):
                    formatted.append((fmt(dep, depth), dep))
                formatted.append(('', None))  # mark newlines

        # unless any of these are set, we can just colify and be done.
        if not any((deps, paths)):
            colify((f[0] for f in formatted), indent=indent, output=output)
            return ''

        # otherwise, we'll print specs one by one
        max_width = max(len(f[0]) for f in formatted)
        path_fmt = "%%-%ds%%s" % (max_width + 2)

        out = ''
        # getting lots of prefixes requires DB lookups. Ensure
        # all spec.prefix calls are in one transaction.
        with spack.store.db.read_transaction():
            for string, spec in formatted:
                if not string:
                    # print newline from above
                    out += '\n'
                    continue

                if paths:
                    out += path_fmt % (string, spec.prefix) + '\n'
                else:
                    out += string + '\n'

        return out

    out = ''
    if groups:
        for specs in iter_groups(specs, indent, all_headers):
            output.write(format_list(specs))
    else:
        out = format_list(sorted(specs))

    output.write(out)
    output.flush()


def spack_is_git_repo():
    """Ensure that this instance of Spack is a git clone."""
    return is_git_repo(spack.paths.prefix)


def is_git_repo(path):
    dotgit_path = join_path(path, '.git')
    if os.path.isdir(dotgit_path):
        # we are in a regular git repo
        return True
    if os.path.isfile(dotgit_path):
        # we might be in a git worktree
        try:
            with open(dotgit_path, "rb") as f:
                dotgit_content = yaml.load(f)
            return os.path.isdir(dotgit_content.get("gitdir", dotgit_path))
        except MarkedYAMLError:
            pass
    return False


class PythonNameError(spack.error.SpackError):
    """Exception class thrown for impermissible python names"""
    def __init__(self, name):
        self.name = name
        super(PythonNameError, self).__init__(
            '{0} is not a permissible Python name.'.format(name))


class CommandNameError(spack.error.SpackError):
    """Exception class thrown for impermissible command names"""
    def __init__(self, name):
        self.name = name
        super(CommandNameError, self).__init__(
            '{0} is not a permissible Spack command name.'.format(name))


########################################
# argparse types for argument validation
########################################
def extant_file(f):
    """
    Argparse type for files that exist.
    """
    if not os.path.isfile(f):
        raise argparse.ArgumentTypeError('%s does not exist' % f)
    return f
