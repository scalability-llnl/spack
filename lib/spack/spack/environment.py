# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os
import re
import sys
import shutil
import copy
import six

from ordereddict_backport import OrderedDict

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.tty.color import colorize

import spack.concretize
import spack.error
import spack.hash_types as ht
import spack.repo
import spack.schema.env
import spack.spec
import spack.store
import spack.stage
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.config
import spack.user_environment as uenv
from spack.filesystem_view import YamlFilesystemView
import spack.util.environment
from spack.spec import Spec
from spack.spec_list import SpecList, InvalidSpecConstraintError
from spack.variant import UnknownVariantError
import spack.util.lock as lk
from spack.util.path import substitute_path_variables
import spack.util.path

#: environment variable used to indicate the active environment
spack_env_var = 'SPACK_ENV'


#: currently activated environment
_active_environment = None


#: path where environments are stored in the spack tree
env_path = os.path.join(spack.paths.var_path, 'environments')


#: Name of the input yaml file for an environment
manifest_name = 'spack.yaml'


#: Name of the input yaml file for an environment
lockfile_name = 'spack.lock'


#: Name of the directory where environments store repos, logs, views
env_subdir_name = '.spack-env'


#: default spack.yaml file to put in new environments
default_manifest_yaml = """\
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
spack:
  # add package specs to the `specs` list
  specs: []
  view: true
"""
#: regex for validating enviroment names
valid_environment_name_re = r'^\w[\w-]*$'

#: version of the lockfile format. Must increase monotonically.
lockfile_format_version = 2

# Magic names
# The name of the standalone spec list in the manifest yaml
user_speclist_name = 'specs'
# The name of the default view (the view loaded on env.activate)
default_view_name = 'default'
# Default behavior to link all packages into views (vs. only root packages)
default_view_link = 'all'


def valid_env_name(name):
    return re.match(valid_environment_name_re, name)


def validate_env_name(name):
    if not valid_env_name(name):
        raise ValueError((
            "'%s': names must start with a letter, and only contain "
            "letters, numbers, _, and -.") % name)
    return name


def activate(
    env, use_env_repo=False, add_view=True, shell='sh', prompt=None
):
    """Activate an environment.

    To activate an environment, we add its configuration scope to the
    existing Spack configuration, and we set active to the current
    environment.

    Arguments:
        env (Environment): the environment to activate
        use_env_repo (bool): use the packages exactly as they appear in the
            environment's repository
        add_view (bool): generate commands to add view to path variables
        shell (string): One of `sh`, `csh`, `fish`.
        prompt (string): string to add to the users prompt, or None

    Returns:
        cmds: Shell commands to activate environment.
    TODO: environment to use the activated spack environment.
    """
    global _active_environment

    _active_environment = env
    prepare_config_scope(_active_environment)
    if use_env_repo:
        spack.repo.path.put_first(_active_environment.repo)

    tty.debug("Using environment '%s'" % _active_environment.name)

    # Construct the commands to run
    cmds = ''
    if shell == 'csh':
        # TODO: figure out how to make color work for csh
        cmds += 'setenv SPACK_ENV %s;\n' % env.path
        cmds += 'alias despacktivate "spack env deactivate";\n'
        if prompt:
            cmds += 'if (! $?SPACK_OLD_PROMPT ) '
            cmds += 'setenv SPACK_OLD_PROMPT "${prompt}";\n'
            cmds += 'set prompt="%s ${prompt}";\n' % prompt
    elif shell == 'fish':
        if os.getenv('TERM') and 'color' in os.getenv('TERM') and prompt:
            prompt = colorize('@G{%s} ' % prompt, color=True)

        cmds += 'set -gx SPACK_ENV %s;\n' % env.path
        cmds += 'function despacktivate;\n'
        cmds += '   spack env deactivate;\n'
        cmds += 'end;\n'
        #
        # NOTE: We're not changing the fish_prompt function (which is fish's
        # solution to the PS1 variable) here. This is a bit fiddly, and easy to
        # screw up => spend time reasearching a solution. Feedback welcome.
        #
    else:
        if os.getenv('TERM') and 'color' in os.getenv('TERM') and prompt:
            prompt = colorize('@G{%s} ' % prompt, color=True)

        cmds += 'export SPACK_ENV=%s;\n' % env.path
        cmds += "alias despacktivate='spack env deactivate';\n"
        if prompt:
            cmds += 'if [ -z ${SPACK_OLD_PS1+x} ]; then\n'
            cmds += '    if [ -z ${PS1+x} ]; then\n'
            cmds += "        PS1='$$$$';\n"
            cmds += '    fi;\n'
            cmds += '    export SPACK_OLD_PS1="${PS1}";\n'
            cmds += 'fi;\n'
            cmds += 'export PS1="%s ${PS1}";\n' % prompt

    #
    # NOTE in the fish-shell: Path variables are a special kind of variable
    # used to support colon-delimited path lists including PATH, CDPATH,
    # MANPATH, PYTHONPATH, etc. All variables that end in PATH (case-sensitive)
    # become PATH variables.
    #
    try:
        if add_view and default_view_name in env.views:
            with spack.store.db.read_transaction():
                cmds += env.add_default_view_to_shell(shell)
    except (spack.repo.UnknownPackageError,
            spack.repo.UnknownNamespaceError) as e:
        tty.error(e)
        tty.die(
            'Environment view is broken due to a missing package or repo.\n',
            '  To activate without views enabled, activate with:\n',
            '    spack env activate -V {0}\n'.format(env.name),
            '  To remove it and resolve the issue, '
            'force concretize with the command:\n',
            '    spack -e {0} concretize --force'.format(env.name))

    return cmds


def deactivate(shell='sh'):
    """Undo any configuration or repo settings modified by ``activate()``.

    Arguments:
        shell (string): One of `sh`, `csh`, `fish`. Shell style to use.

    Returns:
        (string): shell commands for `shell` to undo environment variables

    """
    global _active_environment

    if not _active_environment:
        return

    deactivate_config_scope(_active_environment)

    # use _repo so we only remove if a repo was actually constructed
    if _active_environment._repo:
        spack.repo.path.remove(_active_environment._repo)

    cmds = ''
    if shell == 'csh':
        cmds += 'unsetenv SPACK_ENV;\n'
        cmds += 'if ( $?SPACK_OLD_PROMPT ) '
        cmds += 'set prompt="$SPACK_OLD_PROMPT" && '
        cmds += 'unsetenv SPACK_OLD_PROMPT;\n'
        cmds += 'unalias despacktivate;\n'
    elif shell == 'fish':
        cmds += 'set -e SPACK_ENV;\n'
        cmds += 'functions -e despacktivate;\n'
        #
        # NOTE: Not changing fish_prompt (above) => no need to restore it here.
        #
    else:
        cmds += 'if [ ! -z ${SPACK_ENV+x} ]; then\n'
        cmds += 'unset SPACK_ENV; export SPACK_ENV;\n'
        cmds += 'fi;\n'
        cmds += 'unalias despacktivate;\n'
        cmds += 'if [ ! -z ${SPACK_OLD_PS1+x} ]; then\n'
        cmds += '    if [ "$SPACK_OLD_PS1" = \'$$$$\' ]; then\n'
        cmds += '        unset PS1; export PS1;\n'
        cmds += '    else\n'
        cmds += '        export PS1="$SPACK_OLD_PS1";\n'
        cmds += '    fi;\n'
        cmds += '    unset SPACK_OLD_PS1; export SPACK_OLD_PS1;\n'
        cmds += 'fi;\n'

    try:
        if default_view_name in _active_environment.views:
            with spack.store.db.read_transaction():
                cmds += _active_environment.rm_default_view_from_shell(shell)
    except (spack.repo.UnknownPackageError,
            spack.repo.UnknownNamespaceError) as e:
        tty.warn(e)
        tty.warn('Could not fully deactivate view due to missing package '
                 'or repo, shell environment may be corrupt.')

    tty.debug("Deactivated environmennt '%s'" % _active_environment.name)
    _active_environment = None

    return cmds


def find_environment(args):
    """Find active environment from args, spack.yaml, or environment variable.

    This is called in ``spack.main`` to figure out which environment to
    activate.

    Check for an environment in this order:
        1. via ``spack -e ENV`` or ``spack -D DIR`` (arguments)
        2. as a spack.yaml file in the current directory, or
        3. via a path in the SPACK_ENV environment variable.

    If an environment is found, read it in.  If not, return None.

    Arguments:
        args (Namespace): argparse namespace wtih command arguments

    Returns:
        (Environment): a found environment, or ``None``
    """
    # try arguments
    env = getattr(args, 'env', None)

    # treat env as a name
    if env:
        if exists(env):
            return read(env)

    else:
        # if env was specified, see if it is a dirctory otherwise, look
        # at env_dir (env and env_dir are mutually exclusive)
        env = getattr(args, 'env_dir', None)

        # if no argument, look for the environment variable
        if not env:
            env = os.environ.get(spack_env_var)

            # nothing was set; there's no active environment
            if not env:
                return None

    # if we get here, env isn't the name of a spack environment; it has
    # to be a path to an environment, or there is something wrong.
    if is_env_dir(env):
        return Environment(env)

    raise SpackEnvironmentError('no environment in %s' % env)


def get_env(args, cmd_name, required=False):
    """Used by commands to get the active environment.

    This first checks for an ``env`` argument, then looks at the
    ``active`` environment.  We check args first because Spack's
    subcommand arguments are parsed *after* the ``-e`` and ``-D``
    arguments to ``spack``.  So there may be an ``env`` argument that is
    *not* the active environment, and we give it precedence.

    This is used by a number of commands for determining whether there is
    an active environment.

    If an environment is not found *and* is required, print an error
    message that says the calling command *needs* an active environment.

    Arguments:
        args (Namespace): argparse namespace wtih command arguments
        cmd_name (str): name of calling command
        required (bool): if ``True``, raise an exception when no environment
            is found; if ``False``, just return ``None``

    Returns:
        (Environment): if there is an arg or active environment
    """
    # try argument first
    env = getattr(args, 'env', None)
    if env:
        if exists(env):
            return read(env)
        elif is_env_dir(env):
            return Environment(env)
        else:
            raise SpackEnvironmentError('no environment in %s' % env)

    # try the active environment. This is set by find_environment() (above)
    if _active_environment:
        return _active_environment
    elif not required:
        return None
    else:
        tty.die(
            '`spack %s` requires an environment' % cmd_name,
            'activate an environment first:',
            '    spack env activate ENV',
            'or use:',
            '    spack -e ENV %s ...' % cmd_name)


def _root(name):
    """Non-validating version of root(), to be used internally."""
    return os.path.join(env_path, name)


def root(name):
    """Get the root directory for an environment by name."""
    validate_env_name(name)
    return _root(name)


def exists(name):
    """Whether an environment with this name exists or not."""
    if not valid_env_name(name):
        return False
    return os.path.isdir(root(name))


def active(name):
    """True if the named environment is active."""
    return _active_environment and name == _active_environment.name


def is_env_dir(path):
    """Whether a directory contains a spack environment."""
    return os.path.isdir(path) and os.path.exists(
        os.path.join(path, manifest_name))


def read(name):
    """Get an environment with the supplied name."""
    validate_env_name(name)
    if not exists(name):
        raise SpackEnvironmentError("no such environment '%s'" % name)
    return Environment(root(name))


def create(name, init_file=None, with_view=None, keep_relative=False):
    """Create a named environment in Spack."""
    validate_env_name(name)
    if exists(name):
        raise SpackEnvironmentError("'%s': environment already exists" % name)
    return Environment(root(name), init_file, with_view, keep_relative)


def config_dict(yaml_data):
    """Get the configuration scope section out of an spack.yaml"""
    key = spack.config.first_existing(yaml_data, spack.schema.env.keys)
    return yaml_data[key]


def all_environment_names():
    """List the names of environments that currently exist."""
    # just return empty if the env path does not exist.  A read-only
    # operation like list should not try to create a directory.
    if not os.path.exists(env_path):
        return []

    candidates = sorted(os.listdir(env_path))
    names = []
    for candidate in candidates:
        yaml_path = os.path.join(_root(candidate), manifest_name)
        if valid_env_name(candidate) and os.path.exists(yaml_path):
            names.append(candidate)
    return names


def all_environments():
    """Generator for all named Environments."""
    for name in all_environment_names():
        yield read(name)


def _read_yaml(str_or_file):
    """Read YAML from a file for round-trip parsing."""
    data = syaml.load_config(str_or_file)
    filename = getattr(str_or_file, 'name', None)
    default_data = spack.config.validate(
        data, spack.schema.env.schema, filename)
    return (data, default_data)


def _write_yaml(data, str_or_file):
    """Write YAML to a file preserving comments and dict order."""
    filename = getattr(str_or_file, 'name', None)
    spack.config.validate(data, spack.schema.env.schema, filename)
    syaml.dump_config(data, str_or_file, default_flow_style=False)


def _eval_conditional(string):
    """Evaluate conditional definitions using restricted variable scope."""
    valid_variables = spack.util.environment.get_host_environment()
    valid_variables.update({
        're': re,
        'env': os.environ,
    })
    return eval(string, valid_variables)


class ViewDescriptor(object):
    def __init__(self, base_path, root, projections={}, select=[], exclude=[],
                 link=default_view_link):
        self.base = base_path
        self.root = spack.util.path.canonicalize_path(root)
        self.projections = projections
        self.select = select
        self.select_fn = lambda x: any(x.satisfies(s) for s in self.select)
        self.exclude = exclude
        self.exclude_fn = lambda x: not any(x.satisfies(e)
                                            for e in self.exclude)
        self.link = link

    def __eq__(self, other):
        return all([self.root == other.root,
                    self.projections == other.projections,
                    self.select == other.select,
                    self.exclude == other.exclude,
                    self.link == other.link])

    def to_dict(self):
        ret = {'root': self.root}
        if self.projections:
            ret['projections'] = self.projections
        if self.select:
            ret['select'] = self.select
        if self.exclude:
            ret['exclude'] = self.exclude
        if self.link != default_view_link:
            ret['link'] = self.link
        return ret

    @staticmethod
    def from_dict(base_path, d):
        return ViewDescriptor(base_path,
                              d['root'],
                              d.get('projections', {}),
                              d.get('select', []),
                              d.get('exclude', []),
                              d.get('link', default_view_link))

    def view(self):
        root = self.root
        if not os.path.isabs(root):
            root = os.path.normpath(os.path.join(self.base, self.root))
        return YamlFilesystemView(root, spack.store.layout,
                                  ignore_conflicts=True,
                                  projections=self.projections)

    def __contains__(self, spec):
        """Is the spec described by the view descriptor

        Note: This does not claim the spec is already linked in the view.
        It merely checks that the spec is selected if a select operation is
        specified and is not excluded if an exclude operator is specified.
        """
        if self.select:
            if not self.select_fn(spec):
                return False

        if self.exclude:
            if not self.exclude_fn(spec):
                return False

        return True

    def regenerate(self, all_specs, roots):
        specs_for_view = []
        specs = all_specs if self.link == 'all' else roots
        for spec in specs:
            # The view does not store build deps, so if we want it to
            # recognize environment specs (which do store build deps),
            # then they need to be stripped.
            if spec.concrete:  # Do not link unconcretized roots
                # We preserve _hash _normal to avoid recomputing DAG
                # hashes (DAG hashes don't consider build deps)
                spec_copy = spec.copy(deps=('link', 'run'))
                spec_copy._hash = spec._hash
                spec_copy._normal = spec._normal
                specs_for_view.append(spec_copy)

        # regeneration queries the database quite a bit; this read
        # transaction ensures that we don't repeatedly lock/unlock.
        with spack.store.db.read_transaction():
            installed_specs_for_view = set(
                s for s in specs_for_view if s in self and s.package.installed)

            # To ensure there are no conflicts with packages being installed
            # that cannot be resolved or have repos that have been removed
            # we always regenerate the view from scratch. We must first make
            # sure the root directory exists for the very first time though.
            root = os.path.normpath(
                self.root if os.path.isabs(self.root) else os.path.join(
                    self.base, self.root)
            )
            fs.mkdirp(root)

            # The tempdir for the directory transaction must be in the same
            # filesystem mount as the view for symlinks to work. Provide
            # dirname(root) as the tempdir for the
            # replace_directory_transaction because it must be on the same
            # filesystem mount as the view itself. Otherwise it may be
            # impossible to construct the view in the tempdir even when it can
            # be constructed in-place.
            with fs.replace_directory_transaction(root, os.path.dirname(root)):
                view = self.view()

                view.clean()
                specs_in_view = set(view.get_all_specs())
                tty.msg("Updating view at {0}".format(self.root))

                rm_specs = specs_in_view - installed_specs_for_view
                add_specs = installed_specs_for_view - specs_in_view

                # pass all_specs in, as it's expensive to read all the
                # spec.yaml files twice.
                view.remove_specs(*rm_specs, with_dependents=False,
                                  all_specs=specs_in_view)
                view.add_specs(*add_specs, with_dependencies=False)


class Environment(object):
    def __init__(self, path, init_file=None, with_view=None, keep_relative=False):
        """Create a new environment.

        The environment can be optionally initialized with either a
        spack.yaml or spack.lock file.

        Arguments:
            path (str): path to the root directory of this environment
            init_file (str or file object): filename or file object to
                initialize the environment
            with_view (str or bool): whether a view should be maintained for
                the environment. If the value is a string, it specifies the
                path to the view.
            keep_relative (bool): if True, develop paths are copied verbatim
                into the new environment file, otherwise they are made absolute
                when the environment path is different from init_file's
                directory.
        """
        self.path = os.path.abspath(path)

        self.txlock = lk.Lock(self._transaction_lock_path)

        # This attribute will be set properly from configuration
        # during concretization
        self.concretization = None
        self.clear()

        if init_file:
            # If we are creating the environment from an init file, we don't
            # need to lock, because there are no Spack operations that alter
            # the init file.
            with fs.open_if_filename(init_file) as f:
                if hasattr(f, 'name') and f.name.endswith('.lock'):
                    self._read_manifest(default_manifest_yaml)
                    self._read_lockfile(f)
                    self._set_user_specs_from_lockfile()
                else:
                    self._read_manifest(f, raw_yaml=default_manifest_yaml)

                # Rewrite relative develop paths when initializing a new
                # environment in a different location from the spack.yaml file.
                if not keep_relative and hasattr(f, 'name') and \
                   f.name.endswith('.yaml'):
                    init_file_dir = os.path.abspath(os.path.dirname(f.name))
                    self._rewrite_relative_paths_on_relocation(init_file_dir)
        else:
            with lk.ReadTransaction(self.txlock):
                self._read()

        if with_view is False:
            self.views = {}
        elif with_view is True:
            self.views = {
                default_view_name: ViewDescriptor(self.path,
                                                  self.view_path_default)}
        elif isinstance(with_view, six.string_types):
            self.views = {default_view_name: ViewDescriptor(self.path,
                                                            with_view)}
        # If with_view is None, then defer to the view settings determined by
        # the manifest file

    def _rewrite_relative_paths_on_relocation(self, init_file_dir):
        """When initializing the environment from a manifest file and we plan
           to store the environment in a different directory, we have to rewrite
           relative paths to absolute ones."""
        if init_file_dir == self.path:
            return

        for name, entry in self.dev_specs.items():
            dev_path = entry['path']
            expanded_path = os.path.normpath(os.path.join(
                init_file_dir, entry['path']))

            # Skip if the expanded path is the same (e.g. when absolute)
            if dev_path == expanded_path:
                continue

            tty.debug("Expanding develop path for {0} to {1}".format(
                name, expanded_path))

            self.dev_specs[name]['path'] = expanded_path

    def _re_read(self):
        """Reinitialize the environment object if it has been written (this
           may not be true if the environment was just created in this running
           instance of Spack)."""
        if not os.path.exists(self.manifest_path):
            return

        self.clear()
        self._read()

    def _read(self):
        default_manifest = not os.path.exists(self.manifest_path)
        if default_manifest:
            # No manifest, use default yaml
            self._read_manifest(default_manifest_yaml)
        else:
            with open(self.manifest_path) as f:
                self._read_manifest(f)

        if os.path.exists(self.lock_path):
            with open(self.lock_path) as f:
                read_lock_version = self._read_lockfile(f)
            if default_manifest:
                # No manifest, set user specs from lockfile
                self._set_user_specs_from_lockfile()

            if read_lock_version == 1:
                tty.debug(
                    "Storing backup of old lockfile {0} at {1}".format(
                        self.lock_path, self._lock_backup_v1_path))
                shutil.copy(self.lock_path, self._lock_backup_v1_path)

    def write_transaction(self):
        """Get a write lock context manager for use in a `with` block."""
        return lk.WriteTransaction(self.txlock, acquire=self._re_read)

    def _read_manifest(self, f, raw_yaml=None):
        """Read manifest file and set up user specs."""
        if raw_yaml:
            _, self.yaml = _read_yaml(f)
            self.raw_yaml, _ = _read_yaml(raw_yaml)
        else:
            self.raw_yaml, self.yaml = _read_yaml(f)

        self.spec_lists = OrderedDict()

        for item in config_dict(self.yaml).get('definitions', []):
            entry = copy.deepcopy(item)
            when = _eval_conditional(entry.pop('when', 'True'))
            assert len(entry) == 1
            if when:
                name, spec_list = next(iter(entry.items()))
                user_specs = SpecList(name, spec_list, self.spec_lists.copy())
                if name in self.spec_lists:
                    self.spec_lists[name].extend(user_specs)
                else:
                    self.spec_lists[name] = user_specs

        spec_list = config_dict(self.yaml).get(user_speclist_name, [])
        user_specs = SpecList(user_speclist_name, [s for s in spec_list if s],
                              self.spec_lists.copy())
        self.spec_lists[user_speclist_name] = user_specs

        enable_view = config_dict(self.yaml).get('view')
        # enable_view can be boolean, string, or None
        if enable_view is True or enable_view is None:
            self.views = {
                default_view_name: ViewDescriptor(self.path,
                                                  self.view_path_default)}
        elif isinstance(enable_view, six.string_types):
            self.views = {default_view_name: ViewDescriptor(self.path,
                                                            enable_view)}
        elif enable_view:
            path = self.path
            self.views = dict((name, ViewDescriptor.from_dict(path, values))
                              for name, values in enable_view.items())
        else:
            self.views = {}
        # Retrieve the current concretization strategy
        configuration = config_dict(self.yaml)
        # default concretization to separately
        self.concretization = configuration.get('concretization', 'separately')

        # Retrieve dev-build packages:
        self.dev_specs = configuration.get('develop', {})
        for name, entry in self.dev_specs.items():
            # spec must include a concrete version
            assert Spec(entry['spec']).version.concrete
            # default path is the spec name
            if 'path' not in entry:
                self.dev_specs[name]['path'] = name

    @property
    def user_specs(self):
        return self.spec_lists[user_speclist_name]

    def _set_user_specs_from_lockfile(self):
        """Copy user_specs from a read-in lockfile."""
        self.spec_lists = {
            user_speclist_name: SpecList(
                user_speclist_name,
                [str(s) for s in self.concretized_user_specs]
            )
        }

    def clear(self):
        self.spec_lists = {user_speclist_name: SpecList()}  # specs from yaml
        self.dev_specs = {}               # dev-build specs from yaml
        self.concretized_user_specs = []  # user specs from last concretize
        self.concretized_order = []       # roots of last concretize, in order
        self.specs_by_hash = {}           # concretized specs by hash
        self.new_specs = []               # write packages for these on write()
        self._repo = None                 # RepoPath for this env (memoized)
        self._previous_active = None      # previously active environment

    @property
    def internal(self):
        """Whether this environment is managed by Spack."""
        return self.path.startswith(env_path)

    @property
    def name(self):
        """Human-readable representation of the environment.

        This is the path for directory environments, and just the name
        for named environments.
        """
        if self.internal:
            return os.path.basename(self.path)
        else:
            return self.path

    @property
    def active(self):
        """True if this environment is currently active."""
        return _active_environment and self.path == _active_environment.path

    @property
    def manifest_path(self):
        """Path to spack.yaml file in this environment."""
        return os.path.join(self.path, manifest_name)

    @property
    def _transaction_lock_path(self):
        """The location of the lock file used to synchronize multiple
        processes updating the same environment.
        """
        return os.path.join(self.env_subdir_path, 'transaction_lock')

    @property
    def lock_path(self):
        """Path to spack.lock file in this environment."""
        return os.path.join(self.path, lockfile_name)

    @property
    def _lock_backup_v1_path(self):
        """Path to backup of v1 lockfile before conversion to v2"""
        return self.lock_path + '.backup.v1'

    @property
    def env_subdir_path(self):
        """Path to directory where the env stores repos, logs, views."""
        return os.path.join(self.path, env_subdir_name)

    @property
    def repos_path(self):
        return os.path.join(self.path, env_subdir_name, 'repos')

    @property
    def log_path(self):
        return os.path.join(self.path, env_subdir_name, 'logs')

    @property
    def view_path_default(self):
        # default path for environment views
        return os.path.join(self.env_subdir_path, 'view')

    @property
    def repo(self):
        if self._repo is None:
            self._repo = make_repo_path(self.repos_path)
        return self._repo

    def included_config_scopes(self):
        """List of included configuration scopes from the environment.

        Scopes are listed in the YAML file in order from highest to
        lowest precedence, so configuration from earlier scope will take
        precedence over later ones.

        This routine returns them in the order they should be pushed onto
        the internal scope stack (so, in reverse, from lowest to highest).
        """
        scopes = []

        # load config scopes added via 'include:', in reverse so that
        # highest-precedence scopes are last.
        includes = config_dict(self.yaml).get('include', [])
        missing = []
        for i, config_path in enumerate(reversed(includes)):
            # allow paths to contain spack config/environment variables, etc.
            config_path = substitute_path_variables(config_path)

            # treat relative paths as relative to the environment
            if not os.path.isabs(config_path):
                config_path = os.path.join(self.path, config_path)
                config_path = os.path.normpath(os.path.realpath(config_path))

            if os.path.isdir(config_path):
                # directories are treated as regular ConfigScopes
                config_name = 'env:%s:%s' % (
                    self.name, os.path.basename(config_path))
                scope = spack.config.ConfigScope(config_name, config_path)
            elif os.path.exists(config_path):
                # files are assumed to be SingleFileScopes
                config_name = 'env:%s:%s' % (self.name, config_path)
                scope = spack.config.SingleFileScope(
                    config_name, config_path, spack.schema.merged.schema)
            else:
                missing.append(config_path)
                continue

            scopes.append(scope)

        if missing:
            msg = 'Detected {0} missing include path(s):'.format(len(missing))
            msg += '\n   {0}'.format('\n   '.join(missing))
            tty.die('{0}\nPlease correct and try again.'.format(msg))

        return scopes

    def env_file_config_scope_name(self):
        """Name of the config scope of this environment's manifest file."""
        return 'env:%s' % self.name

    def env_file_config_scope(self):
        """Get the configuration scope for the environment's manifest file."""
        config_name = self.env_file_config_scope_name()
        return spack.config.SingleFileScope(
            config_name,
            self.manifest_path,
            spack.schema.env.schema,
            [spack.config.first_existing(self.raw_yaml,
                                         spack.schema.env.keys)])

    def config_scopes(self):
        """A list of all configuration scopes for this environment."""
        return self.included_config_scopes() + [self.env_file_config_scope()]

    def destroy(self):
        """Remove this environment from Spack entirely."""
        shutil.rmtree(self.path)

    def update_stale_references(self, from_list=None):
        """Iterate over spec lists updating references."""
        if not from_list:
            from_list = next(iter(self.spec_lists.keys()))
        index = list(self.spec_lists.keys()).index(from_list)

        # spec_lists is an OrderedDict, all list entries after the modified
        # list may refer to the modified list. Update stale references
        for i, (name, speclist) in enumerate(
            list(self.spec_lists.items())[index + 1:], index + 1
        ):
            new_reference = dict((n, self.spec_lists[n])
                                 for n in list(self.spec_lists.keys())[:i])
            speclist.update_reference(new_reference)

    def add(self, user_spec, list_name=user_speclist_name):
        """Add a single user_spec (non-concretized) to the Environment

        Returns:
            (bool): True if the spec was added, False if it was already
                present and did not need to be added

        """
        spec = Spec(user_spec)

        if list_name not in self.spec_lists:
            raise SpackEnvironmentError(
                'No list %s exists in environment %s' % (list_name, self.name)
            )

        if list_name == user_speclist_name:
            if not spec.name:
                raise SpackEnvironmentError(
                    'cannot add anonymous specs to an environment!')
            elif not spack.repo.path.exists(spec.name):
                virtuals = spack.repo.path.provider_index.providers.keys()
                if spec.name not in virtuals:
                    msg = 'no such package: %s' % spec.name
                    raise SpackEnvironmentError(msg)

        list_to_change = self.spec_lists[list_name]
        existing = str(spec) in list_to_change.yaml_list
        if not existing:
            list_to_change.add(str(spec))
            self.update_stale_references(list_name)

        return bool(not existing)

    def remove(self, query_spec, list_name=user_speclist_name, force=False):
        """Remove specs from an environment that match a query_spec"""
        query_spec = Spec(query_spec)

        list_to_change = self.spec_lists[list_name]
        matches = []

        if not query_spec.concrete:
            matches = [s for s in list_to_change if s.satisfies(query_spec)]

        if not matches:
            # concrete specs match against concrete specs in the env
            # by *dag hash*, not build hash.
            dag_hashes_in_order = [
                self.specs_by_hash[build_hash].dag_hash()
                for build_hash in self.concretized_order
            ]

            specs_hashes = zip(
                self.concretized_user_specs, dag_hashes_in_order
            )

            matches = [
                s for s, h in specs_hashes
                if query_spec.dag_hash() == h
            ]

        if not matches:
            raise SpackEnvironmentError(
                "Not found: {0}".format(query_spec))

        old_specs = set(self.user_specs)
        new_specs = set()
        for spec in matches:
            if spec in list_to_change:
                try:
                    list_to_change.remove(spec)
                    self.update_stale_references(list_name)
                    new_specs = set(self.user_specs)
                except spack.spec_list.SpecListError:
                    # define new specs list
                    new_specs = set(self.user_specs)
                    msg = "Spec '%s' is part of a spec matrix and " % spec
                    msg += "cannot be removed from list '%s'." % list_to_change
                    if force:
                        msg += " It will be removed from the concrete specs."
                        # Mock new specs so we can remove this spec from
                        # concrete spec lists
                        new_specs.remove(spec)
                    tty.warn(msg)

        # If force, update stale concretized specs
        for spec in old_specs - new_specs:
            if force and spec in self.concretized_user_specs:
                i = self.concretized_user_specs.index(spec)
                del self.concretized_user_specs[i]

                dag_hash = self.concretized_order[i]
                del self.concretized_order[i]
                del self.specs_by_hash[dag_hash]

    def develop(self, spec, path, clone=False):
        """Add dev-build info for package

        Args:
            spec (Spec): Set constraints on development specs. Must include a
                concrete version.
            path (string): Path to find code for developer builds. Relative
                paths will be resolved relative to the environment.
            clone (bool, default False): Clone the package code to the path.
                If clone is False Spack will assume the code is already present
                at ``path``.

        Return:
            (bool): True iff the environment was changed.
        """
        spec = spec.copy()  # defensive copy since we access cached attributes

        if not spec.versions.concrete:
            raise SpackEnvironmentError(
                'Cannot develop spec %s without a concrete version' % spec)

        for name, entry in self.dev_specs.items():
            if name == spec.name:
                e_spec = Spec(entry['spec'])
                e_path = entry['path']

                if e_spec == spec:
                    if path == e_path:
                        tty.msg("Spec %s already configured for development" %
                                spec)
                        return False
                    else:
                        tty.msg("Updating development path for spec %s" % spec)
                        break
                else:
                    msg = "Updating development spec for package "
                    msg += "%s with path %s" % (spec.name, path)
                    tty.msg(msg)
                    break
        else:
            tty.msg("Configuring spec %s for development at path %s" %
                    (spec, path))

        if clone:
            # "steal" the source code via staging API
            abspath = os.path.normpath(os.path.join(self.path, path))

            stage = spec.package.stage
            stage.steal_source(abspath)

        # If it wasn't already in the list, append it
        self.dev_specs[spec.name] = {'path': path, 'spec': str(spec)}
        return True

    def undevelop(self, spec):
        """Remove develop info for abstract spec ``spec``.

        returns True on success, False if no entry existed."""
        spec = Spec(spec)  # In case it's a spec object
        if spec.name in self.dev_specs:
            del self.dev_specs[spec.name]
            return True
        return False

    def concretize(self, force=False, tests=False):
        """Concretize user_specs in this environment.

        Only concretizes specs that haven't been concretized yet unless
        force is ``True``.

        This only modifies the environment in memory. ``write()`` will
        write out a lockfile containing concretized specs.

        Arguments:
            force (bool): re-concretize ALL specs, even those that were
               already concretized
            tests (bool or list or set): False to run no tests, True to test
                all packages, or a list of package names to run tests for some

        Returns:
            List of specs that have been concretized. Each entry is a tuple of
            the user spec and the corresponding concretized spec.
        """
        if force:
            # Clear previously concretized specs
            self.concretized_user_specs = []
            self.concretized_order = []
            self.specs_by_hash = {}

        # Pick the right concretization strategy
        if self.concretization == 'together':
            return self._concretize_together(tests=tests)
        if self.concretization == 'separately':
            return self._concretize_separately(tests=tests)

        msg = 'concretization strategy not implemented [{0}]'
        raise SpackEnvironmentError(msg.format(self.concretization))

    def _concretize_together(self, tests=False):
        """Concretization strategy that concretizes all the specs
        in the same DAG.
        """
        # Exit early if the set of concretized specs is the set of user specs
        user_specs_did_not_change = not bool(
            set(self.user_specs) - set(self.concretized_user_specs)
        )
        if user_specs_did_not_change:
            return []

        # Check that user specs don't have duplicate packages
        counter = collections.defaultdict(int)
        for user_spec in self.user_specs:
            counter[user_spec.name] += 1

        duplicates = []
        for name, count in counter.items():
            if count > 1:
                duplicates.append(name)

        if duplicates:
            msg = ('environment that are configured to concretize specs'
                   ' together cannot contain more than one spec for each'
                   ' package [{0}]'.format(', '.join(duplicates)))
            raise SpackEnvironmentError(msg)

        # Proceed with concretization
        self.concretized_user_specs = []
        self.concretized_order = []
        self.specs_by_hash = {}

        concrete_specs = spack.concretize.concretize_specs_together(
            *self.user_specs, tests=tests)
        concretized_specs = [x for x in zip(self.user_specs, concrete_specs)]
        for abstract, concrete in concretized_specs:
            self._add_concrete_spec(abstract, concrete)
        return concretized_specs

    def _concretize_separately(self, tests=False):
        """Concretization strategy that concretizes separately one
        user spec after the other.
        """
        # keep any concretized specs whose user specs are still in the manifest
        old_concretized_user_specs = self.concretized_user_specs
        old_concretized_order = self.concretized_order
        old_specs_by_hash = self.specs_by_hash

        self.concretized_user_specs = []
        self.concretized_order = []
        self.specs_by_hash = {}

        for s, h in zip(old_concretized_user_specs, old_concretized_order):
            if s in self.user_specs:
                concrete = old_specs_by_hash[h]
                self._add_concrete_spec(s, concrete, new=False)

        # Concretize any new user specs that we haven't concretized yet
        concretized_specs = []
        for uspec, uspec_constraints in zip(
                self.user_specs, self.user_specs.specs_as_constraints):
            if uspec not in old_concretized_user_specs:
                concrete = _concretize_from_constraints(uspec_constraints, tests=tests)
                self._add_concrete_spec(uspec, concrete)
                concretized_specs.append((uspec, concrete))
        return concretized_specs

    def concretize_and_add(self, user_spec, concrete_spec=None, tests=False):
        """Concretize and add a single spec to the environment.

        Concretize the provided ``user_spec`` and add it along with the
        concretized result to the environment. If the given ``user_spec`` was
        already present in the environment, this does not add a duplicate.
        The concretized spec will be added unless the ``user_spec`` was
        already present and an associated concrete spec was already present.

        Args:
            concrete_spec: if provided, then it is assumed that it is the
                result of concretizing the provided ``user_spec``
        """
        if self.concretization == 'together':
            msg = 'cannot install a single spec in an environment that is ' \
                  'configured to be concretized together. Run instead:\n\n' \
                  '    $ spack add <spec>\n' \
                  '    $ spack install\n'
            raise SpackEnvironmentError(msg)

        spec = Spec(user_spec)

        if self.add(spec):
            concrete = concrete_spec or spec.concretized(tests=tests)
            self._add_concrete_spec(spec, concrete)
        else:
            # spec might be in the user_specs, but not installed.
            # TODO: Redo name-based comparison for old style envs
            spec = next(
                s for s in self.user_specs if s.satisfies(user_spec)
            )
            concrete = self.specs_by_hash.get(spec.build_hash())
            if not concrete:
                concrete = spec.concretized(tests=tests)
                self._add_concrete_spec(spec, concrete)

        return concrete

    @property
    def default_view(self):
        if not self.views:
            raise SpackEnvironmentError(
                "{0} does not have a view enabled".format(self.name))

        if default_view_name not in self.views:
            raise SpackEnvironmentError(
                "{0} does not have a default view enabled".format(self.name))

        return self.views[default_view_name]

    def update_default_view(self, viewpath):
        name = default_view_name
        if name in self.views and self.default_view.root != viewpath:
            shutil.rmtree(self.default_view.root)

        if viewpath:
            if name in self.views:
                self.default_view.root = viewpath
            else:
                self.views[name] = ViewDescriptor(self.path, viewpath)
        else:
            self.views.pop(name, None)

    def regenerate_views(self):
        if not self.views:
            tty.debug("Skip view update, this environment does not"
                      " maintain a view")
            return

        specs = self._get_environment_specs()
        for view in self.views.values():
            view.regenerate(specs, self.roots())

    def check_views(self):
        """Checks if the environments default view can be activated."""
        try:
            # This is effectively a no-op, but it touches all packages in the
            # default view if they are installed.
            for view_name, view in self.views.items():
                for _, spec in self.concretized_specs():
                    if spec in view and spec.package.installed:
                        tty.debug(
                            'Spec %s in view %s' % (spec.name, view_name))
        except (spack.repo.UnknownPackageError,
                spack.repo.UnknownNamespaceError) as e:
            tty.warn(e)
            tty.warn(
                'Environment %s includes out of date packages or repos. '
                'Loading the environment view will require reconcretization.'
                % self.name)

    def _env_modifications_for_default_view(self, reverse=False):
        all_mods = spack.util.environment.EnvironmentModifications()

        errors = []
        for _, spec in self.concretized_specs():
            if spec in self.default_view and spec.package.installed:
                try:
                    mods = uenv.environment_modifications_for_spec(
                        spec, self.default_view)
                except Exception as e:
                    msg = ("couldn't get environment settings for %s"
                           % spec.format("{name}@{version} /{hash:7}"))
                    errors.append((msg, str(e)))
                    continue

                all_mods.extend(mods.reversed() if reverse else mods)

        return all_mods, errors

    def add_default_view_to_shell(self, shell):
        env_mod = spack.util.environment.EnvironmentModifications()

        if default_view_name not in self.views:
            # No default view to add to shell
            return env_mod.shell_modifications(shell)

        env_mod.extend(uenv.unconditional_environment_modifications(
            self.default_view))

        mods, errors = self._env_modifications_for_default_view()
        env_mod.extend(mods)
        if errors:
            for err in errors:
                tty.warn(*err)

        # deduplicate paths from specs mapped to the same location
        for env_var in env_mod.group_by_name():
            env_mod.prune_duplicate_paths(env_var)

        return env_mod.shell_modifications(shell)

    def rm_default_view_from_shell(self, shell):
        env_mod = spack.util.environment.EnvironmentModifications()

        if default_view_name not in self.views:
            # No default view to add to shell
            return env_mod.shell_modifications(shell)

        env_mod.extend(uenv.unconditional_environment_modifications(
            self.default_view).reversed())

        mods, _ = self._env_modifications_for_default_view(reverse=True)
        env_mod.extend(mods)

        return env_mod.shell_modifications(shell)

    def _add_concrete_spec(self, spec, concrete, new=True):
        """Called when a new concretized spec is added to the environment.

        This ensures that all internal data structures are kept in sync.

        Arguments:
            spec (Spec): user spec that resulted in the concrete spec
            concrete (Spec): spec concretized within this environment
            new (bool): whether to write this spec's package to the env
                repo on write()
        """
        assert concrete.concrete

        # when a spec is newly concretized, we need to make a note so
        # that we can write its package to the env repo on write()
        if new:
            self.new_specs.append(concrete)

        # update internal lists of specs
        self.concretized_user_specs.append(spec)

        h = concrete.build_hash()
        self.concretized_order.append(h)
        self.specs_by_hash[h] = concrete

    def _spec_needs_overwrite(self, spec):
        # Overwrite the install if it's a dev build (non-transitive)
        # and the code has been changed since the last install
        # or one of the dependencies has been reinstalled since
        # the last install

        # if it's not installed, we don't need to overwrite it
        if not spec.package.installed:
            return False

        # if spec and all deps aren't dev builds, we don't need to overwrite it
        if not any(spec.satisfies(c)
                   for c in ('dev_path=*', '^dev_path=*')):
            return False

        # if any dep needs overwrite, or any dep is missing and is a dev build
        # then overwrite this package
        if any(
            self._spec_needs_overwrite(dep) or
            ((not dep.package.installed) and dep.satisfies('dev_path=*'))
            for dep in spec.traverse(root=False)
        ):
            return True

        # if it's not a direct dev build and its dependencies haven't
        # changed, it hasn't changed.
        # We don't merely check satisfaction (spec.satisfies('dev_path=*')
        # because we need the value of the variant in the next block of code
        dev_path_var = spec.variants.get('dev_path', None)
        if not dev_path_var:
            return False

        # if it is a direct dev build, check whether the code changed
        # we already know it is installed
        _, record = spack.store.db.query_by_spec_hash(spec.dag_hash())
        mtime = fs.last_modification_time_recursive(dev_path_var.value)
        return mtime > record.installation_time

    def _get_overwrite_specs(self):
        ret = []
        for dag_hash in self.concretized_order:
            spec = self.specs_by_hash[dag_hash]
            ret.extend([d.dag_hash() for d in spec.traverse(root=True)
                        if self._spec_needs_overwrite(d)])

        return ret

    def _install_log_links(self, spec):
        if not spec.external:
            # Make sure log directory exists
            log_path = self.log_path
            fs.mkdirp(log_path)

            with fs.working_dir(self.path):
                # Link the resulting log file into logs dir
                build_log_link = os.path.join(
                    log_path, '%s-%s.log' % (spec.name, spec.dag_hash(7)))
                if os.path.lexists(build_log_link):
                    os.remove(build_log_link)
                os.symlink(spec.package.build_log_path, build_log_link)

    def uninstalled_specs(self):
        """Return a list of all uninstalled (and non-dev) specs."""
        # Do the installed check across all specs within a single
        # DB read transaction to reduce time spent in lock acquisition.
        uninstalled_specs = []
        with spack.store.db.read_transaction():
            for concretized_hash in self.concretized_order:
                spec = self.specs_by_hash[concretized_hash]
                if not spec.package.installed or (
                        spec.satisfies('dev_path=*') or
                        spec.satisfies('^dev_path=*')
                ):
                    uninstalled_specs.append(spec)
        return uninstalled_specs

    def install_all(self, args=None, **install_args):
        """Install all concretized specs in an environment.

        Note: this does not regenerate the views for the environment;
        that needs to be done separately with a call to write().

        Args:
            args (Namespace): argparse namespace with command arguments
            install_args (dict): keyword install arguments
        """
        from spack.installer import PackageInstaller
        tty.debug('Assessing installation status of environment packages')
        # If "spack install" is invoked repeatedly for a large environment
        # where all specs are already installed, the operation can take
        # a large amount of time due to repeatedly acquiring and releasing
        # locks, this does an initial check across all specs within a single
        # DB read transaction to reduce time spent in this case.
        specs_to_install = self.uninstalled_specs()

        if not specs_to_install:
            tty.msg('All of the packages are already installed')
            return

        tty.debug('Processing {0} uninstalled specs'
                  .format(len(specs_to_install)))

        install_args['overwrite'] = install_args.get(
            'overwrite', []) + self._get_overwrite_specs()

        installs = []
        for spec in specs_to_install:
            # Parse cli arguments and construct a dictionary
            # that will be passed to the package installer
            kwargs = dict()
            if install_args:
                kwargs.update(install_args)
            if args:
                spack.cmd.install.update_kwargs_from_args(args, kwargs)

            installs.append((spec.package, kwargs))

        try:
            builder = PackageInstaller(installs)
            builder.install()
        finally:
            # Ensure links are set appropriately
            for spec in specs_to_install:
                if spec.package.installed:
                    try:
                        self._install_log_links(spec)
                    except OSError as e:
                        tty.warn('Could not install log links for {0}: {1}'
                                 .format(spec.name, str(e)))

            with self.write_transaction():
                self.regenerate_views()

    def all_specs(self):
        """Return all specs, even those a user spec would shadow."""
        all_specs = set()
        for h in self.concretized_order:
            all_specs.update(self.specs_by_hash[h].traverse())

        return sorted(all_specs)

    def all_hashes(self):
        """Return hashes of all specs.

        Note these hashes exclude build dependencies."""
        return list(set(s.dag_hash() for s in self.all_specs()))

    def roots(self):
        """Specs explicitly requested by the user *in this environment*.

        Yields both added and installed specs that have user specs in
        `spack.yaml`.
        """
        concretized = dict(self.concretized_specs())
        for spec in self.user_specs:
            concrete = concretized.get(spec)
            yield concrete if concrete else spec

    def added_specs(self):
        """Specs that are not yet installed.

        Yields the user spec for non-concretized specs, and the concrete
        spec for already concretized but not yet installed specs.
        """
        # use a transaction to avoid overhead of repeated calls
        # to `package.installed`
        with spack.store.db.read_transaction():
            concretized = dict(self.concretized_specs())
            for spec in self.user_specs:
                concrete = concretized.get(spec)
                if not concrete:
                    yield spec
                elif not concrete.package.installed:
                    yield concrete

    def concretized_specs(self):
        """Tuples of (user spec, concrete spec) for all concrete specs."""
        for s, h in zip(self.concretized_user_specs, self.concretized_order):
            yield (s, self.specs_by_hash[h])

    def matching_spec(self, spec):
        """
        Given a spec (likely not concretized), find a matching concretized
        spec in the environment.

        The matching spec does not have to be installed in the environment,
        but must be concrete (specs added with `spack add` without an
        intervening `spack concretize` will not be matched).

        If there is a single root spec that matches the provided spec or a
        single dependency spec that matches the provided spec, then the
        concretized instance of that spec will be returned.

        If multiple root specs match the provided spec, or no root specs match
        and multiple dependency specs match, then this raises an error
        and reports all matching specs.
        """
        # Root specs will be keyed by concrete spec, value abstract
        # Dependency-only specs will have value None
        matches = {}

        for user_spec, concretized_user_spec in self.concretized_specs():
            if concretized_user_spec.satisfies(spec):
                matches[concretized_user_spec] = user_spec
            for dep_spec in concretized_user_spec.traverse(root=False):
                if dep_spec.satisfies(spec):
                    # Don't overwrite the abstract spec if present
                    # If not present already, set to None
                    matches[dep_spec] = matches.get(dep_spec, None)

        if not matches:
            return None
        elif len(matches) == 1:
            return list(matches.keys())[0]

        root_matches = dict((concrete, abstract)
                            for concrete, abstract in matches.items()
                            if abstract)

        if len(root_matches) == 1:
            return root_matches[0][1]

        # More than one spec matched, and either multiple roots matched or
        # none of the matches were roots
        # If multiple root specs match, it is assumed that the abstract
        # spec will most-succinctly summarize the difference between them
        # (and the user can enter one of these to disambiguate)
        match_strings = []
        fmt_str = '{hash:7}  ' + spack.spec.default_format
        for concrete, abstract in matches.items():
            if abstract:
                s = 'Root spec %s\n  %s' % (abstract, concrete.format(fmt_str))
            else:
                s = 'Dependency spec\n  %s' % concrete.format(fmt_str)
            match_strings.append(s)
        matches_str = '\n'.join(match_strings)

        msg = ("{0} matches multiple specs in the environment {1}: \n"
               "{2}".format(str(spec), self.name, matches_str))
        raise SpackEnvironmentError(msg)

    def removed_specs(self):
        """Tuples of (user spec, concrete spec) for all specs that will be
           removed on nexg concretize."""
        needed = set()
        for s, c in self.concretized_specs():
            if s in self.user_specs:
                for d in c.traverse():
                    needed.add(d)

        for s, c in self.concretized_specs():
            for d in c.traverse():
                if d not in needed:
                    yield d

    def _get_environment_specs(self, recurse_dependencies=True):
        """Returns the specs of all the packages in an environment.

        If these specs appear under different user_specs, only one copy
        is added to the list returned.
        """
        spec_list = list()

        for spec_hash in self.concretized_order:
            spec = self.specs_by_hash[spec_hash]

            specs = (spec.traverse(deptype=('link', 'run'))
                     if recurse_dependencies else (spec,))

            spec_list.extend(specs)

        return spec_list

    def _to_lockfile_dict(self):
        """Create a dictionary to store a lockfile for this environment."""
        concrete_specs = {}
        for spec in self.specs_by_hash.values():
            for s in spec.traverse():
                dag_hash_all = s.build_hash()
                if dag_hash_all not in concrete_specs:
                    spec_dict = s.to_node_dict(hash=ht.build_hash)
                    spec_dict[s.name]['hash'] = s.dag_hash()
                    concrete_specs[dag_hash_all] = spec_dict

        hash_spec_list = zip(
            self.concretized_order, self.concretized_user_specs)

        # this is the lockfile we'll write out
        data = {
            # metadata about the format
            '_meta': {
                'file-type': 'spack-lockfile',
                'lockfile-version': lockfile_format_version,
            },

            # users specs + hashes are the 'roots' of the environment
            'roots': [{
                'hash': h,
                'spec': str(s)
            } for h, s in hash_spec_list],

            # Concrete specs by hash, including dependencies
            'concrete_specs': concrete_specs,
        }

        return data

    def _read_lockfile(self, file_or_json):
        """Read a lockfile from a file or from a raw string."""
        lockfile_dict = sjson.load(file_or_json)
        self._read_lockfile_dict(lockfile_dict)
        return lockfile_dict['_meta']['lockfile-version']

    def _read_lockfile_dict(self, d):
        """Read a lockfile dictionary into this environment."""
        roots = d['roots']
        self.concretized_user_specs = [Spec(r['spec']) for r in roots]
        self.concretized_order = [r['hash'] for r in roots]

        json_specs_by_hash = d['concrete_specs']
        root_hashes = set(self.concretized_order)

        specs_by_hash = {}
        for dag_hash, node_dict in json_specs_by_hash.items():
            specs_by_hash[dag_hash] = Spec.from_node_dict(node_dict)

        for dag_hash, node_dict in json_specs_by_hash.items():
            for dep_name, dep_hash, deptypes in (
                    Spec.dependencies_from_node_dict(node_dict)):
                specs_by_hash[dag_hash]._add_dependency(
                    specs_by_hash[dep_hash], deptypes)

        # If we are reading an older lockfile format (which uses dag hashes
        # that exclude build deps), we use this to convert the old
        # concretized_order to the full hashes (preserving the order)
        old_hash_to_new = {}
        self.specs_by_hash = {}
        for _, spec in specs_by_hash.items():
            dag_hash = spec.dag_hash()
            build_hash = spec.build_hash()
            if dag_hash in root_hashes:
                old_hash_to_new[dag_hash] = build_hash

            if (dag_hash in root_hashes or build_hash in root_hashes):
                self.specs_by_hash[build_hash] = spec

        if old_hash_to_new:
            # Replace any older hashes in concretized_order with hashes
            # that include build deps
            self.concretized_order = [
                old_hash_to_new.get(h, h) for h in self.concretized_order]

    def write(self, regenerate_views=True):
        """Writes an in-memory environment to its location on disk.

        Write out package files for each newly concretized spec.  Also
        regenerate any views associated with the environment, if
        regenerate_views is True.

        Arguments:
            regenerate_views (bool): regenerate views as well as
                writing if True.

        """
        # Intercept environment not using the latest schema format and prevent
        # them from being modified
        manifest_exists = os.path.exists(self.manifest_path)
        if manifest_exists and not is_latest_format(self.manifest_path):
            msg = ('The environment "{0}" needs to be written to disk, but '
                   'is currently using a deprecated format. Please update it '
                   'using:\n\n'
                   '\tspack env update {0}\n\n'
                   'Note that previous versions of Spack will not be able to '
                   'use the updated configuration.')
            raise RuntimeError(msg.format(self.name))

        # ensure path in var/spack/environments
        fs.mkdirp(self.path)

        yaml_dict = config_dict(self.yaml)
        raw_yaml_dict = config_dict(self.raw_yaml)

        if self.specs_by_hash:
            # ensure the prefix/.env directory exists
            fs.mkdirp(self.env_subdir_path)

            for spec in self.new_specs:
                for dep in spec.traverse():
                    if not dep.concrete:
                        raise ValueError('specs passed to environment.write() '
                                         'must be concrete!')

                    root = os.path.join(self.repos_path, dep.namespace)
                    repo = spack.repo.create_or_construct(root, dep.namespace)
                    pkg_dir = repo.dirname_for_package_name(dep.name)

                    fs.mkdirp(pkg_dir)
                    spack.repo.path.dump_provenance(dep, pkg_dir)
            self.new_specs = []

            # write the lock file last
            with fs.write_tmp_and_move(self.lock_path) as f:
                sjson.dump(self._to_lockfile_dict(), stream=f)
            self._update_and_write_manifest(raw_yaml_dict, yaml_dict)
        else:
            with fs.safe_remove(self.lock_path):
                self._update_and_write_manifest(raw_yaml_dict, yaml_dict)

        # TODO: rethink where this needs to happen along with
        # writing. For some of the commands (like install, which write
        # concrete specs AND regen) this might as well be a separate
        # call.  But, having it here makes the views consistent witht the
        # concretized environment for most operations.  Which is the
        # special case?
        if regenerate_views:
            self.regenerate_views()

    def _update_and_write_manifest(self, raw_yaml_dict, yaml_dict):
        """Update YAML manifest for this environment based on changes to
        spec lists and views and write it.
        """
        # invalidate _repo cache
        self._repo = None
        # put any changes in the definitions in the YAML
        for name, speclist in self.spec_lists.items():
            if name == user_speclist_name:
                # The primary list is handled differently
                continue

            active_yaml_lists = [x for x in yaml_dict.get('definitions', [])
                                 if name in x and
                                 _eval_conditional(x.get('when', 'True'))]

            # Remove any specs in yaml that are not in internal representation
            for ayl in active_yaml_lists:
                # If it's not a string, it's a matrix. Those can't have changed
                # If it is a string that starts with '$', it's a reference.
                # Those also can't have changed.
                ayl[name][:] = [s for s in ayl.setdefault(name, [])
                                if (not isinstance(s, six.string_types)) or
                                s.startswith('$') or Spec(s) in speclist.specs]

            # Put the new specs into the first active list from the yaml
            new_specs = [entry for entry in speclist.yaml_list
                         if isinstance(entry, six.string_types) and
                         not any(entry in ayl[name]
                                 for ayl in active_yaml_lists)]
            list_for_new_specs = active_yaml_lists[0].setdefault(name, [])
            list_for_new_specs[:] = list_for_new_specs + new_specs
        # put the new user specs in the YAML.
        # This can be done directly because there can't be multiple definitions
        # nor when clauses for `specs` list.
        yaml_spec_list = yaml_dict.setdefault(user_speclist_name,
                                              [])
        yaml_spec_list[:] = self.user_specs.yaml_list
        # Construct YAML representation of view
        default_name = default_view_name
        if self.views and len(self.views) == 1 and default_name in self.views:
            path = self.default_view.root
            if self.default_view == ViewDescriptor(self.path,
                                                   self.view_path_default):
                view = True
            elif self.default_view == ViewDescriptor(self.path, path):
                view = path
            else:
                view = dict((name, view.to_dict())
                            for name, view in self.views.items())
        elif self.views:
            view = dict((name, view.to_dict())
                        for name, view in self.views.items())
        else:
            view = False
        yaml_dict['view'] = view

        if self.dev_specs:
            # Remove entries that are mirroring defaults
            write_dev_specs = copy.deepcopy(self.dev_specs)
            for name, entry in write_dev_specs.items():
                if entry['path'] == name:
                    del entry['path']
            yaml_dict['develop'] = write_dev_specs
        else:
            yaml_dict.pop('develop', None)

        # Remove yaml sections that are shadowing defaults
        # construct garbage path to ensure we don't find a manifest by accident
        with fs.temp_cwd() as env_dir:
            bare_env = Environment(env_dir, with_view=self.view_path_default)
            keys_present = list(yaml_dict.keys())
            for key in keys_present:
                if yaml_dict[key] == config_dict(bare_env.yaml).get(key, None):
                    if key not in raw_yaml_dict:
                        del yaml_dict[key]
        # if all that worked, write out the manifest file at the top level
        # (we used to check whether the yaml had changed and not write it out
        # if it hadn't. We can't do that anymore because it could be the only
        # thing that changed is the "override" attribute on a config dict,
        # which would not show up in even a string comparison between the two
        # keys).
        changed = not yaml_equivalent(self.yaml, self.raw_yaml)
        written = os.path.exists(self.manifest_path)
        if changed or not written:
            self.raw_yaml = copy.deepcopy(self.yaml)
            with fs.write_tmp_and_move(self.manifest_path) as f:
                _write_yaml(self.yaml, f)

    def __enter__(self):
        self._previous_active = _active_environment
        activate(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        deactivate()
        if self._previous_active:
            activate(self._previous_active)


def yaml_equivalent(first, second):
    """Returns whether two spack yaml items are equivalent, including overrides
    """
    if isinstance(first, dict):
        return isinstance(second, dict) and _equiv_dict(first, second)
    elif isinstance(first, list):
        return isinstance(second, list) and _equiv_list(first, second)
    else:  # it's a string
        return isinstance(second, six.string_types) and first == second


def _equiv_list(first, second):
    """Returns whether two spack yaml lists are equivalent, including overrides
    """
    if len(first) != len(second):
        return False
    return all(yaml_equivalent(f, s) for f, s in zip(first, second))


def _equiv_dict(first, second):
    """Returns whether two spack yaml dicts are equivalent, including overrides
    """
    if len(first) != len(second):
        return False
    same_values = all(yaml_equivalent(fv, sv)
                      for fv, sv in zip(first.values(), second.values()))
    same_keys_with_same_overrides = all(
        fk == sk and getattr(fk, 'override', False) == getattr(sk, 'override',
                                                               False)
        for fk, sk in zip(first.keys(), second.keys()))
    return same_values and same_keys_with_same_overrides


def display_specs(concretized_specs):
    """Displays the list of specs returned by `Environment.concretize()`.

    Args:
        concretized_specs (list): list of specs returned by
            `Environment.concretize()`
    """
    def _tree_to_display(spec):
        return spec.tree(
            recurse_dependencies=True,
            status_fn=spack.spec.Spec.install_status,
            hashlen=7, hashes=True)

    for user_spec, concrete_spec in concretized_specs:
        tty.msg('Concretized {0}'.format(user_spec))
        sys.stdout.write(_tree_to_display(concrete_spec))
        print('')


def _concretize_from_constraints(spec_constraints, tests=False):
    # Accept only valid constraints from list and concretize spec
    # Get the named spec even if out of order
    root_spec = [s for s in spec_constraints if s.name]
    if len(root_spec) != 1:
        m = 'The constraints %s are not a valid spec ' % spec_constraints
        m += 'concretization target. all specs must have a single name '
        m += 'constraint for concretization.'
        raise InvalidSpecConstraintError(m)
    spec_constraints.remove(root_spec[0])

    invalid_constraints = []
    while True:
        # Attach all anonymous constraints to one named spec
        s = root_spec[0].copy()
        for c in spec_constraints:
            if c not in invalid_constraints:
                s.constrain(c)
        try:
            return s.concretized(tests=tests)
        except spack.spec.InvalidDependencyError as e:
            invalid_deps_string = ['^' + d for d in e.invalid_deps]
            invalid_deps = [c for c in spec_constraints
                            if any(c.satisfies(invd, strict=True)
                                   for invd in invalid_deps_string)]
            if len(invalid_deps) != len(invalid_deps_string):
                raise e
            invalid_constraints.extend(invalid_deps)
        except UnknownVariantError as e:
            invalid_variants = e.unknown_variants
            inv_variant_constraints = [c for c in spec_constraints
                                       if any(name in c.variants
                                              for name in invalid_variants)]
            if len(inv_variant_constraints) != len(invalid_variants):
                raise e
            invalid_constraints.extend(inv_variant_constraints)


def make_repo_path(root):
    """Make a RepoPath from the repo subdirectories in an environment."""
    path = spack.repo.RepoPath()

    if os.path.isdir(root):
        for repo_root in os.listdir(root):
            repo_root = os.path.join(root, repo_root)

            if not os.path.isdir(repo_root):
                continue

            repo = spack.repo.Repo(repo_root)
            path.put_last(repo)

    return path


def prepare_config_scope(env):
    """Add env's scope to the global configuration search path."""
    for scope in env.config_scopes():
        spack.config.config.push_scope(scope)


def deactivate_config_scope(env):
    """Remove any scopes from env from the global config path."""
    for scope in env.config_scopes():
        spack.config.config.remove_scope(scope.name)


def manifest_file(env_name_or_dir):
    """Return the absolute path to a manifest file given the environment
    name or directory.

    Args:
        env_name_or_dir (str): either the name of a valid environment
            or a directory where a manifest file resides

    Raises:
        AssertionError: if the environment is not found
    """
    env_dir = None
    if is_env_dir(env_name_or_dir):
        env_dir = os.path.abspath(env_name_or_dir)
    elif exists(env_name_or_dir):
        env_dir = os.path.abspath(root(env_name_or_dir))

    assert env_dir, "environment not found [env={0}]".format(env_name_or_dir)
    return os.path.join(env_dir, manifest_name)


def update_yaml(manifest, backup_file):
    """Update a manifest file from an old format to the current one.

    Args:
        manifest (str): path to a manifest file
        backup_file (str): file where to copy the original manifest

    Returns:
        True if the manifest was updated, False otherwise.

    Raises:
        AssertionError: in case anything goes wrong during the update
    """
    # Check if the environment needs update
    with open(manifest) as f:
        data = syaml.load(f)

    top_level_key = _top_level_key(data)
    needs_update = spack.schema.env.update(data[top_level_key])
    if not needs_update:
        msg = "No update needed [manifest={0}]".format(manifest)
        tty.debug(msg)
        return False

    # Copy environment to a backup file and update it
    msg = ('backup file "{0}" already exists on disk. Check its content '
           'and remove it before trying to update again.')
    assert not os.path.exists(backup_file), msg.format(backup_file)

    shutil.copy(manifest, backup_file)
    with open(manifest, 'w') as f:
        syaml.dump_config(data, f)
    return True


def _top_level_key(data):
    """Return the top level key used in this environment

    Args:
        data (dict): raw yaml data of the environment

    Returns:
        Either 'spack' or 'env'
    """
    msg = ('cannot find top level attribute "spack" or "env"'
           'in the environment')
    assert any(x in data for x in ('spack', 'env')), msg
    if 'spack' in data:
        return 'spack'
    return 'env'


def is_latest_format(manifest):
    """Return True if the manifest file is at the latest schema format,
    False otherwise.

    Args:
        manifest (str): manifest file to be analyzed
    """
    with open(manifest) as f:
        data = syaml.load(f)
    top_level_key = _top_level_key(data)
    changed = spack.schema.env.update(data[top_level_key])
    return not changed


class SpackEnvironmentError(spack.error.SpackError):
    """Superclass for all errors to do with Spack environments."""
