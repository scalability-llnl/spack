# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.repo
import spack.util.editor
from spack.build_systems import autotools, cmake
from spack.main import SpackCommand

edit = SpackCommand("edit")


def test_edit_packages(monkeypatch, mock_packages: spack.repo.RepoPath):
    """Test spack edit pkg-a pkg-b"""
    path_a = mock_packages.filename_for_package_name("pkg-a")
    path_b = mock_packages.filename_for_package_name("pkg-b")
    called = False

    def editor(*args: str, **kwargs):
        nonlocal called
        called = True
        assert args[0] == path_a
        assert args[1] == path_b

    monkeypatch.setattr(spack.util.editor, "editor", editor)
    edit("pkg-a", "pkg-b")
    assert called


def test_edit_files(monkeypatch):
    """Test spack edit --build-system autotools cmake"""
    called = False

    def editor(*args: str, **kwargs):
        nonlocal called
        called = True
        assert os.path.samefile(args[0], autotools.__file__)
        assert os.path.samefile(args[1], cmake.__file__)

    monkeypatch.setattr(spack.util.editor, "editor", editor)
    edit("--build-system", "autotools", "cmake")
    assert called
