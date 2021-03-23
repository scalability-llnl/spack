# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import errno
import inspect
import itertools
import json
import os
import os.path
import shutil
import tempfile
import xml.etree.ElementTree

import py
import pytest

import archspec.cpu.microarchitecture
import archspec.cpu.schema
from llnl.util.filesystem import mkdirp, remove_linked_tree

import spack.architecture
import spack.compilers
import spack.config
import spack.caches
import spack.database
import spack.directory_layout
import spack.environment as ev
import spack.package
import spack.package_prefs
import spack.paths
import spack.platforms.test
import spack.repo
import spack.stage
import spack.store
import spack.util.executable
import spack.util.gpg
import spack.subprocess_context
import spack.util.spack_yaml as syaml

from spack.util.pattern import Bunch
from spack.fetch_strategy import FetchStrategyComposite, URLFetchStrategy
from spack.fetch_strategy import FetchError


@pytest.fixture(autouse=True)
def clear_recorded_monkeypatches():
    yield
    spack.subprocess_context.clear_patches()


@pytest.fixture(scope='session', autouse=True)
def record_monkeypatch_setattr():
    import _pytest
    saved_setattr = _pytest.monkeypatch.MonkeyPatch.setattr

    def record_setattr(cls, target, name, value, *args, **kwargs):
        spack.subprocess_context.append_patch((target, name, value))
        saved_setattr(cls, target, name, value, *args, **kwargs)

    _pytest.monkeypatch.MonkeyPatch.setattr = record_setattr
    try:
        yield
    finally:
        _pytest.monkeypatch.MonkeyPatch.setattr = saved_setattr


def _can_access(path, perms):
    return False


@pytest.fixture
def no_path_access(monkeypatch):
    monkeypatch.setattr(os, 'access', _can_access)


#
# Disable any activate Spack environment BEFORE all tests
#
@pytest.fixture(scope='session', autouse=True)
def clean_user_environment():
    env_var = ev.spack_env_var in os.environ
    active = ev._active_environment

    if env_var:
        spack_env_value = os.environ.pop(ev.spack_env_var)
    if active:
        ev.deactivate()

    yield

    if env_var:
        os.environ[ev.spack_env_var] = spack_env_value
    if active:
        ev.activate(active)


def _verify_executables_noop(*args):
    return None


#
# Disable checks on compiler executable existence
#
@pytest.fixture(scope='function', autouse=True)
def mock_compiler_executable_verification(request, monkeypatch):
    """Mock the compiler executable verification to allow missing executables.

    This fixture can be disabled for tests of the compiler verification
    functionality by::

        @pytest.mark.enable_compiler_verification

    If a test is marked in that way this is a no-op."""
    if 'enable_compiler_verification' not in request.keywords:
        monkeypatch.setattr(spack.compiler.Compiler,
                            'verify_executables',
                            _verify_executables_noop)


# Hooks to add command line options or set other custom behaviors.
# They must be placed here to be found by pytest. See:
#
# https://docs.pytest.org/en/latest/writing_plugins.html
#
def pytest_addoption(parser):
    group = parser.getgroup("Spack specific command line options")
    group.addoption(
        '--fast', action='store_true', default=False,
        help='runs only "fast" unit tests, instead of the whole suite')


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--fast'):
        # --fast not given, run all the tests
        return

    slow_tests = ['db', 'network', 'maybeslow']
    skip_as_slow = pytest.mark.skip(
        reason='skipped slow test [--fast command line option given]'
    )
    for item in items:
        if any(x in item.keywords for x in slow_tests):
            item.add_marker(skip_as_slow)


#
# These fixtures are applied to all tests
#
@pytest.fixture(scope='function', autouse=True)
def no_chdir():
    """Ensure that no test changes Spack's working dirctory.

    This prevents Spack tests (and therefore Spack commands) from
    changing the working directory and causing other tests to fail
    mysteriously. Tests should use ``working_dir`` or ``py.path``'s
    ``.as_cwd()`` instead of ``os.chdir`` to avoid failing this check.

    We assert that the working directory hasn't changed, unless the
    original wd somehow ceased to exist.

    """
    original_wd = os.getcwd()
    yield
    if os.path.isdir(original_wd):
        assert os.getcwd() == original_wd


@pytest.fixture(scope='function', autouse=True)
def reset_compiler_cache():
    """Ensure that the compiler cache is not shared across Spack tests

    This cache can cause later tests to fail if left in a state incompatible
    with the new configuration. Since tests can make almost unlimited changes
    to their setup, default to not use the compiler cache across tests."""
    spack.compilers._compiler_cache = {}
    yield
    spack.compilers._compiler_cache = {}


@pytest.fixture(scope='function', autouse=True)
def mock_stage(tmpdir_factory, monkeypatch, request):
    """Establish the temporary build_stage for the mock archive."""
    # The approach with this autouse fixture is to set the stage root
    # instead of using spack.config.override() to avoid configuration
    # conflicts with dozens of tests that rely on other configuration
    # fixtures, such as config.
    if 'nomockstage' not in request.keywords:
        # Set the build stage to the requested path
        new_stage = tmpdir_factory.mktemp('mock-stage')
        new_stage_path = str(new_stage)

        # Ensure the source directory exists within the new stage path
        source_path = os.path.join(new_stage_path,
                                   spack.stage._source_path_subdir)
        mkdirp(source_path)

        monkeypatch.setattr(spack.stage, '_stage_root', new_stage_path)

        yield new_stage_path

        # Clean up the test stage directory
        if os.path.isdir(new_stage_path):
            shutil.rmtree(new_stage_path)
    else:
        # Must yield a path to avoid a TypeError on test teardown
        yield str(tmpdir_factory)


@pytest.fixture(scope='session')
def ignore_stage_files():
    """Session-scoped helper for check_for_leftover_stage_files.

    Used to track which leftover files in the stage have been seen.
    """
    # to start with, ignore the .lock file at the stage root.
    return set(['.lock', spack.stage._source_path_subdir, 'build_cache'])


def remove_whatever_it_is(path):
    """Type-agnostic remove."""
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.islink(path):
        remove_linked_tree(path)
    else:
        shutil.rmtree(path)


@pytest.fixture
def working_env():
    saved_env = os.environ.copy()
    yield
    # os.environ = saved_env doesn't work
    # it causes module_parsing::test_module_function to fail
    # when it's run after any test using this fixutre
    os.environ.clear()
    os.environ.update(saved_env)


@pytest.fixture(scope='function', autouse=True)
def check_for_leftover_stage_files(request, mock_stage, ignore_stage_files):
    """
    Ensure that each (mock_stage) test leaves a clean stage when done.

    Tests that are expected to dirty the stage can disable the check by
    adding::

        @pytest.mark.disable_clean_stage_check

    and the associated stage files will be removed.
    """
    stage_path = mock_stage

    yield

    files_in_stage = set()
    try:
        stage_files = os.listdir(stage_path)
        files_in_stage = set(stage_files) - ignore_stage_files
    except OSError as err:
        if err.errno == errno.ENOENT:
            pass
        else:
            raise

    if 'disable_clean_stage_check' in request.keywords:
        # clean up after tests that are expected to be dirty
        for f in files_in_stage:
            path = os.path.join(stage_path, f)
            remove_whatever_it_is(path)
    else:
        ignore_stage_files |= files_in_stage
        assert not files_in_stage


class MockCache(object):
    def store(self, copy_cmd, relative_dest):
        pass

    def fetcher(self, target_path, digest, **kwargs):
        return MockCacheFetcher()


class MockCacheFetcher(object):
    def fetch(self):
        raise FetchError('Mock cache always fails for tests')

    def __str__(self):
        return "[mock fetch cache]"


@pytest.fixture(autouse=True)
def mock_fetch_cache(monkeypatch):
    """Substitutes spack.paths.fetch_cache with a mock object that does nothing
    and raises on fetch.
    """
    monkeypatch.setattr(spack.caches, 'fetch_cache', MockCache())


@pytest.fixture(autouse=True)
def _skip_if_missing_executables(request):
    """Permits to mark tests with 'require_executables' and skip the
    tests if the executables passed as arguments are not found.
    """
    if request.node.get_marker('requires_executables'):
        required_execs = request.node.get_marker('requires_executables').args
        missing_execs = [
            x for x in required_execs if spack.util.executable.which(x) is None
        ]
        if missing_execs:
            msg = 'could not find executables: {0}'
            pytest.skip(msg.format(', '.join(missing_execs)))


@pytest.fixture(scope='session')
def test_platform():
    return spack.platforms.test.Test()


@pytest.fixture(autouse=True, scope='session')
def _use_test_platform(test_platform):
    # This is the only context manager used at session scope (see note
    # below for more insight) since we want to use the test platform as
    # a default during tests.
    with spack.architecture.use_platform(test_platform):
        yield

#
# Note on context managers used by fixtures
#
# Because these context managers modify global state, they should really
# ONLY be used persistently (i.e., around yield statements) in
# function-scoped fixtures, OR in autouse session- or module-scoped
# fixtures.
#
# If they're used in regular tests or in module-scoped fixtures that are
# then injected as function arguments, weird things can happen, because
# the original state won't be restored until *after* the fixture is
# destroyed.  This makes sense for an autouse fixture, where you know
# everything in the module/session is going to need the modified
# behavior, but modifying global state for one function in a way that
# won't be restored until after the module or session is done essentially
# leaves garbage behind for other tests.
#
# In general, we should module- or session-scope the *STATE* required for
# these global objects, but we shouldn't module- or session-scope their
# *USE*, or things can get really confusing.
#


#
# Test-specific fixtures
#
@pytest.fixture(scope='session')
def mock_repo_path():
    yield spack.repo.Repo(spack.paths.mock_packages_path)


def _pkg_install_fn(pkg, spec, prefix):
    # sanity_check_prefix requires something in the install directory
    mkdirp(prefix.bin)


@pytest.fixture
def mock_pkg_install(monkeypatch):
    monkeypatch.setattr(spack.package.PackageBase, 'install',
                        _pkg_install_fn, raising=False)


@pytest.fixture(scope='function')
def mock_packages(mock_repo_path, mock_pkg_install):
    """Use the 'builtin.mock' repository instead of 'builtin'"""
    with spack.repo.use_repositories(mock_repo_path) as mock_repo:
        yield mock_repo


@pytest.fixture(scope='function')
def mutable_mock_repo(mock_repo_path):
    """Function-scoped mock packages, for tests that need to modify them."""
    mock_repo = spack.repo.Repo(spack.paths.mock_packages_path)
    with spack.repo.use_repositories(mock_repo) as mock_repo_path:
        yield mock_repo_path


@pytest.fixture(scope='session')
def linux_os():
    """Returns a named tuple with attributes 'name' and 'version'
    representing the OS.
    """
    platform = spack.architecture.platform()
    name, version = 'debian', '6'
    if platform.name == 'linux':
        platform = spack.architecture.platform()
        current_os = platform.operating_system('default_os')
        name, version = current_os.name, current_os.version
    LinuxOS = collections.namedtuple('LinuxOS', ['name', 'version'])
    return LinuxOS(name=name, version=version)


@pytest.fixture(scope='session')
def default_config():
    """Isolates the default configuration from the user configs.

    This ensures we can test the real default configuration without having
    tests fail when the user overrides the defaults that we test against."""
    defaults_path = os.path.join(spack.paths.etc_path, 'spack', 'defaults')
    with spack.config.use_configuration(defaults_path) as defaults_config:
        yield defaults_config


@pytest.fixture(scope='session')
def mock_uarch_json(tmpdir_factory):
    """Mock microarchitectures.json with test architecture descriptions."""
    tmpdir = tmpdir_factory.mktemp('microarchitectures')

    uarch_json = py.path.local(spack.paths.test_path).join(
        "data", "microarchitectures", "microarchitectures.json")
    uarch_json.copy(tmpdir)
    yield str(tmpdir.join("microarchitectures.json"))


@pytest.fixture(scope='session')
def mock_uarch_configuration(mock_uarch_json):
    """Create mock dictionaries for the archspec.cpu."""
    def load_json():
        with open(mock_uarch_json) as f:
            return json.load(f)

    targets_json = load_json()
    targets = archspec.cpu.microarchitecture._known_microarchitectures()

    yield targets_json, targets


@pytest.fixture(scope='function')
def mock_targets(mock_uarch_configuration, monkeypatch):
    """Use this fixture to enable mock uarch targets for testing."""
    targets_json, targets = mock_uarch_configuration

    monkeypatch.setattr(archspec.cpu.schema, "TARGETS_JSON", targets_json)
    monkeypatch.setattr(archspec.cpu.microarchitecture, "TARGETS", targets)


@pytest.fixture(scope='session')
def configuration_dir(tmpdir_factory, linux_os):
    """Copies mock configuration files in a temporary directory. Returns the
    directory path.
    """
    tmpdir = tmpdir_factory.mktemp('configurations')

    # <test_path>/data/config has mock config yaml files in it
    # copy these to the site config.
    test_config = py.path.local(spack.paths.test_path).join('data', 'config')
    test_config.copy(tmpdir.join('site'))

    # Create temporary 'defaults', 'site' and 'user' folders
    tmpdir.ensure('user', dir=True)

    # Slightly modify config.yaml and compilers.yaml
    solver = os.environ.get('SPACK_TEST_SOLVER', 'original')
    config_yaml = test_config.join('config.yaml')
    modules_root = tmpdir_factory.mktemp('share')
    tcl_root = modules_root.ensure('modules', dir=True)
    lmod_root = modules_root.ensure('lmod', dir=True)
    content = ''.join(config_yaml.read()).format(
        solver, str(tcl_root), str(lmod_root)
    )
    t = tmpdir.join('site', 'config.yaml')
    t.write(content)

    compilers_yaml = test_config.join('compilers.yaml')
    content = ''.join(compilers_yaml.read()).format(linux_os)
    t = tmpdir.join('site', 'compilers.yaml')
    t.write(content)
    yield tmpdir

    # Once done, cleanup the directory
    shutil.rmtree(str(tmpdir))


@pytest.fixture(scope='session')
def mock_configuration_scopes(configuration_dir):
    """Create a persistent Configuration object from the configuration_dir."""
    defaults = spack.config.InternalConfigScope(
        '_builtin', spack.config.config_defaults
    )
    test_scopes = [defaults]
    test_scopes += [
        spack.config.ConfigScope(name, str(configuration_dir.join(name)))
        for name in ['site', 'system', 'user']]
    test_scopes.append(spack.config.InternalConfigScope('command_line'))

    yield test_scopes


@pytest.fixture(scope='function')
def config(mock_configuration_scopes):
    """This fixture activates/deactivates the mock configuration."""
    with spack.config.use_configuration(*mock_configuration_scopes) as config:
        yield config


@pytest.fixture(scope='function')
def mutable_config(tmpdir_factory, configuration_dir):
    """Like config, but tests can modify the configuration."""
    mutable_dir = tmpdir_factory.mktemp('mutable_config').join('tmp')
    configuration_dir.copy(mutable_dir)

    scopes = [spack.config.ConfigScope(name, str(mutable_dir.join(name)))
              for name in ['site', 'system', 'user']]

    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg


@pytest.fixture(scope='function')
def mutable_empty_config(tmpdir_factory, configuration_dir):
    """Empty configuration that can be modified by the tests."""
    mutable_dir = tmpdir_factory.mktemp('mutable_config').join('tmp')
    scopes = [spack.config.ConfigScope(name, str(mutable_dir.join(name)))
              for name in ['site', 'system', 'user']]

    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg


@pytest.fixture()
def mock_low_high_config(tmpdir):
    """Mocks two configuration scopes: 'low' and 'high'."""
    scopes = [spack.config.ConfigScope(name, str(tmpdir.join(name)))
              for name in ['low', 'high']]

    with spack.config.use_configuration(*scopes) as config:
        yield config


def _populate(mock_db):
    r"""Populate a mock database with packages.

    Here is what the mock DB looks like:

    o  mpileaks     o  mpileaks'    o  mpileaks''
    |\              |\              |\
    | o  callpath   | o  callpath'  | o  callpath''
    |/|             |/|             |/|
    o |  mpich      o |  mpich2     o |  zmpi
      |               |             o |  fake
      |               |               |
      |               |______________/
      | .____________/
      |/
      o  dyninst
      |\
      | o  libdwarf
      |/
      o  libelf
    """
    def _install(spec):
        s = spack.spec.Spec(spec).concretized()
        pkg = spack.repo.get(s)
        pkg.do_install(fake=True, explicit=True)

    _install('mpileaks ^mpich')
    _install('mpileaks ^mpich2')
    _install('mpileaks ^zmpi')
    _install('externaltest')


@pytest.fixture(scope='session')
def _store_dir_and_cache(tmpdir_factory):
    """Returns the directory where to build the mock database and
    where to cache it.
    """
    store = tmpdir_factory.mktemp('mock_store')
    cache = tmpdir_factory.mktemp('mock_store_cache')
    return store, cache


@pytest.fixture(scope='session')
def mock_store(tmpdir_factory, mock_repo_path, mock_configuration_scopes,
               _store_dir_and_cache):
    """Creates a read-only mock database with some packages installed note
    that the ref count for dyninst here will be 3, as it's recycled
    across each install.

    This does not actually activate the store for use by Spack -- see the
    ``database`` fixture for that.

    """
    store_path, store_cache = _store_dir_and_cache

    # If the cache does not exist populate the store and create it
    if not os.path.exists(str(store_cache.join('.spack-db'))):
        with spack.config.use_configuration(*mock_configuration_scopes):
            with spack.store.use_store(str(store_path)) as store:
                with spack.repo.use_repositories(mock_repo_path):
                    _populate(store.db)
        store_path.copy(store_cache, mode=True, stat=True)

    # Make the DB filesystem read-only to ensure we can't modify entries
    store_path.join('.spack-db').chmod(mode=0o555, rec=1)

    yield store_path

    store_path.join('.spack-db').chmod(mode=0o755, rec=1)


@pytest.fixture(scope='function')
def database(mock_store, mock_packages, config, monkeypatch):
    """This activates the mock store, packages, AND config."""
    with spack.store.use_store(str(mock_store)) as store:
        yield store.db
        store.db.last_seen_verifier = ''


@pytest.fixture(scope='function')
def mutable_database(database, _store_dir_and_cache):
    """Writeable version of the fixture, restored to its initial state
    after each test.
    """
    # Make the database writeable, as we are going to modify it
    store_path, store_cache = _store_dir_and_cache
    store_path.join('.spack-db').chmod(mode=0o755, rec=1)

    yield database

    # Restore the initial state by copying the content of the cache back into
    # the store and making the database read-only
    store_path.remove(rec=1)
    store_cache.copy(store_path, mode=True, stat=True)
    store_path.join('.spack-db').chmod(mode=0o555, rec=1)


@pytest.fixture()
def dirs_with_libfiles(tmpdir_factory):
    lib_to_libfiles = {
        'libstdc++': ['libstdc++.so', 'libstdc++.tbd'],
        'libgfortran': ['libgfortran.a', 'libgfortran.dylib'],
        'libirc': ['libirc.a', 'libirc.so']
    }

    root = tmpdir_factory.mktemp('root')
    lib_to_dirs = {}
    i = 0
    for lib, libfiles in lib_to_libfiles.items():
        dirs = []
        for libfile in libfiles:
            root.ensure(str(i), dir=True)
            root.join(str(i)).ensure(libfile)
            dirs.append(str(root.join(str(i))))
            i += 1
        lib_to_dirs[lib] = dirs

    all_dirs = list(itertools.chain.from_iterable(lib_to_dirs.values()))

    yield lib_to_dirs, all_dirs


def _compiler_link_paths_noop(*args):
    return []


@pytest.fixture(scope='function', autouse=True)
def disable_compiler_execution(monkeypatch, request):
    """
    This fixture can be disabled for tests of the compiler link path
    functionality by::

        @pytest.mark.enable_compiler_link_paths

    If a test is marked in that way this is a no-op."""
    if 'enable_compiler_link_paths' not in request.keywords:
        # Compiler.determine_implicit_rpaths actually runs the compiler. So
        # replace that function with a noop that simulates finding no implicit
        # RPATHs
        monkeypatch.setattr(
            spack.compiler.Compiler,
            '_get_compiler_link_paths',
            _compiler_link_paths_noop
        )


@pytest.fixture(scope='function')
def install_mockery(temporary_store, config, mock_packages):
    """Hooks a fake install directory, DB, and stage directory into Spack."""
    # We use a fake package, so temporarily disable checksumming
    with spack.config.override('config:checksum', False):
        yield

    # Also wipe out any cached prefix failure locks (associated with
    # the session-scoped mock archive).
    for pkg_id in list(temporary_store.db._prefix_failures.keys()):
        lock = spack.store.db._prefix_failures.pop(pkg_id, None)
        if lock:
            try:
                lock.release_write()
            except Exception:
                pass


@pytest.fixture(scope='function')
def temporary_store(tmpdir):
    """Hooks a temporary empty store for the test function."""
    temporary_store_path = tmpdir.join('opt')
    with spack.store.use_store(str(temporary_store_path)) as s:
        yield s
    temporary_store_path.remove()


@pytest.fixture(scope='function')
def install_mockery_mutable_config(
        temporary_store, mutable_config, mock_packages
):
    """Hooks a fake install directory, DB, and stage directory into Spack.

    This is specifically for tests which want to use 'install_mockery' but
    also need to modify configuration (and hence would want to use
    'mutable config'): 'install_mockery' does not support this.
    """
    # We use a fake package, so temporarily disable checksumming
    with spack.config.override('config:checksum', False):
        yield


@pytest.fixture()
def mock_fetch(mock_archive, monkeypatch):
    """Fake the URL for a package so it downloads from a file."""
    mock_fetcher = FetchStrategyComposite()
    mock_fetcher.append(URLFetchStrategy(mock_archive.url))

    monkeypatch.setattr(
        spack.package.PackageBase, 'fetcher', mock_fetcher)


class MockLayout(object):
    def __init__(self, root):
        self.root = root

    def path_for_spec(self, spec):
        return '/'.join([self.root, spec.name])

    def check_installed(self, spec):
        return True


@pytest.fixture()
def gen_mock_layout(tmpdir):
    # Generate a MockLayout in a temporary directory. In general the prefixes
    # specified by MockLayout should never be written to, but this ensures
    # that even if they are, that it causes no harm
    def create_layout(root):
        subroot = tmpdir.mkdir(root)
        return MockLayout(str(subroot))

    yield create_layout


class MockConfig(object):
    def __init__(self, configuration, writer_key):
        self._configuration = configuration
        self.writer_key = writer_key

    def configuration(self):
        return self._configuration

    def writer_configuration(self):
        return self.configuration()[self.writer_key]


class ConfigUpdate(object):
    def __init__(self, root_for_conf, writer_mod, writer_key, monkeypatch):
        self.root_for_conf = root_for_conf
        self.writer_mod = writer_mod
        self.writer_key = writer_key
        self.monkeypatch = monkeypatch

    def __call__(self, filename):
        file = os.path.join(self.root_for_conf, filename + '.yaml')
        with open(file) as f:
            mock_config = MockConfig(syaml.load_config(f), self.writer_key)

        self.monkeypatch.setattr(
            spack.modules.common,
            'configuration',
            mock_config.configuration
        )
        self.monkeypatch.setattr(
            self.writer_mod,
            'configuration',
            mock_config.writer_configuration
        )
        self.monkeypatch.setattr(
            self.writer_mod,
            'configuration_registry',
            {}
        )


@pytest.fixture()
def module_configuration(monkeypatch, request):
    """Reads the module configuration file from the mock ones prepared
    for tests and monkeypatches the right classes to hook it in.
    """
    # Class of the module file writer
    writer_cls = getattr(request.module, 'writer_cls')
    # Module where the module file writer is defined
    writer_mod = inspect.getmodule(writer_cls)
    # Key for specific settings relative to this module type
    writer_key = str(writer_mod.__name__).split('.')[-1]
    # Root folder for configuration
    root_for_conf = os.path.join(
        spack.paths.test_path, 'data', 'modules', writer_key
    )

    return ConfigUpdate(root_for_conf, writer_mod, writer_key, monkeypatch)


@pytest.fixture()
def mock_gnupghome(monkeypatch):
    # GNU PGP can't handle paths longer than 108 characters (wtf!@#$) so we
    # have to make our own tmpdir with a shorter name than pytest's.
    # This comes up because tmp paths on macOS are already long-ish, and
    # pytest makes them longer.
    short_name_tmpdir = tempfile.mkdtemp()
    with spack.util.gpg.gnupg_home_override(short_name_tmpdir):
        yield short_name_tmpdir

    # clean up, since we are doing this manually
    shutil.rmtree(short_name_tmpdir)

##########
# Fake archives and repositories
##########


@pytest.fixture(scope='session', params=[('.tar.gz', 'z')])
def mock_archive(request, tmpdir_factory):
    """Creates a very simple archive directory with a configure script and a
    makefile that installs to a prefix. Tars it up into an archive.
    """
    tar = spack.util.executable.which('tar', required=True)

    tmpdir = tmpdir_factory.mktemp('mock-archive-dir')
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)

    # Create the configure script
    configure_path = str(tmpdir.join(spack.stage._source_path_subdir,
                                     'configure'))
    with open(configure_path, 'w') as f:
        f.write(
            "#!/bin/sh\n"
            "prefix=$(echo $1 | sed 's/--prefix=//')\n"
            "cat > Makefile <<EOF\n"
            "all:\n"
            "\techo Building...\n\n"
            "install:\n"
            "\tmkdir -p $prefix\n"
            "\ttouch $prefix/dummy_file\n"
            "EOF\n"
        )
    os.chmod(configure_path, 0o755)

    # Archive it
    with tmpdir.as_cwd():
        archive_name = '{0}{1}'.format(spack.stage._source_path_subdir,
                                       request.param[0])
        tar('-c{0}f'.format(request.param[1]), archive_name,
            spack.stage._source_path_subdir)

    Archive = collections.namedtuple('Archive',
                                     ['url', 'path', 'archive_file',
                                      'expanded_archive_basedir'])
    archive_file = str(tmpdir.join(archive_name))

    # Return the url
    yield Archive(
        url=('file://' + archive_file),
        archive_file=archive_file,
        path=str(repodir),
        expanded_archive_basedir=spack.stage._source_path_subdir)


@pytest.fixture(scope='session')
def mock_git_repository(tmpdir_factory):
    """Creates a simple git repository with two branches,
    two commits and two submodules. Each submodule has one commit.
    """
    git = spack.util.executable.which('git', required=True)

    suburls = []
    for submodule_count in range(2):
        tmpdir = tmpdir_factory.mktemp('mock-git-repo-submodule-dir-{0}'
                                       .format(submodule_count))
        tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
        repodir = tmpdir.join(spack.stage._source_path_subdir)
        suburls.append((submodule_count, 'file://' + str(repodir)))

        # Initialize the repository
        with repodir.as_cwd():
            git('init')
            git('config', 'user.name', 'Spack')
            git('config', 'user.email', 'spack@spack.io')

            # r0 is just the first commit
            submodule_file = 'r0_file_{0}'.format(submodule_count)
            repodir.ensure(submodule_file)
            git('add', submodule_file)
            git('-c', 'commit.gpgsign=false', 'commit',
                '-m', 'mock-git-repo r0 {0}'.format(submodule_count))

    tmpdir = tmpdir_factory.mktemp('mock-git-repo-dir')
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)

    # Initialize the repository
    with repodir.as_cwd():
        git('init')
        git('config', 'user.name', 'Spack')
        git('config', 'user.email', 'spack@spack.io')
        url = 'file://' + str(repodir)
        for number, suburl in suburls:
            git('submodule', 'add', suburl,
                'third_party/submodule{0}'.format(number))

        # r0 is just the first commit
        r0_file = 'r0_file'
        repodir.ensure(r0_file)
        git('add', r0_file)
        git('-c', 'commit.gpgsign=false', 'commit', '-m', 'mock-git-repo r0')

        branch = 'test-branch'
        branch_file = 'branch_file'
        git('branch', branch)

        tag_branch = 'tag-branch'
        tag_file = 'tag_file'
        git('branch', tag_branch)

        # Check out first branch
        git('checkout', branch)
        repodir.ensure(branch_file)
        git('add', branch_file)
        git('-c', 'commit.gpgsign=false', 'commit', '-m' 'r1 test branch')

        # Check out a second branch and tag it
        git('checkout', tag_branch)
        repodir.ensure(tag_file)
        git('add', tag_file)
        git('-c', 'commit.gpgsign=false', 'commit', '-m' 'tag test branch')

        tag = 'test-tag'
        git('tag', tag)

        git('checkout', 'master')

        # R1 test is the same as test for branch
        rev_hash = lambda x: git('rev-parse', x, output=str).strip()
        r1 = rev_hash(branch)
        r1_file = branch_file

    checks = {
        'master': Bunch(
            revision='master', file=r0_file, args={'git': url}
        ),
        'branch': Bunch(
            revision=branch, file=branch_file, args={
                'git': url, 'branch': branch
            }
        ),
        'tag-branch': Bunch(
            revision=tag_branch, file=tag_file, args={
                'git': url, 'branch': tag_branch
            }
        ),
        'tag': Bunch(
            revision=tag, file=tag_file, args={'git': url, 'tag': tag}
        ),
        'commit': Bunch(
            revision=r1, file=r1_file, args={'git': url, 'commit': r1}
        )
    }

    t = Bunch(checks=checks, url=url, hash=rev_hash,
              path=str(repodir), git_exe=git)
    yield t


@pytest.fixture(scope='session')
def mock_hg_repository(tmpdir_factory):
    """Creates a very simple hg repository with two commits."""
    hg = spack.util.executable.which('hg', required=True)

    tmpdir = tmpdir_factory.mktemp('mock-hg-repo-dir')
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)

    get_rev = lambda: hg('id', '-i', output=str).strip()

    # Initialize the repository
    with repodir.as_cwd():
        url = 'file://' + str(repodir)
        hg('init')

        # Commit file r0
        r0_file = 'r0_file'
        repodir.ensure(r0_file)
        hg('add', r0_file)
        hg('commit', '-m', 'revision 0', '-u', 'test')
        r0 = get_rev()

        # Commit file r1
        r1_file = 'r1_file'
        repodir.ensure(r1_file)
        hg('add', r1_file)
        hg('commit', '-m' 'revision 1', '-u', 'test')
        r1 = get_rev()

    checks = {
        'default': Bunch(
            revision=r1, file=r1_file, args={'hg': str(repodir)}
        ),
        'rev0': Bunch(
            revision=r0, file=r0_file, args={
                'hg': str(repodir), 'revision': r0
            }
        )
    }
    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t


@pytest.fixture(scope='session')
def mock_svn_repository(tmpdir_factory):
    """Creates a very simple svn repository with two commits."""
    svn = spack.util.executable.which('svn', required=True)
    svnadmin = spack.util.executable.which('svnadmin', required=True)

    tmpdir = tmpdir_factory.mktemp('mock-svn-stage')
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)
    url = 'file://' + str(repodir)

    # Initialize the repository
    with repodir.as_cwd():
        # NOTE: Adding --pre-1.5-compatible works for NERSC
        # Unknown if this is also an issue at other sites.
        svnadmin('create', '--pre-1.5-compatible', str(repodir))

        # Import a structure (first commit)
        r0_file = 'r0_file'
        tmpdir.ensure('tmp-path', r0_file)
        tmp_path = tmpdir.join('tmp-path')
        svn('import',
            str(tmp_path),
            url,
            '-m',
            'Initial import r0')
        tmp_path.remove()

        # Second commit
        r1_file = 'r1_file'
        svn('checkout', url, str(tmp_path))
        tmpdir.ensure('tmp-path', r1_file)

        with tmp_path.as_cwd():
            svn('add', str(tmpdir.ensure('tmp-path', r1_file)))
            svn('ci', '-m', 'second revision r1')

        tmp_path.remove()
        r0 = '1'
        r1 = '2'

    checks = {
        'default': Bunch(
            revision=r1, file=r1_file, args={'svn': url}),
        'rev0': Bunch(
            revision=r0, file=r0_file, args={
                'svn': url, 'revision': r0})
    }

    def get_rev():
        output = svn('info', '--xml', output=str)
        info = xml.etree.ElementTree.fromstring(output)
        return info.find('entry/commit').get('revision')

    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t


@pytest.fixture()
def mutable_mock_env_path(tmpdir_factory):
    """Fixture for mocking the internal spack environments directory."""
    saved_path = spack.environment.env_path
    mock_path = tmpdir_factory.mktemp('mock-env-path')
    spack.environment.env_path = str(mock_path)
    yield mock_path
    spack.environment.env_path = saved_path


@pytest.fixture()
def installation_dir_with_headers(tmpdir_factory):
    """Mock installation tree with a few headers placed in different
    subdirectories. Shouldn't be modified by tests as it is session
    scoped.
    """
    root = tmpdir_factory.mktemp('prefix')

    # Create a few header files:
    #
    # <prefix>
    # |-- include
    # |   |--boost
    # |   |   |-- ex3.h
    # |   |-- ex3.h
    # |-- path
    #     |-- to
    #         |-- ex1.h
    #         |-- subdir
    #             |-- ex2.h
    #
    root.ensure('include', 'boost', 'ex3.h')
    root.ensure('include', 'ex3.h')
    root.ensure('path', 'to', 'ex1.h')
    root.ensure('path', 'to', 'subdir', 'ex2.h')

    return root


##########
# Specs of various kind
##########


@pytest.fixture(
    params=[
        'conflict%clang+foo',
        'conflict-parent@0.9^conflict~foo'
    ]
)
def conflict_spec(request):
    """Specs which violate constraints specified with the "conflicts"
    directive in the "conflict" package.
    """
    return request.param


@pytest.fixture(
    params=[
        'conflict%~'
    ]
)
def invalid_spec(request):
    """Specs that do not parse cleanly due to invalid formatting.
    """
    return request.param


@pytest.fixture("module")
def mock_test_repo(tmpdir_factory):
    """Create an empty repository."""
    repo_namespace = 'mock_test_repo'
    repodir = tmpdir_factory.mktemp(repo_namespace)
    repodir.ensure(spack.repo.packages_dir_name, dir=True)
    yaml = repodir.join('repo.yaml')
    yaml.write("""
repo:
    namespace: mock_test_repo
""")

    with spack.repo.use_repositories(str(repodir)) as repo:
        yield repo, repodir

    shutil.rmtree(str(repodir))


##########
# Class and fixture to work around problems raising exceptions in directives,
# which cause tests like test_from_list_url to hang for Python 2.x metaclass
# processing.
#
# At this point only version and patch directive handling has been addressed.
##########

class MockBundle(object):
    has_code = False
    name = 'mock-bundle'
    versions = {}  # type: ignore


@pytest.fixture
def mock_directive_bundle():
    """Return a mock bundle package for directive tests."""
    return MockBundle()


@pytest.fixture
def clear_directive_functions():
    """Clear all overidden directive functions for subsequent tests."""
    yield

    # Make sure any directive functions overidden by tests are cleared before
    # proceeding with subsequent tests that may depend on the original
    # functions.
    spack.directives.DirectiveMeta._directives_to_be_executed = []


@pytest.fixture
def mock_executable(tmpdir):
    """Factory to create a mock executable in a temporary directory that
    output a custom string when run.
    """
    import jinja2

    def _factory(name, output, subdir=('bin',)):
        f = tmpdir.ensure(*subdir, dir=True).join(name)
        t = jinja2.Template('#!/bin/bash\n{{ output }}\n')
        f.write(t.render(output=output))
        f.chmod(0o755)
        return str(f)

    return _factory


@pytest.fixture()
def mock_test_stage(mutable_config, tmpdir):
    # NOTE: This fixture MUST be applied after any fixture that uses
    # the config fixture under the hood
    # No need to unset because we use mutable_config
    tmp_stage = str(tmpdir.join('test_stage'))
    mutable_config.set('config:test_stage', tmp_stage)

    yield tmp_stage
