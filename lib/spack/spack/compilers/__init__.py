# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains functions related to finding compilers on the
system and configuring Spack to use multiple compilers.
"""
import collections
import itertools
import multiprocessing.pool
import os
import six

import llnl.util.lang
import llnl.util.filesystem as fs
import llnl.util.tty as tty
import archspec.cpu

import spack.paths
import spack.error
import spack.spec
import spack.config
import spack.architecture
import spack.util.imp as simp
from spack.util.environment import get_path
from spack.util.naming import mod_to_class

_imported_compilers_module = 'spack.compilers'
_path_instance_vars = ['cc', 'cxx', 'f77', 'fc']
_flags_instance_vars = ['cflags', 'cppflags', 'cxxflags', 'fflags']
_other_instance_vars = ['modules', 'operating_system', 'environment',
                        'implicit_rpaths', 'extra_rpaths']
_cache_config_file = []

# TODO: Caches at module level make it difficult to mock configurations in
# TODO: unit tests. It might be worth reworking their implementation.
#: cache of compilers constructed from config data, keyed by config entry id.
_compiler_cache = {}

_compiler_to_pkg = {
    'clang': 'llvm+clang'
}


def pkg_spec_for_compiler(cspec):
    """Return the spec of the package that provides the compiler."""
    spec_str = '%s@%s' % (_compiler_to_pkg.get(cspec.name, cspec.name),
                          cspec.versions)
    return spack.spec.Spec(spec_str)


def _auto_compiler_spec(function):
    def converter(cspec_like, *args, **kwargs):
        if not isinstance(cspec_like, spack.spec.CompilerSpec):
            cspec_like = spack.spec.CompilerSpec(cspec_like)
        return function(cspec_like, *args, **kwargs)
    return converter


def _to_dict(compiler):
    """Return a dict version of compiler suitable to insert in YAML."""
    d = {}
    d['spec'] = str(compiler.spec)
    d['paths'] = dict((attr, getattr(compiler, attr, None))
                      for attr in _path_instance_vars)
    d['flags'] = dict((fname, fvals) for fname, fvals in compiler.flags)
    d['flags'].update(dict((attr, getattr(compiler, attr, None))
                      for attr in _flags_instance_vars
                           if hasattr(compiler, attr)))
    d['operating_system'] = str(compiler.operating_system)
    d['target'] = str(compiler.target)
    d['modules'] = compiler.modules or []
    d['environment'] = compiler.environment or {}
    d['extra_rpaths'] = compiler.extra_rpaths or []
    if compiler.enable_implicit_rpaths is not None:
        d['implicit_rpaths'] = compiler.enable_implicit_rpaths

    if compiler.alias:
        d['alias'] = compiler.alias

    return {'compiler': d}


def get_compiler_config(scope=None, init_config=True):
    """Return the compiler configuration for the specified architecture.
    """
    def init_compiler_config():
        """Compiler search used when Spack has no compilers."""
        compilers = find_compilers()
        compilers_dict = []
        for compiler in compilers:
            compilers_dict.append(_to_dict(compiler))
        spack.config.set('compilers', compilers_dict, scope=scope)

    config = spack.config.get('compilers', scope=scope)
    # Update the configuration if there are currently no compilers
    # configured.  Avoid updating automatically if there ARE site
    # compilers configured but no user ones.
    if not config and init_config:
        if scope is None:
            # We know no compilers were configured in any scope.
            init_compiler_config()
            config = spack.config.get('compilers', scope=scope)
        elif scope == 'user':
            # Check the site config and update the user config if
            # nothing is configured at the site level.
            site_config = spack.config.get('compilers', scope='site')
            sys_config = spack.config.get('compilers', scope='system')
            if not site_config and not sys_config:
                init_compiler_config()
                config = spack.config.get('compilers', scope=scope)
        return config
    elif config:
        return config
    else:
        return []  # Return empty list which we will later append to.


def compiler_config_files():
    config_files = list()
    config = spack.config.config
    for scope in config.file_scopes:
        name = scope.name
        compiler_config = config.get('compilers', scope=name)
        if compiler_config:
            config_files.append(config.get_config_filename(name, 'compilers'))
    return config_files


def add_compilers_to_config(compilers, scope=None, init_config=True):
    """Add compilers to the config for the specified architecture.

    Arguments:
      - compilers: a list of Compiler objects.
      - scope:     configuration scope to modify.
    """
    compiler_config = get_compiler_config(scope, init_config)
    for compiler in compilers:
        compiler_config.append(_to_dict(compiler))
    global _cache_config_file
    _cache_config_file = compiler_config
    spack.config.set('compilers', compiler_config, scope=scope)


@_auto_compiler_spec
def remove_compiler_from_config(compiler_spec, scope=None):
    """Remove compilers from the config, by spec.

    Arguments:
      - compiler_specs: a list of CompilerSpec objects.
      - scope:          configuration scope to modify.
    """
    # Need a better way for this
    global _cache_config_file

    compiler_config = get_compiler_config(scope)
    config_length = len(compiler_config)

    filtered_compiler_config = [
        comp for comp in compiler_config
        if spack.spec.CompilerSpec(comp['compiler']['spec']) != compiler_spec]

    # Update the cache for changes
    _cache_config_file = filtered_compiler_config
    if len(filtered_compiler_config) == config_length:  # No items removed
        CompilerSpecInsufficientlySpecificError(compiler_spec)
    spack.config.set('compilers', filtered_compiler_config, scope=scope)


def all_compilers_config(scope=None, init_config=True):
    """Return a set of specs for all the compiler versions currently
       available to build with.  These are instances of CompilerSpec.
    """
    # Get compilers for this architecture.
    # Create a cache of the config file so we don't load all the time.
    global _cache_config_file
    if not _cache_config_file:
        _cache_config_file = get_compiler_config(scope, init_config)
        return _cache_config_file
    else:
        return _cache_config_file


def all_compiler_specs(scope=None, init_config=True):
    # Return compiler specs from the merged config.
    return [spack.spec.CompilerSpec(s['compiler']['spec'])
            for s in all_compilers_config(scope, init_config)]


def find_compilers(path_hints=None):
    """Returns the list of compilers found in the paths given as arguments.

    Args:
        path_hints (list or None): list of path hints where to look for.
            A sensible default based on the ``PATH`` environment variable
            will be used if the value is None

    Returns:
        List of compilers found
    """
    if path_hints is None:
        path_hints = get_path('PATH')
    default_paths = fs.search_paths_for_executables(*path_hints)

    # To detect the version of the compilers, we dispatch a certain number
    # of function calls to different workers. Here we construct the list
    # of arguments for each call.
    arguments = []
    for o in all_os_classes():
        search_paths = getattr(o, 'compiler_search_paths', default_paths)
        arguments.extend(arguments_to_detect_version_fn(o, search_paths))

    # Here we map the function arguments to the corresponding calls
    tp = multiprocessing.pool.ThreadPool()
    try:
        detected_versions = tp.map(detect_version, arguments)
    finally:
        tp.close()

    def valid_version(item):
        value, error = item
        if error is None:
            return True
        try:
            # This will fail on Python 2.6 if a non ascii
            # character is in the error
            tty.debug(error)
        except UnicodeEncodeError:
            pass
        return False

    def remove_errors(item):
        value, _ = item
        return value

    return make_compiler_list(
        map(remove_errors, filter(valid_version, detected_versions))
    )


def supported_compilers():
    """Return a set of names of compilers supported by Spack.

       See available_compilers() to get a list of all the available
       versions of supported compilers.
    """
    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    return sorted(name if name != 'apple_clang' else 'apple-clang' for name in
                  llnl.util.lang.list_modules(spack.paths.compilers_path))


@_auto_compiler_spec
def supported(compiler_spec):
    """Test if a particular compiler is supported."""
    return compiler_spec.name in supported_compilers()


@_auto_compiler_spec
def find(compiler_spec, scope=None, init_config=True):
    """Return specs of available compilers that match the supplied
       compiler spec.  Return an empty list if nothing found."""
    return [c for c in all_compiler_specs(scope, init_config)
            if c.satisfies(compiler_spec)]


@_auto_compiler_spec
def find_specs_by_arch(compiler_spec, arch_spec, scope=None, init_config=True):
    """Return specs of available compilers that match the supplied
       compiler spec.  Return an empty list if nothing found."""
    return [c.spec for c in compilers_for_spec(compiler_spec,
                                               arch_spec,
                                               scope,
                                               True,
                                               init_config)]


def all_compilers(scope=None):
    config = get_compiler_config(scope)
    compilers = list()
    for items in config:
        items = items['compiler']
        compilers.append(_compiler_from_config_entry(items))
    return compilers


@_auto_compiler_spec
def compilers_for_spec(compiler_spec, arch_spec=None, scope=None,
                       use_cache=True, init_config=True):
    """This gets all compilers that satisfy the supplied CompilerSpec.
       Returns an empty list if none are found.
    """
    if use_cache:
        config = all_compilers_config(scope, init_config)
    else:
        config = get_compiler_config(scope, init_config)

    matches = set(find(compiler_spec, scope, init_config))
    compilers = []
    for cspec in matches:
        compilers.extend(get_compilers(config, cspec, arch_spec))
    return compilers


def compilers_for_arch(arch_spec, scope=None):
    config = all_compilers_config(scope)
    return list(get_compilers(config, arch_spec=arch_spec))


class CacheReference(object):
    """This acts as a hashable reference to any object (regardless of whether
       the object itself is hashable) and also prevents the object from being
       garbage-collected (so if two CacheReference objects are equal, they
       will refer to the same object, since it will not have been gc'ed since
       the creation of the first CacheReference).
    """
    def __init__(self, val):
        self.val = val
        self.id = id(val)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, CacheReference) and self.id == other.id


def compiler_from_dict(items):
    cspec = spack.spec.CompilerSpec(items['spec'])
    os = items.get('operating_system', None)
    target = items.get('target', None)

    if not ('paths' in items and
            all(n in items['paths'] for n in _path_instance_vars)):
        raise InvalidCompilerConfigurationError(cspec)

    cls  = class_for_compiler_name(cspec.name)

    compiler_paths = []
    for c in _path_instance_vars:
        compiler_path = items['paths'][c]
        if compiler_path != 'None':
            compiler_paths.append(compiler_path)
        else:
            compiler_paths.append(None)

    mods = items.get('modules')
    if mods == 'None':
        mods = []

    alias = items.get('alias', None)
    compiler_flags = items.get('flags', {})
    environment = items.get('environment', {})
    extra_rpaths = items.get('extra_rpaths', [])
    implicit_rpaths = items.get('implicit_rpaths', None)

    # Starting with c22a145, 'implicit_rpaths' was a list. Now it is a
    # boolean which can be set by the user to disable all automatic
    # RPATH insertion of compiler libraries
    if implicit_rpaths is not None and not isinstance(implicit_rpaths, bool):
        implicit_rpaths = None

    return cls(cspec, os, target, compiler_paths, mods, alias,
               environment, extra_rpaths,
               enable_implicit_rpaths=implicit_rpaths,
               **compiler_flags)


def _compiler_from_config_entry(items):
    """Note this is intended for internal use only. To avoid re-parsing
       the same config dictionary this keeps track of its location in
       memory. If you provide the same dictionary twice it will return
       the same Compiler object (regardless of whether the dictionary
       entries have changed).
    """
    config_id = CacheReference(items)
    compiler = _compiler_cache.get(config_id, None)

    if compiler is None:
        compiler = compiler_from_dict(items)
        _compiler_cache[config_id] = compiler

    return compiler


def get_compilers(config, cspec=None, arch_spec=None):
    compilers = []

    for items in config:
        items = items['compiler']
        if cspec and items['spec'] != str(cspec):
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given operating system
        os = items.get('operating_system', None)
        if arch_spec and os != arch_spec.os:
            continue

        # If an arch spec is given, confirm that this compiler
        # is for the given target. If the target is 'any', match
        # any given arch spec. If the compiler has no assigned
        # target this is an old compiler config file, skip this logic.
        target = items.get('target', None)

        try:
            current_target = archspec.cpu.TARGETS[str(arch_spec.target)]
            family = str(current_target.family)
        except KeyError:
            # TODO: Check if this exception handling makes sense, or if we
            # TODO: need to change / refactor tests
            family = arch_spec.target
        except AttributeError:
            assert arch_spec is None

        if arch_spec and target and (target != family and target != 'any'):
            # If the family of the target is the family we are seeking,
            # there's an error in the underlying configuration
            if archspec.cpu.TARGETS[target].family == family:
                msg = ('the "target" field in compilers.yaml accepts only '
                       'target families [replace "{0}" with "{1}"'
                       ' in "{2}" specification]')
                msg = msg.format(str(target), family, items.get('spec', '??'))
                raise ValueError(msg)
            continue

        compilers.append(_compiler_from_config_entry(items))

    return compilers


@_auto_compiler_spec
def compiler_for_spec(compiler_spec, arch_spec):
    """Get the compiler that satisfies compiler_spec.  compiler_spec must
       be concrete."""
    assert(compiler_spec.concrete)
    assert(arch_spec.concrete)

    compilers = compilers_for_spec(compiler_spec, arch_spec=arch_spec)
    if len(compilers) < 1:
        raise NoCompilerForSpecError(compiler_spec, arch_spec.os)
    if len(compilers) > 1:
        msg = 'Multiple definitions of compiler %s' % compiler_spec
        msg += 'for architecture %s:\n %s' % (arch_spec, compilers)
        tty.debug(msg)
    return compilers[0]


@_auto_compiler_spec
def get_compiler_duplicates(compiler_spec, arch_spec):
    config = spack.config.config

    scope_to_compilers = {}
    for scope in config.scopes:
        compilers = compilers_for_spec(compiler_spec, arch_spec=arch_spec,
                                       scope=scope, use_cache=False)
        if compilers:
            scope_to_compilers[scope] = compilers

    cfg_file_to_duplicates = {}
    for scope, compilers in scope_to_compilers.items():
        config_file = config.get_config_filename(scope, 'compilers')
        cfg_file_to_duplicates[config_file] = compilers

    return cfg_file_to_duplicates


@llnl.util.lang.memoized
def class_for_compiler_name(compiler_name):
    """Given a compiler module name, get the corresponding Compiler class."""
    assert(supported(compiler_name))

    # Hack to be able to call the compiler `apple-clang` while still
    # using a valid python name for the module
    module_name = compiler_name
    if compiler_name == 'apple-clang':
        module_name = compiler_name.replace('-', '_')

    file_path = os.path.join(spack.paths.compilers_path, module_name + ".py")
    compiler_mod = simp.load_source(_imported_compilers_module, file_path)
    cls = getattr(compiler_mod, mod_to_class(compiler_name))

    # make a note of the name in the module so we can get to it easily.
    cls.name = compiler_name

    return cls


def all_os_classes():
    """
    Return the list of classes for all operating systems available on
    this platform
    """
    classes = []

    platform = spack.architecture.platform()
    for os_class in platform.operating_sys.values():
        classes.append(os_class)

    return classes


def all_compiler_types():
    return [class_for_compiler_name(c) for c in supported_compilers()]


#: Gathers the attribute values by which a detected compiler is considered
#: unique in Spack.
#:
#:  - os: the operating system
#:  - compiler_name: the name of the compiler (e.g. 'gcc', 'clang', etc.)
#:  - version: the version of the compiler
#:
CompilerID = collections.namedtuple(
    'CompilerID', ['os', 'compiler_name', 'version']
)

#: Variations on a matched compiler name
NameVariation = collections.namedtuple('NameVariation', ['prefix', 'suffix'])

#: Groups together the arguments needed by `detect_version`. The four entries
#: in the tuple are:
#:
#: - id: An instance of the CompilerID named tuple (version can be set to None
#:       as it will be detected later)
#: - variation: a NameVariation for file being tested
#: - language: compiler language being tested (one of 'cc', 'cxx', 'fc', 'f77')
#: - path: full path to the executable being tested
#:
DetectVersionArgs = collections.namedtuple(
    'DetectVersionArgs', ['id', 'variation', 'language', 'path']
)


def arguments_to_detect_version_fn(operating_system, paths):
    """Returns a list of DetectVersionArgs tuples to be used in a
    corresponding function to detect compiler versions.

    The ``operating_system`` instance can customize the behavior of this
    function by providing a method called with the same name.

    Args:
        operating_system (OperatingSystem): the operating system on which
            we are looking for compilers
        paths: paths to search for compilers

    Returns:
        List of DetectVersionArgs tuples. Each item in the list will be later
        mapped to the corresponding function call to detect the version of the
        compilers in this OS.
    """
    def _default(search_paths):
        command_arguments = []
        files_to_be_tested = fs.files_in(*search_paths)
        for compiler_name in spack.compilers.supported_compilers():

            compiler_cls = class_for_compiler_name(compiler_name)

            for language in ('cc', 'cxx', 'f77', 'fc'):

                # Select only the files matching a regexp
                for (file, full_path), regexp in itertools.product(
                        files_to_be_tested,
                        compiler_cls.search_regexps(language)
                ):
                    match = regexp.match(file)
                    if match:
                        compiler_id = CompilerID(
                            operating_system, compiler_name, None
                        )
                        detect_version_args = DetectVersionArgs(
                            id=compiler_id,
                            variation=NameVariation(*match.groups()),
                            language=language, path=full_path
                        )
                        command_arguments.append(detect_version_args)

        return command_arguments

    fn = getattr(
        operating_system, 'arguments_to_detect_version_fn', _default
    )
    return fn(paths)


def detect_version(detect_version_args):
    """Computes the version of a compiler and adds it to the information
    passed as input.

    As this function is meant to be executed by worker processes it won't
    raise any exception but instead will return a (value, error) tuple that
    needs to be checked by the code dispatching the calls.

    Args:
        detect_version_args (DetectVersionArgs): information on the
            compiler for which we should detect the version.

    Returns:
        A ``(DetectVersionArgs, error)`` tuple. If ``error`` is ``None`` the
        version of the compiler was computed correctly and the first argument
        of the tuple will contain it. Otherwise ``error`` is a string
        containing an explanation on why the version couldn't be computed.
    """
    def _default(fn_args):
        compiler_id = fn_args.id
        language = fn_args.language
        compiler_cls = class_for_compiler_name(compiler_id.compiler_name)
        path = fn_args.path

        # Get compiler names and the callback to detect their versions
        callback = getattr(compiler_cls, '{0}_version'.format(language))

        try:
            version = callback(path)
            if version and six.text_type(version).strip() \
                    and version != 'unknown':
                value = fn_args._replace(
                    id=compiler_id._replace(version=version)
                )
                return value, None

            error = "Couldn't get version for compiler {0}".format(path)
        except spack.util.executable.ProcessError as e:
            error = "Couldn't get version for compiler {0}\n".format(path) + \
                    six.text_type(e)
        except Exception as e:
            # Catching "Exception" here is fine because it just
            # means something went wrong running a candidate executable.
            error = "Error while executing candidate compiler {0}" \
                    "\n{1}: {2}".format(path, e.__class__.__name__,
                                        six.text_type(e))
        return None, error

    operating_system = detect_version_args.id.os
    fn = getattr(operating_system, 'detect_version', _default)
    return fn(detect_version_args)


def make_compiler_list(detected_versions):
    """Process a list of detected versions and turn them into a list of
    compiler specs.

    Args:
        detected_versions (list): list of DetectVersionArgs containing a
            valid version

    Returns:
        list of Compiler objects
    """
    group_fn = lambda x: (x.id, x.variation, x.language)
    sorted_compilers = sorted(detected_versions, key=group_fn)

    # Gather items in a dictionary by the id, name variation and language
    compilers_d = {}
    for sort_key, group in itertools.groupby(sorted_compilers, key=group_fn):
        compiler_id, name_variation, language = sort_key
        by_compiler_id = compilers_d.setdefault(compiler_id, {})
        by_name_variation = by_compiler_id.setdefault(name_variation, {})
        by_name_variation[language] = next(x.path for x in group)

    def _default_make_compilers(cmp_id, paths):
        operating_system, compiler_name, version = cmp_id
        compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
        spec = spack.spec.CompilerSpec(compiler_cls.name, version)
        paths = [paths.get(x, None) for x in ('cc', 'cxx', 'f77', 'fc')]
        target = archspec.cpu.host()
        compiler = compiler_cls(
            spec, operating_system, str(target.family), paths
        )
        return [compiler]

    # For compilers with the same compiler id:
    #
    # - Prefer with C compiler to without
    # - Prefer with C++ compiler to without
    # - Prefer no variations to variations (e.g., clang to clang-gpu)
    #
    sort_fn = lambda variation: (
        'cc' not in by_compiler_id[variation],  # None last
        'cxx' not in by_compiler_id[variation],  # None last
        getattr(variation, 'prefix', None),
        getattr(variation, 'suffix', None),
    )

    compilers = []
    for compiler_id, by_compiler_id in compilers_d.items():
        ordered = sorted(by_compiler_id, key=sort_fn)
        selected_variation = ordered[0]
        selected = by_compiler_id[selected_variation]

        # fill any missing parts from subsequent entries
        for lang in ['cxx', 'f77', 'fc']:
            if lang not in selected:
                next_lang = next((
                    by_compiler_id[v][lang] for v in ordered
                    if lang in by_compiler_id[v]), None)
                if next_lang:
                    selected[lang] = next_lang

        operating_system, _, _ = compiler_id
        make_compilers = getattr(
            operating_system, 'make_compilers', _default_make_compilers)

        compilers.extend(make_compilers(compiler_id, selected))

    return compilers


def is_mixed_toolchain(compiler):
    """Returns True if the current compiler is a mixed toolchain,
    False otherwise.

    Args:
        compiler (Compiler): a valid compiler object
    """
    cc = os.path.basename(compiler.cc or '')
    cxx = os.path.basename(compiler.cxx or '')
    f77 = os.path.basename(compiler.f77 or '')
    fc = os.path.basename(compiler.fc or '')

    toolchains = set()
    for compiler_cls in all_compiler_types():
        # Inspect all the compiler toolchain we know. If a compiler is the
        # only compiler supported there it belongs to that toolchain.
        def name_matches(name, name_list):
            # This is such that 'gcc' matches variations
            # like 'ggc-9' etc that are found in distros
            name, _, _ = name.partition('-')
            return len(name_list) == 1 and name and name in name_list

        if any([
            name_matches(cc, compiler_cls.cc_names),
            name_matches(cxx, compiler_cls.cxx_names),
            name_matches(f77, compiler_cls.f77_names),
            name_matches(fc, compiler_cls.fc_names)
        ]):
            tty.debug("[TOOLCHAIN] MATCH {0}".format(compiler_cls.__name__))
            toolchains.add(compiler_cls.__name__)

    if len(toolchains) > 1:
        if toolchains == set(['Clang', 'AppleClang', 'Aocc']):
            return False
        tty.debug("[TOOLCHAINS] {0}".format(toolchains))
        return True

    return False


class InvalidCompilerConfigurationError(spack.error.SpackError):

    def __init__(self, compiler_spec):
        super(InvalidCompilerConfigurationError, self).__init__(
            "Invalid configuration for [compiler \"%s\"]: " % compiler_spec,
            "Compiler configuration must contain entries for all compilers: %s"
            % _path_instance_vars)


class NoCompilersError(spack.error.SpackError):
    def __init__(self):
        super(NoCompilersError, self).__init__(
            "Spack could not find any compilers!")


class NoCompilerForSpecError(spack.error.SpackError):
    def __init__(self, compiler_spec, target):
        super(NoCompilerForSpecError, self).__init__(
            "No compilers for operating system %s satisfy spec %s"
            % (target, compiler_spec))


class CompilerDuplicateError(spack.error.SpackError):
    def __init__(self, compiler_spec, arch_spec):
        config_file_to_duplicates = get_compiler_duplicates(
            compiler_spec, arch_spec)
        duplicate_table = list(
            (x, len(y)) for x, y in config_file_to_duplicates.items())
        descriptor = lambda num: 'time' if num == 1 else 'times'
        duplicate_msg = (
            lambda cfgfile, count: "{0}: {1} {2}".format(
                cfgfile, str(count), descriptor(count)))
        msg = (
            "Compiler configuration contains entries with duplicate" +
            " specification ({0}, {1})".format(compiler_spec, arch_spec) +
            " in the following files:\n\t" +
            '\n\t'.join(duplicate_msg(x, y) for x, y in duplicate_table))
        super(CompilerDuplicateError, self).__init__(msg)


class CompilerSpecInsufficientlySpecificError(spack.error.SpackError):
    def __init__(self, compiler_spec):
        super(CompilerSpecInsufficientlySpecificError, self).__init__(
            "Multiple compilers satisfy spec %s" % compiler_spec)
