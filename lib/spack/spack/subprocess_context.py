# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module handles transmission of Spack state to child processes started
using the 'spawn' start method. Notably, installations are performed in a
subprocess and require transmitting the Package object (in such a way
that the repository is available for importing when it is deserialized);
installations performed in Spack unit tests may include additional
modifications to global state in memory that must be replicated in the
child process.
"""
import importlib
import io
import multiprocessing
import pickle
import pydoc
import sys
from types import ModuleType

import spack.config
import spack.environment
import spack.paths
import spack.platforms
import spack.repo
import spack.store

_SERIALIZE = sys.platform == "win32" or (sys.version_info >= (3, 8) and sys.platform == "darwin")


patches = None


def append_patch(patch):
    global patches
    if not patches:
        patches = list()
    patches.append(patch)


def serialize(obj):
    serialized_obj = io.BytesIO()
    pickle.dump(obj, serialized_obj)
    serialized_obj.seek(0)
    return serialized_obj


class SpackTestProcess:
    def __init__(self, fn):
        self.fn = fn

    def _restore_and_run(self, fn, test_state):
        test_state.restore()
        fn()

    def create(self):
        test_state = TestState()
        return multiprocessing.Process(target=self._restore_and_run, args=(self.fn, test_state))


class PackageInstallContext:
    """Captures the in-memory process state of a package installation that
    needs to be transmitted to a child process.
    """

    def __init__(self, pkg):
        if _SERIALIZE:
            self.serialized_pkg = serialize(pkg)
            self.serialized_env = serialize(spack.environment.active_environment())
        else:
            self.pkg = pkg
            self.env = spack.environment.active_environment()
        self.spack_working_dir = spack.paths.spack_working_dir
        self.test_state = TestState()

    def restore(self):
        self.test_state.restore()
        spack.paths.spack_working_dir = self.spack_working_dir
        env = pickle.load(self.serialized_env) if _SERIALIZE else self.env
        if env:
            spack.environment.activate(env)
        # Order of operation is important, since the package might be retrieved
        # from a repo defined within the environment configuration
        pkg = pickle.load(self.serialized_pkg) if _SERIALIZE else self.pkg
        return pkg


class TestState:
    """Spack tests may modify state that is normally read from disk in memory;
    this object is responsible for properly serializing that state to be
    applied to a subprocess. This isn't needed outside of a testing environment
    but this logic is designed to behave the same inside or outside of tests.
    """

    def __init__(self):
        if _SERIALIZE:
            self.config = spack.config.CONFIG
            self.platform = spack.platforms.host
            self.test_patches = store_patches()
            self.store = spack.store.STORE

    def restore(self):
        if _SERIALIZE:
            spack.config.CONFIG = self.config
            spack.repo.PATH = spack.repo.create(self.config)
            spack.platforms.host = self.platform
            spack.store.STORE = self.store
            self.test_patches.restore()


class TestPatches:
    def __init__(self, module_patches, class_patches):
        self.module_patches = list((x, y, serialize(z)) for (x, y, z) in module_patches)
        self.class_patches = list((x, y, serialize(z)) for (x, y, z) in class_patches)

    def restore(self):
        for module_name, attr_name, value in self.module_patches:
            value = pickle.load(value)
            module = importlib.import_module(module_name)
            setattr(module, attr_name, value)
        for class_fqn, attr_name, value in self.class_patches:
            value = pickle.load(value)
            cls = pydoc.locate(class_fqn)
            setattr(cls, attr_name, value)


def store_patches():
    global patches
    module_patches = list()
    class_patches = list()
    if not patches:
        return TestPatches(list(), list())
    for target, name, _ in patches:
        if isinstance(target, ModuleType):
            new_val = getattr(target, name)
            module_name = target.__name__
            module_patches.append((module_name, name, new_val))
        elif isinstance(target, type):
            new_val = getattr(target, name)
            class_fqn = ".".join([target.__module__, target.__name__])
            class_patches.append((class_fqn, name, new_val))

    return TestPatches(module_patches, class_patches)


def clear_patches():
    global patches
    patches = None
