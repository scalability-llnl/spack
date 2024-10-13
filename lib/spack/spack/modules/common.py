# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Here we consolidate the logic for creating an abstract description
of the information that module systems need.

This information maps **a single spec** to:

  * a unique module filename
  * the module file content

and is divided among four classes:

  * a configuration class that provides a convenient interface to query
    details about the configuration for the spec under consideration.

  * a layout class that provides the information associated with module
    file names and directories

  * a context class that provides the dictionary used by the template engine
    to generate the module file

  * a writer that collects and uses the information above to either write
    or remove the module file

Each of the four classes needs to be sub-classed when implementing a new
module type.
"""
import collections
import contextlib
import copy
import datetime
import inspect
import os.path
import re
import string
from typing import List, Optional

import llnl.util.filesystem
import llnl.util.tty as tty
from llnl.util.lang import dedupe, memoized

import spack.build_environment
import spack.config
import spack.deptypes as dt
import spack.environment
import spack.error
import spack.paths
import spack.projections as proj
import spack.schema.environment
import spack.spec
import spack.store
import spack.tengine as tengine
import spack.user_environment
import spack.util.environment
import spack.util.file_permissions as fp
import spack.util.path
import spack.util.spack_yaml as syaml
from spack.context import Context


#: config section for this file
def configuration(module_set_name):
    config_path = f"modules:{module_set_name}"
    return spack.config.get(config_path, {})


#: Valid tokens for naming scheme and env variable names
_valid_tokens = (
    "name",
    "version",
    "compiler",
    "compiler.name",
    "compiler.version",
    "architecture",
    # tokens from old-style format strings
    "package",
    "compilername",
    "compilerver",
)


_FORMAT_STRING_RE = re.compile(r"({[^}]*})")


def _format_env_var_name(spec, var_name_fmt):
    """Format the variable name, but uppercase any formatted fields."""
    fmt_parts = _FORMAT_STRING_RE.split(var_name_fmt)
    return "".join(
        spec.format(part).upper() if _FORMAT_STRING_RE.match(part) else part for part in fmt_parts
    )


def _check_tokens_are_valid(format_string, message):
    """Checks that the tokens used in the format string are valid in
    the context of module file and environment variable naming.

    Args:
        format_string (str): string containing the format to be checked. This
            is supposed to be a 'template' for ``Spec.format``

        message (str): first sentence of the error message in case invalid
            tokens are found

    """
    named_tokens = re.findall(r"{(\w*)}", format_string)
    invalid_tokens = [x for x in named_tokens if x.lower() not in _valid_tokens]
    if invalid_tokens:
        raise RuntimeError(
            f"{message} [{', '.join(invalid_tokens)}]. "
            f"Did you check your 'modules.yaml' configuration?"
        )


def update_dictionary_extending_lists(target, update):
    """Updates a dictionary, but extends lists instead of overriding them.

    Args:
        target: dictionary to be updated
        update: update to be applied
    """
    for key in update:
        value = target.get(key, None)
        if isinstance(value, list):
            target[key].extend(update[key])
        elif isinstance(value, dict):
            update_dictionary_extending_lists(target[key], update[key])
        else:
            target[key] = update[key]


def dependencies(spec: spack.spec.Spec, request: str = "all") -> List[spack.spec.Spec]:
    """Returns the list of dependent specs for a given spec.

    Args:
        spec: spec to be analyzed
        request: one of "none", "run", "direct", "all"

    Returns:
        list of requested dependencies
    """
    if request == "none":
        return []
    elif request == "run":
        return spec.dependencies(deptype=dt.RUN)
    elif request == "direct":
        return spec.dependencies(deptype=dt.RUN | dt.LINK)
    elif request == "all":
        return list(spec.traverse(order="topo", deptype=dt.LINK | dt.RUN, root=False))

    raise ValueError(f'request "{request}" is not one of "none", "direct", "run", "all"')


def merge_config_rules(configuration, spec):
    """Parses the module specific part of a configuration and returns a
    dictionary containing the actions to be performed on the spec passed as
    an argument.

    Args:
        configuration: module specific configuration (e.g. entries under
            the top-level 'tcl' key)
        spec: spec for which we need to generate a module file

    Returns:
        dict: actions to be taken on the spec passed as an argument
    """
    # The keyword 'all' is always evaluated first, all the others are
    # evaluated in order of appearance in the module file
    spec_configuration = copy.deepcopy(configuration.get("all", {}))
    for constraint, action in configuration.items():
        if spec.satisfies(constraint):
            if hasattr(constraint, "override") and constraint.override:
                spec_configuration = {}
            update_dictionary_extending_lists(spec_configuration, copy.deepcopy(action))

    # Transform keywords for dependencies or prerequisites into a list of spec

    # Which modulefiles we want to autoload
    autoload_strategy = spec_configuration.get("autoload", "direct")
    spec_configuration["autoload"] = dependencies(spec, autoload_strategy)

    # Which instead we want to mark as prerequisites
    prerequisite_strategy = spec_configuration.get("prerequisites", "none")
    spec_configuration["prerequisites"] = dependencies(spec, prerequisite_strategy)

    # Attach options that are spec-independent to the spec-specific
    # configuration

    # Hash length in module files
    hash_length = configuration.get("hash_length", 7)
    spec_configuration["hash_length"] = hash_length

    verbose = configuration.get("verbose", False)
    spec_configuration["verbose"] = verbose

    # module defaults per-package
    defaults = configuration.get("defaults", [])
    spec_configuration["defaults"] = defaults

    return spec_configuration


def root_path(name, module_set_name):
    """Returns the root folder for module file installation.

    Args:
        name: name of the module system to be used (e.g. 'tcl')
        module_set_name: name of the set of module configs to use

    Returns:
        root folder for module file installation
    """
    defaults = {"lmod": "$spack/share/spack/lmod", "tcl": "$spack/share/spack/modules"}
    # Root folders where the various module files should be written
    roots = spack.config.get(f"modules:{module_set_name}:roots", {})

    # Merge config values into the defaults so we prefer configured values
    roots = spack.config.merge_yaml(defaults, roots)

    path = roots.get(name, os.path.join(spack.paths.share_path, name))
    return spack.util.path.canonicalize_path(path)


def generate_module_index(root, modules, overwrite=False):
    index_path = os.path.join(root, "module-index.yaml")
    if overwrite or not os.path.exists(index_path):
        entries = syaml.syaml_dict()
    else:
        with open(index_path) as index_file:
            yaml_content = syaml.load(index_file)
            entries = yaml_content["module_index"]

    for m in modules:
        entry = {"path": m.layout.filename, "use_name": m.layout.use_name}
        entries[m.spec.dag_hash()] = entry
    index = {"module_index": entries}
    llnl.util.filesystem.mkdirp(root)
    with open(index_path, "w") as index_file:
        syaml.dump(index, default_flow_style=False, stream=index_file)


def _generate_upstream_module_index():
    module_indices = read_module_indices()

    return UpstreamModuleIndex(spack.store.STORE.db, module_indices)


upstream_module_index = llnl.util.lang.Singleton(_generate_upstream_module_index)


ModuleIndexEntry = collections.namedtuple("ModuleIndexEntry", ["path", "use_name"])


def read_module_index(root):
    index_path = os.path.join(root, "module-index.yaml")
    if not os.path.exists(index_path):
        return {}
    with open(index_path) as index_file:
        return _read_module_index(index_file)


def _read_module_index(str_or_file):
    """Read in the mapping of spec hash to module location/name. For a given
    Spack installation there is assumed to be (at most) one such mapping
    per module type."""
    yaml_content = syaml.load(str_or_file)
    index = {}
    yaml_index = yaml_content["module_index"]
    for dag_hash, module_properties in yaml_index.items():
        index[dag_hash] = ModuleIndexEntry(
            module_properties["path"], module_properties["use_name"]
        )
    return index


def read_module_indices():
    other_spack_instances = spack.config.get("upstreams") or {}

    module_indices = []

    for install_properties in other_spack_instances.values():
        module_type_to_index = {}
        module_type_to_root = install_properties.get("modules", {})
        for module_type, root in module_type_to_root.items():
            module_type_to_index[module_type] = read_module_index(root)
        module_indices.append(module_type_to_index)

    return module_indices


class UpstreamModuleIndex:
    """This is responsible for taking the individual module indices of all
    upstream Spack installations and locating the module for a given spec
    based on which upstream install it is located in."""

    def __init__(self, local_db, module_indices):
        self.local_db = local_db
        self.upstream_dbs = local_db.upstream_dbs
        self.module_indices = module_indices

    def upstream_module(self, spec, module_type):
        db_for_spec = self.local_db.db_for_spec_hash(spec.dag_hash())
        if db_for_spec in self.upstream_dbs:
            db_index = self.upstream_dbs.index(db_for_spec)
        elif db_for_spec:
            raise spack.error.SpackError(f"Unexpected: {spec} is installed locally")
        else:
            raise spack.error.SpackError(f"Unexpected: no install DB found for {spec}")
        module_index = self.module_indices[db_index]
        module_type_index = module_index.get(module_type, {})
        if not module_type_index:
            tty.debug(
                f"No {module_type} modules associated with the Spack instance "
                f"where {spec} is installed"
            )
            return None
        if spec.dag_hash() in module_type_index:
            return module_type_index[spec.dag_hash()]
        else:
            tty.debug(f"No module is available for upstream package {spec}")
            return None


class BaseConfiguration:
    """Manipulates the information needed to generate a module file to make
    querying easier. It needs to be sub-classed for specific module types.
    """

    default_projections = {"all": "{name}/{version}-{compiler.name}-{compiler.version}"}

    def __init__(self, spec: spack.spec.Spec, module_set_name: str, explicit: bool) -> None:
        # Module where type(self) is defined
        m = inspect.getmodule(self)
        assert m is not None  # make mypy happy
        self.module = m
        # Spec for which we want to generate a module file
        self.spec = spec
        self.name = module_set_name
        self.explicit = explicit
        # Dictionary of configuration options that should be applied
        # to the spec
        self.conf = merge_config_rules(self.module.configuration(self.name), self.spec)

    @property
    def projections(self):
        """Projection from specs to module names"""
        # backwards compatiblity for naming_scheme key
        conf = self.module.configuration(self.name)
        if "naming_scheme" in conf:
            default = {"all": conf["naming_scheme"]}
        else:
            default = self.default_projections
        projections = conf.get("projections", default)

        # Ensure the named tokens we are expanding are allowed, see
        # issue #2884 for reference
        msg = "some tokens cannot be part of the module naming scheme"
        for projection in projections.values():
            _check_tokens_are_valid(projection, message=msg)

        return projections

    @property
    def template(self):
        """Returns the name of the template to use for the module file
        or None if not specified in the configuration.
        """
        return self.conf.get("template", None)

    @property
    def defaults(self):
        """Returns the specs configured as defaults or []."""
        return self.conf.get("defaults", [])

    @property
    def env(self):
        """List of environment modifications that should be done in the
        module.
        """
        return spack.schema.environment.parse(self.conf.get("environment", {}))

    @property
    def suffixes(self):
        """List of suffixes that should be appended to the module
        file name.
        """
        suffixes = []
        for constraint, suffix in self.conf.get("suffixes", {}).items():
            if constraint in self.spec:
                suffixes.append(suffix)
        suffixes = list(dedupe(suffixes))
        # For hidden modules we can always add a fixed length hash as suffix, since it guards
        # against file name clashes, and the module is not exposed to the user anyways.
        if self.hidden:
            suffixes.append(self.spec.dag_hash(length=7))
        elif self.hash:
            suffixes.append(self.hash)
        return suffixes

    @property
    def hash(self):
        """Hash tag for the module or None"""
        hash_length = self.conf.get("hash_length", 7)
        if hash_length != 0:
            return self.spec.dag_hash(length=hash_length)
        return None

    @property
    def conflicts(self):
        """Conflicts for this module file"""
        return self.conf.get("conflict", [])

    @property
    def excluded(self):
        """Returns True if the module has been excluded, False otherwise."""

        # A few variables for convenience of writing the method
        spec = self.spec
        conf = self.module.configuration(self.name)

        # Compute the list of matching include / exclude rules, and whether excluded as implicit
        include_matches = [x for x in conf.get("include", []) if spec.satisfies(x)]
        exclude_matches = [x for x in conf.get("exclude", []) if spec.satisfies(x)]
        excluded_as_implicit = not self.explicit and conf.get("exclude_implicits", False)

        def debug_info(line_header, match_list):
            if match_list:
                tty.debug(f"\t{line_header} : {spec.cshort_spec}")
                for rule in match_list:
                    tty.debug(f"\t\tmatches rule: {rule}")

        debug_info("INCLUDE", include_matches)
        debug_info("EXCLUDE", exclude_matches)

        if excluded_as_implicit:
            tty.debug(f"\tEXCLUDED_AS_IMPLICIT : {spec.cshort_spec}")

        return not include_matches and (exclude_matches or excluded_as_implicit)

    @property
    def hidden(self):
        """Returns True if the module has been hidden, False otherwise."""

        conf = self.module.configuration(self.name)

        hidden_as_implicit = not self.explicit and conf.get("hide_implicits", False)

        if hidden_as_implicit:
            tty.debug(f"\tHIDDEN_AS_IMPLICIT : {self.spec.cshort_spec}")

        return hidden_as_implicit

    @property
    def context(self):
        return self.conf.get("context", {})

    @property
    def specs_to_load(self):
        """List of specs that should be loaded in the module file."""
        return self._create_list_for("autoload")

    @property
    def literals_to_load(self):
        """List of literal modules to be loaded."""
        return self.conf.get("load", [])

    @property
    def specs_to_prereq(self):
        """List of specs that should be prerequisite of the module file."""
        return self._create_list_for("prerequisites")

    @property
    def exclude_env_vars(self):
        """List of variables that should be left unmodified."""
        filter_subsection = self.conf.get("filter", {})
        return filter_subsection.get("exclude_env_vars", {})

    def _create_list_for(self, what):
        include = []
        for item in self.conf[what]:
            if not self.module.make_configuration(item, self.name).excluded:
                include.append(item)
        return include

    @property
    def verbose(self):
        """Returns True if the module file needs to be verbose, False
        otherwise
        """
        return self.conf.get("verbose")


class BaseFileLayout:
    """Provides information on the layout of module files. Needs to be
    sub-classed for specific module types.
    """

    #: This needs to be redefined
    extension: Optional[str] = None

    def __init__(self, configuration):
        self.conf = configuration

    @property
    def spec(self):
        """Spec under consideration"""
        return self.conf.spec

    def dirname(self):
        """Root folder for module files of this type."""
        module_system = str(self.conf.module.__name__).split(".")[-1]
        return root_path(module_system, self.conf.name)

    @property
    def use_name(self):
        """Returns the 'use' name of the module i.e. the name you have to type
        to console to use it. This implementation fits the needs of most
        non-hierarchical layouts.
        """
        projection = proj.get_projection(self.conf.projections, self.spec)
        if not projection:
            projection = self.conf.default_projections["all"]

        name = self.spec.format_path(projection)
        # Not everybody is working on linux...
        parts = name.split("/")
        name = os.path.join(*parts)
        # Add optional suffixes based on constraints
        path_elements = [name] + self.conf.suffixes
        return "-".join(path_elements)

    @property
    def filename(self):
        """Name of the module file for the current spec."""
        # Just the name of the file
        filename = self.use_name
        if self.extension:
            filename = f"{self.use_name}.{self.extension}"
        # Architecture sub-folder
        arch_folder_conf = spack.config.get("modules:%s:arch_folder" % self.conf.name, True)
        if arch_folder_conf:
            # include an arch specific folder between root and filename
            arch_folder = str(self.spec.architecture)
            filename = os.path.join(arch_folder, filename)
        # Return the absolute path
        return os.path.join(self.dirname(), filename)


class BaseContext(tengine.Context):
    """Provides the base context needed for template rendering.

    This class needs to be sub-classed for specific module types. The
    following attributes need to be implemented:

    - fields

    """

    def __init__(self, configuration):
        self.conf = configuration

    @tengine.context_property
    def spec(self):
        return self.conf.spec

    @tengine.context_property
    def timestamp(self):
        return datetime.datetime.now()

    @tengine.context_property
    def category(self):
        return getattr(self.spec, "category", "spack")

    @tengine.context_property
    def short_description(self):
        # If we have a valid docstring return the first paragraph.
        docstring = type(self.spec.package).__doc__
        if docstring:
            value = docstring.split("\n\n")[0]
            # Transform tabs and friends into spaces
            value = re.sub(r"\s+", " ", value)
            # Turn double quotes into single quotes (double quotes are needed
            # to start and end strings)
            value = re.sub(r'"', "'", value)
            return value
        # Otherwise the short description is just the package + version
        return self.spec.format("{name} {@version}")

    @tengine.context_property
    def long_description(self):
        # long description is the docstring with reduced whitespace.
        if self.spec.package.__doc__:
            return re.sub(r"\s+", " ", self.spec.package.__doc__)
        return None

    @tengine.context_property
    def configure_options(self):
        pkg = self.spec.package

        # If the spec is external Spack doesn't know its configure options
        if self.spec.external:
            msg = "unknown, software installed outside of Spack"
            return msg

        if os.path.exists(pkg.install_configure_args_path):
            with open(pkg.install_configure_args_path) as args_file:
                return spack.util.path.padding_filter(args_file.read())

        # Returning a false-like value makes the default templates skip
        # the configure option section
        return None

    def modification_needs_formatting(self, modification):
        """Returns True if environment modification entry needs to be formatted."""
        return (
            not isinstance(modification, (spack.util.environment.SetEnv)) or not modification.raw
        )

    @tengine.context_property
    @memoized
    def environment_modifications(self):
        """List of environment modifications to be processed."""
        # Modifications guessed by inspecting the spec prefix
        prefix_inspections = syaml.syaml_dict()
        spack.config.merge_yaml(
            prefix_inspections, spack.config.get("modules:prefix_inspections", {})
        )
        spack.config.merge_yaml(
            prefix_inspections,
            spack.config.get(f"modules:{self.conf.name}:prefix_inspections", {}),
        )

        use_view = spack.config.get(f"modules:{self.conf.name}:use_view", False)

        assert isinstance(use_view, (bool, str))

        if use_view:
            env = spack.environment.active_environment()
            if not env:
                raise spack.environment.SpackEnvironmentViewError(
                    "Module generation with views requires active environment"
                )

            view_name = spack.environment.default_view_name if use_view is True else use_view

            if not env.has_view(view_name):
                raise spack.environment.SpackEnvironmentViewError(
                    f"View {view_name} not found in environment {env.name} when generating modules"
                )

            view = env.views[view_name]
        else:
            view = None

        env = spack.util.environment.inspect_path(
            self.spec.prefix, prefix_inspections, exclude=spack.util.environment.is_system_path
        )

        # Let the extendee/dependency modify their extensions/dependencies

        # The only thing we care about is `setup_dependent_run_environment`, but
        # for that to work, globals have to be set on the package modules, and the
        # whole chain of setup_dependent_package has to be followed from leaf to spec.
        # So: just run it here, but don't collect env mods.
        spack.build_environment.SetupContext(
            self.spec, context=Context.RUN
        ).set_all_package_py_globals()

        # Then run setup_dependent_run_environment before setup_run_environment.
        for dep in self.spec.dependencies(deptype=("link", "run")):
            dep.package.setup_dependent_run_environment(env, self.spec)
        self.spec.package.setup_run_environment(env)

        # Project the environment variables from prefix to view if needed
        if view and self.spec in view:
            spack.user_environment.project_env_mods(
                *self.spec.traverse(deptype=dt.LINK | dt.RUN), view=view, env=env
            )

        # Modifications required from modules.yaml
        env.extend(self.conf.env)

        # List of variables that are excluded in modules.yaml
        exclude = self.conf.exclude_env_vars

        # We may have tokens to substitute in environment commands
        for x in env:
            # Ensure all the tokens are valid in this context
            msg = "some tokens cannot be expanded in an environment variable name"

            _check_tokens_are_valid(x.name, message=msg)
            x.name = _format_env_var_name(self.spec, x.name)
            if self.modification_needs_formatting(x):
                try:
                    # Not every command has a value
                    x.value = self.spec.format(x.value)
                except AttributeError:
                    pass
            x.name = str(x.name).replace("-", "_")

        return [(type(x).__name__, x) for x in env if x.name not in exclude]

    @tengine.context_property
    def has_manpath_modifications(self):
        """True if MANPATH environment variable is modified."""
        for modification_type, cmd in self.environment_modifications:
            if not isinstance(
                cmd, (spack.util.environment.PrependPath, spack.util.environment.AppendPath)
            ):
                continue
            if cmd.name == "MANPATH":
                return True
        else:
            return False

    @tengine.context_property
    def conflicts(self):
        """List of conflicts for the module file."""
        fmts = []
        projection = proj.get_projection(self.conf.projections, self.spec)
        for item in self.conf.conflicts:
            self._verify_conflict_naming_consistency_or_raise(item, projection)
            item = self.spec.format(item)
            fmts.append(item)
        return fmts

    def _verify_conflict_naming_consistency_or_raise(self, item, projection):
        f = string.Formatter()
        errors = []
        if len([x for x in f.parse(item)]) > 1:
            for naming_dir, conflict_dir in zip(projection.split("/"), item.split("/")):
                if naming_dir != conflict_dir:
                    errors.extend(
                        [
                            f"spec={self.spec.cshort_spec}",
                            f"conflict_scheme={item}",
                            f"naming_scheme={projection}",
                        ]
                    )
        if errors:
            raise ModulesError(
                message="conflict scheme does not match naming scheme",
                long_message="\n    ".join(errors),
            )

    @tengine.context_property
    def autoload(self):
        """List of modules that needs to be loaded automatically."""
        # From 'autoload' configuration option
        specs = self._create_module_list_of("specs_to_load")
        # From 'load' configuration option
        literals = self.conf.literals_to_load
        return specs + literals

    def _create_module_list_of(self, what):
        m = self.conf.module
        name = self.conf.name
        return [m.make_layout(x, name).use_name for x in getattr(self.conf, what)]

    @tengine.context_property
    def verbose(self):
        """Verbosity level."""
        return self.conf.verbose


class BaseModuleFileWriter:
    default_template: str
    hide_cmd_format: str
    modulerc_header: List[str]

    def __init__(
        self, spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
    ) -> None:
        self.spec = spec

        # This class is meant to be derived. Get the module of the
        # actual writer.
        self.module = inspect.getmodule(self)
        assert self.module is not None  # make mypy happy
        m = self.module

        # Create the triplet of configuration/layout/context
        self.conf = m.make_configuration(spec, module_set_name, explicit)
        self.layout = m.make_layout(spec, module_set_name, explicit)
        self.context = m.make_context(spec, module_set_name, explicit)

        # Check if a default template has been defined,
        # throw if not found
        try:
            self.default_template
        except AttributeError:
            msg = "'{0}' object has no attribute 'default_template'\n"
            msg += "Did you forget to define it in the class?"
            name = type(self).__name__
            raise DefaultTemplateNotDefined(msg.format(name))

        # Check if format for module hide command has been defined,
        # throw if not found
        try:
            self.hide_cmd_format
        except AttributeError:
            msg = "'{0}' object has no attribute 'hide_cmd_format'\n"
            msg += "Did you forget to define it in the class?"
            name = type(self).__name__
            raise HideCmdFormatNotDefined(msg.format(name))

        # Check if modulerc header content has been defined,
        # throw if not found
        try:
            self.modulerc_header
        except AttributeError:
            msg = "'{0}' object has no attribute 'modulerc_header'\n"
            msg += "Did you forget to define it in the class?"
            name = type(self).__name__
            raise ModulercHeaderNotDefined(msg.format(name))

    def _get_template(self):
        """Gets the template that will be rendered for this spec."""
        # Get templates and put them in the order of importance:
        # 1. template specified in "modules.yaml"
        # 2. template specified in a package directly
        # 3. default template (must be defined, check in __init__)
        module_system_name = str(self.module.__name__).split(".")[-1]
        package_attribute = f"{module_system_name}_template"
        choices = [
            self.conf.template,
            getattr(self.spec.package, package_attribute, None),
            self.default_template,  # This is always defined at this point
        ]
        # Filter out false-ish values
        choices = list(filter(lambda x: bool(x), choices))
        # ... and return the first match
        return choices.pop(0)

    def write(self, overwrite=False):
        """Writes the module file.

        Args:
            overwrite (bool): if True it is fine to overwrite an already
                existing file. If False the operation is skipped an we print
                a warning to the user.
        """
        # Return immediately if the module is excluded
        if self.conf.excluded:
            msg = "\tNOT WRITING: {0} [EXCLUDED]"
            tty.debug(msg.format(self.spec.cshort_spec))
            return

        # Print a warning in case I am accidentally overwriting
        # a module file that is already there (name clash)
        if not overwrite and os.path.exists(self.layout.filename):
            message = "Module file {0.filename} exists and will not be overwritten"
            tty.warn(message.format(self.layout))
            return

        # If we are here it means it's ok to write the module file
        msg = "\tWRITE: {0} [{1}]"
        tty.debug(msg.format(self.spec.cshort_spec, self.layout.filename))

        # If the directory where the module should reside does not exist
        # create it
        module_dir = os.path.dirname(self.layout.filename)
        if not os.path.exists(module_dir):
            llnl.util.filesystem.mkdirp(module_dir)

        # Get the template for the module
        template_name = self._get_template()
        import jinja2

        try:
            env = tengine.make_environment()
            template = env.get_template(template_name)
        except jinja2.TemplateNotFound:
            # If the template was not found raise an exception with a little
            # more information
            msg = "template '{0}' was not found for '{1}'"
            name = type(self).__name__
            msg = msg.format(template_name, name)
            raise ModulesTemplateNotFoundError(msg)

        # Construct the context following the usual hierarchy of updates:
        # 1. start with the default context from the module writer class
        # 2. update with package specific context
        # 3. update with 'modules.yaml' specific context

        context = self.context.to_dict()

        # Attribute from package
        module_name = str(self.module.__name__).split(".")[-1]
        attr_name = f"{module_name}_context"
        pkg_update = getattr(self.spec.package, attr_name, {})
        context.update(pkg_update)

        # Context key in modules.yaml
        conf_update = self.conf.context
        context.update(conf_update)

        # Render the template
        text = template.render(context)
        # Write it to file
        with open(self.layout.filename, "w") as f:
            f.write(text)

        # Set the file permissions of the module to match that of the package
        if os.path.exists(self.layout.filename):
            fp.set_permissions_by_spec(self.layout.filename, self.spec)

        # Symlink defaults if needed
        self.update_module_defaults()

        # record module hiddenness if implicit
        self.update_module_hiddenness()

    def update_module_defaults(self):
        if any(self.spec.satisfies(default) for default in self.conf.defaults):
            # This spec matches a default, it needs to be symlinked to default
            # Symlink to a tmp location first and move, so that existing
            # symlinks do not cause an error.
            default_path = os.path.join(os.path.dirname(self.layout.filename), "default")
            default_tmp = os.path.join(os.path.dirname(self.layout.filename), ".tmp_spack_default")
            os.symlink(self.layout.filename, default_tmp)
            os.rename(default_tmp, default_path)

    def update_module_hiddenness(self, remove=False):
        """Update modulerc file corresponding to module to add or remove
        command that hides module depending on its hidden state.

        Args:
            remove (bool): if True, hiddenness information for module is
                removed from modulerc.
        """
        modulerc_path = self.layout.modulerc
        hide_module_cmd = self.hide_cmd_format % self.layout.use_name
        hidden = self.conf.hidden and not remove
        modulerc_exists = os.path.exists(modulerc_path)
        updated = False

        if modulerc_exists:
            # retrieve modulerc content
            with open(modulerc_path) as f:
                content = f.readlines()
                content = "".join(content).split("\n")
                # remove last empty item if any
                if len(content[-1]) == 0:
                    del content[-1]
            already_hidden = hide_module_cmd in content

            # remove hide command if module not hidden
            if already_hidden and not hidden:
                content.remove(hide_module_cmd)
                updated = True

            # add hide command if module is hidden
            elif not already_hidden and hidden:
                if len(content) == 0:
                    content = self.modulerc_header.copy()
                content.append(hide_module_cmd)
                updated = True
        else:
            content = self.modulerc_header.copy()
            if hidden:
                content.append(hide_module_cmd)
                updated = True

        # no modulerc file change if no content update
        if updated:
            is_empty = content == self.modulerc_header or len(content) == 0
            # remove existing modulerc if empty
            if modulerc_exists and is_empty:
                os.remove(modulerc_path)
            # create or update modulerc
            elif content != self.modulerc_header:
                # ensure file ends with a newline character
                content.append("")
                with open(modulerc_path, "w") as f:
                    f.write("\n".join(content))

    def remove(self):
        """Deletes the module file."""
        mod_file = self.layout.filename
        if os.path.exists(mod_file):
            try:
                os.remove(mod_file)  # Remove the module file
                self.remove_module_defaults()  # Remove default targeting module file
                self.update_module_hiddenness(remove=True)  # Remove hide cmd in modulerc
                os.removedirs(
                    os.path.dirname(mod_file)
                )  # Remove all the empty directories from the leaf up
            except OSError:
                # removedirs throws OSError on first non-empty directory found
                pass

    def remove_module_defaults(self):
        if not any(self.spec.satisfies(default) for default in self.conf.defaults):
            return

        # This spec matches a default, symlink needs to be removed as we remove the module
        # file it targets.
        default_symlink = os.path.join(os.path.dirname(self.layout.filename), "default")
        try:
            os.unlink(default_symlink)
        except OSError:
            pass


@contextlib.contextmanager
def disable_modules():
    """Disable the generation of modulefiles within the context manager."""
    data = {"modules:": {"default": {"enable": []}}}
    disable_scope = spack.config.InternalConfigScope("disable_modules", data=data)
    with spack.config.override(disable_scope):
        yield


class ModulesError(spack.error.SpackError):
    """Base error for modules."""


class ModuleNotFoundError(ModulesError):
    """Raised when a module cannot be found for a spec"""


class DefaultTemplateNotDefined(AttributeError, ModulesError):
    """Raised if the attribute 'default_template' has not been specified
    in the derived classes.
    """


class HideCmdFormatNotDefined(AttributeError, ModulesError):
    """Raised if the attribute 'hide_cmd_format' has not been specified
    in the derived classes.
    """


class ModulercHeaderNotDefined(AttributeError, ModulesError):
    """Raised if the attribute 'modulerc_header' has not been specified
    in the derived classes.
    """


class ModulesTemplateNotFoundError(ModulesError, RuntimeError):
    """Raised if the template for a module file was not found."""
