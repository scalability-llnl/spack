# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.util.environment as environment
from spack.paths import spack_root
from spack.util.environment import (
    AppendPath,
    EnvironmentModifications,
    PrependPath,
    RemovePath,
    SetEnv,
    UnsetEnv,
    filter_system_paths,
    is_system_path,
)

datadir = os.path.join(spack_root, "lib", "spack", "spack", "test", "data")


def test_inspect_path(tmpdir):
    inspections = {
        "bin": ["PATH"],
        "man": ["MANPATH"],
        "share/man": ["MANPATH"],
        "share/aclocal": ["ACLOCAL_PATH"],
        "lib": ["LIBRARY_PATH", "LD_LIBRARY_PATH"],
        "lib64": ["LIBRARY_PATH", "LD_LIBRARY_PATH"],
        "include": ["CPATH"],
        "lib/pkgconfig": ["PKG_CONFIG_PATH"],
        "lib64/pkgconfig": ["PKG_CONFIG_PATH"],
        "share/pkgconfig": ["PKG_CONFIG_PATH"],
        "": ["CMAKE_PREFIX_PATH"],
    }

    tmpdir.mkdir("bin")
    tmpdir.mkdir("lib")
    tmpdir.mkdir("include")

    env = environment.inspect_path(str(tmpdir), inspections)
    names = [item.name for item in env]
    assert "PATH" in names
    assert "LIBRARY_PATH" in names
    assert "LD_LIBRARY_PATH" in names
    assert "CPATH" in names


def test_exclude_paths_from_inspection():
    inspections = {
        "lib": ["LIBRARY_PATH", "LD_LIBRARY_PATH"],
        "lib64": ["LIBRARY_PATH", "LD_LIBRARY_PATH"],
        "include": ["CPATH"],
    }

    env = environment.inspect_path("/usr", inspections, exclude=is_system_path)

    assert len(env) == 0


@pytest.fixture()
def prepare_environment_for_tests(working_env):
    """Sets a few dummy variables in the current environment, that will be
    useful for the tests below.
    """
    os.environ["UNSET_ME"] = "foo"
    os.environ["EMPTY_PATH_LIST"] = ""
    os.environ["PATH_LIST"] = "/path/second:/path/third"
    os.environ["REMOVE_PATH_LIST"] = "/a/b:/duplicate:/a/c:/remove/this:/a/d:/duplicate/:/f/g"
    os.environ["PATH_LIST_WITH_SYSTEM_PATHS"] = "/usr/include:" + os.environ["REMOVE_PATH_LIST"]
    os.environ["PATH_LIST_WITH_DUPLICATES"] = os.environ["REMOVE_PATH_LIST"]


@pytest.fixture
def env(prepare_environment_for_tests):
    """Returns an empty EnvironmentModifications object."""
    return EnvironmentModifications()


@pytest.fixture
def miscellaneous_paths():
    """Returns a list of paths, including system ones."""
    return [
        "/usr/local/Cellar/gcc/5.3.0/lib",
        "/usr/local/lib",
        "/usr/local",
        "/usr/local/include",
        "/usr/local/lib64",
        "/usr/local/opt/some-package/lib",
        "/usr/opt/lib",
        "/usr/local/../bin",
        "/lib",
        "/",
        "/usr",
        "/usr/",
        "/usr/bin",
        "/bin64",
        "/lib64",
        "/include",
        "/include/",
        "/opt/some-package/include",
        "/opt/some-package/local/..",
    ]


@pytest.fixture
def files_to_be_sourced():
    """Returns a list of files to be sourced"""
    return [
        os.path.join(datadir, "sourceme_first.sh"),
        os.path.join(datadir, "sourceme_second.sh"),
        os.path.join(datadir, "sourceme_parameters.sh"),
        os.path.join(datadir, "sourceme_unicode.sh"),
    ]


def test_set(env):
    """Tests setting values in the environment."""

    # Here we are storing the commands to set a couple of variables
    env.set("A", "dummy value")
    env.set("B", 3)

    # ...and then we are executing them
    env.apply_modifications()

    assert "dummy value" == os.environ["A"]
    assert str(3) == os.environ["B"]


def test_append_flags(env):
    """Tests appending to a value in the environment."""

    # Store a couple of commands
    env.append_flags("APPEND_TO_ME", "flag1")
    env.append_flags("APPEND_TO_ME", "flag2")

    # ... execute the commands
    env.apply_modifications()

    assert "flag1 flag2" == os.environ["APPEND_TO_ME"]


def test_unset(env):
    """Tests unsetting values in the environment."""

    # Assert that the target variable is there and unset it
    assert "foo" == os.environ["UNSET_ME"]
    env.unset("UNSET_ME")
    env.apply_modifications()

    # Trying to retrieve is after deletion should cause a KeyError
    with pytest.raises(KeyError):
        os.environ["UNSET_ME"]


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_filter_system_paths(miscellaneous_paths):
    """Tests that the filtering of system paths works as expected."""
    filtered = filter_system_paths(miscellaneous_paths)
    expected = [
        "/usr/local/Cellar/gcc/5.3.0/lib",
        "/usr/local/opt/some-package/lib",
        "/usr/opt/lib",
        "/opt/some-package/include",
        "/opt/some-package/local/..",
    ]
    assert filtered == expected


# TODO 27021
@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_set_path(env):
    """Tests setting paths in an environment variable."""

    # Check setting paths with the default separator
    env.set_path("A", ["foo", "bar", "baz"])
    env.apply_modifications()

    assert "foo:bar:baz" == os.environ["A"]

    env.set_path("B", ["foo", "bar", "baz"], separator=";")
    env.apply_modifications()

    assert "foo;bar;baz" == os.environ["B"]


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_path_manipulation(env):
    """Tests manipulating list of paths in the environment."""

    env.append_path("PATH_LIST", "/path/last")
    env.prepend_path("PATH_LIST", "/path/first")

    env.append_path("EMPTY_PATH_LIST", "/path/middle")
    env.append_path("EMPTY_PATH_LIST", "/path/last")
    env.prepend_path("EMPTY_PATH_LIST", "/path/first")

    env.append_path("NEWLY_CREATED_PATH_LIST", "/path/middle")
    env.append_path("NEWLY_CREATED_PATH_LIST", "/path/last")
    env.prepend_path("NEWLY_CREATED_PATH_LIST", "/path/first")

    env.remove_path("REMOVE_PATH_LIST", "/remove/this")
    env.remove_path("REMOVE_PATH_LIST", "/duplicate/")

    env.deprioritize_system_paths("PATH_LIST_WITH_SYSTEM_PATHS")
    env.prune_duplicate_paths("PATH_LIST_WITH_DUPLICATES")

    env.apply_modifications()

    expected = "/path/first:/path/second:/path/third:/path/last"
    assert os.environ["PATH_LIST"] == expected

    expected = "/path/first:/path/middle:/path/last"
    assert os.environ["EMPTY_PATH_LIST"] == expected

    expected = "/path/first:/path/middle:/path/last"
    assert os.environ["NEWLY_CREATED_PATH_LIST"] == expected

    assert os.environ["REMOVE_PATH_LIST"] == "/a/b:/a/c:/a/d:/f/g"

    assert not os.environ["PATH_LIST_WITH_SYSTEM_PATHS"].startswith("/usr/include:")
    assert os.environ["PATH_LIST_WITH_SYSTEM_PATHS"].endswith(":/usr/include")

    assert os.environ["PATH_LIST_WITH_DUPLICATES"].count("/duplicate") == 1


def test_extend(env):
    """Tests that we can construct a list of environment modifications
    starting from another list.
    """
    env.set("A", "dummy value")
    env.set("B", 3)
    copy_construct = EnvironmentModifications(env)

    assert len(copy_construct) == 2

    for x, y in zip(env, copy_construct):
        assert x is y


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
@pytest.mark.usefixtures("prepare_environment_for_tests")
def test_source_files(files_to_be_sourced):
    """Tests the construction of a list of environment modifications that are
    the result of sourcing a file.
    """
    env = EnvironmentModifications()
    for filename in files_to_be_sourced:
        if filename.endswith("sourceme_parameters.sh"):
            env.extend(EnvironmentModifications.from_sourcing_file(filename, "intel64"))
        else:
            env.extend(EnvironmentModifications.from_sourcing_file(filename))

    modifications = env.group_by_name()

    # This is sensitive to the user's environment; can include
    # spurious entries for things like PS1
    #
    # TODO: figure out how to make a bit more robust.
    assert len(modifications) >= 5

    # Set new variables
    assert len(modifications["NEW_VAR"]) == 1
    assert isinstance(modifications["NEW_VAR"][0], SetEnv)
    assert modifications["NEW_VAR"][0].value == "new"

    assert len(modifications["FOO"]) == 1
    assert isinstance(modifications["FOO"][0], SetEnv)
    assert modifications["FOO"][0].value == "intel64"

    # Unset variables
    assert len(modifications["EMPTY_PATH_LIST"]) == 1
    assert isinstance(modifications["EMPTY_PATH_LIST"][0], UnsetEnv)

    # Modified variables
    assert len(modifications["UNSET_ME"]) == 1
    assert isinstance(modifications["UNSET_ME"][0], SetEnv)
    assert modifications["UNSET_ME"][0].value == "overridden"

    assert len(modifications["PATH_LIST"]) == 3
    assert isinstance(modifications["PATH_LIST"][0], RemovePath)
    assert modifications["PATH_LIST"][0].value == "/path/third"
    assert isinstance(modifications["PATH_LIST"][1], AppendPath)
    assert modifications["PATH_LIST"][1].value == "/path/fourth"
    assert isinstance(modifications["PATH_LIST"][2], PrependPath)
    assert modifications["PATH_LIST"][2].value == "/path/first"


@pytest.mark.regression("8345")
def test_preserve_environment(prepare_environment_for_tests):
    # UNSET_ME is defined, and will be unset in the context manager,
    # NOT_SET is not in the environment and will be set within the
    # context manager, PATH_LIST is set and will be changed.
    with environment.preserve_environment("UNSET_ME", "NOT_SET", "PATH_LIST"):
        os.environ["NOT_SET"] = "a"
        assert os.environ["NOT_SET"] == "a"

        del os.environ["UNSET_ME"]
        assert "UNSET_ME" not in os.environ

        os.environ["PATH_LIST"] = "changed"

    assert "NOT_SET" not in os.environ
    assert os.environ["UNSET_ME"] == "foo"
    assert os.environ["PATH_LIST"] == "/path/second:/path/third"


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
@pytest.mark.parametrize(
    "files,expected,deleted",
    [
        # Sets two variables
        (
            (os.path.join(datadir, "sourceme_first.sh"),),
            {"NEW_VAR": "new", "UNSET_ME": "overridden"},
            [],
        ),
        # Check if we can set a variable to different values depending
        # on command line parameters
        ((os.path.join(datadir, "sourceme_parameters.sh"),), {"FOO": "default"}, []),
        (([os.path.join(datadir, "sourceme_parameters.sh"), "intel64"],), {"FOO": "intel64"}, []),
        # Check unsetting variables
        (
            (os.path.join(datadir, "sourceme_second.sh"),),
            {"PATH_LIST": "/path/first:/path/second:/path/fourth"},
            ["EMPTY_PATH_LIST"],
        ),
        # Check that order of sourcing matters
        (
            (
                os.path.join(datadir, "sourceme_unset.sh"),
                os.path.join(datadir, "sourceme_first.sh"),
            ),
            {"NEW_VAR": "new", "UNSET_ME": "overridden"},
            [],
        ),
        (
            (
                os.path.join(datadir, "sourceme_first.sh"),
                os.path.join(datadir, "sourceme_unset.sh"),
            ),
            {"NEW_VAR": "new"},
            ["UNSET_ME"],
        ),
    ],
)
@pytest.mark.usefixtures("prepare_environment_for_tests")
def test_environment_from_sourcing_files(files, expected, deleted):
    env = environment.environment_after_sourcing_files(*files)

    # Test that variables that have been modified are still there and contain
    # the expected output
    for name, value in expected.items():
        assert name in env
        assert value in env[name]

    # Test that variables that have been unset are not there
    for name in deleted:
        assert name not in env


def test_clear(env):
    env.set("A", "dummy value")
    assert len(env) > 0
    env.clear()
    assert len(env) == 0


@pytest.mark.parametrize(
    "env,exclude,include",
    [
        # Check we can exclude a literal
        ({"SHLVL": "1"}, ["SHLVL"], []),
        # Check include takes precedence
        ({"SHLVL": "1"}, ["SHLVL"], ["SHLVL"]),
    ],
)
def test_sanitize_literals(env, exclude, include):
    after = environment.sanitize(env, exclude, include)

    # Check that all the included variables are there
    assert all(x in after for x in include)

    # Check that the excluded variables that are not
    # included are there
    exclude = list(set(exclude) - set(include))
    assert all(x not in after for x in exclude)


@pytest.mark.parametrize(
    "env,exclude,include,expected,deleted",
    [
        # Check we can exclude using a regex
        ({"SHLVL": "1"}, ["SH.*"], [], [], ["SHLVL"]),
        # Check we can include using a regex
        ({"SHLVL": "1"}, ["SH.*"], ["SH.*"], ["SHLVL"], []),
        # Check regex to exclude Environment Modules related vars
        (
            {"MODULES_LMALTNAME": "1", "MODULES_LMCONFLICT": "2"},
            ["MODULES_(.*)"],
            [],
            [],
            ["MODULES_LMALTNAME", "MODULES_LMCONFLICT"],
        ),
        (
            {"A_modquar": "1", "b_modquar": "2", "C_modshare": "3"},
            [r"(\w*)_mod(quar|share)"],
            [],
            [],
            ["A_modquar", "b_modquar", "C_modshare"],
        ),
        (
            {"__MODULES_LMTAG": "1", "__MODULES_LMPREREQ": "2"},
            ["__MODULES_(.*)"],
            [],
            [],
            ["__MODULES_LMTAG", "__MODULES_LMPREREQ"],
        ),
    ],
)
def test_sanitize_regex(env, exclude, include, expected, deleted):
    after = environment.sanitize(env, exclude, include)

    assert all(x in after for x in expected)
    assert all(x not in after for x in deleted)


@pytest.mark.regression("12085")
@pytest.mark.parametrize(
    "before,after,search_list",
    [
        # Set environment variables
        ({}, {"FOO": "foo"}, [environment.SetEnv("FOO", "foo")]),
        # Unset environment variables
        ({"FOO": "foo"}, {}, [environment.UnsetEnv("FOO")]),
        # Append paths to an environment variable
        (
            {"FOO_PATH": "/a/path"},
            {"FOO_PATH": "/a/path:/b/path"},
            [environment.AppendPath("FOO_PATH", "/b/path")],
        ),
        (
            {},
            {"FOO_PATH": "/a/path" + os.sep + "/b/path"},
            [environment.AppendPath("FOO_PATH", "/a/path" + os.sep + "/b/path")],
        ),
        (
            {"FOO_PATH": "/a/path:/b/path"},
            {"FOO_PATH": "/b/path"},
            [environment.RemovePath("FOO_PATH", "/a/path")],
        ),
        (
            {"FOO_PATH": "/a/path:/b/path"},
            {"FOO_PATH": "/a/path:/c/path"},
            [
                environment.RemovePath("FOO_PATH", "/b/path"),
                environment.AppendPath("FOO_PATH", "/c/path"),
            ],
        ),
        (
            {"FOO_PATH": "/a/path:/b/path"},
            {"FOO_PATH": "/c/path:/a/path"},
            [
                environment.RemovePath("FOO_PATH", "/b/path"),
                environment.PrependPath("FOO_PATH", "/c/path"),
            ],
        ),
        # Modify two variables in the same environment
        (
            {"FOO": "foo", "BAR": "bar"},
            {"FOO": "baz", "BAR": "baz"},
            [environment.SetEnv("FOO", "baz"), environment.SetEnv("BAR", "baz")],
        ),
    ],
)
def test_from_environment_diff(before, after, search_list):
    mod = environment.EnvironmentModifications.from_environment_diff(before, after)

    for item in search_list:
        assert item in mod


@pytest.mark.not_on_windows("Lmod not supported on Windows")
@pytest.mark.regression("15775")
def test_exclude_lmod_variables():
    # Construct the list of environment modifications
    file = os.path.join(datadir, "sourceme_lmod.sh")
    env = EnvironmentModifications.from_sourcing_file(file)

    # Check that variables related to lmod are not in there
    modifications = env.group_by_name()
    assert not any(x.startswith("LMOD_") for x in modifications)


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
@pytest.mark.regression("13504")
def test_exclude_modules_variables():
    # Construct the list of environment modifications
    file = os.path.join(datadir, "sourceme_modules.sh")
    env = EnvironmentModifications.from_sourcing_file(file)

    # Check that variables related to modules are not in there
    modifications = env.group_by_name()
    assert not any(x.startswith("MODULES_") for x in modifications)
    assert not any(x.startswith("__MODULES_") for x in modifications)
    assert not any(x.startswith("BASH_FUNC_ml") for x in modifications)
    assert not any(x.startswith("BASH_FUNC_module") for x in modifications)
    assert not any(x.startswith("BASH_FUNC__module_raw") for x in modifications)
