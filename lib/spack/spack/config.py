# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

* :func:`~spack.config.Configuration.get_config`
* :func:`~spack.config.Configuration.update_config`

``get_config`` reads in YAML data for a particular scope and returns
it. Callers can then modify the data and write it back with
``update_config``.

When read in, Spack validates configurations with jsonschemas.  The
schemas are in submodules of :py:mod:`spack.schema`.

"""
import collections
import contextlib
import copy
import functools
import os
import re
import sys
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

from llnl.util import filesystem, lang, tty

import spack.error
import spack.paths
import spack.platforms
import spack.schema
import spack.schema.bootstrap
import spack.schema.cdash
import spack.schema.ci
import spack.schema.compilers
import spack.schema.concretizer
import spack.schema.config
import spack.schema.definitions
import spack.schema.develop
import spack.schema.env
import spack.schema.mirrors
import spack.schema.modules
import spack.schema.packages
import spack.schema.repos
import spack.schema.upstreams
import spack.schema.view

# Hacked yaml for configuration files preserves line numbers.
import spack.util.spack_yaml as syaml
import spack.util.web as web_util
from spack.util.cpus import cpus_available

#: Dict from section names -> schema for that section
SECTION_SCHEMAS: Dict[str, Any] = {
    "compilers": spack.schema.compilers.schema,
    "concretizer": spack.schema.concretizer.schema,
    "definitions": spack.schema.definitions.schema,
    "view": spack.schema.view.schema,
    "develop": spack.schema.develop.schema,
    "mirrors": spack.schema.mirrors.schema,
    "repos": spack.schema.repos.schema,
    "packages": spack.schema.packages.schema,
    "modules": spack.schema.modules.schema,
    "config": spack.schema.config.schema,
    "upstreams": spack.schema.upstreams.schema,
    "bootstrap": spack.schema.bootstrap.schema,
    "ci": spack.schema.ci.schema,
    "cdash": spack.schema.cdash.schema,
}

# Same as above, but including keys for environments
# this allows us to unify config reading between configs and environments
_ALL_SCHEMAS: Dict[str, Any] = copy.deepcopy(SECTION_SCHEMAS)
_ALL_SCHEMAS.update({spack.schema.env.TOP_LEVEL_KEY: spack.schema.env.schema})

#: Path to the default configuration
CONFIGURATION_DEFAULTS_PATH = ("defaults", os.path.join(spack.paths.etc_path, "defaults"))

#: Hard-coded default values for some key configuration options.
#: This ensures that Spack will still work even if config.yaml in
#: the defaults scope is removed.
CONFIG_DEFAULTS = {
    "config": {
        "debug": False,
        "connect_timeout": 10,
        "verify_ssl": True,
        "checksum": True,
        "dirty": False,
        "build_jobs": min(16, cpus_available()),
        "build_stage": "$tempdir/spack-stage",
        "license_dir": spack.paths.default_license_dir,
    }
}

#: metavar to use for commands that accept scopes
#: this is shorter and more readable than listing all choices
SCOPES_METAVAR = "{defaults,system,site,user,command_line}[/PLATFORM] or env:ENVIRONMENT"

#: Base name for the (internal) overrides scope.
_OVERRIDES_BASE_NAME = "overrides-"

#: Type used for raw YAML configuration
YamlConfigDict = Dict[str, Any]


class ConfigScope:
    def __init__(self, name: str) -> None:
        self.name = name
        self.writable = False
        self.sections = syaml.syaml_dict()

    def get_section_filename(self, section: str) -> str:
        raise NotImplementedError

    def get_section(self, section: str) -> Optional[YamlConfigDict]:
        raise NotImplementedError

    def _write_section(self, section: str) -> None:
        raise NotImplementedError

    @property
    def is_platform_dependent(self) -> bool:
        return False

    def clear(self) -> None:
        """Empty cached config information."""
        self.sections = syaml.syaml_dict()

    def __repr__(self) -> str:
        return f"<ConfigScope: {self.name}>"


class DirectoryConfigScope(ConfigScope):
    """Config scope backed by a directory containing one file per section."""

    def __init__(self, name: str, path: str, *, writable: bool = True) -> None:
        super().__init__(name)
        self.path = path
        self.writable = writable

    def get_section_filename(self, section: str) -> str:
        """Returns the filename associated with a given section"""
        _validate_section_name(section)
        return os.path.join(self.path, f"{section}.yaml")

    def get_section(self, section: str) -> Optional[YamlConfigDict]:
        """Returns the data associated with a given section"""
        if section not in self.sections:
            path = self.get_section_filename(section)
            schema = SECTION_SCHEMAS[section]
            data = read_config_file(path, schema)
            self.sections[section] = data
        return self.sections[section]

    def _write_section(self, section: str) -> None:
        if not self.writable:
            raise spack.error.ConfigError(f"Cannot write to immutable scope {self}")

        filename = self.get_section_filename(section)
        data = self.get_section(section)
        if data is None:
            return

        validate(data, SECTION_SCHEMAS[section])

        try:
            filesystem.mkdirp(self.path)
            with open(filename, "w") as f:
                syaml.dump_config(data, stream=f, default_flow_style=False)
        except (syaml.SpackYAMLError, OSError) as e:
            raise ConfigFileError(f"cannot write to '{filename}'") from e

    @property
    def is_platform_dependent(self) -> bool:
        """Returns true if the scope name is platform specific"""
        return "/" in self.name


class SingleFileScope(ConfigScope):
    """This class represents a configuration scope in a single YAML file."""

    def __init__(
        self,
        name: str,
        path: str,
        schema: YamlConfigDict,
        *,
        yaml_path: Optional[List[str]] = None,
        writable: bool = True,
    ) -> None:
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
        super().__init__(name)
        self._raw_data: Optional[YamlConfigDict] = None
        self.schema = schema
        self.path = path
        self.writable = writable
        self.yaml_path = yaml_path or []

    def get_section_filename(self, section) -> str:
        return self.path

    def get_section(self, section: str) -> Optional[YamlConfigDict]:
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

        # This bit ensures we have read the file and have
        # the raw data in memory
        if self._raw_data is None:
            self._raw_data = read_config_file(self.path, self.schema)
            if self._raw_data is None:
                return None

        # Here we know we have the raw data and ensure we
        # populate the sections dictionary, which may be
        # cleared by the clear() method
        if not self.sections:
            section_data = self._raw_data
            for key in self.yaml_path:
                if section_data is None:
                    return None
                section_data = section_data[key]

            for section_key, data in section_data.items():
                self.sections[section_key] = {section_key: data}

        return self.sections.get(section, None)

    def _write_section(self, section: str) -> None:
        if not self.writable:
            raise spack.error.ConfigError(f"Cannot write to immutable scope {self}")
        data_to_write: Optional[YamlConfigDict] = self._raw_data

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
            filesystem.mkdirp(parent)

            tmp = os.path.join(parent, f".{os.path.basename(self.path)}.tmp")
            with open(tmp, "w") as f:
                syaml.dump_config(data_to_write, stream=f, default_flow_style=False)
            filesystem.rename(tmp, self.path)

        except (syaml.SpackYAMLError, OSError) as e:
            raise ConfigFileError(f"cannot write to config file {str(e)}") from e

    def __repr__(self) -> str:
        return f"<SingleFileScope: {self.name}: {self.path}>"


class InternalConfigScope(ConfigScope):
    """An internal configuration scope that is not persisted to a file.

    This is for spack internal use so that command-line options and
    config file settings are accessed the same way, and Spack can easily
    override settings from files.
    """

    def __init__(self, name: str, data: Optional[YamlConfigDict] = None) -> None:
        super().__init__(name)
        self.sections = syaml.syaml_dict()

        if data is not None:
            data = InternalConfigScope._process_dict_keyname_overrides(data)
            for section in data:
                dsec = data[section]
                validate({section: dsec}, SECTION_SCHEMAS[section])
                self.sections[section] = _mark_internal(syaml.syaml_dict({section: dsec}), name)

    def get_section(self, section: str) -> Optional[YamlConfigDict]:
        """Just reads from an internal dictionary."""
        if section not in self.sections:
            self.sections[section] = None
        return self.sections[section]

    def _write_section(self, section: str) -> None:
        """This only validates, as the data is already in memory."""
        data = self.get_section(section)
        if data is not None:
            validate(data, SECTION_SCHEMAS[section])
        self.sections[section] = _mark_internal(data, self.name)

    def __repr__(self) -> str:
        return f"<InternalConfigScope: {self.name}>"

    def clear(self) -> None:
        # no cache to clear here.
        pass

    @staticmethod
    def _process_dict_keyname_overrides(data: YamlConfigDict) -> YamlConfigDict:
        """Turn a trailing `:' in a key name into an override attribute."""
        # Below we have a lot of type directives, since we hack on types and monkey-patch them
        # by adding attributes that otherwise they won't have.
        result: YamlConfigDict = {}
        for sk, sv in data.items():
            if sk.endswith(":"):
                key = syaml.syaml_str(sk[:-1])
                key.override = True  # type: ignore[attr-defined]
            elif sk.endswith("+"):
                key = syaml.syaml_str(sk[:-1])
                key.prepend = True  # type: ignore[attr-defined]
            elif sk.endswith("-"):
                key = syaml.syaml_str(sk[:-1])
                key.append = True  # type: ignore[attr-defined]
            else:
                key = sk  # type: ignore[assignment]

            if isinstance(sv, dict):
                result[key] = InternalConfigScope._process_dict_keyname_overrides(sv)
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


class Configuration:
    """A full Spack configuration, from a hierarchy of config files.

    This class makes it easy to add a new scope on top of an existing one.
    """

    # convert to typing.OrderedDict when we drop 3.6, or OrderedDict when we reach 3.9
    scopes: Dict[str, ConfigScope]

    def __init__(self, *scopes: ConfigScope) -> None:
        """Initialize a configuration with an initial list of scopes.

        Args:
            scopes: list of scopes to add to this
                Configuration, ordered from lowest to highest precedence

        """
        self.scopes = collections.OrderedDict()
        for scope in scopes:
            self.push_scope(scope)
        self.format_updates: Dict[str, List[ConfigScope]] = collections.defaultdict(list)

    @_config_mutator
    def push_scope(self, scope: ConfigScope) -> None:
        """Add a higher precedence scope to the Configuration."""
        tty.debug(f"[CONFIGURATION: PUSH SCOPE]: {str(scope)}", level=2)
        self.scopes[scope.name] = scope

    @_config_mutator
    def pop_scope(self) -> ConfigScope:
        """Remove the highest precedence scope and return it."""
        name, scope = self.scopes.popitem(last=True)  # type: ignore[call-arg]
        tty.debug(f"[CONFIGURATION: POP SCOPE]: {str(scope)}", level=2)
        return scope

    @_config_mutator
    def remove_scope(self, scope_name: str) -> Optional[ConfigScope]:
        """Remove scope by name; has no effect when ``scope_name`` does not exist"""
        scope = self.scopes.pop(scope_name, None)
        tty.debug(f"[CONFIGURATION: POP SCOPE]: {str(scope)}", level=2)
        return scope

    @property
    def writable_scopes(self) -> Generator[ConfigScope, None, None]:
        """Generator of writable scopes with an associated file."""
        return (s for s in self.scopes.values() if s.writable)

    def highest_precedence_scope(self) -> ConfigScope:
        """Writable scope with highest precedence."""
        return next(s for s in reversed(self.scopes.values()) if s.writable)  # type: ignore

    def highest_precedence_non_platform_scope(self) -> ConfigScope:
        """Writable non-platform scope with highest precedence"""
        return next(
            s
            for s in reversed(self.scopes.values())  # type: ignore
            if s.writable and not s.is_platform_dependent
        )

    def matching_scopes(self, reg_expr) -> List[ConfigScope]:
        """
        List of all scopes whose names match the provided regular expression.

        For example, matching_scopes(r'^command') will return all scopes
        whose names begin with `command`.
        """
        return [s for s in self.scopes.values() if re.search(reg_expr, s.name)]

    def _validate_scope(self, scope: Optional[str]) -> ConfigScope:
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
            raise ValueError(
                f"Invalid config scope: '{scope}'.  Must be one of {self.scopes.keys()}"
            )

    def get_config_filename(self, scope: str, section: str) -> str:
        """For some scope and section, get the name of the configuration file."""
        scope = self._validate_scope(scope)
        return scope.get_section_filename(section)

    @_config_mutator
    def clear_caches(self) -> None:
        """Clears the caches for configuration files,

        This will cause files to be re-read upon the next request."""
        for scope in self.scopes.values():
            scope.clear()

    @_config_mutator
    def update_config(
        self, section: str, update_data: Dict, scope: Optional[str] = None, force: bool = False
    ) -> None:
        """Update the configuration file for a particular scope.

        Overwrites contents of a section in a scope with update_data,
        then writes out the config file.

        update_data should have the top-level section name stripped off
        (it will be re-added).  Data itself can be a list, dict, or any
        other yaml-ish structure.

        Configuration scopes that are still written in an old schema
        format will fail to update unless ``force`` is True.

        Args:
            section: section of the configuration to be updated
            update_data: data to be used for the update
            scope: scope to be updated
            force: force the update
        """
        if self.format_updates.get(section) and not force:
            msg = (
                'The "{0}" section of the configuration needs to be written'
                " to disk, but is currently using a deprecated format. "
                "Please update it using:\n\n"
                "\tspack config [--scope=<scope>] update {0}\n\n"
                "Note that previous versions of Spack will not be able to "
                "use the updated configuration."
            )
            msg = msg.format(section)
            raise RuntimeError(msg)

        _validate_section_name(section)  # validate section name
        scope = self._validate_scope(scope)  # get ConfigScope object

        # manually preserve comments
        need_comment_copy = section in scope.sections and scope.sections[section]
        if need_comment_copy:
            comments = syaml.extract_comments(scope.sections[section][section])

        # read only the requested section's data.
        scope.sections[section] = syaml.syaml_dict({section: update_data})
        if need_comment_copy and comments:
            syaml.set_comments(scope.sections[section][section], data_comments=comments)

        scope._write_section(section)

    def get_config(self, section: str, scope: Optional[str] = None) -> YamlConfigDict:
        """Get configuration settings for a section.

        If ``scope`` is ``None`` or not provided, return the merged contents
        of all of Spack's configuration scopes.  If ``scope`` is provided,
        return only the configuration as specified in that scope.

        This off the top-level name from the YAML section.  That is, for a
        YAML config file that looks like this::

           config:
             install_tree:
               root: $spack/opt/spack
             build_stage:
             - $tmpdir/$user/spack-stage

        ``get_config('config')`` will return::

           { 'install_tree': {
                 'root': '$spack/opt/spack',
             }
             'build_stage': ['$tmpdir/$user/spack-stage']
           }

        """
        return self._get_config_memoized(section, scope)

    @lang.memoized
    def _get_config_memoized(self, section: str, scope: Optional[str]) -> YamlConfigDict:
        _validate_section_name(section)

        if scope is None:
            scopes = list(self.scopes.values())
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

            merged_section = merge_yaml(merged_section, data)

        # no config files -- empty config.
        if section not in merged_section:
            return syaml.syaml_dict()

        # take the top key off before returning.
        ret = merged_section[section]
        if isinstance(ret, dict):
            ret = syaml.syaml_dict(ret)
        return ret

    def get(self, path: str, default: Optional[Any] = None, scope: Optional[str] = None) -> Any:
        """Get a config section or a single value from one.

        Accepts a path syntax that allows us to grab nested config map
        entries.  Getting the 'config' section would look like::

            spack.config.get('config')

        and the ``dirty`` section in the ``config`` scope would be::

            spack.config.get('config:dirty')

        We use ``:`` as the separator, like YAML objects.
        """
        parts = process_config_path(path)
        section = parts.pop(0)

        value = self.get_config(section, scope=scope)

        while parts:
            key = parts.pop(0)
            # cannot use value.get(key, default) in case there is another part
            # and default is not a dict
            if key not in value:
                return default
            value = value[key]

        return value

    @_config_mutator
    def set(self, path: str, value: Any, scope: Optional[str] = None) -> None:
        """Convenience function for setting single values in config files.

        Accepts the path syntax described in ``get()``.
        """
        if ":" not in path:
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
        yield from self.scopes.values()

    def print_section(self, section: str, blame: bool = False, *, scope=None) -> None:
        """Print a configuration to stdout."""
        try:
            data = syaml.syaml_dict()
            data[section] = self.get_config(section, scope=scope)
            syaml.dump_config(data, stream=sys.stdout, default_flow_style=False, blame=blame)
        except (syaml.SpackYAMLError, OSError) as e:
            raise spack.error.ConfigError(f"cannot read '{section}' configuration") from e


@contextlib.contextmanager
def override(
    path_or_scope: Union[ConfigScope, str], value: Optional[Any] = None
) -> Generator[Union[lang.Singleton, Configuration], None, None]:
    """Simple way to override config settings within a context.

    Arguments:
        path_or_scope (ConfigScope or str): scope or single option to override
        value (object or None): value for the single option

    Temporarily push a scope on the current configuration, then remove it
    after the context completes. If a single option is provided, create
    an internal config scope for it and push/pop that scope.

    """
    if isinstance(path_or_scope, ConfigScope):
        overrides = path_or_scope
        CONFIG.push_scope(path_or_scope)
    else:
        base_name = _OVERRIDES_BASE_NAME
        # Ensure the new override gets a unique scope name
        current_overrides = [s.name for s in CONFIG.matching_scopes(rf"^{base_name}")]
        num_overrides = len(current_overrides)
        while True:
            scope_name = f"{base_name}{num_overrides}"
            if scope_name in current_overrides:
                num_overrides += 1
            else:
                break

        overrides = InternalConfigScope(scope_name)
        CONFIG.push_scope(overrides)
        CONFIG.set(path_or_scope, value, scope=scope_name)

    try:
        yield CONFIG
    finally:
        scope = CONFIG.remove_scope(overrides.name)
        assert scope is overrides


#: configuration scopes added on the command line set by ``spack.main.main()``
COMMAND_LINE_SCOPES: List[str] = []


def _add_platform_scope(
    cfg: Union[Configuration, lang.Singleton], name: str, path: str, writable: bool = True
) -> None:
    """Add a platform-specific subdirectory for the current platform."""
    platform = spack.platforms.host().name
    scope = DirectoryConfigScope(
        f"{name}/{platform}", os.path.join(path, platform), writable=writable
    )
    cfg.push_scope(scope)


def config_paths_from_entry_points() -> List[Tuple[str, str]]:
    """Load configuration paths from entry points

    A python package can register entry point metadata so that Spack can find
    its configuration by adding the following to the project's pyproject.toml:

    .. code-block:: toml

       [project.entry-points."spack.config"]
       baz = "baz:get_spack_config_path"

    The function ``get_spack_config_path`` returns the path to the package's
    spack configuration scope

    """
    config_paths: List[Tuple[str, str]] = []
    for entry_point in lang.get_entry_points(group="spack.config"):
        hook = entry_point.load()
        if callable(hook):
            config_path = hook()
            if config_path and os.path.exists(config_path):
                config_paths.append(("plugin-%s" % entry_point.name, str(config_path)))
    return config_paths


def _add_command_line_scopes(
    cfg: Union[Configuration, lang.Singleton], command_line_scopes: List[str]
) -> None:
    """Add additional scopes from the --config-scope argument, either envs or dirs."""
    import spack.environment.environment as env  # circular import

    for i, path in enumerate(command_line_scopes):
        name = f"cmd_scope_{i}"

        if env.exists(path):  # managed environment
            manifest = env.EnvironmentManifestFile(env.root(path))
        elif env.is_env_dir(path):  # anonymous environment
            manifest = env.EnvironmentManifestFile(path)
        elif os.path.isdir(path):  # directory with config files
            cfg.push_scope(DirectoryConfigScope(name, path, writable=False))
            _add_platform_scope(cfg, name, path, writable=False)
            continue
        else:
            raise spack.error.ConfigError(f"Invalid configuration scope: {path}")

        for scope in manifest.env_config_scopes:
            scope.name = f"{name}:{scope.name}"
            scope.writable = False
            cfg.push_scope(scope)


def create() -> Configuration:
    """Singleton Configuration instance.

    This constructs one instance associated with this module and returns
    it. It is bundled inside a function so that configuration can be
    initialized lazily.
    """
    cfg = Configuration()

    # first do the builtin, hardcoded defaults
    builtin = InternalConfigScope("_builtin", CONFIG_DEFAULTS)
    cfg.push_scope(builtin)

    # Builtin paths to configuration files in Spack
    configuration_paths = [
        # Default configuration scope is the lowest-level scope. These are
        # versioned with Spack and can be overridden by systems, sites or users
        CONFIGURATION_DEFAULTS_PATH
    ]

    disable_local_config = "SPACK_DISABLE_LOCAL_CONFIG" in os.environ

    # System configuration is per machine.
    # This is disabled if user asks for no local configuration.
    if not disable_local_config:
        configuration_paths.append(("system", spack.paths.system_config_path))

    # Site configuration is per spack instance, for sites or projects
    # No site-level configs should be checked into spack by default.
    configuration_paths.append(("site", os.path.join(spack.paths.etc_path)))

    # Python package's can register configuration scopes via entry_points
    configuration_paths.extend(config_paths_from_entry_points())

    # User configuration can override both spack defaults and site config
    # This is disabled if user asks for no local configuration.
    if not disable_local_config:
        configuration_paths.append(("user", spack.paths.user_config_path))

    # add each scope and its platform-specific directory
    for name, path in configuration_paths:
        cfg.push_scope(DirectoryConfigScope(name, path))

        # Each scope can have per-platfom overrides in subdirectories
        _add_platform_scope(cfg, name, path)

    # add command-line scopes
    _add_command_line_scopes(cfg, COMMAND_LINE_SCOPES)

    # we make a special scope for spack commands so that they can
    # override configuration options.
    cfg.push_scope(InternalConfigScope("command_line"))

    return cfg


#: This is the singleton configuration instance for Spack.
CONFIG: Union[Configuration, lang.Singleton] = lang.Singleton(create)


def add_from_file(filename: str, scope: Optional[str] = None) -> None:
    """Add updates to a config from a filename"""
    # Extract internal attributes, if we are dealing with an environment
    data = read_config_file(filename)
    if data is None:
        return

    if spack.schema.env.TOP_LEVEL_KEY in data:
        data = data[spack.schema.env.TOP_LEVEL_KEY]

    msg = (
        "unexpected 'None' value when retrieving configuration. "
        "Please submit a bug-report at https://github.com/spack/spack/issues"
    )
    assert data is not None, msg

    # update all sections from config dict
    # We have to iterate on keys to keep overrides from the file
    for section in data.keys():
        if section in SECTION_SCHEMAS.keys():
            # Special handling for compiler scope difference
            # Has to be handled after we choose a section
            if scope is None:
                scope = default_modify_scope(section)

            value = data[section]
            existing = get(section, scope=scope)
            new = merge_yaml(existing, value)

            # We cannot call config.set directly (set is a type)
            CONFIG.set(section, new, scope)


def add(fullpath: str, scope: Optional[str] = None) -> None:
    """Add the given configuration to the specified config scope.
    Add accepts a path. If you want to add from a filename, use add_from_file"""
    components = process_config_path(fullpath)

    has_existing_value = True
    path = ""
    override = False
    value = components[-1]
    if not isinstance(value, syaml.syaml_str):
        value = syaml.load_config(value)
    for idx, name in enumerate(components[:-1]):
        # First handle double colons in constructing path
        colon = "::" if override else ":" if path else ""
        path += colon + name
        if getattr(name, "override", False):
            override = True
        else:
            override = False

        # Test whether there is an existing value at this level
        existing = get(path, scope=scope)

        if existing is None:
            has_existing_value = False
            # We've nested further than existing config, so we need the
            # type information for validation to know how to handle bare
            # values appended to lists.
            existing = get_valid_type(path)

            # construct value from this point down
            for component in reversed(components[idx + 1 : -1]):
                value: Dict[str, str] = {component: value}  # type: ignore[no-redef]
            break

    if override:
        path += "::"

    if has_existing_value:
        existing = get(path, scope=scope)

    # append values to lists
    if isinstance(existing, list) and not isinstance(value, list):
        value: List[str] = [value]  # type: ignore[no-redef]

    # merge value into existing
    new = merge_yaml(existing, value)
    CONFIG.set(path, new, scope)


def get(path: str, default: Optional[Any] = None, scope: Optional[str] = None) -> Any:
    """Module-level wrapper for ``Configuration.get()``."""
    return CONFIG.get(path, default, scope)


def set(path: str, value: Any, scope: Optional[str] = None) -> None:
    """Convenience function for setting single values in config files.

    Accepts the path syntax described in ``get()``.
    """
    return CONFIG.set(path, value, scope)


def add_default_platform_scope(platform: str) -> None:
    plat_name = os.path.join("defaults", platform)
    plat_path = os.path.join(CONFIGURATION_DEFAULTS_PATH[1], platform)
    CONFIG.push_scope(DirectoryConfigScope(plat_name, plat_path))


def scopes() -> Dict[str, ConfigScope]:
    """Convenience function to get list of configuration scopes."""
    return CONFIG.scopes


def writable_scopes() -> List[ConfigScope]:
    """Return list of writable scopes. Higher-priority scopes come first in the list."""
    scopes = [x for x in CONFIG.scopes.values() if x.writable]
    scopes.reverse()
    return scopes


def writable_scope_names() -> List[str]:
    return list(x.name for x in writable_scopes())


def matched_config(cfg_path: str) -> List[Tuple[str, Any]]:
    return [(scope, get(cfg_path, scope=scope)) for scope in writable_scope_names()]


def change_or_add(
    section_name: str, find_fn: Callable[[str], bool], update_fn: Callable[[str], None]
) -> None:
    """Change or add a subsection of config, with additional logic to
    select a reasonable scope where the change is applied.

    Search through config scopes starting with the highest priority:
    the first matching a criteria (determined by ``find_fn``) is updated;
    if no such config exists, find the first config scope that defines
    any config for the named section; if no scopes define any related
    config, then update the highest-priority config scope.
    """
    configs_by_section = matched_config(section_name)

    found = False
    for scope, section in configs_by_section:
        found = find_fn(section)
        if found:
            break

    if found:
        update_fn(section)
        CONFIG.set(section_name, section, scope=scope)
        return

    # If no scope meets the criteria specified by ``find_fn``,
    # then look for a scope that has any content (for the specified
    # section name)
    for scope, section in configs_by_section:
        if section:
            update_fn(section)
            found = True
            break

    if found:
        CONFIG.set(section_name, section, scope=scope)
        return

    # If no scopes define any config for the named section, then
    # modify the highest-priority scope.
    scope, section = configs_by_section[0]
    update_fn(section)
    CONFIG.set(section_name, section, scope=scope)


def update_all(section_name: str, change_fn: Callable[[str], bool]) -> None:
    """Change a config section, which may have details duplicated
    across multiple scopes.
    """
    configs_by_section = matched_config("develop")

    for scope, section in configs_by_section:
        modified = change_fn(section)
        if modified:
            CONFIG.set(section_name, section, scope=scope)


def _validate_section_name(section: str) -> None:
    """Exit if the section is not a valid section."""
    if section not in SECTION_SCHEMAS:
        raise ConfigSectionError(
            f"Invalid config section: '{section}'. Options are: {' '.join(SECTION_SCHEMAS.keys())}"
        )


def validate(
    data: YamlConfigDict, schema: YamlConfigDict, filename: Optional[str] = None
) -> YamlConfigDict:
    """Validate data read in from a Spack YAML file.

    Arguments:
        data: data read from a Spack YAML file
        schema: jsonschema to validate data

    This leverages the line information (start_mark, end_mark) stored
    on Spack YAML structures.
    """
    import jsonschema

    try:
        spack.schema.Validator(schema).validate(data)
    except jsonschema.ValidationError as e:
        if hasattr(e.instance, "lc"):
            line_number = e.instance.lc.line + 1
        else:
            line_number = None
        raise ConfigFormatError(e, data, filename, line_number) from e
    # return the validated data so that we can access the raw data
    # mostly relevant for environments
    return data


def read_config_file(
    path: str, schema: Optional[YamlConfigDict] = None
) -> Optional[YamlConfigDict]:
    """Read a YAML configuration file.

    User can provide a schema for validation. If no schema is provided,
    we will infer the schema from the top-level key."""
    # Dev: Inferring schema and allowing it to be provided directly allows us
    # to preserve flexibility in calling convention (don't need to provide
    # schema when it's not necessary) while allowing us to validate against a
    # known schema when the top-level key could be incorrect.
    try:
        with open(path) as f:
            tty.debug(f"Reading config from file {path}")
            data = syaml.load_config(f)

        if data:
            if schema is None:
                key = next(iter(data))
                schema = _ALL_SCHEMAS[key]
            validate(data, schema)

        return data

    except FileNotFoundError:
        # Ignore nonexistent files.
        tty.debug(f"Skipping nonexistent config path {path}", level=3)
        return None

    except OSError as e:
        raise ConfigFileError(f"Path is not a file or is not readable: {path}: {str(e)}") from e

    except StopIteration as e:
        raise ConfigFileError(f"Config file is empty or is not a valid YAML dict: {path}") from e

    except syaml.SpackYAMLError as e:
        raise ConfigFileError(str(e)) from e


def _override(string: str) -> bool:
    """Test if a spack YAML string is an override.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `::`,
    and if they do, their values completely replace lower-precedence
    configs instead of merging into them.

    """
    return hasattr(string, "override") and string.override


def _append(string: str) -> bool:
    """Test if a spack YAML string is an override.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `+:`,
    and if they do, their values append lower-precedence
    configs.

    str, str : concatenate strings.
    [obj], [obj] : append lists.

    """
    return getattr(string, "append", False)


def _prepend(string: str) -> bool:
    """Test if a spack YAML string is an override.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `+:`,
    and if they do, their values prepend lower-precedence
    configs.

    str, str : concatenate strings.
    [obj], [obj] : prepend lists. (default behavior)
    """
    return getattr(string, "prepend", False)


def _mark_internal(data, name):
    """Add a simple name mark to raw YAML/JSON data.

    This is used by `spack config blame` to show where config lines came from.
    """
    if isinstance(data, dict):
        d = syaml.syaml_dict(
            (_mark_internal(k, name), _mark_internal(v, name)) for k, v in data.items()
        )
    elif isinstance(data, list):
        d = syaml.syaml_list(_mark_internal(e, name) for e in data)
    else:
        d = syaml.syaml_type(data)

    if syaml.markable(d):
        d._start_mark = syaml.name_mark(name)
        d._end_mark = syaml.name_mark(name)

    return d


def get_valid_type(path):
    """Returns an instance of a type that will pass validation for path.

    The instance is created by calling the constructor with no arguments.
    If multiple types will satisfy validation for data at the configuration
    path given, the priority order is ``list``, ``dict``, ``str``, ``bool``,
    ``int``, ``float``.
    """
    types = {
        "array": list,
        "object": syaml.syaml_dict,
        "string": str,
        "boolean": bool,
        "integer": int,
        "number": float,
    }

    components = process_config_path(path)
    section = components[0]

    # Use None to construct the test data
    test_data = None
    for component in reversed(components):
        test_data = {component: test_data}

    try:
        validate(test_data, SECTION_SCHEMAS[section])
    except (ConfigFormatError, AttributeError) as e:
        jsonschema_error = e.validation_error
        if jsonschema_error.validator == "type":
            return types[jsonschema_error.validator_value]()
        elif jsonschema_error.validator in ("anyOf", "oneOf"):
            for subschema in jsonschema_error.validator_value:
                schema_type = subschema.get("type")
                if schema_type is not None:
                    return types[schema_type]()
    else:
        return type(None)
    raise spack.error.ConfigError(f"Cannot determine valid type for path '{path}'.")


def remove_yaml(dest, source):
    """UnMerges source from dest; entries in source take precedence over dest.

    This routine may modify dest and should be assigned to dest, in
    case dest was None to begin with, e.g.:

       dest = remove_yaml(dest, source)

    In the result, elements from lists from ``source`` will not appear
    as elements of lists from ``dest``. Likewise, when iterating over keys
    or items in merged ``OrderedDict`` objects, keys from ``source`` will not
    appear as keys in ``dest``.

    Config file authors can optionally end any attribute in a dict
    with `::` instead of `:`, and the key will remove the entire section
    from ``dest``
    """

    def they_are(t):
        return isinstance(dest, t) and isinstance(source, t)

    # If source is None, overwrite with source.
    if source is None:
        return dest

    # Source list is prepended (for precedence)
    if they_are(list):
        # Make sure to copy ruamel comments
        dest[:] = [x for x in dest if x not in source]
        return dest

    # Source dict is merged into dest.
    elif they_are(dict):
        for sk, sv in source.items():
            # always remove the dest items. Python dicts do not overwrite
            # keys on insert, so this ensures that source keys are copied
            # into dest along with mark provenance (i.e., file/line info).
            unmerge = sk in dest
            old_dest_value = dest.pop(sk, None)

            if unmerge and not _override(sk):
                dest[sk] = remove_yaml(old_dest_value, sv)

        return dest

    # If we reach here source and dest are either different types or are
    # not both lists or dicts: replace with source.
    return dest


def merge_yaml(dest, source, prepend=False, append=False):
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

    `+:` will extend the default prepend merge strategy to include string concatenation
    `-:` will change the merge strategy to append, it also includes string concatentation
    """

    def they_are(t):
        return isinstance(dest, t) and isinstance(source, t)

    # If source is None, overwrite with source.
    if source is None:
        return None

    # Source list is prepended (for precedence)
    if they_are(list):
        if append:
            # Make sure to copy ruamel comments
            dest[:] = [x for x in dest if x not in source] + source
        else:
            # Make sure to copy ruamel comments
            dest[:] = source + [x for x in dest if x not in source]
        return dest

    # Source dict is merged into dest.
    elif they_are(dict):
        # save dest keys to reinsert later -- this ensures that  source items
        # come *before* dest in OrderdDicts
        dest_keys = [dk for dk in dest.keys() if dk not in source]

        for sk, sv in source.items():
            # always remove the dest items. Python dicts do not overwrite
            # keys on insert, so this ensures that source keys are copied
            # into dest along with mark provenance (i.e., file/line info).
            merge = sk in dest
            old_dest_value = dest.pop(sk, None)

            if merge and not _override(sk):
                dest[sk] = merge_yaml(old_dest_value, sv, _prepend(sk), _append(sk))
            else:
                # if sk ended with ::, or if it's new, completely override
                dest[sk] = copy.deepcopy(sv)

        # reinsert dest keys so they are last in the result
        for dk in dest_keys:
            dest[dk] = dest.pop(dk)

        return dest

    elif they_are(str):
        # Concatenate strings in prepend mode
        if prepend:
            return source + dest
        elif append:
            return dest + source

    # If we reach here source and dest are either different types or are
    # not both lists or dicts: replace with source.
    return copy.copy(source)


class ConfigPath:
    quoted_string = "(?:\"[^\"]+\")|(?:'[^']+')"
    unquoted_string = "[^:'\"]+"
    element = rf"(?:(?:{quoted_string})|(?:{unquoted_string}))"
    next_key_pattern = rf"({element}[+-]?)(?:\:|$)"

    @staticmethod
    def _split_front(string, extract):
        m = re.match(extract, string)
        if not m:
            return None, None
        token = m.group(1)
        return token, string[len(token) :]

    @staticmethod
    def _validate(path):
        """Example valid config paths:

        x:y:z
        x:"y":z
        x:y+:z
        x:y::z
        x:y+::z
        x:y:
        x:y::
        """
        first_key, path = ConfigPath._split_front(path, ConfigPath.next_key_pattern)
        if not first_key:
            raise ValueError(f"Config path does not start with a parse-able key: {path}")
        path_elements = [first_key]
        path_index = 1
        while path:
            separator, path = ConfigPath._split_front(path, r"(\:+)")
            if not separator:
                raise ValueError(f"Expected separator for {path}")

            path_elements[path_index - 1] += separator
            if not path:
                break

            element, remainder = ConfigPath._split_front(path, ConfigPath.next_key_pattern)
            if not element:
                # If we can't parse something as a key, then it must be a
                # value (if it's valid).
                try:
                    syaml.load_config(path)
                except spack.util.spack_yaml.SpackYAMLError as e:
                    raise ValueError(
                        "Remainder of path is not a valid key"
                        f" and does not parse as a value {path}"
                    ) from e
                element = path
                path = None  # The rest of the path was consumed into the value
            else:
                path = remainder

            path_elements.append(element)
            path_index += 1

        return path_elements

    @staticmethod
    def process(path):
        result = []
        quote = "['\"]"
        seen_override_in_path = False

        path_elements = ConfigPath._validate(path)
        last_element_idx = len(path_elements) - 1
        for i, element in enumerate(path_elements):
            override = False
            append = False
            prepend = False
            quoted = False
            if element.endswith("::") or (element.endswith(":") and i == last_element_idx):
                if seen_override_in_path:
                    raise syaml.SpackYAMLError(
                        "Meaningless second override indicator `::' in path `{0}'".format(path), ""
                    )
                override = True
                seen_override_in_path = True
            element = element.rstrip(":")

            if element.endswith("+"):
                prepend = True
            elif element.endswith("-"):
                append = True
            element = element.rstrip("+-")

            if re.match(f"^{quote}", element):
                quoted = True
            element = element.strip("'\"")

            if any([append, prepend, override, quoted]):
                element = syaml.syaml_str(element)
                if append:
                    element.append = True
                if prepend:
                    element.prepend = True
                if override:
                    element.override = True

            result.append(element)

        return result


def process_config_path(path: str) -> List[str]:
    """Process a path argument to config.set() that may contain overrides ('::' or
    trailing ':')

    Colons will be treated as static strings if inside of quotes,
    e.g. `this:is:a:path:'value:with:colon'` will yield:

        [this, is, a, path, value:with:colon]

    The path may consist only of keys (e.g. for a `get`) or may end in a value.
    Keys are always strings: if a user encloses a key in quotes, the quotes
    should be removed. Values with quotes should be treated as strings,
    but without quotes, may be parsed as a different yaml object (e.g.
    '{}' is a dict, but '"{}"' is a string).

    This function does not know whether the final element of the path is a
    key or value, so:

    * It must strip the quotes, in case it is a key (so we look for "key" and
      not '"key"'))
    * It must indicate somehow that the quotes were stripped, in case it is a
      value (so that we don't process '"{}"' as a YAML dict)

    Therefore, all elements with quotes are stripped, and then also converted
    to ``syaml_str`` (if treating the final element as a value, the caller
    should not parse it in this case).
    """
    return ConfigPath.process(path)


#
# Settings for commands that modify configuration
#
def default_modify_scope(section: str = "config") -> str:
    """Return the config scope that commands should modify by default.

    Commands that modify configuration by default modify the *highest*
    priority scope.

    Arguments:
        section (bool): Section for which to get the default scope.
            If this is not 'compilers', a general (non-platform) scope is used.
    """
    if section == "compilers":
        return CONFIG.highest_precedence_scope().name
    else:
        return CONFIG.highest_precedence_non_platform_scope().name


def _update_in_memory(data: YamlConfigDict, section: str) -> bool:
    """Update the format of the configuration data in memory.

    This function assumes the section is valid (i.e. validation
    is responsibility of the caller)

    Args:
        data: configuration data
        section: section of the configuration to update

    Returns:
        True if the data was changed, False otherwise
    """
    update_fn = ensure_latest_format_fn(section)
    changed = update_fn(data[section])
    return changed


def ensure_latest_format_fn(section: str) -> Callable[[YamlConfigDict], bool]:
    """Return a function that takes as input a dictionary read from
    a configuration file and update it to the latest format.

    The function returns True if there was any update, False otherwise.

    Args:
        section: section of the configuration e.g. "packages",
            "config", etc.
    """
    # The line below is based on the fact that every module we need
    # is already imported at the top level
    section_module = getattr(spack.schema, section)
    update_fn = getattr(section_module, "update", lambda x: False)
    return update_fn


@contextlib.contextmanager
def use_configuration(
    *scopes_or_paths: Union[ConfigScope, str]
) -> Generator[Configuration, None, None]:
    """Use the configuration scopes passed as arguments within the context manager.

    This function invalidates caches, and is therefore very slow.

    Args:
        *scopes_or_paths: scope objects or paths to be used

    Returns:
        Configuration object associated with the scopes passed as arguments
    """
    global CONFIG

    # Normalize input and construct a Configuration object
    configuration = _config_from(scopes_or_paths)
    CONFIG.clear_caches(), configuration.clear_caches()

    saved_config, CONFIG = CONFIG, configuration

    try:
        yield configuration
    finally:
        CONFIG = saved_config


@lang.memoized
def _config_from(scopes_or_paths: List[Union[ConfigScope, str]]) -> Configuration:
    scopes = []
    for scope_or_path in scopes_or_paths:
        # If we have a config scope we are already done
        if isinstance(scope_or_path, ConfigScope):
            scopes.append(scope_or_path)
            continue

        # Otherwise we need to construct it
        path = os.path.normpath(scope_or_path)
        assert os.path.isdir(path), f'"{path}" must be a directory'
        name = os.path.basename(path)
        scopes.append(DirectoryConfigScope(name, path))

    configuration = Configuration(*scopes)
    return configuration


def raw_github_gitlab_url(url: str) -> str:
    """Transform a github URL to the raw form to avoid undesirable html.

    Args:
        url: url to be converted to raw form

    Returns:
        Raw github/gitlab url or the original url
    """
    # Note we rely on GitHub to redirect the 'raw' URL returned here to the
    # actual URL under https://raw.githubusercontent.com/ with '/blob'
    # removed and or, '/blame' if needed.
    if "github" in url or "gitlab" in url:
        return url.replace("/blob/", "/raw/")

    return url


def collect_urls(base_url: str) -> list:
    """Return a list of configuration URLs.

    Arguments:
        base_url: URL for a configuration (yaml) file or a directory
            containing yaml file(s)

    Returns:
        List of configuration file(s) or empty list if none
    """
    if not base_url:
        return []

    extension = ".yaml"

    if base_url.endswith(extension):
        return [base_url]

    # Collect configuration URLs if the base_url is a "directory".
    _, links = web_util.spider(base_url, 0)
    return [link for link in links if link.endswith(extension)]


def fetch_remote_configs(url: str, dest_dir: str, skip_existing: bool = True) -> str:
    """Retrieve configuration file(s) at the specified URL.

    Arguments:
        url: URL for a configuration (yaml) file or a directory containing
            yaml file(s)
        dest_dir: destination directory
        skip_existing: Skip files that already exist in dest_dir if
            ``True``; otherwise, replace those files

    Returns:
        Path to the corresponding file if URL is or contains a
        single file and it is the only file in the destination directory or
        the root (dest_dir) directory if multiple configuration files exist
        or are retrieved.
    """

    def _fetch_file(url):
        raw = raw_github_gitlab_url(url)
        tty.debug(f"Reading config from url {raw}")
        return web_util.fetch_url_text(raw, dest_dir=dest_dir)

    if not url:
        raise ConfigFileError("Cannot retrieve configuration without a URL")

    # Return the local path to the cached configuration file OR to the
    # directory containing the cached configuration files.
    config_links = collect_urls(url)
    existing_files = os.listdir(dest_dir) if os.path.isdir(dest_dir) else []

    paths = []
    for config_url in config_links:
        basename = os.path.basename(config_url)
        if skip_existing and basename in existing_files:
            tty.warn(
                f"Will not fetch configuration from {config_url} since a "
                f"version already exists in {dest_dir}"
            )
            path = os.path.join(dest_dir, basename)
        else:
            path = _fetch_file(config_url)

        if path:
            paths.append(path)

    if paths:
        return dest_dir if len(paths) > 1 else paths[0]

    raise ConfigFileError(f"Cannot retrieve configuration (yaml) from {url}")


def get_mark_from_yaml_data(obj):
    """Try to get ``spack.util.spack_yaml`` mark from YAML data.

    We try the object, and if that fails we try its first member (if it's a container).

    Returns:
        mark if one is found, otherwise None.
    """
    # mark of object itelf
    mark = getattr(obj, "_start_mark", None)
    if mark:
        return mark

    # mark of first member if it is a container
    if isinstance(obj, (list, dict)):
        first_member = next(iter(obj), None)
        if first_member:
            mark = getattr(first_member, "_start_mark", None)

    return mark


def determine_number_of_jobs(
    *,
    parallel: bool = False,
    max_cpus: int = cpus_available(),
    config: Optional[Configuration] = None,
) -> int:
    """
    Packages that require sequential builds need 1 job. Otherwise we use the
    number of jobs set on the command line. If not set, then we use the config
    defaults (which is usually set through the builtin config scope), but we
    cap to the number of CPUs available to avoid oversubscription.

    Parameters:
        parallel: true when package supports parallel builds
        max_cpus: maximum number of CPUs to use (defaults to cpus_available())
        config: configuration object (defaults to global config)
    """
    if not parallel:
        return 1

    cfg = config or CONFIG

    # Command line overrides all
    try:
        command_line = cfg.get("config:build_jobs", default=None, scope="command_line")
        if command_line is not None:
            return command_line
    except ValueError:
        pass

    return min(max_cpus, cfg.get("config:build_jobs", 16))


class ConfigSectionError(spack.error.ConfigError):
    """Error for referring to a bad config section name in a configuration."""


class ConfigFileError(spack.error.ConfigError):
    """Issue reading or accessing a configuration file."""


class ConfigFormatError(spack.error.ConfigError):
    """Raised when a configuration format does not match its schema."""

    def __init__(
        self,
        validation_error,
        data: YamlConfigDict,
        filename: Optional[str] = None,
        line: Optional[int] = None,
    ) -> None:
        # spack yaml has its own file/line marks -- try to find them
        # we prioritize these over the inputs
        self.validation_error = validation_error
        mark = self._get_mark(validation_error, data)
        if mark:
            filename = mark.name
            line = mark.line + 1

        self.filename = filename  # record this for ruamel.yaml

        # construct location
        location = "<unknown file>"
        if filename:
            location = f"{filename}"
        if line is not None:
            location += f":{line:d}"

        message = f"{location}: {validation_error.message}"
        super().__init__(message)

    def _get_mark(self, validation_error, data):
        """Get the file/line mark fo a validation error from a Spack YAML file."""

        # Try various places, starting with instance and parent
        for obj in (validation_error.instance, validation_error.parent):
            mark = get_mark_from_yaml_data(obj)
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
                mark = getattr(keylist[idx], "_start_mark", None)
                if mark:
                    return mark

        # give up and return None if nothing worked
        return None
