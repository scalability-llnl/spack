# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import llnl.util.filesystem as fs

import spack.caches
import spack.cmd.clean
import spack.environment as ev
import spack.main
import spack.package_base
import spack.spec
import spack.stage
import spack.store

clean = spack.main.SpackCommand("clean")


@pytest.fixture()
def mock_calls_for_clean(monkeypatch):
    counts = {}

    class Counter:
        def __init__(self, name):
            self.name = name
            counts[name] = 0

        def __call__(self, *args, **kwargs):
            counts[self.name] += 1

    monkeypatch.setattr(spack.package_base.PackageBase, "do_clean", Counter("package"))
    monkeypatch.setattr(spack.stage, "purge", Counter("stages"))
    monkeypatch.setattr(spack.caches.FETCH_CACHE, "destroy", Counter("downloads"), raising=False)
    monkeypatch.setattr(spack.caches.MISC_CACHE, "destroy", Counter("caches"))
    monkeypatch.setattr(spack.store.STORE.failure_tracker, "clear_all", Counter("failures"))
    monkeypatch.setattr(spack.cmd.clean, "remove_python_cache", Counter("python_cache"))

    yield counts


all_effects = ["stages", "downloads", "caches", "failures", "python_cache"]


@pytest.mark.usefixtures("mock_packages", "config")
@pytest.mark.parametrize(
    "command_line,effects",
    [
        ("mpileaks", ["package"]),
        ("-s", ["stages"]),
        ("-sd", ["stages", "downloads"]),
        ("-m", ["caches"]),
        ("-f", ["failures"]),
        ("-p", ["python_cache"]),
        ("-a", all_effects),
        ("", []),
    ],
)
def test_function_calls(command_line, effects, mock_calls_for_clean):
    # Call the command with the supplied command line
    clean(command_line)

    # Assert that we called the expected functions the correct
    # number of times
    for name in ["package"] + all_effects:
        assert mock_calls_for_clean[name] == (1 if name in effects else 0)


def test_env_aware_clean(mock_stage, install_mockery, mutable_mock_env_path, monkeypatch):
    e = ev.create("test", with_view=False)
    e.add("mpileaks")
    e.concretize()

    def fail(*args, **kwargs):
        raise Exception("This should not have been called")

    monkeypatch.setattr(spack.spec.Spec, "concretize", fail)

    with e:
        clean("mpileaks")


def test_remove_python_cache(tmpdir, monkeypatch):
    cache_files = ["file1.pyo", "file2.pyc"]
    source_file = "file1.py"

    def _setup_files(directory):
        # Create a python cache and source file.
        cache_dir = fs.join_path(directory, "__pycache__")
        fs.mkdirp(cache_dir)
        fs.touch(fs.join_path(directory, source_file))
        fs.touch(fs.join_path(directory, cache_files[0]))
        for filename in cache_files:
            # Ensure byte code files in python cache directory
            fs.touch(fs.join_path(cache_dir, filename))

    def _check_files(directory):
        # Ensure the python cache created by _setup_files is removed
        # and the source file is not.
        assert os.path.exists(fs.join_path(directory, source_file))
        assert not os.path.exists(fs.join_path(directory, cache_files[0]))
        assert not os.path.exists(fs.join_path(directory, "__pycache__"))

    source_dir = fs.join_path(tmpdir, "lib", "spack", "spack")
    var_dir = fs.join_path(tmpdir, "var", "spack", "stuff")

    for d in [source_dir, var_dir]:
        _setup_files(d)

    # Patching the path variables from-import'd by spack.cmd.clean is needed
    # to ensure the paths used by the command for this test reflect the
    # temporary directory locations and not those from spack.paths when
    # the clean command's module was imported.
    monkeypatch.setattr(spack.cmd.clean, "lib_path", source_dir)
    monkeypatch.setattr(spack.cmd.clean, "var_path", var_dir)

    spack.cmd.clean.remove_python_cache()

    for d in [source_dir, var_dir]:
        _check_files(d)
