# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

from types import ModuleType

import pickle
import pydoc
import io
import sys
import multiprocessing

import spack.architecture
import spack.config


_serialize = sys.version_info >= (3, 8) and sys.platform == 'darwin'


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


class SpackTestProcess(object):
    def __init__(self, fn):
        self.fn = fn

    def _restore_and_run(self, fn, test_state):
        test_state.restore()
        fn()

    def create(self):
        test_state = TestState()
        return multiprocessing.Process(
            target=self._restore_and_run,
            args=(self.fn, test_state))


class PackageInstallContext(object):
    """Captures the in-memory process state of a package installation that
    needs to be transmitted to a child process.
    """
    def __init__(self, pkg):
        if _serialize:
            self.serialized_pkg = serialize(pkg)
        else:
            self.pkg = pkg
        self.spack_working_dir = spack.main.spack_working_dir
        self.test_state = TestState()

    def restore(self):
        self.test_state.restore()
        spack.main.spack_working_dir = self.spack_working_dir
        if _serialize:
            return pickle.load(self.serialized_pkg)
        else:
            return self.pkg


class TestState(object):
    """Spack tests may modify state that is normally read from disk in memory;
    this object is responsible for properly serializing that state to be
    applied to a subprocess. This isn't needed outside of a testing environment
    but this logic is designed to behave the same inside or outside of tests.
    """
    def __init__(self):
        if _serialize:
            self.repo_dirs = list(r.root for r in spack.repo.path.repos)
            self.config = spack.config.config
            self.platform = spack.architecture.platform
            self.test_patches = store_patches()
            self.store_token = spack.store.store.serialize()

    def restore(self):
        if _serialize:
            spack.repo.path = spack.repo._path(self.repo_dirs)
            spack.config.config = self.config
            spack.architecture.platform = self.platform

            new_store = spack.store.Store.deserialize(self.store_token)
            spack.store.store = new_store
            spack.store.root = new_store.root
            spack.store.unpadded_root = new_store.unpadded_root
            spack.store.db = new_store.db
            spack.store.layout = new_store.layout

            self.test_patches.restore()


class TestPatches(object):
    def __init__(self, module_patches, class_patches):
        self.module_patches = list(
            (x, y, serialize(z)) for (x, y, z) in module_patches)
        self.class_patches = list(
            (x, y, serialize(z)) for (x, y, z) in class_patches)

    def restore(self):
        for module_name, attr_name, value in self.module_patches:
            value = pickle.load(value)
            module = __import__(module_name)
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
    for patch in patches:
        for target, name, _ in patches:
            if isinstance(target, ModuleType):
                new_val = getattr(target, name)
                module_name = target.__name__
                module_patches.append((module_name, name, new_val))
            elif isinstance(target, type):
                new_val = getattr(target, name)
                class_fqn = '.'.join([target.__module__, target.__name__])
                class_patches.append((class_fqn, name, new_val))

    return TestPatches(module_patches, class_patches)


def clear_patches():
    global patches
    patches = None
