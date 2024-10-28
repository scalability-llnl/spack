# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import datetime
import errno
import functools
import inspect
import itertools
import json
import os
import os.path
import pathlib
import re
import shutil
import stat
import sys
import tempfile
import xml.etree.ElementTree

import py
import pytest

import archspec.cpu
import archspec.cpu.microarchitecture
import archspec.cpu.schema

import llnl.util.lang
import llnl.util.lock
import llnl.util.tty as tty
from llnl.util.filesystem import copy_tree, mkdirp, remove_linked_tree, touchp, working_dir

import spack.binary_distribution
import spack.bootstrap.core
import spack.caches
import spack.compiler
import spack.compilers
import spack.config
import spack.directives
import spack.environment as ev
import spack.error
import spack.modules.common
import spack.package_base
import spack.paths
import spack.platforms
import spack.repo
import spack.solver.asp
import spack.spec
import spack.stage
import spack.store
import spack.subprocess_context
import spack.util.executable
import spack.util.file_cache
import spack.util.git
import spack.util.gpg
import spack.util.parallel
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web
import spack.version
from spack.fetch_strategy import URLFetchStrategy
from spack.installer import PackageInstaller
from spack.main import SpackCommand
from spack.util.pattern import Bunch

mirror_cmd = SpackCommand("mirror")


@pytest.fixture(autouse=True)
def check_config_fixture(request):
    if "config" in request.fixturenames and "mutable_config" in request.fixturenames:
        raise RuntimeError("'config' and 'mutable_config' are both requested")


def ensure_configuration_fixture_run_before(request):
    """Ensure that fixture mutating the configuration run before the one where
    the function is called.
    """
    if "config" in request.fixturenames:
        request.getfixturevalue("config")
    if "mutable_config" in request.fixturenames:
        request.getfixturevalue("mutable_config")


@pytest.fixture(scope="session")
def git():
    """Fixture for tests that use git."""
    if not spack.util.git.git():
        pytest.skip("requires git to be installed")

    return spack.util.git.git(required=True)


#
# Return list of shas for latest two git commits in local spack repo
#
@pytest.fixture(scope="session")
def last_two_git_commits(git):
    spack_git_path = spack.paths.prefix
    with working_dir(spack_git_path):
        git_log_out = git("log", "-n", "2", output=str, error=os.devnull)

    regex = re.compile(r"^commit\s([^\s]+$)", re.MULTILINE)
    yield regex.findall(git_log_out)


def write_file(filename, contents):
    with open(filename, "w") as f:
        f.write(contents)


commit_counter = 0


@pytest.fixture
def override_git_repos_cache_path(tmpdir):
    saved = spack.paths.user_repos_cache_path
    tmp_path = tmpdir.mkdir("git-repo-cache-path-for-tests")
    spack.paths.user_repos_cache_path = str(tmp_path)
    yield
    spack.paths.user_repos_cache_path = saved


@pytest.fixture
def mock_git_version_info(git, tmpdir, override_git_repos_cache_path):
    """Create a mock git repo with known structure

    The structure of commits in this repo is as follows::

       | o fourth 1.x commit (1.2)
       | o third 1.x commit
       | |
       o | fourth main commit (v2.0)
       o | third main commit
       | |
       | o second 1.x commit (v1.1)
       | o first 1.x commit
       | /
       |/
       o second commit (v1.0)
       o first commit

    The repo consists of a single file, in which the GitVersion._ref_version representation
    of each commit is expressed as a string.

    Important attributes of the repo for test coverage are: multiple branches,
    version tags on multiple branches, and version order is not equal to time
    order or topological order.
    """
    repo_path = str(tmpdir.mkdir("git_repo"))
    filename = "file.txt"

    def commit(message):
        global commit_counter
        git(
            "commit",
            "--no-gpg-sign",
            "--date",
            "2020-01-%02d 12:0:00 +0300" % commit_counter,
            "-am",
            message,
        )
        commit_counter += 1

    with working_dir(repo_path):
        git("init")

        git("config", "user.name", "Spack")
        git("config", "user.email", "spack@spack.io")

        commits = []

        def latest_commit():
            return git("rev-list", "-n1", "HEAD", output=str, error=str).strip()

        # Add two commits on main branch

        # A commit without a previous version counts as "0"
        write_file(filename, "[0]")
        git("add", filename)
        commit("first commit")
        commits.append(latest_commit())

        # Get name of default branch (differs by git version)
        main = git("rev-parse", "--abbrev-ref", "HEAD", output=str, error=str).strip()

        # Tag second commit as v1.0
        write_file(filename, "[1, 0]")
        commit("second commit")
        commits.append(latest_commit())
        git("tag", "v1.0")

        # Add two commits and a tag on 1.x branch
        git("checkout", "-b", "1.x")
        write_file(filename, "[1, 0, 'git', 1]")
        commit("first 1.x commit")
        commits.append(latest_commit())

        write_file(filename, "[1, 1]")
        commit("second 1.x commit")
        commits.append(latest_commit())
        git("tag", "v1.1")

        # Add two commits and a tag on main branch
        git("checkout", main)
        write_file(filename, "[1, 0, 'git', 1]")
        commit("third main commit")
        commits.append(latest_commit())
        write_file(filename, "[2, 0]")
        commit("fourth main commit")
        commits.append(latest_commit())
        git("tag", "v2.0")

        # Add two more commits on 1.x branch to ensure we aren't cheating by using time
        git("checkout", "1.x")
        write_file(filename, "[1, 1, 'git', 1]")
        commit("third 1.x commit")
        commits.append(latest_commit())
        write_file(filename, "[1, 2]")
        commit("fourth 1.x commit")
        commits.append(latest_commit())
        git("tag", "1.2")  # test robust parsing to different syntax, no v

        # The commits are ordered with the last commit first in the list
        commits = list(reversed(commits))

    # Return the git directory to install, the filename used, and the commits
    yield repo_path, filename, commits


@pytest.fixture(autouse=True)
def clear_recorded_monkeypatches():
    yield
    spack.subprocess_context.clear_patches()


@pytest.fixture(scope="session", autouse=True)
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
    monkeypatch.setattr(os, "access", _can_access)


#
# Disable any active Spack environment BEFORE all tests
#
@pytest.fixture(scope="session", autouse=True)
def clean_user_environment():
    spack_env_value = os.environ.pop(ev.spack_env_var, None)
    with ev.no_active_environment():
        yield
    if spack_env_value:
        os.environ[ev.spack_env_var] = spack_env_value


#
# Make sure global state of active env does not leak between tests.
#
@pytest.fixture(scope="function", autouse=True)
def clean_test_environment():
    yield
    ev.deactivate()


def _host():
    """Mock archspec host so there is no inconsistency on the Windows platform
    This function cannot be local as it needs to be pickleable"""
    return archspec.cpu.Microarchitecture("x86_64", [], "generic", [], {}, 0)


@pytest.fixture(scope="function")
def archspec_host_is_spack_test_host(monkeypatch):
    monkeypatch.setattr(archspec.cpu, "host", _host)


#
# Disable checks on compiler executable existence
#
@pytest.fixture(scope="function", autouse=True)
def mock_compiler_executable_verification(request, monkeypatch):
    """Mock the compiler executable verification to allow missing executables.

    This fixture can be disabled for tests of the compiler verification
    functionality by::

        @pytest.mark.enable_compiler_verification

    If a test is marked in that way this is a no-op."""
    if "enable_compiler_verification" not in request.keywords:
        monkeypatch.setattr(spack.compiler.Compiler, "verify_executables", _return_none)


# Hooks to add command line options or set other custom behaviors.
# They must be placed here to be found by pytest. See:
#
# https://docs.pytest.org/en/latest/writing_plugins.html
#
def pytest_addoption(parser):
    group = parser.getgroup("Spack specific command line options")
    group.addoption(
        "--fast",
        action="store_true",
        default=False,
        help='runs only "fast" unit tests, instead of the whole suite',
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--fast"):
        # --fast not given, run all the tests
        return

    slow_tests = ["db", "network", "maybeslow"]
    skip_as_slow = pytest.mark.skip(reason="skipped slow test [--fast command line option given]")
    for item in items:
        if any(x in item.keywords for x in slow_tests):
            item.add_marker(skip_as_slow)


#
# These fixtures are applied to all tests
#
@pytest.fixture(scope="function", autouse=True)
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


@pytest.fixture(scope="function", autouse=True)
def reset_compiler_cache():
    """Ensure that the compiler cache is not shared across Spack tests

    This cache can cause later tests to fail if left in a state incompatible
    with the new configuration. Since tests can make almost unlimited changes
    to their setup, default to not use the compiler cache across tests."""
    spack.compilers._compiler_cache = {}
    yield
    spack.compilers._compiler_cache = {}


def onerror(func, path, error_info):
    # Python on Windows is unable to remvove paths without
    # write (IWUSR) permissions (such as those generated by Git on Windows)
    # This method changes file permissions to allow removal by Python
    os.chmod(path, stat.S_IWUSR)
    func(path)


@pytest.fixture(scope="function", autouse=True)
def mock_stage(tmpdir_factory, monkeypatch, request):
    """Establish the temporary build_stage for the mock archive."""
    # The approach with this autouse fixture is to set the stage root
    # instead of using spack.config.override() to avoid configuration
    # conflicts with dozens of tests that rely on other configuration
    # fixtures, such as config.
    if "nomockstage" not in request.keywords:
        # Set the build stage to the requested path
        new_stage = tmpdir_factory.mktemp("mock-stage")
        new_stage_path = str(new_stage)

        # Ensure the source directory exists within the new stage path
        source_path = os.path.join(new_stage_path, spack.stage._source_path_subdir)
        mkdirp(source_path)

        monkeypatch.setattr(spack.stage, "_stage_root", new_stage_path)

        yield new_stage_path

        # Clean up the test stage directory
        if os.path.isdir(new_stage_path):
            shutil.rmtree(new_stage_path, onerror=onerror)
    else:
        # Must yield a path to avoid a TypeError on test teardown
        yield str(tmpdir_factory)


@pytest.fixture(scope="session")
def ignore_stage_files():
    """Session-scoped helper for check_for_leftover_stage_files.

    Used to track which leftover files in the stage have been seen.
    """
    # to start with, ignore the .lock file at the stage root.
    return set([".lock", spack.stage._source_path_subdir, "build_cache"])


def remove_whatever_it_is(path):
    """Type-agnostic remove."""
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.islink(path):
        remove_linked_tree(path)
    else:
        shutil.rmtree(path, onerror=onerror)


@pytest.fixture
def working_env():
    saved_env = os.environ.copy()
    yield
    # os.environ = saved_env doesn't work
    # it causes module_parsing::test_module_function to fail
    # when it's run after any test using this fixutre
    os.environ.clear()
    os.environ.update(saved_env)


@pytest.fixture(scope="function", autouse=True)
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
        if err.errno == errno.ENOENT or err.errno == errno.EINVAL:
            pass
        else:
            raise

    if "disable_clean_stage_check" in request.keywords:
        # clean up after tests that are expected to be dirty
        for f in files_in_stage:
            path = os.path.join(stage_path, f)
            remove_whatever_it_is(path)
    else:
        ignore_stage_files |= files_in_stage
        assert not files_in_stage


class MockCache:
    def store(self, copy_cmd, relative_dest):
        pass

    def fetcher(self, target_path, digest, **kwargs):
        return MockCacheFetcher()


class MockCacheFetcher:
    def fetch(self):
        raise spack.error.FetchError("Mock cache always fails for tests")

    def __str__(self):
        return "[mock fetch cache]"


@pytest.fixture(autouse=True)
def mock_fetch_cache(monkeypatch):
    """Substitutes spack.paths.FETCH_CACHE with a mock object that does nothing
    and raises on fetch.
    """
    monkeypatch.setattr(spack.caches, "FETCH_CACHE", MockCache())


@pytest.fixture()
def mock_binary_index(monkeypatch, tmpdir_factory):
    """Changes the directory for the binary index and creates binary index for
    every test. Clears its own index when it's done.
    """
    tmpdir = tmpdir_factory.mktemp("mock_binary_index")
    index_path = tmpdir.join("binary_index").strpath
    mock_index = spack.binary_distribution.BinaryCacheIndex(index_path)
    monkeypatch.setattr(spack.binary_distribution, "BINARY_INDEX", mock_index)
    yield


@pytest.fixture(autouse=True)
def _skip_if_missing_executables(request):
    """Permits to mark tests with 'require_executables' and skip the
    tests if the executables passed as arguments are not found.
    """
    if hasattr(request.node, "get_marker"):
        # TODO: Remove the deprecated API as soon as we drop support for Python 2.6
        marker = request.node.get_marker("requires_executables")
    else:
        marker = request.node.get_closest_marker("requires_executables")

    if marker:
        required_execs = marker.args
        missing_execs = [x for x in required_execs if spack.util.executable.which(x) is None]
        if missing_execs:
            msg = "could not find executables: {0}"
            pytest.skip(msg.format(", ".join(missing_execs)))


@pytest.fixture(scope="session")
def test_platform():
    return spack.platforms.Test()


@pytest.fixture(autouse=True, scope="session")
def _use_test_platform(test_platform):
    # This is the only context manager used at session scope (see note
    # below for more insight) since we want to use the test platform as
    # a default during tests.
    with spack.platforms.use_platform(test_platform):
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
@pytest.fixture(scope="session")
def mock_repo_path():
    yield spack.repo.from_path(spack.paths.mock_packages_path)


def _pkg_install_fn(pkg, spec, prefix):
    # sanity_check_prefix requires something in the install directory
    mkdirp(prefix.bin)
    if not os.path.exists(spec.package.install_log_path):
        touchp(spec.package.install_log_path)


@pytest.fixture
def mock_pkg_install(monkeypatch):
    monkeypatch.setattr(spack.package_base.PackageBase, "install", _pkg_install_fn, raising=False)


@pytest.fixture(scope="function")
def mock_packages(mock_repo_path, mock_pkg_install, request):
    """Use the 'builtin.mock' repository instead of 'builtin'"""
    ensure_configuration_fixture_run_before(request)
    with spack.repo.use_repositories(mock_repo_path) as mock_repo:
        yield mock_repo


@pytest.fixture(scope="function")
def mutable_mock_repo(mock_repo_path, request):
    """Function-scoped mock packages, for tests that need to modify them."""
    ensure_configuration_fixture_run_before(request)
    mock_repo = spack.repo.from_path(spack.paths.mock_packages_path)
    with spack.repo.use_repositories(mock_repo) as mock_repo_path:
        yield mock_repo_path


@pytest.fixture()
def mock_custom_repository(tmpdir, mutable_mock_repo):
    """Create a custom repository with a single package "c" and return its path."""
    builder = spack.repo.MockRepositoryBuilder(tmpdir.mkdir("myrepo"))
    builder.add_package("pkg-c")
    return builder.root


@pytest.fixture(scope="session")
def linux_os():
    """Returns a named tuple with attributes 'name' and 'version'
    representing the OS.
    """
    platform = spack.platforms.host()
    name, version = "debian", "6"
    if platform.name == "linux":
        current_os = platform.operating_system("default_os")
        name, version = current_os.name, current_os.version
    LinuxOS = collections.namedtuple("LinuxOS", ["name", "version"])
    return LinuxOS(name=name, version=version)


@pytest.fixture
def ensure_debug(monkeypatch):
    current_debug_level = tty.debug_level()
    tty.set_debug(1)

    yield

    tty.set_debug(current_debug_level)


@pytest.fixture(autouse=sys.platform == "win32", scope="session")
def platform_config():
    spack.config.add_default_platform_scope(spack.platforms.real_host().name)


@pytest.fixture
def default_config():
    """Isolates the default configuration from the user configs.

    This ensures we can test the real default configuration without having
    tests fail when the user overrides the defaults that we test against."""
    defaults_path = os.path.join(spack.paths.etc_path, "defaults")
    if sys.platform == "win32":
        defaults_path = os.path.join(defaults_path, "windows")
    with spack.config.use_configuration(defaults_path) as defaults_config:
        yield defaults_config


@pytest.fixture(scope="session")
def mock_uarch_json(tmpdir_factory):
    """Mock microarchitectures.json with test architecture descriptions."""
    tmpdir = tmpdir_factory.mktemp("microarchitectures")

    uarch_json = py.path.local(spack.paths.test_path).join(
        "data", "microarchitectures", "microarchitectures.json"
    )
    uarch_json.copy(tmpdir)
    yield str(tmpdir.join("microarchitectures.json"))


@pytest.fixture(scope="session")
def mock_uarch_configuration(mock_uarch_json):
    """Create mock dictionaries for the archspec.cpu."""

    def load_json():
        with open(mock_uarch_json) as f:
            return json.load(f)

    targets_json = load_json()
    targets = archspec.cpu.microarchitecture._known_microarchitectures()

    yield targets_json, targets


@pytest.fixture(scope="function")
def mock_targets(mock_uarch_configuration, monkeypatch):
    """Use this fixture to enable mock uarch targets for testing."""
    targets_json, targets = mock_uarch_configuration

    monkeypatch.setattr(archspec.cpu.schema, "TARGETS_JSON", targets_json)
    monkeypatch.setattr(archspec.cpu.microarchitecture, "TARGETS", targets)


@pytest.fixture(scope="session")
def configuration_dir(tmpdir_factory, linux_os):
    """Copies mock configuration files in a temporary directory. Returns the
    directory path.
    """
    tmpdir = tmpdir_factory.mktemp("configurations")
    install_tree_root = tmpdir_factory.mktemp("opt")
    modules_root = tmpdir_factory.mktemp("share")
    tcl_root = modules_root.ensure("modules", dir=True)
    lmod_root = modules_root.ensure("lmod", dir=True)

    # <test_path>/data/config has mock config yaml files in it
    # copy these to the site config.
    test_config = pathlib.Path(spack.paths.test_path) / "data" / "config"
    shutil.copytree(test_config, tmpdir.join("site"))

    # Create temporary 'defaults', 'site' and 'user' folders
    tmpdir.ensure("user", dir=True)

    # Fill out config.yaml, compilers.yaml and modules.yaml templates.
    locks = sys.platform != "win32"
    config = tmpdir.join("site", "config.yaml")
    config_template = test_config / "config.yaml"
    config.write(config_template.read_text().format(install_tree_root, locks))

    target = str(archspec.cpu.host().family)
    compilers = tmpdir.join("site", "compilers.yaml")
    compilers_template = test_config / "compilers.yaml"
    compilers.write(compilers_template.read_text().format(linux_os=linux_os, target=target))

    modules = tmpdir.join("site", "modules.yaml")
    modules_template = test_config / "modules.yaml"
    modules.write(modules_template.read_text().format(tcl_root, lmod_root))
    yield tmpdir


def _create_mock_configuration_scopes(configuration_dir):
    """Create the configuration scopes used in `config` and `mutable_config`."""
    return [
        spack.config.InternalConfigScope("_builtin", spack.config.CONFIG_DEFAULTS),
        spack.config.DirectoryConfigScope("site", str(configuration_dir.join("site"))),
        spack.config.DirectoryConfigScope("system", str(configuration_dir.join("system"))),
        spack.config.DirectoryConfigScope("user", str(configuration_dir.join("user"))),
        spack.config.InternalConfigScope("command_line"),
    ]


@pytest.fixture(scope="session")
def mock_configuration_scopes(configuration_dir):
    """Create a persistent Configuration object from the configuration_dir."""
    yield _create_mock_configuration_scopes(configuration_dir)


@pytest.fixture(scope="function")
def config(mock_configuration_scopes):
    """This fixture activates/deactivates the mock configuration."""
    with spack.config.use_configuration(*mock_configuration_scopes) as config:
        yield config


@pytest.fixture(scope="function")
def mutable_config(tmpdir_factory, configuration_dir):
    """Like config, but tests can modify the configuration."""
    mutable_dir = tmpdir_factory.mktemp("mutable_config").join("tmp")
    configuration_dir.copy(mutable_dir)

    scopes = _create_mock_configuration_scopes(mutable_dir)
    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg


@pytest.fixture(scope="function")
def mutable_empty_config(tmpdir_factory, configuration_dir):
    """Empty configuration that can be modified by the tests."""
    mutable_dir = tmpdir_factory.mktemp("mutable_config").join("tmp")
    scopes = [
        spack.config.DirectoryConfigScope(name, str(mutable_dir.join(name)))
        for name in ["site", "system", "user"]
    ]

    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg


# From  https://github.com/pytest-dev/pytest/issues/363#issuecomment-1335631998
# Current suggested implementation from issue compatible with pytest >= 6.2
# this may be subject to change as new versions of Pytest are released
# and update the suggested solution
@pytest.fixture(scope="session")
def monkeypatch_session():
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield monkeypatch


@pytest.fixture(scope="session", autouse=True)
def mock_wsdk_externals(monkeypatch_session):
    """Skip check for required external packages on Windows during testing
    Note: In general this should cover this behavior for all tests,
    however any session scoped fixture involving concretization should
    include this fixture
    """
    monkeypatch_session.setattr(
        spack.bootstrap.core, "ensure_winsdk_external_or_raise", _return_none
    )


@pytest.fixture(scope="function")
def concretize_scope(mutable_config, tmpdir):
    """Adds a scope for concretization preferences"""
    tmpdir.ensure_dir("concretize")
    mutable_config.push_scope(
        spack.config.DirectoryConfigScope("concretize", str(tmpdir.join("concretize")))
    )

    yield str(tmpdir.join("concretize"))

    mutable_config.pop_scope()
    spack.repo.PATH._provider_index = None


@pytest.fixture
def no_compilers_yaml(mutable_config):
    """Creates a temporary configuration without compilers.yaml"""
    for local_config in mutable_config.scopes.values():
        if not isinstance(local_config, spack.config.DirectoryConfigScope):
            continue
        compilers_yaml = local_config.get_section_filename("compilers")
        if os.path.exists(compilers_yaml):
            os.remove(compilers_yaml)
    return mutable_config


@pytest.fixture()
def mock_low_high_config(tmpdir):
    """Mocks two configuration scopes: 'low' and 'high'."""
    scopes = [
        spack.config.DirectoryConfigScope(name, str(tmpdir.join(name))) for name in ["low", "high"]
    ]

    with spack.config.use_configuration(*scopes) as config:
        yield config


def _populate(mock_db):
    r"""Populate a mock database with packages.

    Here is what the mock DB looks like (explicit roots at top):

    o  mpileaks     o  mpileaks'    o  mpileaks''     o externaltest     o trivial-smoke-test
    |\              |\              |\                |
    | o  callpath   | o  callpath'  | o  callpath''   o externaltool
    |/|             |/|             |/|               |
    o |  mpich      o |  mpich2     o |  zmpi         o externalvirtual
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
        PackageInstaller([s.package], fake=True, explicit=True).install()

    _install("mpileaks ^mpich")
    _install("mpileaks ^mpich2")
    _install("mpileaks ^zmpi")
    _install("externaltest ^externalvirtual")
    _install("trivial-smoke-test")


@pytest.fixture(scope="session")
def _store_dir_and_cache(tmpdir_factory):
    """Returns the directory where to build the mock database and
    where to cache it.
    """
    store = tmpdir_factory.mktemp("mock_store")
    cache = tmpdir_factory.mktemp("mock_store_cache")
    return store, cache


@pytest.fixture(scope="session")
def mock_store(
    tmpdir_factory,
    mock_wsdk_externals,
    mock_repo_path,
    mock_configuration_scopes,
    _store_dir_and_cache,
):
    """Creates a read-only mock database with some packages installed note
    that the ref count for dyninst here will be 3, as it's recycled
    across each install.

    This does not actually activate the store for use by Spack -- see the
    ``database`` fixture for that.

    """
    store_path, store_cache = _store_dir_and_cache

    # If the cache does not exist populate the store and create it
    if not os.path.exists(str(store_cache.join(".spack-db"))):
        with spack.config.use_configuration(*mock_configuration_scopes):
            with spack.store.use_store(str(store_path)) as store:
                with spack.repo.use_repositories(mock_repo_path):
                    _populate(store.db)
        copy_tree(str(store_path), str(store_cache))

    # Make the DB filesystem read-only to ensure we can't modify entries
    store_path.join(".spack-db").chmod(mode=0o555, rec=1)

    yield store_path

    store_path.join(".spack-db").chmod(mode=0o755, rec=1)


@pytest.fixture(scope="function")
def database(mock_store, mock_packages, config):
    """This activates the mock store, packages, AND config."""
    with spack.store.use_store(str(mock_store)) as store:
        yield store.db
        # Force reading the database again between tests
        store.db.last_seen_verifier = ""


@pytest.fixture(scope="function")
def database_mutable_config(mock_store, mock_packages, mutable_config, monkeypatch):
    """This activates the mock store, packages, AND config."""
    with spack.store.use_store(str(mock_store)) as store:
        yield store.db
        store.db.last_seen_verifier = ""


@pytest.fixture(scope="function")
def mutable_database(database_mutable_config, _store_dir_and_cache):
    """Writeable version of the fixture, restored to its initial state
    after each test.
    """
    # Make the database writeable, as we are going to modify it
    store_path, store_cache = _store_dir_and_cache
    store_path.join(".spack-db").chmod(mode=0o755, rec=1)

    yield database_mutable_config

    # Restore the initial state by copying the content of the cache back into
    # the store and making the database read-only
    store_path.remove(rec=1)
    copy_tree(str(store_cache), str(store_path))
    store_path.join(".spack-db").chmod(mode=0o555, rec=1)


@pytest.fixture()
def dirs_with_libfiles(tmpdir_factory):
    lib_to_libfiles = {
        "libstdc++": ["libstdc++.so", "libstdc++.tbd"],
        "libgfortran": ["libgfortran.a", "libgfortran.dylib"],
        "libirc": ["libirc.a", "libirc.so"],
    }

    root = tmpdir_factory.mktemp("root")
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


def _return_none(*args):
    return None


@pytest.fixture(scope="function", autouse=True)
def disable_compiler_execution(monkeypatch, request):
    """Disable compiler execution to determine implicit link paths and libc flavor and version.
    To re-enable use `@pytest.mark.enable_compiler_execution`"""
    if "enable_compiler_execution" not in request.keywords:
        monkeypatch.setattr(spack.compiler.Compiler, "_compile_dummy_c_source", _return_none)


@pytest.fixture(scope="function")
def install_mockery(temporary_store: spack.store.Store, mutable_config, mock_packages):
    """Hooks a fake install directory, DB, and stage directory into Spack."""
    # We use a fake package, so temporarily disable checksumming
    with spack.config.override("config:checksum", False):
        yield

    # Wipe out any cached prefix failure locks (associated with the session-scoped mock archive)
    temporary_store.failure_tracker.clear_all()


@pytest.fixture(scope="module")
def temporary_mirror_dir(tmpdir_factory):
    dir = tmpdir_factory.mktemp("mirror")
    dir.ensure("build_cache", dir=True)
    yield str(dir)
    dir.join("build_cache").remove()


@pytest.fixture(scope="function")
def temporary_mirror(temporary_mirror_dir):
    mirror_url = url_util.path_to_file_url(temporary_mirror_dir)
    mirror_cmd("add", "--scope", "site", "test-mirror-func", mirror_url)
    yield temporary_mirror_dir
    mirror_cmd("rm", "--scope=site", "test-mirror-func")


@pytest.fixture(scope="function")
def mutable_temporary_mirror_dir(tmpdir_factory):
    dir = tmpdir_factory.mktemp("mirror")
    dir.ensure("build_cache", dir=True)
    yield str(dir)
    dir.join("build_cache").remove()


@pytest.fixture(scope="function")
def mutable_temporary_mirror(mutable_temporary_mirror_dir):
    mirror_url = url_util.path_to_file_url(mutable_temporary_mirror_dir)
    mirror_cmd("add", "--scope", "site", "test-mirror-func", mirror_url)
    yield mutable_temporary_mirror_dir
    mirror_cmd("rm", "--scope=site", "test-mirror-func")


@pytest.fixture(scope="function")
def temporary_store(tmpdir, request):
    """Hooks a temporary empty store for the test function."""
    ensure_configuration_fixture_run_before(request)
    temporary_store_path = tmpdir.join("opt")
    with spack.store.use_store(str(temporary_store_path)) as s:
        yield s
    temporary_store_path.remove()


@pytest.fixture()
def mock_fetch(mock_archive, monkeypatch):
    """Fake the URL for a package so it downloads from a file."""
    monkeypatch.setattr(
        spack.package_base.PackageBase, "fetcher", URLFetchStrategy(url=mock_archive.url)
    )


class MockLayout:
    def __init__(self, root):
        self.root = root

    def path_for_spec(self, spec):
        return os.path.sep.join([self.root, spec.name + "-" + spec.dag_hash()])

    def ensure_installed(self, spec):
        pass


@pytest.fixture()
def gen_mock_layout(tmpdir):
    # Generate a MockLayout in a temporary directory. In general the prefixes
    # specified by MockLayout should never be written to, but this ensures
    # that even if they are, that it causes no harm
    def create_layout(root):
        subroot = tmpdir.mkdir(root)
        return MockLayout(str(subroot))

    yield create_layout


class MockConfig:
    def __init__(self, configuration, writer_key):
        self._configuration = configuration
        self.writer_key = writer_key

    def configuration(self, module_set_name):
        return self._configuration

    def writer_configuration(self, module_set_name):
        return self.configuration(module_set_name)[self.writer_key]


class ConfigUpdate:
    def __init__(self, root_for_conf, writer_mod, writer_key, monkeypatch):
        self.root_for_conf = root_for_conf
        self.writer_mod = writer_mod
        self.writer_key = writer_key
        self.monkeypatch = monkeypatch

    def __call__(self, filename):
        file = os.path.join(self.root_for_conf, filename + ".yaml")
        with open(file) as f:
            config_settings = syaml.load_config(f)
        spack.config.set("modules:default", config_settings)
        mock_config = MockConfig(config_settings, self.writer_key)

        self.monkeypatch.setattr(spack.modules.common, "configuration", mock_config.configuration)
        self.monkeypatch.setattr(
            self.writer_mod, "configuration", mock_config.writer_configuration
        )
        self.monkeypatch.setattr(self.writer_mod, "configuration_registry", {})


@pytest.fixture()
def module_configuration(monkeypatch, request, mutable_config):
    """Reads the module configuration file from the mock ones prepared
    for tests and monkeypatches the right classes to hook it in.
    """
    # Class of the module file writer
    writer_cls = getattr(request.module, "writer_cls")
    # Module where the module file writer is defined
    writer_mod = inspect.getmodule(writer_cls)
    # Key for specific settings relative to this module type
    writer_key = str(writer_mod.__name__).split(".")[-1]
    # Root folder for configuration
    root_for_conf = os.path.join(spack.paths.test_path, "data", "modules", writer_key)

    # ConfigUpdate, when called, will modify configuration, so we need to use
    # the mutable_config fixture
    return ConfigUpdate(root_for_conf, writer_mod, writer_key, monkeypatch)


@pytest.fixture()
def mock_gnupghome(monkeypatch):
    # GNU PGP can't handle paths longer than 108 characters (wtf!@#$) so we
    # have to make our own tmpdir with a shorter name than pytest's.
    # This comes up because tmp paths on macOS are already long-ish, and
    # pytest makes them longer.
    try:
        spack.util.gpg.init()
    except spack.util.gpg.SpackGPGError:
        if not spack.util.gpg.GPG:
            pytest.skip("This test requires gpg")

    short_name_tmpdir = tempfile.mkdtemp()
    with spack.util.gpg.gnupghome_override(short_name_tmpdir):
        yield short_name_tmpdir

    # clean up, since we are doing this manually
    # Ignore errors cause we seem to be hitting a bug similar to
    # https://bugs.python.org/issue29699 in CI (FileNotFoundError: [Errno 2] No such
    # file or directory: 'S.gpg-agent.extra').
    shutil.rmtree(short_name_tmpdir, ignore_errors=True)


##########
# Fake archives and repositories
##########


@pytest.fixture(scope="session", params=[(".tar.gz", "z")])
def mock_archive(request, tmpdir_factory):
    """Creates a very simple archive directory with a configure script and a
    makefile that installs to a prefix. Tars it up into an archive.
    """
    tar = spack.util.executable.which("tar")
    if not tar:
        pytest.skip("requires tar to be installed")

    tmpdir = tmpdir_factory.mktemp("mock-archive-dir")
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)

    # Create the configure script
    configure_path = str(tmpdir.join(spack.stage._source_path_subdir, "configure"))
    with open(configure_path, "w") as f:
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
        archive_name = "{0}{1}".format(spack.stage._source_path_subdir, request.param[0])
        tar("-c{0}f".format(request.param[1]), archive_name, spack.stage._source_path_subdir)

    Archive = collections.namedtuple(
        "Archive", ["url", "path", "archive_file", "expanded_archive_basedir"]
    )
    archive_file = str(tmpdir.join(archive_name))
    url = url_util.path_to_file_url(archive_file)

    # Return the url
    yield Archive(
        url=url,
        archive_file=archive_file,
        path=str(repodir),
        expanded_archive_basedir=spack.stage._source_path_subdir,
    )


def _parse_cvs_date(line):
    """Turn a CVS log date into a datetime.datetime"""
    # dates in CVS logs can have slashes or dashes and may omit the time zone:
    # date: 2021-07-07 02:43:33 -0700;  ...
    # date: 2021-07-07 02:43:33;  ...
    # date: 2021/07/07 02:43:33;  ...
    m = re.search(r"date:\s+(\d+)[/-](\d+)[/-](\d+)\s+(\d+):(\d+):(\d+)", line)
    if not m:
        return None
    year, month, day, hour, minute, second = [int(g) for g in m.groups()]
    return datetime.datetime(year, month, day, hour, minute, second)


@pytest.fixture(scope="session")
def mock_cvs_repository(tmpdir_factory):
    """Creates a very simple CVS repository with two commits and a branch."""
    cvs = spack.util.executable.which("cvs", required=True)

    tmpdir = tmpdir_factory.mktemp("mock-cvs-repo-dir")
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)
    cvsroot = str(repodir)

    # The CVS repository and source tree need to live in a different directories
    sourcedirparent = tmpdir_factory.mktemp("mock-cvs-source-dir")
    module = spack.stage._source_path_subdir
    url = cvsroot + "%module=" + module
    sourcedirparent.ensure(module, dir=True)
    sourcedir = sourcedirparent.join(module)

    def format_date(date):
        if date is None:
            return None
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def get_cvs_timestamp(output):
        """Find the most recent CVS time stamp in a `cvs log` output"""
        latest_timestamp = None
        for line in output.splitlines():
            timestamp = _parse_cvs_date(line)
            if timestamp:
                if latest_timestamp is None:
                    latest_timestamp = timestamp
                else:
                    latest_timestamp = max(latest_timestamp, timestamp)
        return latest_timestamp

    # We use this to record the time stamps for when we create CVS revisions,
    # so that we can later check that we retrieve the proper commits when
    # specifying a date. (CVS guarantees checking out the lastest revision
    # before or on the specified date). As we create each revision, we
    # separately record the time by querying CVS.
    revision_date = {}

    # Initialize the repository
    with sourcedir.as_cwd():
        cvs("-d", cvsroot, "init")
        cvs(
            "-d",
            cvsroot,
            "import",
            "-m",
            "initial mock repo commit",
            module,
            "mockvendor",
            "mockrelease",
        )
        with sourcedirparent.as_cwd():
            cvs("-d", cvsroot, "checkout", module)

        # Commit file r0
        r0_file = "r0_file"
        sourcedir.ensure(r0_file)
        cvs("-d", cvsroot, "add", r0_file)
        cvs("-d", cvsroot, "commit", "-m", "revision 0", r0_file)
        output = cvs("log", "-N", r0_file, output=str)
        revision_date["1.1"] = format_date(get_cvs_timestamp(output))

        # Commit file r1
        r1_file = "r1_file"
        sourcedir.ensure(r1_file)
        cvs("-d", cvsroot, "add", r1_file)
        cvs("-d", cvsroot, "commit", "-m" "revision 1", r1_file)
        output = cvs("log", "-N", r0_file, output=str)
        revision_date["1.2"] = format_date(get_cvs_timestamp(output))

        # Create branch 'mock-branch'
        cvs("-d", cvsroot, "tag", "mock-branch-root")
        cvs("-d", cvsroot, "tag", "-b", "mock-branch")

    # CVS does not have the notion of a unique branch; branches and revisions
    # are managed separately for every file
    def get_branch():
        """Return the branch name if all files are on the same branch, else
        return None. Also return None if all files are on the trunk."""
        lines = cvs("-d", cvsroot, "status", "-v", output=str).splitlines()
        branch = None
        for line in lines:
            m = re.search(r"(\S+)\s+[(]branch:", line)
            if m:
                tag = m.group(1)
                if branch is None:
                    # First branch name found
                    branch = tag
                elif tag == branch:
                    # Later branch name found; all branch names found so far
                    # agree
                    pass
                else:
                    # Later branch name found; branch names differ
                    branch = None
                    break
        return branch

    # CVS does not have the notion of a unique revision; usually, one uses
    # commit dates instead
    def get_date():
        """Return latest date of the revisions of all files"""
        output = cvs("log", "-N", r0_file, output=str)
        timestamp = get_cvs_timestamp(output)
        if timestamp is None:
            return None
        return format_date(timestamp)

    checks = {
        "default": Bunch(file=r1_file, branch=None, date=None, args={"cvs": url}),
        "branch": Bunch(
            file=r1_file,
            branch="mock-branch",
            date=None,
            args={"cvs": url, "branch": "mock-branch"},
        ),
        "date": Bunch(
            file=r0_file,
            branch=None,
            date=revision_date["1.1"],
            args={"cvs": url, "date": revision_date["1.1"]},
        ),
    }

    test = Bunch(
        checks=checks, url=url, get_branch=get_branch, get_date=get_date, path=str(repodir)
    )

    yield test


@pytest.fixture(scope="session")
def mock_git_repository(git, tmpdir_factory):
    """Creates a git repository multiple commits, branches, submodules, and
    a tag. Visual representation of the commit history (starting with the
    earliest commit at c0)::

       c3       c1 (test-branch, r1)  c2 (tag-branch)
        |______/_____________________/
       c0 (r0)

    We used to test with 'master', but git has since developed the ability to
    have differently named default branches, so now we query the user's config to
    determine what the default branch should be.

    There are two branches aside from 'default': 'test-branch' and 'tag-branch';
    each has one commit; the tag-branch has a tag referring to its commit
    (c2 in the diagram).

    Two submodules are added as part of the very first commit on 'default'; each
    of these refers to a repository with a single commit.

    c0, c1, and c2 include information to define explicit versions in the
    associated builtin.mock package 'git-test'. c3 is a commit in the
    repository but does not have an associated explicit package version.
    """
    suburls = []
    # Create two git repositories which will be used as submodules in the
    # main repository
    for submodule_count in range(2):
        tmpdir = tmpdir_factory.mktemp("mock-git-repo-submodule-dir-{0}".format(submodule_count))
        tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
        repodir = tmpdir.join(spack.stage._source_path_subdir)
        suburls.append((submodule_count, url_util.path_to_file_url(str(repodir))))

        with repodir.as_cwd():
            git("init")
            git("config", "user.name", "Spack")
            git("config", "user.email", "spack@spack.io")

            # r0 is just the first commit
            submodule_file = "r0_file_{0}".format(submodule_count)
            repodir.ensure(submodule_file)
            git("add", submodule_file)
            git(
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-m",
                "mock-git-repo r0 {0}".format(submodule_count),
            )

    tmpdir = tmpdir_factory.mktemp("mock-git-repo-dir")
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)

    # Create the main repository
    with repodir.as_cwd():
        git("init")
        git("config", "user.name", "Spack")
        git("config", "user.email", "spack@spack.io")
        url = url_util.path_to_file_url(str(repodir))
        for number, suburl in suburls:
            git("submodule", "add", suburl, "third_party/submodule{0}".format(number))

        # r0 is the first commit: it consists of one file and two submodules
        r0_file = "r0_file"
        repodir.ensure(r0_file)
        git("add", r0_file)
        git("-c", "commit.gpgsign=false", "commit", "-m", "mock-git-repo r0")

        branch = "test-branch"
        branch_file = "branch_file"
        git("branch", branch)

        tag_branch = "tag-branch"
        tag_file = "tag_file"
        git("branch", tag_branch)

        # Check out test branch and add one commit
        git("checkout", branch)
        repodir.ensure(branch_file)
        git("add", branch_file)
        git("-c", "commit.gpgsign=false", "commit", "-m" "r1 test branch")

        # Check out the tag branch, add one commit, and then add a tag for it
        git("checkout", tag_branch)
        repodir.ensure(tag_file)
        git("add", tag_file)
        git("-c", "commit.gpgsign=false", "commit", "-m" "tag test branch")

        tag = "test-tag"
        git("tag", tag)

        try:
            default_branch = git("config", "--get", "init.defaultBranch", output=str).strip()
        except Exception:
            default_branch = "master"
        git("checkout", default_branch)

        r2_file = "r2_file"
        repodir.ensure(r2_file)
        git("add", r2_file)
        git("-c", "commit.gpgsign=false", "commit", "-m", "mock-git-repo r2")

        rev_hash = lambda x: git("rev-parse", x, output=str).strip()
        r2 = rev_hash(default_branch)

        # Record the commit hash of the (only) commit from test-branch and
        # the file added by that commit
        r1 = rev_hash(branch)
        r1_file = branch_file

        multiple_directories_branch = "many_dirs"
        num_dirs = 3
        num_files = 2
        dir_files = []
        for i in range(num_dirs):
            for j in range(num_files):
                dir_files.append(f"dir{i}/file{j}")

        git("checkout", "-b", multiple_directories_branch)
        for f in dir_files:
            repodir.ensure(f, file=True)
            git("add", f)

        git("-c", "commit.gpgsign=false", "commit", "-m", "many_dirs add files")

        # restore default
        git("checkout", default_branch)

    # Map of version -> bunch. Each bunch includes; all the args
    # that must be specified as part of a version() declaration (used to
    # manufacture a version for the 'git-test' package); the associated
    # revision for the version; a file associated with (and particular to)
    # that revision/branch.
    checks = {
        "default": Bunch(revision=default_branch, file=r0_file, args={"git": url}),
        "branch": Bunch(revision=branch, file=branch_file, args={"git": url, "branch": branch}),
        "tag-branch": Bunch(
            revision=tag_branch, file=tag_file, args={"git": url, "branch": tag_branch}
        ),
        "tag": Bunch(revision=tag, file=tag_file, args={"git": url, "tag": tag}),
        "commit": Bunch(revision=r1, file=r1_file, args={"git": url, "commit": r1}),
        # In this case, the version() args do not include a 'git' key:
        # this is the norm for packages, so this tests how the fetching logic
        # would most-commonly assemble a Git fetcher
        "default-no-per-version-git": Bunch(
            revision=default_branch, file=r0_file, args={"branch": default_branch}
        ),
        "many-directories": Bunch(
            revision=multiple_directories_branch,
            file=dir_files[0],
            args={"git": url, "branch": multiple_directories_branch},
        ),
    }

    t = Bunch(
        checks=checks,
        url=url,
        hash=rev_hash,
        path=str(repodir),
        git_exe=git,
        unversioned_commit=r2,
    )
    yield t


@pytest.fixture(scope="function")
def mock_git_test_package(mock_git_repository, mutable_mock_repo, monkeypatch):
    # install a fake git version in the package class
    pkg_class = spack.repo.PATH.get_pkg_class("git-test")
    monkeypatch.delattr(pkg_class, "git")
    monkeypatch.setitem(pkg_class.versions, spack.version.Version("git"), mock_git_repository.url)
    return pkg_class


@pytest.fixture(scope="session")
def mock_hg_repository(tmpdir_factory):
    """Creates a very simple hg repository with two commits."""
    hg = spack.util.executable.which("hg")
    if not hg:
        pytest.skip("requires mercurial to be installed")

    tmpdir = tmpdir_factory.mktemp("mock-hg-repo-dir")
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)

    get_rev = lambda: hg("id", "-i", output=str).strip()

    # Initialize the repository
    with repodir.as_cwd():
        url = url_util.path_to_file_url(str(repodir))
        hg("init")

        # Commit file r0
        r0_file = "r0_file"
        repodir.ensure(r0_file)
        hg("add", r0_file)
        hg("commit", "-m", "revision 0", "-u", "test")
        r0 = get_rev()

        # Commit file r1
        r1_file = "r1_file"
        repodir.ensure(r1_file)
        hg("add", r1_file)
        hg("commit", "-m" "revision 1", "-u", "test")
        r1 = get_rev()

    checks = {
        "default": Bunch(revision=r1, file=r1_file, args={"hg": str(repodir)}),
        "rev0": Bunch(revision=r0, file=r0_file, args={"hg": str(repodir), "revision": r0}),
    }
    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t


@pytest.fixture(scope="session")
def mock_svn_repository(tmpdir_factory):
    """Creates a very simple svn repository with two commits."""
    svn = spack.util.executable.which("svn")
    if not svn:
        pytest.skip("requires svn to be installed")

    svnadmin = spack.util.executable.which("svnadmin", required=True)

    tmpdir = tmpdir_factory.mktemp("mock-svn-stage")
    tmpdir.ensure(spack.stage._source_path_subdir, dir=True)
    repodir = tmpdir.join(spack.stage._source_path_subdir)
    url = url_util.path_to_file_url(str(repodir))

    # Initialize the repository
    with repodir.as_cwd():
        # NOTE: Adding --pre-1.5-compatible works for NERSC
        # Unknown if this is also an issue at other sites.
        svnadmin("create", "--pre-1.5-compatible", str(repodir))

        # Import a structure (first commit)
        r0_file = "r0_file"
        tmpdir.ensure("tmp-path", r0_file)
        tmp_path = tmpdir.join("tmp-path")
        svn("import", str(tmp_path), url, "-m", "Initial import r0")
        tmp_path.remove()

        # Second commit
        r1_file = "r1_file"
        svn("checkout", url, str(tmp_path))
        tmpdir.ensure("tmp-path", r1_file)

        with tmp_path.as_cwd():
            svn("add", str(tmpdir.ensure("tmp-path", r1_file)))
            svn("ci", "-m", "second revision r1")

        tmp_path.remove()
        r0 = "1"
        r1 = "2"

    checks = {
        "default": Bunch(revision=r1, file=r1_file, args={"svn": url}),
        "rev0": Bunch(revision=r0, file=r0_file, args={"svn": url, "revision": r0}),
    }

    def get_rev():
        output = svn("info", "--xml", output=str)
        info = xml.etree.ElementTree.fromstring(output)
        return info.find("entry/commit").get("revision")

    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t


@pytest.fixture(scope="function")
def mutable_mock_env_path(tmp_path, mutable_config, monkeypatch):
    """Fixture for mocking the internal spack environments directory."""
    mock_path = tmp_path / "mock-env-path"
    mutable_config.set("config:environments_root", str(mock_path))
    monkeypatch.setattr(ev.environment, "default_env_path", str(mock_path))
    return mock_path


@pytest.fixture()
def installation_dir_with_headers(tmpdir_factory):
    """Mock installation tree with a few headers placed in different
    subdirectories. Shouldn't be modified by tests as it is session
    scoped.
    """
    root = tmpdir_factory.mktemp("prefix")

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
    root.ensure("include", "boost", "ex3.h")
    root.ensure("include", "ex3.h")
    root.ensure("path", "to", "ex1.h")
    root.ensure("path", "to", "subdir", "ex2.h")

    return root


##########
# Specs of various kind
##########


@pytest.fixture(params=["conflict%clang+foo", "conflict-parent@0.9^conflict~foo"])
def conflict_spec(request):
    """Specs which violate constraints specified with the "conflicts"
    directive in the "conflict" package.
    """
    return request.param


@pytest.fixture(params=["conflict%~"])
def invalid_spec(request):
    """Specs that do not parse cleanly due to invalid formatting."""
    return request.param


@pytest.fixture(scope="module")
def mock_test_repo(tmpdir_factory):
    """Create an empty repository."""
    repo_namespace = "mock_test_repo"
    repodir = tmpdir_factory.mktemp(repo_namespace)
    repodir.ensure(spack.repo.packages_dir_name, dir=True)
    yaml = repodir.join("repo.yaml")
    yaml.write(
        """
repo:
    namespace: mock_test_repo
"""
    )

    with spack.repo.use_repositories(str(repodir)) as repo:
        yield repo, repodir

    shutil.rmtree(str(repodir))


@pytest.fixture(scope="function")
def mock_clone_repo(tmpdir_factory):
    """Create a cloned repository."""
    repo_namespace = "mock_clone_repo"
    repodir = tmpdir_factory.mktemp(repo_namespace)
    yaml = repodir.join("repo.yaml")
    yaml.write(
        """
repo:
    namespace: mock_clone_repo
"""
    )

    shutil.copytree(
        os.path.join(spack.paths.mock_packages_path, spack.repo.packages_dir_name),
        os.path.join(str(repodir), spack.repo.packages_dir_name),
    )

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


class MockBundle:
    has_code = False
    name = "mock-bundle"


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
def mock_executable(tmp_path):
    """Factory to create a mock executable in a temporary directory that
    output a custom string when run.
    """
    shebang = "#!/bin/sh\n" if sys.platform != "win32" else "@ECHO OFF\n"

    def _factory(name, output, subdir=("bin",)):
        executable_dir = tmp_path.joinpath(*subdir)
        executable_dir.mkdir(parents=True, exist_ok=True)
        executable_path = executable_dir / name
        if sys.platform == "win32":
            executable_path = executable_dir / (name + ".bat")
        executable_path.write_text(f"{shebang}{output}\n")
        executable_path.chmod(0o755)
        return executable_path

    return _factory


@pytest.fixture()
def mock_test_stage(mutable_config, tmpdir):
    # NOTE: This fixture MUST be applied after any fixture that uses
    # the config fixture under the hood
    # No need to unset because we use mutable_config
    tmp_stage = str(tmpdir.join("test_stage"))
    mutable_config.set("config:test_stage", tmp_stage)

    yield tmp_stage


@pytest.fixture(autouse=True)
def inode_cache():
    llnl.util.lock.FILE_TRACKER.purge()
    yield
    # TODO: it is a bug when the file tracker is non-empty after a test,
    # since it means a lock was not released, or the inode was not purged
    # when acquiring the lock failed. So, we could assert that here, but
    # currently there are too many issues to fix, so look for the more
    # serious issue of having a closed file descriptor in the cache.
    assert not any(f.fh.closed for f in llnl.util.lock.FILE_TRACKER._descriptors.values())
    llnl.util.lock.FILE_TRACKER.purge()


@pytest.fixture(autouse=True)
def brand_new_binary_cache():
    yield
    spack.binary_distribution.BINARY_INDEX = llnl.util.lang.Singleton(
        spack.binary_distribution.BinaryCacheIndex
    )


@pytest.fixture()
def noncyclical_dir_structure(tmpdir):
    """
    Create some non-trivial directory structure with
    symlinks to dirs and dangling symlinks, but no cycles::

        .
        |-- a/
        |   |-- d/
        |   |-- file_1
        |   |-- to_file_1 -> file_1
        |   `-- to_c -> ../c
        |-- b -> a
        |-- c/
        |   |-- dangling_link -> nowhere
        |   `-- file_2
        `-- file_3
    """
    d, j = tmpdir.mkdir("nontrivial-dir"), os.path.join

    with d.as_cwd():
        os.mkdir(j("a"))
        os.mkdir(j("a", "d"))
        with open(j("a", "file_1"), "wb"):
            pass
        os.symlink(j("file_1"), j("a", "to_file_1"))
        os.symlink(j("..", "c"), j("a", "to_c"))
        os.symlink(j("a"), j("b"))
        os.mkdir(j("c"))
        os.symlink(j("nowhere"), j("c", "dangling_link"))
        with open(j("c", "file_2"), "wb"):
            pass
        with open(j("file_3"), "wb"):
            pass
    yield d


@pytest.fixture(scope="function")
def mock_config_data():
    config_data_dir = os.path.join(spack.paths.test_path, "data", "config")
    return config_data_dir, os.listdir(config_data_dir)


@pytest.fixture(scope="function")
def mock_curl_configs(mock_config_data, monkeypatch):
    """
    Mock curl-based retrieval of configuration files from the web by grabbing
    them from the test data configuration directory.

    Fetches a single (configuration) file if the name matches one in the test
    data directory.
    """
    config_data_dir, config_files = mock_config_data

    class MockCurl:
        def __init__(self):
            self.returncode = None

        def __call__(self, *args, **kwargs):
            url = [a for a in args if a.startswith("http")][0]
            basename = os.path.basename(url)
            if os.path.splitext(url)[1]:
                if basename in config_files:
                    filename = os.path.join(config_data_dir, basename)

                    with open(filename, "r") as f:
                        lines = f.readlines()
                        write_file(os.path.basename(filename), "".join(lines))

                    self.returncode = 0
                else:
                    # This is a "404" and is technically only returned if -f
                    # flag is provided to curl.
                    tty.msg("curl: (22) The requested URL returned error: 404")
                    self.returncode = 22

    monkeypatch.setattr(spack.util.web, "require_curl", MockCurl)


@pytest.fixture(scope="function")
def mock_spider_configs(mock_config_data, monkeypatch):
    """
    Mock retrieval of configuration file URLs from the web by grabbing
    them from the test data configuration directory.
    """
    config_data_dir, config_files = mock_config_data

    def _spider(*args, **kwargs):
        root_urls = args[0]
        if not root_urls:
            return [], set()

        root_urls = [root_urls] if isinstance(root_urls, str) else root_urls

        # Any URL with an extension will be treated like a file; otherwise,
        # it is considered a directory/folder and we'll grab all available
        # files.
        urls = []
        for url in root_urls:
            if os.path.splitext(url)[1]:
                urls.append(url)
            else:
                urls.extend([os.path.join(url, f) for f in config_files])

        return [], set(urls)

    monkeypatch.setattr(spack.util.web, "spider", _spider)

    yield


@pytest.fixture(scope="function")
def mock_tty_stdout(monkeypatch):
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)


@pytest.fixture
def prefix_like():
    return "package-0.0.0.a1-hashhashhashhashhashhashhashhash"


@pytest.fixture()
def prefix_tmpdir(tmpdir, prefix_like):
    return tmpdir.mkdir(prefix_like)


@pytest.fixture()
def binary_with_rpaths(prefix_tmpdir):
    """Factory fixture that compiles an ELF binary setting its RPATH. Relative
    paths are encoded with `$ORIGIN` prepended.
    """

    def _factory(rpaths, message="Hello world!", dynamic_linker="/lib64/ld-linux.so.2"):
        source = prefix_tmpdir.join("main.c")
        source.write(
            """
        #include <stdio.h>
        int main(){{
            printf("{0}");
        }}
        """.format(
                message
            )
        )
        gcc = spack.util.executable.which("gcc")
        executable = source.dirpath("main.x")
        # Encode relative RPATHs using `$ORIGIN` as the root prefix
        rpaths = [x if os.path.isabs(x) else os.path.join("$ORIGIN", x) for x in rpaths]
        opts = [
            "-Wl,--disable-new-dtags",
            f"-Wl,-rpath={':'.join(rpaths)}",
            f"-Wl,--dynamic-linker,{dynamic_linker}",
            str(source),
            "-o",
            str(executable),
        ]
        gcc(*opts)
        return executable

    return _factory


@pytest.fixture(scope="session")
def concretized_specs_cache():
    """Cache for mock concrete specs"""
    return {}


@pytest.fixture
def default_mock_concretization(config, mock_packages, concretized_specs_cache):
    """Return the default mock concretization of a spec literal, obtained using the mock
    repository and the mock configuration.

    This fixture is unsafe to call in a test when either the default configuration or mock
    repository are not used or have been modified.
    """

    def _func(spec_str, tests=False):
        key = spec_str, tests
        if key not in concretized_specs_cache:
            concretized_specs_cache[key] = spack.spec.Spec(spec_str).concretized(tests=tests)
        return concretized_specs_cache[key].copy()

    return _func


@pytest.fixture
def shell_as(shell):
    if sys.platform != "win32":
        yield
        return
    if shell not in ("pwsh", "bat"):
        raise RuntimeError("Shell must be one of supported Windows shells (pwsh|bat)")
    try:
        # fetch and store old shell type
        _shell = os.environ.get("SPACK_SHELL", None)
        os.environ["SPACK_SHELL"] = shell
        yield
    finally:
        # restore old shell if one was set
        if _shell:
            os.environ["SPACK_SHELL"] = _shell


@pytest.fixture()
def nullify_globals(request, monkeypatch):
    ensure_configuration_fixture_run_before(request)
    monkeypatch.setattr(spack.config, "CONFIG", None)
    monkeypatch.setattr(spack.caches, "MISC_CACHE", None)
    monkeypatch.setattr(spack.caches, "FETCH_CACHE", None)
    monkeypatch.setattr(spack.repo, "PATH", None)
    monkeypatch.setattr(spack.store, "STORE", None)


def pytest_runtest_setup(item):
    # Skip test marked "not_on_windows" if they're run on Windows
    not_on_windows_marker = item.get_closest_marker(name="not_on_windows")
    if not_on_windows_marker and sys.platform == "win32":
        pytest.skip(*not_on_windows_marker.args)

    # Skip items marked "only windows" if they're run anywhere but Windows
    only_windows_marker = item.get_closest_marker(name="only_windows")
    if only_windows_marker and sys.platform != "win32":
        pytest.skip(*only_windows_marker.args)


def _sequential_executor(*args, **kwargs):
    return spack.util.parallel.SequentialExecutor()


@pytest.fixture(autouse=True)
def disable_parallel_buildcache_push(monkeypatch):
    """Disable process pools in tests."""
    monkeypatch.setattr(spack.util.parallel, "make_concurrent_executor", _sequential_executor)


def _root_path(x, y, *, path):
    return path


@pytest.fixture
def mock_modules_root(tmp_path, monkeypatch):
    """Sets the modules root to a temporary directory, to avoid polluting configuration scopes."""
    fn = functools.partial(_root_path, path=str(tmp_path))
    monkeypatch.setattr(spack.modules.common, "root_path", fn)


_repo_name_id = 0


def create_test_repo(tmpdir, pkg_name_content_tuples):
    global _repo_name_id

    repo_path = str(tmpdir)
    repo_yaml = tmpdir.join("repo.yaml")
    with open(str(repo_yaml), "w") as f:
        f.write(
            f"""\
repo:
  namespace: testrepo{str(_repo_name_id)}
"""
        )

    _repo_name_id += 1

    packages_dir = tmpdir.join("packages")
    for pkg_name, pkg_str in pkg_name_content_tuples:
        pkg_dir = packages_dir.ensure(pkg_name, dir=True)
        pkg_file = pkg_dir.join("package.py")
        with open(str(pkg_file), "w") as f:
            f.write(pkg_str)

    repo_cache = spack.util.file_cache.FileCache(str(tmpdir.join("cache")))
    return spack.repo.Repo(repo_path, cache=repo_cache)


@pytest.fixture()
def compiler_factory():
    """Factory for a compiler dict, taking a spec and an OS as arguments."""

    def _factory(*, spec, operating_system):
        return {
            "compiler": {
                "spec": spec,
                "operating_system": operating_system,
                "paths": {"cc": "/path/to/cc", "cxx": "/path/to/cxx", "f77": None, "fc": None},
                "modules": [],
                "target": str(archspec.cpu.host().family),
            }
        }

    return _factory


@pytest.fixture()
def host_architecture_str():
    """Returns the broad architecture family (x86_64, aarch64, etc.)"""
    return str(archspec.cpu.host().family)


def _true(x):
    return True


@pytest.fixture()
def do_not_check_runtimes_on_reuse(monkeypatch):
    monkeypatch.setattr(spack.solver.asp, "_has_runtime_dependencies", _true)


@pytest.fixture(autouse=True, scope="session")
def _c_compiler_always_exists():
    fn = spack.solver.asp.c_compiler_runs
    spack.solver.asp.c_compiler_runs = _true
    yield
    spack.solver.asp.c_compiler_runs = fn


@pytest.fixture(scope="session")
def mock_test_cache(tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp("cache")
    print(cache_dir)
    return spack.util.file_cache.FileCache(str(cache_dir))
