# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test Spack's environment utility functions."""
import os
import sys

import pytest

import spack.util.environment as envutil


@pytest.fixture()
def prepare_environment_for_tests():
    if "TEST_ENV_VAR" in os.environ:
        del os.environ["TEST_ENV_VAR"]
    yield
    del os.environ["TEST_ENV_VAR"]


def test_is_system_path():
    sys_path = "C:\\Users" if sys.platform == "win32" else "/usr/bin"
    assert envutil.is_system_path(sys_path)
    assert not envutil.is_system_path("/nonsense_path/bin")
    assert not envutil.is_system_path("")
    assert not envutil.is_system_path(None)


if sys.platform == "win32":
    test_paths = [
        "C:\\Users",
        "C:\\",
        "C:\\ProgramData",
        "C:\\nonsense_path",
        "C:\\Program Files",
        "C:\\nonsense_path\\extra\\bin",
    ]
else:
    test_paths = [
        "/usr/bin",
        "/nonsense_path/lib",
        "/usr/local/lib",
        "/bin",
        "/nonsense_path/extra/bin",
        "/usr/lib64",
    ]


def test_filter_system_paths():
    nonsense_prefix = "C:\\nonsense_path" if sys.platform == "win32" else "/nonsense_path"
    expected = [p for p in test_paths if p.startswith(nonsense_prefix)]
    filtered = envutil.filter_system_paths(test_paths)
    assert expected == filtered


def deprioritize_system_paths():
    expected = [p for p in test_paths if p.startswith("/nonsense_path")]
    expected.extend([p for p in test_paths if not p.startswith("/nonsense_path")])
    filtered = envutil.deprioritize_system_paths(test_paths)
    assert expected == filtered


def test_prune_duplicate_paths():
    test_paths = ["/a/b", "/a/c", "/a/b", "/a/a", "/a/c", "/a/a/.."]
    expected = ["/a/b", "/a/c", "/a/a", "/a/a/.."]
    assert expected == envutil.prune_duplicate_paths(test_paths)


def test_get_path(prepare_environment_for_tests):
    os.environ["TEST_ENV_VAR"] = os.pathsep.join(["/a", "/b", "/c/d"])
    expected = ["/a", "/b", "/c/d"]
    assert envutil.get_path("TEST_ENV_VAR") == expected


def test_env_flag(prepare_environment_for_tests):
    assert not envutil.env_flag("TEST_NO_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "1"
    assert envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "TRUE"
    assert envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "True"
    assert envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "TRue"
    assert envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "true"
    assert envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "27"
    assert not envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "-2.3"
    assert not envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "0"
    assert not envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "False"
    assert not envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "false"
    assert not envutil.env_flag("TEST_ENV_VAR")
    os.environ["TEST_ENV_VAR"] = "garbage"
    assert not envutil.env_flag("TEST_ENV_VAR")


def test_path_set(prepare_environment_for_tests):
    envutil.path_set("TEST_ENV_VAR", ["/a", "/a/b", "/a/a"])
    assert os.environ["TEST_ENV_VAR"] == "/a" + os.pathsep + "/a/b" + os.pathsep + "/a/a"


def test_path_put_first(prepare_environment_for_tests):
    envutil.path_set("TEST_ENV_VAR", test_paths)
    expected = ["/usr/bin", "/new_nonsense_path/a/b"]
    expected.extend([p for p in test_paths if p != "/usr/bin"])
    envutil.path_put_first("TEST_ENV_VAR", expected)
    assert envutil.get_path("TEST_ENV_VAR") == expected


@pytest.mark.parametrize("shell", ["pwsh", "bat"] if sys.platform == "win32" else ["bash"])
def test_dump_environment(prepare_environment_for_tests, shell_as, shell, tmpdir):
    test_paths = "/a:/b/x:/b/c"
    os.environ["TEST_ENV_VAR"] = test_paths
    dumpfile_path = str(tmpdir.join("envdump.txt"))
    envutil.dump_environment(dumpfile_path)
    with open(dumpfile_path, "r") as dumpfile:
        if shell == "pwsh":
            assert "$Env:TEST_ENV_VAR={}\n".format(test_paths) in list(dumpfile)
        elif shell == "bat":
            assert 'set "TEST_ENV_VAR={}"\n'.format(test_paths) in list(dumpfile)
        else:
            assert "TEST_ENV_VAR={0}; export TEST_ENV_VAR\n".format(test_paths) in list(dumpfile)


def test_reverse_environment_modifications(working_env):
    start_env = {
        "PREPEND_PATH": os.sep + os.path.join("path", "to", "prepend", "to"),
        "APPEND_PATH": os.sep + os.path.join("path", "to", "append", "to"),
        "UNSET": "var_to_unset",
        "APPEND_FLAGS": "flags to append to",
    }

    to_reverse = envutil.EnvironmentModifications()

    to_reverse.prepend_path("PREPEND_PATH", "/new/path/prepended")
    to_reverse.append_path("APPEND_PATH", "/new/path/appended")
    to_reverse.set_path("SET_PATH", ["/one/set/path", "/two/set/path"])
    to_reverse.set("SET", "a var")
    to_reverse.unset("UNSET")
    to_reverse.append_flags("APPEND_FLAGS", "more_flags")

    reversal = to_reverse.reversed()

    os.environ.clear()
    os.environ.update(start_env)

    print(os.environ)
    to_reverse.apply_modifications()
    print(os.environ)
    reversal.apply_modifications()
    print(os.environ)

    start_env.pop("UNSET")
    assert os.environ == start_env


def test_shell_modifications_are_properly_escaped():
    """Test that variable values are properly escaped so that they can safely be eval'd."""
    changes = envutil.EnvironmentModifications()
    changes.set("VAR", "$PATH")
    changes.append_path("VAR", "$ANOTHER_PATH")
    changes.set("RM_RF", "$(rm -rf /)")

    script = changes.shell_modifications(shell="sh")
    assert f"export VAR='$PATH{os.pathsep}$ANOTHER_PATH'" in script
    assert "export RM_RF='$(rm -rf /)'" in script
