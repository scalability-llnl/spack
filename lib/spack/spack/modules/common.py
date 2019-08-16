# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
import copy
import datetime
import inspect
import os.path
import re
import collections

import six
import llnl.util.filesystem
import llnl.util.tty as tty

import spack.paths
import spack.build_environment as build_environment
import spack.util.environment
import spack.tengine as tengine
import spack.error
import spack.util.spack_yaml as syaml
import spack.util.file_permissions as fp

#: config section for this file
configuration = spack.config.get('modules')

#: Root folders where the various module files should be written
roots = spack.config.get('config:module_roots', {})

#: Inspections that needs to be done on spec prefixes
prefix_inspections = spack.config.get('modules:prefix_inspections', {})

#: Valid tokens for naming scheme and env variable names
_valid_tokens = (
    'name',
    'version',
    'compiler',
    'compiler.name',
    'compiler.version',
    'architecture',
    # tokens from old-style format strings
    'package',
    'compilername',
    'compilerver',
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
    named_tokens = re.findall(r'{(\w*)}', format_string)
    invalid_tokens = [x for x in named_tokens
                      if x.lower() not in _valid_tokens]
    if invalid_tokens:
        msg = message
        msg += ' [{0}]. '.format(', '.join(invalid_tokens))
        msg += 'Did you check your "modules.yaml" configuration?'
        raise RuntimeError(msg)


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


def dependencies(spec, request='all'):
    """Returns the list of dependent specs for a given spec, according to the
    request passed as parameter.

    Args:
        spec: spec to be analyzed
        request: either 'none', 'direct' or 'all'

    Returns:
        list of dependencies

        The return list will be empty if request is 'none', will contain
        the direct dependencies if request is 'direct', or the entire DAG
        if request is 'all'.
    """
    if request not in ('none', 'direct', 'all'):
        message = "Wrong value for argument 'request' : "
        message += "should be one of ('none', 'direct', 'all')"
        raise tty.error(message + " [current value is '%s']" % request)

    if request == 'none':
        return []

    if request == 'direct':
        return spec.dependencies(deptype=('link', 'run'))

    # FIXME : during module file creation nodes seem to be visited multiple
    # FIXME : times even if cover='nodes' is given. This work around permits
    # FIXME : to get a unique list of spec anyhow. Do we miss a merge
    # FIXME : step among nodes that refer to the same package?
    seen = set()
    seen_add = seen.add
    deps = sorted(
        spec.traverse(order='post',
                      cover='nodes',
                      deptype=('link', 'run'),
                      root=False),
        reverse=True)
    return [d for d in deps if not (d in seen or seen_add(d))]


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

    # Get the top-level configuration for the module type we are using
    module_specific_configuration = copy.deepcopy(configuration)

    # Construct a dictionary with the actions we need to perform on the spec
    # passed as a parameter

    # The keyword 'all' is always evaluated first, all the others are
    # evaluated in order of appearance in the module file
    spec_configuration = module_specific_configuration.pop('all', {})
    for constraint, action in module_specific_configuration.items():
        override = False
        if constraint.endswith(':'):
            constraint = constraint.strip(':')
            override = True
        if spec.satisfies(constraint, strict=True):
            if override:
                spec_configuration = {}
            update_dictionary_extending_lists(spec_configuration, action)

    # Transform keywords for dependencies or prerequisites into a list of spec

    # Which modulefiles we want to autoload
    autoload_strategy = spec_configuration.get('autoload', 'none')
    spec_configuration['autoload'] = dependencies(spec, autoload_strategy)

    # Which instead we want to mark as prerequisites
    prerequisite_strategy = spec_configuration.get('prerequisites', 'none')
    spec_configuration['prerequisites'] = dependencies(
        spec, prerequisite_strategy)

    # Attach options that are spec-independent to the spec-specific
    # configuration

    # Hash length in module files
    hash_length = module_specific_configuration.get('hash_length', 7)
    spec_configuration['hash_length'] = hash_length

    verbose = module_specific_configuration.get('verbose', False)
    spec_configuration['verbose'] = verbose

    return spec_configuration


def root_path(name):
    """Returns the root folder for module file installation.

    Args:
        name: name of the module system t be used (e.g. 'tcl')

    Returns:
        root folder for module file installation
    """
    path = roots.get(name, os.path.join(spack.paths.share_path, name))
    return spack.config.canonicalize_path(path)


def generate_module_index(root, modules):
    entries = syaml.syaml_dict()
    for m in modules:
        entry = {
            'path': m.layout.filename,
            'use_name': m.layout.use_name
        }
        entries[m.spec.dag_hash()] = entry
    index = {'module_index': entries}
    index_path = os.path.join(root, 'module-index.yaml')
    llnl.util.filesystem.mkdirp(root)
    with open(index_path, 'w') as index_file:
        syaml.dump(index, index_file, default_flow_style=False)


def _generate_upstream_module_index():
    module_indices = read_module_indices()

    return UpstreamModuleIndex(spack.store.db, module_indices)


upstream_module_index = llnl.util.lang.Singleton(
    _generate_upstream_module_index)


ModuleIndexEntry = collections.namedtuple(
    'ModuleIndexEntry', ['path', 'use_name'])


def read_module_index(root):
    index_path = os.path.join(root, 'module-index.yaml')
    if not os.path.exists(index_path):
        return {}
    with open(index_path, 'r') as index_file:
        return _read_module_index(index_file)


def _read_module_index(str_or_file):
    """Read in the mapping of spec hash to module location/name. For a given
       Spack installation there is assumed to be (at most) one such mapping
       per module type."""
    yaml_content = syaml.load(str_or_file)
    index = {}
    yaml_index = yaml_content['module_index']
    for dag_hash, module_properties in yaml_index.items():
        index[dag_hash] = ModuleIndexEntry(
            module_properties['path'],
            module_properties['use_name'])
    return index


def read_module_indices():
    other_spack_instances = spack.config.get(
        'upstreams') or {}

    module_indices = []

    for install_properties in other_spack_instances.values():
        module_type_to_index = {}
        module_type_to_root = install_properties.get('modules', {})
        for module_type, root in module_type_to_root.items():
            module_type_to_index[module_type] = read_module_index(root)
        module_indices.append(module_type_to_index)

    return module_indices


class UpstreamModuleIndex(object):
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
            raise spack.error.SpackError(
                "Unexpected: {0} is installed locally".format(spec))
        else:
            raise spack.error.SpackError(
                "Unexpected: no install DB found for {0}".format(spec))
        module_index = self.module_indices[db_index]
        module_type_index = module_index.get(module_type, {})
        if not module_type_index:
            raise ModuleNotFoundError(
                "No {0} modules associated with the Spack instance where"
                " {1} is installed".format(module_type, spec))
        if spec.dag_hash() in module_type_index:
            return module_type_index[spec.dag_hash()]
        else:
            raise ModuleNotFoundError(
                "No module is available for upstream package {0}".format(spec))


def get_module(module_type, spec, get_full_path):
    if spec.package.installed_upstream:
        module = spack.modules.common.upstream_module_index.upstream_module(
            spec, module_type)
        if get_full_path:
            return module.path
        else:
            return module.use_name
    else:
        writer = spack.modules.module_types[module_type](spec)
        if not os.path.isfile(writer.layout.filename):
            err_msg = "No module available for package {0} at {1}".format(
                spec, writer.layout.filename
            )
            raise ModuleNotFoundError(err_msg)
        if get_full_path:
            return writer.layout.filename
        else:
            return writer.layout.use_name


class BaseConfiguration(object):
    """Manipulates the information needed to generate a module file to make
    querying easier. It needs to be sub-classed for specific module types.
    """

    def __init__(self, spec):
        # Module where type(self) is defined
        self.module = inspect.getmodule(self)
        # Spec for which we want to generate a module file
        self.spec = spec
        # Dictionary of configuration options that should be applied
        # to the spec
        self.conf = merge_config_rules(self.module.configuration, self.spec)

    @property
    def naming_scheme(self):
        """Naming scheme suitable for non-hierarchical layouts"""
        scheme = self.module.configuration.get(
            'naming_scheme',
            '{name}-{version}-{compiler.name}-{compiler.version}'
        )

        # Ensure the named tokens we are expanding are allowed, see
        # issue #2884 for reference
        msg = 'some tokens cannot be part of the module naming scheme'
        _check_tokens_are_valid(scheme, message=msg)

        return scheme

    @property
    def template(self):
        """Returns the name of the template to use for the module file
        or None if not specified in the configuration.
        """
        return self.conf.get('template', None)

    @property
    def env(self):
        """List of environment modifications that should be done in the
        module.
        """
        env_mods = spack.util.environment.EnvironmentModifications()
        actions = self.conf.get('environment', {})

        def process_arglist(arglist):
            if method == 'unset':
                for x in arglist:
                    yield (x,)
            else:
                for x in six.iteritems(arglist):
                    yield x

        for method, arglist in actions.items():
            for args in process_arglist(arglist):
                getattr(env_mods, method)(*args)

        return env_mods

    @property
    def suffixes(self):
        """List of suffixes that should be appended to the module
        file name.
        """
        suffixes = []
        for constraint, suffix in self.conf.get('suffixes', {}).items():
            if constraint in self.spec:
                suffixes.append(suffix)
        if self.hash:
            suffixes.append(self.hash)
        return suffixes

    @property
    def hash(self):
        """Hash tag for the module or None"""
        hash_length = self.conf.get('hash_length', 7)
        if hash_length != 0:
            return self.spec.dag_hash(length=hash_length)
        return None

    @property
    def blacklisted(self):
        """Returns True if the module has been blacklisted,
        False otherwise.
        """
        # A few variables for convenience of writing the method
        spec = self.spec
        conf = self.module.configuration

        # Compute the list of whitelist rules that match
        wlrules = conf.get('whitelist', [])
        whitelist_matches = [x for x in wlrules if spec.satisfies(x)]

        # Compute the list of blacklist rules that match
        blrules = conf.get('blacklist', [])
        blacklist_matches = [x for x in blrules if spec.satisfies(x)]

        # Should I blacklist the module because it's implicit?
        blacklist_implicits = conf.get('blacklist_implicits')
        installed_implicitly = not spec._installed_explicitly()
        blacklisted_as_implicit = blacklist_implicits and installed_implicitly

        def debug_info(line_header, match_list):
            if match_list:
                msg = '\t{0} : {1}'.format(line_header, spec.cshort_spec)
                tty.debug(msg)
                for rule in match_list:
                    tty.debug('\t\tmatches rule: {0}'.format(rule))

        debug_info('WHITELIST', whitelist_matches)
        debug_info('BLACKLIST', blacklist_matches)

        if blacklisted_as_implicit:
            msg = '\tBLACKLISTED_AS_IMPLICIT : {0}'.format(spec.cshort_spec)
            tty.debug(msg)

        is_blacklisted = blacklist_matches or blacklisted_as_implicit
        if not whitelist_matches and is_blacklisted:
            return True

        return False

    @property
    def context(self):
        return self.conf.get('context', {})

    @property
    def specs_to_load(self):
        """List of specs that should be loaded in the module file."""
        return self._create_list_for('autoload')

    @property
    def literals_to_load(self):
        """List of literal modules to be loaded."""
        return self.conf.get('load', [])

    @property
    def specs_to_prereq(self):
        """List of specs that should be prerequisite of the module file."""
        return self._create_list_for('prerequisites')

    @property
    def environment_blacklist(self):
        """List of variables that should be left unmodified."""
        return self.conf.get('filter', {}).get('environment_blacklist', {})

    def _create_list_for(self, what):
        whitelist = []
        for item in self.conf[what]:
            conf = type(self)(item)
            if not conf.blacklisted:
                whitelist.append(item)
        return whitelist

    @property
    def verbose(self):
        """Returns True if the module file needs to be verbose, False
        otherwise
        """
        return self.conf.get('verbose')


class BaseFileLayout(object):
    """Provides information on the layout of module files. Needs to be
    sub-classed for specific module types.
    """

    #: This needs to be redefined
    extension = None

    def __init__(self, configuration):
        self.conf = configuration

    @property
    def spec(self):
        """Spec under consideration"""
        return self.conf.spec

    @classmethod
    def dirname(cls):
        """Root folder for module files of this type."""
        module_system = str(inspect.getmodule(cls).__name__).split('.')[-1]
        return root_path(module_system)

    @property
    def use_name(self):
        """Returns the 'use' name of the module i.e. the name you have to type
        to console to use it. This implementation fits the needs of most
        non-hierarchical layouts.
        """
        name = self.spec.format(self.conf.naming_scheme)
        # Not everybody is working on linux...
        parts = name.split('/')
        name = os.path.join(*parts)
        # Add optional suffixes based on constraints
        path_elements = [name] + self.conf.suffixes
        return '-'.join(path_elements)

    @property
    def filename(self):
        """Name of the module file for the current spec."""
        # Just the name of the file
        filename = self.use_name
        if self.extension:
            filename = '{0}.{1}'.format(self.use_name, self.extension)
        # Architecture sub-folder
        arch_folder = str(self.spec.architecture)
        # Return the absolute path
        return os.path.join(self.dirname(), arch_folder, filename)


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
        return getattr(self.spec, 'category', 'spack')

    @tengine.context_property
    def short_description(self):
        # If we have a valid docstring return the first paragraph.
        docstring = type(self.spec.package).__doc__
        if docstring:
            value = docstring.split('\n\n')[0]
            # Transform tabs and friends into spaces
            value = re.sub(r'\s+', ' ', value)
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
            return re.sub(r'\s+', ' ', self.spec.package.__doc__)
        return None

    @tengine.context_property
    def configure_options(self):
        pkg = self.spec.package

        # If the spec is external Spack doesn't know its configure options
        if self.spec.external:
            msg = 'unknown, software installed outside of Spack'
            return msg

        # This is quite simple right now, but contains information on how
        # to call different build system classes.
        for attr in ('configure_args', 'cmake_args'):
            try:
                configure_args = getattr(pkg, attr)()
                return ' '.join(configure_args)
            except (AttributeError, IOError, KeyError):
                # The method doesn't exist in the current spec,
                # or it's not usable
                pass

        # Returning a false-like value makes the default templates skip
        # the configure option section
        return None

    @tengine.context_property
    def environment_modifications(self):
        """List of environment modifications to be processed."""
        # Modifications guessed inspecting the spec prefix
        env = spack.util.environment.inspect_path(
            self.spec.prefix,
            prefix_inspections,
            exclude=spack.util.environment.is_system_path
        )

        # Modifications that are coded at package level
        _ = spack.util.environment.EnvironmentModifications()
        # TODO : the code down below is quite similar to
        # TODO : build_environment.setup_package and needs to be factored out
        # TODO : to a single place
        # Let the extendee/dependency modify their extensions/dependencies
        # before asking for package-specific modifications
        for item in dependencies(self.spec, 'all'):
            package = self.spec[item.name].package
            build_environment.set_module_variables_for_package(package)
            package.setup_dependent_package(
                self.spec.package.module, self.spec
            )
            package.setup_dependent_environment(_, env, self.spec)
        # Package specific modifications
        build_environment.set_module_variables_for_package(self.spec.package)
        self.spec.package.setup_environment(_, env)

        # Modifications required from modules.yaml
        env.extend(self.conf.env)

        # List of variables that are blacklisted in modules.yaml
        blacklist = self.conf.environment_blacklist

        # We may have tokens to substitute in environment commands

        # Prepare a suitable transformation dictionary for the names
        # of the environment variables. This means turn the valid
        # tokens uppercase.
        transform = {}
        for token in _valid_tokens:
            transform[token] = lambda spec, string: str.upper(string)

        for x in env:
            # Ensure all the tokens are valid in this context
            msg = 'some tokens cannot be expanded in an environment variable name'  # noqa: E501
            _check_tokens_are_valid(x.name, message=msg)
            # Transform them
            x.name = self.spec.format(x.name, transform=transform)
            try:
                # Not every command has a value
                x.value = self.spec.format(x.value)
            except AttributeError:
                pass
            x.name = str(x.name).replace('-', '_')

        return [(type(x).__name__, x) for x in env if x.name not in blacklist]

    @tengine.context_property
    def autoload(self):
        """List of modules that needs to be loaded automatically."""
        # From 'autoload' configuration option
        specs = self._create_module_list_of('specs_to_load')
        # From 'load' configuration option
        literals = self.conf.literals_to_load
        return specs + literals

    def _create_module_list_of(self, what):
        m = self.conf.module
        return [m.make_layout(x).use_name
                for x in getattr(self.conf, what)]

    @tengine.context_property
    def verbose(self):
        """Verbosity level."""
        return self.conf.verbose


class BaseModuleFileWriter(object):
    def __init__(self, spec):
        self.spec = spec

        # This class is meant to be derived. Get the module of the
        # actual writer.
        self.module = inspect.getmodule(self)
        m = self.module

        # Create the triplet of configuration/layout/context
        self.conf = m.make_configuration(spec)
        self.layout = m.make_layout(spec)
        self.context = m.make_context(spec)

        # Check if a default template has been defined,
        # throw if not found
        try:
            self.default_template
        except AttributeError:
            msg = '\'{0}\' object has no attribute \'default_template\'\n'
            msg += 'Did you forget to define it in the class?'
            name = type(self).__name__
            raise DefaultTemplateNotDefined(msg.format(name))

    def _get_template(self):
        """Gets the template that will be rendered for this spec."""
        # Get templates and put them in the order of importance:
        # 1. template specified in "modules.yaml"
        # 2. template specified in a package directly
        # 3. default template (must be defined, check in __init__)
        module_system_name = str(self.module.__name__).split('.')[-1]
        package_attribute = '{0}_template'.format(module_system_name)
        choices = [
            self.conf.template,
            getattr(self.spec.package, package_attribute, None),
            self.default_template  # This is always defined at this point
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
        # Return immediately if the module is blacklisted
        if self.conf.blacklisted:
            msg = '\tNOT WRITING: {0} [BLACKLISTED]'
            tty.debug(msg.format(self.spec.cshort_spec))
            return

        # Print a warning in case I am accidentally overwriting
        # a module file that is already there (name clash)
        if not overwrite and os.path.exists(self.layout.filename):
            message = 'Module file already exists : skipping creation\n'
            message += 'file : {0.filename}\n'
            message += 'spec : {0.spec}'
            tty.warn(message.format(self.layout))
            return

        # If we are here it means it's ok to write the module file
        msg = '\tWRITE: {0} [{1}]'
        tty.debug(msg.format(self.spec.cshort_spec, self.layout.filename))

        # If the directory where the module should reside does not exist
        # create it
        module_dir = os.path.dirname(self.layout.filename)
        if not os.path.exists(module_dir):
            llnl.util.filesystem.mkdirp(module_dir)

        # Get the template for the module
        template_name = self._get_template()
        try:
            env = tengine.make_environment()
            template = env.get_template(template_name)
        except tengine.TemplateNotFound:
            # If the template was not found raise an exception with a little
            # more information
            msg = 'template \'{0}\' was not found for \'{1}\''
            name = type(self).__name__
            msg = msg.format(template_name, name)
            raise ModulesTemplateNotFoundError(msg)

        # Construct the context following the usual hierarchy of updates:
        # 1. start with the default context from the module writer class
        # 2. update with package specific context
        # 3. update with 'modules.yaml' specific context

        context = self.context.to_dict()

        # Attribute from package
        module_name = str(self.module.__name__).split('.')[-1]
        attr_name = '{0}_context'.format(module_name)
        pkg_update = getattr(self.spec.package, attr_name, {})
        context.update(pkg_update)

        # Context key in modules.yaml
        conf_update = self.conf.context
        context.update(conf_update)

        # Render the template
        text = template.render(context)
        # Write it to file
        with open(self.layout.filename, 'w') as f:
            f.write(text)

        # Set the file permissions of the module to match that of the package
        if os.path.exists(self.layout.filename):
            fp.set_permissions_by_spec(self.layout.filename, self.spec)

    def remove(self):
        """Deletes the module file."""
        mod_file = self.layout.filename
        if os.path.exists(mod_file):
            try:
                os.remove(mod_file)  # Remove the module file
                os.removedirs(
                    os.path.dirname(mod_file)
                )  # Remove all the empty directories from the leaf up
            except OSError:
                # removedirs throws OSError on first non-empty directory found
                pass


class ModulesError(spack.error.SpackError):
    """Base error for modules."""


class ModuleNotFoundError(ModulesError):
    """Raised when a module cannot be found for a spec"""


class DefaultTemplateNotDefined(AttributeError, ModulesError):
    """Raised if the attribute 'default_template' has not been specified
    in the derived classes.
    """


class ModulesTemplateNotFoundError(ModulesError, RuntimeError):
    """Raised if the template for a module file was not found."""
