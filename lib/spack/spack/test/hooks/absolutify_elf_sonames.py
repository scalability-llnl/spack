# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

import pytest

import llnl.util.filesystem as fs

import spack.platforms
from spack.hooks.absolutify_elf_sonames import SharedLibrariesVisitor, find_and_patch_sonames
from spack.util.executable import Executable


def skip_unless_linux(f):
    return pytest.mark.skipif(
        str(spack.platforms.real_host()) != "linux", reason="only tested on linux for now"
    )(f)


class ExecutableIntercept:
    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append(args)

    @property
    def returncode(self):
        return 0


@pytest.mark.requires_executables("gcc")
@skip_unless_linux
def test_shared_libraries_visitor(tmpdir):
    """Integration test for soname rewriting"""
    gcc = Executable("gcc")

    # Create a directory structure like this:
    # ./no-soname.so                        # just a shared library without a soname
    # ./soname.so                           # a shared library with a soname
    # ./executable.so                       # an executable masquerading as a shared lib
    # ./libskipme.so                        # a shared library with a soname
    # ./mydir/parent_dir -> ..              # a symlinked dir, causing a cycle
    # ./mydir/skip_symlink -> ../libskipme  # a symlink to a library

    with fs.working_dir(str(tmpdir)):
        with open("hello.c", "w") as f:
            f.write("int main(){return 0;}")
        gcc("hello.c", "-o", "no-soname.so", "--shared")
        gcc("hello.c", "-o", "soname.so", "--shared", "-Wl,-soname,example.so")
        gcc("hello.c", "-pie", "-o", "executable.so")
        gcc("hello.c", "-o", "libskipme.so", "-Wl,-soname,libskipme.so")
        os.mkdir("my_dir")
        os.symlink("..", os.path.join("my_dir", "parent_dir"))
        os.symlink(os.path.join("..", "libskipme.so"), os.path.join("my_dir", "skip_symlink"))

    # Visit the whole prefix, but exclude `skip_symlink`
    visitor = SharedLibrariesVisitor(exclude_list=["skip_symlink"])
    fs.visit_directory_tree(str(tmpdir), visitor)
    relative_paths = visitor.get_shared_libraries_relative_paths()

    assert "no-soname.so" in relative_paths
    assert "soname.so" in relative_paths
    assert "executable.so" not in relative_paths
    assert "libskipme.so" not in relative_paths

    # Run the full hook of finding libs and setting sonames.
    patchelf = ExecutableIntercept()
    find_and_patch_sonames(str(tmpdir), ["skip_symlink"], patchelf)
    assert len(patchelf.calls) == 2
    elf_1 = tmpdir.join("no-soname.so")
    elf_2 = tmpdir.join("soname.so")
    assert ("--set-soname", elf_1, elf_1) in patchelf.calls
    assert ("--set-soname", elf_2, elf_2) in patchelf.calls
