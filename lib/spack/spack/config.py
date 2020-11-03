# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module implements Spack's configuration file handling.

This implements Spack's configuration system, which handles merging
multiple scopes with different levels of precedence.  See the
documentation on :ref:`configuration-scopes` for details on how Spack's
configuration system behaves.  The scopes are:

  #. ``default``
  #. ``system``
  #. ``site``
  #. ``user``

And corresponding :ref:`per-platform scopes <platform-scopes>`. Important
functions in this module are:

* :py:func:`get_config`
* :py:func:`update_config`

``get_config`` reads in YAML data for a particular scope and returns
it. Callers can then modify the data and write it back with
``update_config``.

When read in, Spack validates configurations with jsonschemas.  The
schemas are in submodules of :py:mod:`spack.schema`.

"""
import collections
import copy
import functools
import os
import re
import sys
import multiprocessing
from contextlib import contextmanager
from six import iteritems
from ordereddict_backport import OrderedDict

import ruamel.yaml as yaml
from ruamel.yaml.error import MarkedYAMLError

import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.paths
import spack.architecture
import spack.schema
import spack.schema.compilers
import spack.schema.mirrors
import spack.schema.repos
import spack.schema.packages
import spack.schema.modules
import spack.schema.config
import spack.schema.upstreams
import spack.schema.env
from spack.error import SpackError

# Hacked yaml for configuration files preserves line numbers.
import spack.util.spack_yaml as syaml

#: Dict from section names -> schema for that section
section_schemas = {
    'compilers': spack.schema.compilers.schema,
    'mirrors': spack.schema.mirrors.schema,
    'repos': spack.schema.repos.schema,
    'packages': spack.schema.packages.schema,
    'modules': spack.schema.modules.schema,
    'config': spack.schema.config.schema,
    'upstreams': spack.schema.upstreams.schema,
}

# Same as above, but including keys for environments
# this allows us to unify config reading between configs and environments
all_schemas = copy.deepcopy(section_schemas)
all_schemas.update(dict((key, spack.schema.env.schema)
                        for key in spack.schema.env.keys))

#: Builtin paths to configuration files in Spack
configuration_paths = (
    # Default configuration scope is the lowest-level scope. These are
    # versioned with Spack and can be overridden by systems, sites or users
    ('defaults', os.path.join(spack.paths.etc_path, 'spack', 'defaults')),

    # System configuration is per machine.
    # No system-level configs should be checked into spack by default
    ('system', os.path.join(spack.paths.system_etc_path, 'spack')),

    # Site configuration is per spack instance, for sites or projects
    # No site-level configs should be checked into spack by default.
    ('site', os.path.join(spack.paths.etc_path, 'spack')),

    # User configuration can override both spack defaults and site config
    ('user', spack.paths.user_config_path)
)

#: Hard-coded default values for some key configuration options.
#: This ensures that Spack will still work even if config.yaml in
#: the defaults scope is removed.
config_defaults = {
    'config': {
        'debug': False,
        'connect_timeout': 10,
        'verify_ssl': True,
        'checksum': True,
        'dirty': False,
        'build_jobs': min(16, multiprocessing.cpu_count()),
        'build_stage': '$tempdir/spack-stage',
    }
}

#: metavar to use for commands that accept scopes
#: this is shorter and more readable than listing all choices
scopes_metavar = '{defaults,system,site,user}[/PLATFORM]'

#: Base name for the (internal) overrides scope.
overrides_base_name = 'overrides-'


def first_existing(dictionary, keys):
    """Get the value of the first key in keys that is in the dictionary."""
    try:
        return next(k for k in keys if k in dictionary)
    except StopIteration:
        raise KeyError("None of %s is in dict!" % keys)


class ConfigScope(object):
    """This class represents a configuration scope.

       A scope is one directory containing named configuration files.
       Each file is a config "section" (e.g., mirrors, compilers, etc).
    """

    def __init__(self, name, path):
        self.name = name           # scope name.
        self.path = path           # path to directory containing configs.
        self.sections = syaml.syaml_dict()  # sections read from config files.

    @property
    def is_platform_dependent(self):
        return '/' in self.name

    def get_section_filename(self, section):
        _validate_section_name(section)
        return os.path.join(self.path, "%s.yaml" % section)

    def get_section(self, section):
        if section not in self.sections:
            path   = self.get_section_filename(section)
            schema = section_schemas[section]
            data   = read_config_file(path, schema)
            self.sections[section] = data
        return self.sections[section]

    def _write_section(self, section):
        filename = self.get_section_filename(section)
        data = self.get_section(section)

        # We copy data here to avoid adding defaults at write time
        validate_data = copy.deepcopy(data)
        validate(validate_data, section_schemas[section])

        try:
            mkdirp(self.path)
            with open(filename, 'w') as f:
                syaml.dump_config(data, stream=f, default_flow_style=False)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigFileError(
                "Error writing to config file: '%s'" % str(e))

    def clear(self):
        """Empty cached config information."""
        self.sections = syaml.syaml_dict()

    def __repr__(self):
        return '<ConfigScope: %s: %s>' % (self.name, self.path)


class SingleFileScope(ConfigScope):
    """This class represents a configuration scope in a single YAML file."""
    def __init__(self, name, path, schema, yaml_path=None):
        """Similar to ``ConfigScope`` but can be embedded in another schema.

        Arguments:
            schema (dict): jsonschema for the file to read
            yaml_path (list): path in the schema where config data can be
                found.
                If the schema accepts the following yaml data, the yaml_path
                would be ['outer', 'inner']

                .. code-block:: yaml

                   outer:
                     inner:
                       config:
                         install_tree: $spack/opt/spack
        """
        super(SingleFileScope, self).__init__(name, path)
        self._raw_data = None
        self.schema = schema
        self.yaml_path = yaml_path or []

    @property
    def is_platform_dependent(self):
        return False

    def get_section_filename(self, section):
        return self.path

    def get_section(self, section):
        # read raw data from the file, which looks like:
        # {
        #   'config': {
        #      ... data ...
        #   },
        #   'packages': {
        #      ... data ...
        #   },
        # }
        #
        # To preserve overrides up to the section level (e.g. to override
        # the "packages" section with the "::" syntax), data in self.sections
        # looks like this:
        # {
        #   'config': {
        #      'config': {
        #         ... data ...
        #       }
        #   },
        #   'packages': {
        #      'packages': {
        #         ... data ...
        #      }
        #   }
        # }
        if self._raw_data is None:
            self._raw_data = read_config_file(self.path, self.schema)
            if self._raw_data is None:
                return None

            section_data = self._raw_data
            for key in self.yaml_path:
                if section_data is None:
                    return None
                section_data = section_data[key]

            for section_key, data in section_data.items():
                self.sections[section_key] = {section_key: data}
        return self.sections.get(section, None)

    def _write_section(self, section):
        data_to_write = self._raw_data

        # If there is no existing data, this section SingleFileScope has never
        # been written to disk. We need to construct the portion of the data
        # from the root of self._raw_data to the level at which the config
        # sections are defined. That requires creating keys for every entry in
        # self.yaml_path
        if not data_to_write:
            data_to_write = {}
            # reverse because we construct it from the inside out
            for key in reversed(self.yaml_path):
                data_to_write = {key: data_to_write}

        # data_update_pointer is a pointer to the part of data_to_write
        # that we are currently updating.
        # We start by traversing into the data to the point at which the
        # config sections are defined. This means popping the keys from
        # self.yaml_path
        data_update_pointer = data_to_write
        for key in self.yaml_path:
            data_update_pointer = data_update_pointer[key]

        # For each section, update the data at the level of our pointer
        # with the data from the section
        for key, data in self.sections.items():
            data_update_pointer[key] = data[key]

        validate(data_to_write, self.schema)
        try:
            parent = os.path.dirname(self.path)
            mkdirp(parent)

            tmp = os.path.join(parent, '.%s.tmp' % os.path.basename(self.path))
            with open(tmp, 'w') as f:
                syaml.dump_config(data_to_write, stream=f,
                                  default_flow_style=False)
            os.rename(tmp, self.path)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigFileError(
                "Error writing to config file: '%s'" % str(e))

    def __repr__(self):
        return '<SingleFileScope: %s: %s>' % (self.name, self.path)


class ImmutableConfigScope(ConfigScope):
    """A configuration scope that cannot be written to.

    This is used for ConfigScopes passed on the command line.
    """

    def _write_section(self, section):
        raise ConfigError("Cannot write to immutable scope %s" % self)

    def __repr__(self):
        return '<ImmutableConfigScope: %s: %s>' % (self.name, self.path)


class InternalConfigScope(ConfigScope):
    """An internal configuration scope that is not persisted to a file.

    This is for spack internal use so that command-line options and
    config file settings are accessed the same way, and Spack can easily
    override settings from files.
    """
    def __init__(self, name, data=None):
        super(InternalConfigScope, self).__init__(name, None)
        self.sections = syaml.syaml_dict()

        if data:
            data = InternalConfigScope._process_dict_keyname_overrides(data)
            for section in data:
                dsec = data[section]
                validate({section: dsec}, section_schemas[section])
                self.sections[section] = _mark_internal(
                    syaml.syaml_dict({section: dsec}), name)

    def get_section_filename(self, section):
        raise NotImplementedError(
            "Cannot get filename for InternalConfigScope.")

    def get_section(self, section):
        """Just reads from an internal dictionary."""
        if section not in self.sections:
            self.sections[section] = None
        return self.sections[section]

    def _write_section(self, section):
        """This only validates, as the data is already in memory."""
        data = self.get_section(section)
        if data is not None:
            validate(data, section_schemas[section])
        self.sections[section] = _mark_internal(data, self.name)

    def __repr__(self):
        return '<InternalConfigScope: %s>' % self.name

    @staticmethod
    def _process_dict_keyname_overrides(data):
        """Turn a trailing `:' in a key name into an override attribute."""
        result = {}
        for sk, sv in iteritems(data):
            if sk.endswith(':'):
                key = syaml.syaml_str(sk[:-1])
                key.override = True
            else:
                key = sk

            if isinstance(sv, dict):
                result[key]\
                    = InternalConfigScope._process_dict_keyname_overrides(sv)
            else:
                result[key] = copy.copy(sv)

        return result


def _config_mutator(method):
    """Decorator to mark all the methods in the Configuration class
    that mutate the underlying configuration. Used to clear the
    memoization cache.
    """
    @functools.wraps(method)
    def _method(self, *args, **kwargs):
        self._get_config_memoized.cache.clear()
        return method(self, *args, **kwargs)
    return _method


class Configuration(object):
    """A full Spack configuration, from a hierarchy of config files.

    This class makes it easy to add a new scope on top of an existing one.
    """

    def __init__(self, *scopes):
        """Initialize a configuration with an initial list of scopes.

        Args:
            scopes (list of ConfigScope): list of scopes to add to this
                Configuration, ordered from lowest to highest precedence

        """
        self.scopes = OrderedDict()
        for scope in scopes:
            self.push_scope(scope)
        self.format_updates = collections.defaultdict(list)

    @_config_mutator
    def push_scope(self, scope):
        """Add a higher precedence scope to the Configuration."""
        cmd_line_scope = None
        if self.scopes:
            highest_precedence_scope = list(self.scopes.values())[-1]
            if highest_precedence_scope.name == 'command_line':
                # If the command-line scope is present, it should always
                # be the scope of highest precedence
                cmd_line_scope = self.pop_scope()

        self.scopes[scope.name] = scope
        if cmd_line_scope:
            self.scopes['command_line'] = cmd_line_scope

    @_config_mutator
    def pop_scope(self):
        """Remove the highest precedence scope and return it."""
        name, scope = self.scopes.popitem(last=True)
        return scope

    @_config_mutator
    def remove_scope(self, scope_name):
        return self.scopes.pop(scope_name)

    @property
    def file_scopes(self):
        """List of writable scopes with an associated file."""
        return [s for s in self.scopes.values()
                if (type(s) == ConfigScope
                    or type(s) == SingleFileScope)]

    def highest_precedence_scope(self):
        """Non-internal scope with highest precedence."""
        return next(reversed(self.file_scopes), None)

    def highest_precedence_non_platform_scope(self):
        """Non-internal non-platform scope with highest precedence

        Platform-specific scopes are of the form scope/platform"""
        generator = reversed(self.file_scopes)
        highest = next(generator, None)
        while highest and highest.is_platform_dependent:
            highest = next(generator, None)
        return highest

    def matching_scopes(self, reg_expr):
        """
        List of all scopes whose names match the provided regular expression.

        For example, matching_scopes(r'^command') will return all scopes
        whose names begin with `command`.
        """
        return [s for s in self.scopes.values() if re.search(reg_expr, s.name)]

    def _validate_scope(self, scope):
        """Ensure that scope is valid in this configuration.

        This should be used by routines in ``config.py`` to validate
        scope name arguments, and to determine a default scope where no
        scope is specified.

        Raises:
            ValueError: if ``scope`` is not valid

        Returns:
            ConfigScope: a valid ConfigScope if ``scope`` is ``None`` or valid
        """
        if scope is None:
            # default to the scope with highest precedence.
            return self.highest_precedence_scope()

        elif scope in self.scopes:
            return self.scopes[scope]

        else:
            raise ValueError("Invalid config scope: '%s'.  Must be one of %s"
                             % (scope, self.scopes.keys()))

    def get_config_filename(self, scope, section):
        """For some scope and section, get the name of the configuration file.
        """
        scope = self._validate_scope(scope)
        return scope.get_section_filename(section)

    @_config_mutator
    def clear_caches(self):
        """Clears the caches for configuration files,

        This will cause files to be re-read upon the next request."""
        for scope in self.scopes.values():
            scope.clear()

    @_config_mutator
    def update_config(self, section, update_data, scope=None, force=False):
        """Update the configuration file for a particular scope.

        Overwrites contents of a section in a scope with update_data,
        then writes out the config file.

        update_data should have the top-level section name stripped off
        (it will be re-added).  Data itself can be a list, dict, or any
        other yaml-ish structure.

        Configuration scopes that are still written in an old schema
        format will fail to update unless ``force`` is True.

        Args:
            section (str): section of the configuration to be updated
            update_data (dict): data to be used for the update
            scope (str): scope to be updated
            force (str): force the update
        """
        if self.format_updates.get(section) and not force:
            msg = ('The "{0}" section of the configuration needs to be written'
                   ' to disk, but is currently using a deprecated format. '
                   'Please update it using:\n\n'
                   '\tspack config [--scope=<scope] update {0}\n\n'
                   'Note that previous versions of Spack will not be able to '
                   'use the updated configuration.')
            msg = msg.format(section)
            raise RuntimeError(msg)

        _validate_section_name(section)  # validate section name
        scope = self._validate_scope(scope)  # get ConfigScope object

        # manually preserve comments
        need_comment_copy = (section in scope.sections and
                             scope.sections[section] is not None)
        if need_comment_copy:
            comments = getattr(scope.sections[section][section],
                               yaml.comments.Comment.attrib,
                               None)

        # read only the requested section's data.
        scope.sections[section] = syaml.syaml_dict({section: update_data})
        if need_comment_copy and comments:
            setattr(scope.sections[section][section],
                    yaml.comments.Comment.attrib,
                    comments)

        scope._write_section(section)

    def get_config(self, section, scope=None):
        """Get configuration settings for a section.

        If ``scope`` is ``None`` or not provided, return the merged contents
        of all of Spack's configuration scopes.  If ``scope`` is provided,
        return only the confiugration as specified in that scope.

        This off the top-level name from the YAML section.  That is, for a
        YAML config file that looks like this::

           config:
             install_tree: $spack/opt/spack
             module_roots:
               lmod:   $spack/share/spack/lmod

        ``get_config('config')`` will return::

           { 'install_tree': '$spack/opt/spack',
             'module_roots: {
                 'lmod': '$spack/share/spack/lmod'
             }
           }

        """
        return self._get_config_memoized(section, scope)

    @llnl.util.lang.memoized
    def _get_config_memoized(self, section, scope):
        _validate_section_name(section)

        if scope is None:
            scopes = self.scopes.values()
        else:
            scopes = [self._validate_scope(scope)]

        merged_section = syaml.syaml_dict()
        for scope in scopes:
            # read potentially cached data from the scope.

            data = scope.get_section(section)

            # Skip empty configs
            if not data or not isinstance(data, dict):
                continue

            if section not in data:
                continue

            # We might be reading configuration files in an old format,
            # thus read data and update it in memory if need be.
            changed = _update_in_memory(data, section)
            if changed:
                self.format_updates[section].append(scope)
                msg = ('OUTDATED CONFIGURATION FILE '
                       '[section={0}, scope={1}, dir={2}]')
                tty.debug(msg.format(section, scope.name, scope.path))

            merged_section = merge_yaml(merged_section, data)

        # no config files -- empty config.
        if section not in merged_section:
            return syaml.syaml_dict()

        # take the top key off before returning.
        ret = merged_section[section]
        if isinstance(ret, dict):
            ret = syaml.syaml_dict(ret)
        return ret

    def get(self, path, default=None, scope=None):
        """Get a config section or a single value from one.

        Accepts a path syntax that allows us to grab nested config map
        entries.  Getting the 'config' section would look like::

            spack.config.get('config')

        and the ``dirty`` section in the ``config`` scope would be::

            spack.config.get('config:dirty')

        We use ``:`` as the separator, like YAML objects.
    """
        # TODO: Currently only handles maps. Think about lists if needed.
        parts = process_config_path(path)
        section = parts.pop(0)

        value = self.get_config(section, scope=scope)

        while parts:
            key = parts.pop(0)
            value = value.get(key, default)

        return value

    @_config_mutator
    def set(self, path, value, scope=None):
        """Convenience function for setting single values in config files.

        Accepts the path syntax described in ``get()``.
        """
        if ':' not in path:
            # handle bare section name as path
            self.update_config(path, value, scope=scope)
            return

        parts = process_config_path(path)
        section = parts.pop(0)

        section_data = self.get_config(section, scope=scope)

        data = section_data
        while len(parts) > 1:
            key = parts.pop(0)

            if _override(key):
                new = type(data[key])()
                del data[key]
            else:
                new = data[key]

            if isinstance(new, dict):
                # Make it an ordered dict
                new = syaml.syaml_dict(new)
                # reattach to parent object
                data[key] = new
            data = new

        if _override(parts[0]):
            data.pop(parts[0], None)

        # update new value
        data[parts[0]] = value

        self.update_config(section, section_data, scope=scope)

    def __iter__(self):
        """Iterate over scopes in this configuration."""
        for scope in self.scopes.values():
            yield scope

    def print_section(self, section, blame=False):
        """Print a configuration to stdout."""
        try:
            data = syaml.syaml_dict()
            data[section] = self.get_config(section)
            syaml.dump_config(
                data, stream=sys.stdout, default_flow_style=False, blame=blame)
        except (yaml.YAMLError, IOError):
            raise ConfigError("Error reading configuration: %s" % section)


@contextmanager
def override(path_or_scope, value=None):
    """Simple way to override config settings within a context.

    Arguments:
        path_or_scope (ConfigScope or str): scope or single option to override
        value (object, optional): value for the single option

    Temporarily push a scope on the current configuration, then remove it
    after the context completes. If a single option is provided, create
    an internal config scope for it and push/pop that scope.

    """
    if isinstance(path_or_scope, ConfigScope):
        overrides = path_or_scope
        config.push_scope(path_or_scope)
    else:
        base_name = overrides_base_name
        # Ensure the new override gets a unique scope name
        current_overrides = [s.name for s in
                             config.matching_scopes(r'^{0}'.format(base_name))]
        num_overrides = len(current_overrides)
        while True:
            scope_name = '{0}{1}'.format(base_name, num_overrides)
            if scope_name in current_overrides:
                num_overrides += 1
            else:
                break

        overrides = InternalConfigScope(scope_name)
        config.push_scope(overrides)
        config.set(path_or_scope, value, scope=scope_name)

    yield config

    scope = config.remove_scope(overrides.name)
    assert scope is overrides


#: configuration scopes added on the command line
#: set by ``spack.main.main()``.
command_line_scopes = []


def _add_platform_scope(cfg, scope_type, name, path):
    """Add a platform-specific subdirectory for the current platform."""
    platform = spack.architecture.platform().name
    plat_name = '%s/%s' % (name, platform)
    plat_path = os.path.join(path, platform)
    cfg.push_scope(scope_type(plat_name, plat_path))


def _add_command_line_scopes(cfg, command_line_scopes):
    """Add additional scopes from the --config-scope argument.

    Command line scopes are named after their position in the arg list.
    """
    for i, path in enumerate(command_line_scopes):
        # We ensure that these scopes exist and are readable, as they are
        # provided on the command line by the user.
        if not os.path.isdir(path):
            raise ConfigError("config scope is not a directory: '%s'" % path)
        elif not os.access(path, os.R_OK):
            raise ConfigError("config scope is not readable: '%s'" % path)

        # name based on order on the command line
        name = 'cmd_scope_%d' % i
        cfg.push_scope(ImmutableConfigScope(name, path))
        _add_platform_scope(cfg, ImmutableConfigScope, name, path)


def _config():
    """Singleton Configuration instance.

    This constructs one instance associated with this module and returns
    it. It is bundled inside a function so that configuration can be
    initialized lazily.

    Return:
        (Configuration): object for accessing spack configuration

    """
    cfg = Configuration()

    # first do the builtin, hardcoded defaults
    defaults = InternalConfigScope('_builtin', config_defaults)
    cfg.push_scope(defaults)

    # add each scope and its platform-specific directory
    for name, path in configuration_paths:
        cfg.push_scope(ConfigScope(name, path))

        # Each scope can have per-platfom overrides in subdirectories
        _add_platform_scope(cfg, ConfigScope, name, path)

    # add command-line scopes
    _add_command_line_scopes(cfg, command_line_scopes)

    # we make a special scope for spack commands so that they can
    # override configuration options.
    cfg.push_scope(InternalConfigScope('command_line'))

    return cfg


#: This is the singleton configuration instance for Spack.
config = llnl.util.lang.Singleton(_config)


def replace_config(configuration):
    """Replace the current global configuration with the instance passed as
    argument.

    Args:
        configuration (Configuration): the new configuration to be used.

    Returns:
        The old configuration that has been removed
    """
    global config
    config.clear_caches(), configuration.clear_caches()
    old_config, config = config, configuration
    return old_config


def get(path, default=None, scope=None):
    """Module-level wrapper for ``Configuration.get()``."""
    return config.get(path, default, scope)


def set(path, value, scope=None):
    """Convenience function for setting single values in config files.

    Accepts the path syntax described in ``get()``.
    """
    return config.set(path, value, scope)


def scopes():
    """Convenience function to get list of configuration scopes."""
    return config.scopes


def _validate_section_name(section):
    """Exit if the section is not a valid section."""
    if section not in section_schemas:
        raise ConfigSectionError(
            "Invalid config section: '%s'. Options are: %s"
            % (section, " ".join(section_schemas.keys())))


def validate(data, schema, filename=None):
    """Validate data read in from a Spack YAML file.

    Arguments:
        data (dict or list): data read from a Spack YAML file
        schema (dict or list): jsonschema to validate data

    This leverages the line information (start_mark, end_mark) stored
    on Spack YAML structures.
    """
    import jsonschema
    # validate a copy to avoid adding defaults
    # This allows us to round-trip data without adding to it.
    test_data = copy.deepcopy(data)

    if isinstance(test_data, yaml.comments.CommentedMap):
        # HACK to fully copy ruamel CommentedMap that doesn't provide copy
        # method. Especially necessary for environments
        setattr(test_data,
                yaml.comments.Comment.attrib,
                getattr(data,
                        yaml.comments.Comment.attrib,
                        yaml.comments.Comment()))

    try:
        spack.schema.Validator(schema).validate(test_data)
    except jsonschema.ValidationError as e:
        if hasattr(e.instance, 'lc'):
            line_number = e.instance.lc.line + 1
        else:
            line_number = None
        raise ConfigFormatError(e, data, filename, line_number)
    # return the validated data so that we can access the raw data
    # mostly relevant for environments
    return test_data


def read_config_file(filename, schema=None):
    """Read a YAML configuration file.

    User can provide a schema for validation. If no schema is provided,
    we will infer the schema from the top-level key."""
    # Dev: Inferring schema and allowing it to be provided directly allows us
    # to preserve flexibility in calling convention (don't need to provide
    # schema when it's not necessary) while allowing us to validate against a
    # known schema when the top-level key could be incorrect.

    # Ignore nonexisting files.
    if not os.path.exists(filename):
        return None

    elif not os.path.isfile(filename):
        raise ConfigFileError(
            "Invalid configuration. %s exists but is not a file." % filename)

    elif not os.access(filename, os.R_OK):
        raise ConfigFileError("Config file is not readable: %s" % filename)

    try:
        tty.debug("Reading config file %s" % filename)
        with open(filename) as f:
            data = syaml.load_config(f)

        if data:
            if not schema:
                key = next(iter(data))
                schema = all_schemas[key]
            validate(data, schema)
        return data

    except StopIteration:
        raise ConfigFileError(
            "Config file is empty or is not a valid YAML dict: %s" % filename)

    except MarkedYAMLError as e:
        raise ConfigFileError(
            "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))

    except IOError as e:
        raise ConfigFileError(
            "Error reading configuration file %s: %s" % (filename, str(e)))


def _override(string):
    """Test if a spack YAML string is an override.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `::`,
    and if they do, their values completely replace lower-precedence
    configs instead of merging into them.

    """
    return hasattr(string, 'override') and string.override


def _mark_internal(data, name):
    """Add a simple name mark to raw YAML/JSON data.

    This is used by `spack config blame` to show where config lines came from.
    """
    if isinstance(data, dict):
        d = syaml.syaml_dict((_mark_internal(k, name), _mark_internal(v, name))
                             for k, v in data.items())
    elif isinstance(data, list):
        d = syaml.syaml_list(_mark_internal(e, name) for e in data)
    else:
        d = syaml.syaml_type(data)

    if syaml.markable(d):
        d._start_mark = yaml.Mark(name, None, None, None, None, None)
        d._end_mark = yaml.Mark(name, None, None, None, None, None)

    return d


def get_valid_type(path):
    """Returns an instance of a type that will pass validation for path.

    The instance is created by calling the constructor with no arguments.
    If multiple types will satisfy validation for data at the configuration
    path given, the priority order is ``list``, ``dict``, ``str``, ``bool``,
    ``int``, ``float``.
    """
    components = process_config_path(path)
    section = components[0]
    for type in (list, syaml.syaml_dict, str, bool, int, float):
        try:
            ret = type()
            test_data = ret
            for component in reversed(components):
                test_data = {component: test_data}
            validate(test_data, section_schemas[section])
            return ret
        except (ConfigFormatError, AttributeError):
            # This type won't validate, try the next one
            # Except AttributeError because undefined behavior of dict ordering
            # in python 3.5 can cause the validator to raise an AttributeError
            # instead of a ConfigFormatError.
            pass
    raise ConfigError("Cannot determine valid type for path '%s'." % path)


def merge_yaml(dest, source):
    """Merges source into dest; entries in source take precedence over dest.

    This routine may modify dest and should be assigned to dest, in
    case dest was None to begin with, e.g.:

       dest = merge_yaml(dest, source)

    In the result, elements from lists from ``source`` will appear before
    elements of lists from ``dest``. Likewise, when iterating over keys
    or items in merged ``OrderedDict`` objects, keys from ``source`` will
    appear before keys from ``dest``.

    Config file authors can optionally end any attribute in a dict
    with `::` instead of `:`, and the key will override that of the
    parent instead of merging.
    """
    def they_are(t):
        return isinstance(dest, t) and isinstance(source, t)

    # If source is None, overwrite with source.
    if source is None:
        return None

    # Source list is prepended (for precedence)
    if they_are(list):
        # Make sure to copy ruamel comments
        dest[:] = source + [x for x in dest if x not in source]
        return dest

    # Source dict is merged into dest.
    elif they_are(dict):
        # save dest keys to reinsert later -- this ensures that  source items
        # come *before* dest in OrderdDicts
        dest_keys = [dk for dk in dest.keys() if dk not in source]

        for sk, sv in iteritems(source):
            # always remove the dest items. Python dicts do not overwrite
            # keys on insert, so this ensures that source keys are copied
            # into dest along with mark provenance (i.e., file/line info).
            merge = sk in dest
            old_dest_value = dest.pop(sk, None)

            if merge and not _override(sk):
                dest[sk] = merge_yaml(old_dest_value, sv)
            else:
                # if sk ended with ::, or if it's new, completely override
                dest[sk] = copy.deepcopy(sv)

        # reinsert dest keys so they are last in the result
        for dk in dest_keys:
            dest[dk] = dest.pop(dk)

        return dest

    # If we reach here source and dest are either different types or are
    # not both lists or dicts: replace with source.
    return copy.copy(source)


#
# Process a path argument to config.set() that may contain overrides ('::' or
# trailing ':')
#
def process_config_path(path):
    result = []
    if path.startswith(':'):
        raise syaml.SpackYAMLError("Illegal leading `:' in path `{0}'".
                                   format(path), '')
    seen_override_in_path = False
    while path:
        front, sep, path = path.partition(':')
        if (sep and not path) or path.startswith(':'):
            if seen_override_in_path:
                raise syaml.SpackYAMLError("Meaningless second override"
                                           " indicator `::' in path `{0}'".
                                           format(path), '')
            path = path.lstrip(':')
            front = syaml.syaml_str(front)
            front.override = True
            seen_override_in_path = True
        result.append(front)
    return result


#
# Settings for commands that modify configuration
#
def default_modify_scope(section='config'):
    """Return the config scope that commands should modify by default.

    Commands that modify configuration by default modify the *highest*
    priority scope.

    Arguments:
        section (boolean): Section for which to get the default scope.
            If this is not 'compilers', a general (non-platform) scope is used.
    """
    if section == 'compilers':
        return spack.config.config.highest_precedence_scope().name
    else:
        return spack.config.config.highest_precedence_non_platform_scope().name


def default_list_scope():
    """Return the config scope that is listed by default.

    Commands that list configuration list *all* scopes (merged) by default.
    """
    return None


def _update_in_memory(data, section):
    """Update the format of the configuration data in memory.

    This function assumes the section is valid (i.e. validation
    is responsibility of the caller)

    Args:
        data (dict): configuration data
        section (str): section of the configuration to update

    Returns:
        True if the data was changed, False otherwise
    """
    update_fn = ensure_latest_format_fn(section)
    changed = update_fn(data[section])
    return changed


def ensure_latest_format_fn(section):
    """Return a function that takes as input a dictionary read from
    a configuration file and update it to the latest format.

    The function returns True if there was any update, False otherwise.

    Args:
        section (str): section of the configuration e.g. "packages",
            "config", etc.
    """
    # The line below is based on the fact that every module we need
    # is already imported at the top level
    section_module = getattr(spack.schema, section)
    update_fn = getattr(section_module, 'update', lambda x: False)
    return update_fn


class ConfigError(SpackError):
    """Superclass for all Spack config related errors."""


class ConfigSectionError(ConfigError):
    """Error for referring to a bad config section name in a configuration."""


class ConfigFileError(ConfigError):
    """Issue reading or accessing a configuration file."""


class ConfigFormatError(ConfigError):
    """Raised when a configuration format does not match its schema."""

    def __init__(self, validation_error, data, filename=None, line=None):
        # spack yaml has its own file/line marks -- try to find them
        # we prioritize these over the inputs
        mark = self._get_mark(validation_error, data)
        if mark:
            filename = mark.name
            line = mark.line + 1

        self.filename = filename  # record this for ruamel.yaml

        # construct location
        location = '<unknown file>'
        if filename:
            location = '%s' % filename
        if line is not None:
            location += ':%d' % line

        message = '%s: %s' % (location, validation_error.message)
        super(ConfigError, self).__init__(message)

    def _get_mark(self, validation_error, data):
        """Get the file/line mark fo a validation error from a Spack YAML file.
        """
        def _get_mark_or_first_member_mark(obj):
            # mark of object itelf
            mark = getattr(obj, '_start_mark', None)
            if mark:
                return mark

            # mark of first member if it is a container
            if isinstance(obj, (list, dict)):
                first_member = next(iter(obj), None)
                if first_member:
                    mark = getattr(first_member, '_start_mark', None)
                    if mark:
                        return mark

        # Try various places, starting with instance and parent
        for obj in (validation_error.instance, validation_error.parent):
            mark = _get_mark_or_first_member_mark(obj)
            if mark:
                return mark

        def get_path(path, data):
            if path:
                return get_path(path[1:], data[path[0]])
            else:
                return data

        # Try really hard to get the parent (which sometimes is not
        # set) This digs it out of the validated structure if it's not
        # on the validation_error.
        path = validation_error.path
        if path:
            parent = get_path(list(path)[:-1], data)
            if path[-1] in parent:
                if isinstance(parent, dict):
                    keylist = list(parent.keys())
                elif isinstance(parent, list):
                    keylist = parent
                idx = keylist.index(path[-1])
                mark = getattr(keylist[idx], '_start_mark', None)
                if mark:
                    return mark

        # give up and return None if nothing worked
        return None
