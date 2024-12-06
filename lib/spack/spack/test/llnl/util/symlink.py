# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``llnl/util/symlink.py``"""
import os
import tempfile

import pytest

from llnl.util import symlink


def test_symlink_file(tmpdir):
    """Test the symlink.symlink functionality on all operating systems for a file"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmpdir.join("link.txt"))
        assert os.path.exists(link_file) is False
        symlink.symlink(real_file, link_file)
        assert os.path.exists(link_file)
        assert symlink.islink(link_file)


def test_symlink_dir(tmpdir):
    """Test the symlink.symlink functionality on all operating systems for a directory"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(real_dir)
        symlink.symlink(real_dir, link_dir)
        assert os.path.exists(link_dir)
        assert symlink.islink(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_source_not_exists(tmpdir):
    """Test the symlink.symlink method for the case where a source path does not exist"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        with pytest.raises(symlink.SymlinkError):
            symlink._windows_symlink(real_dir, link_dir)


def test_symlink_src_relative_to_link(tmpdir):
    """Test the symlink.symlink functionality where the source value exists relative to the link
    but not relative to the cwd"""
    with tmpdir.as_cwd():
        subdir_1 = tmpdir.join("a")
        subdir_2 = os.path.join(subdir_1, "b")
        link_dir = os.path.join(subdir_1, "c")

        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=subdir_2)
        link_file = os.path.join(subdir_1, "link.txt")

        symlink.symlink(f"b/{os.path.basename(real_file)}", f"a/{os.path.basename(link_file)}")
        assert os.path.exists(link_file)
        assert symlink.islink(link_file)
        # Check dirs
        assert not os.path.lexists(link_dir)
        symlink.symlink("b", "a/c")
        assert os.path.lexists(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_src_not_relative_to_link(tmpdir):
    """Test the symlink.symlink functionality where the source value does not exist relative to
    the link and not relative to the cwd. NOTE that this symlink api call is EXPECTED to raise
    a symlink.SymlinkError exception that we catch."""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        subdir_1 = os.path.join(test_dir, "a")
        subdir_2 = os.path.join(subdir_1, "b")
        link_dir = os.path.join(subdir_1, "c")
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=subdir_2)
        link_file = str(tmpdir.join("link.txt"))
        # Expected SymlinkError because source path does not exist relative to link path
        with pytest.raises(symlink.SymlinkError):
            symlink._windows_symlink(
                f"d/{os.path.basename(real_file)}", f"a/{os.path.basename(link_file)}"
            )
        assert not os.path.exists(link_file)
        # Check dirs
        assert not os.path.lexists(link_dir)
        with pytest.raises(symlink.SymlinkError):
            symlink._windows_symlink("d", "a/c")
        assert not os.path.lexists(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_link_already_exists(tmpdir):
    """Test the symlink.symlink method for the case where a link already exists"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        real_dir = os.path.join(test_dir, "real_dir")
        link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(real_dir)
        symlink._windows_symlink(real_dir, link_dir)
        assert os.path.exists(link_dir)
        with pytest.raises(symlink.SymlinkError):
            symlink._windows_symlink(real_dir, link_dir)


@pytest.mark.skipif(not symlink._windows_can_symlink(), reason="Test requires elevated privileges")
@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_win_file(tmpdir):
    """Check that symlink.symlink makes a symlink file when run with elevated permissions"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmpdir.join("link.txt"))
        symlink.symlink(real_file, link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert symlink.islink(link_file)
        assert os.path.islink(link_file)
        assert not symlink._windows_is_hardlink(link_file)
        assert not symlink._windows_is_junction(link_file)


@pytest.mark.skipif(not symlink._windows_can_symlink(), reason="Test requires elevated privileges")
@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_symlink_win_dir(tmpdir):
    """Check that symlink.symlink makes a symlink dir when run with elevated permissions"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        real_dir = os.path.join(test_dir, "real")
        link_dir = os.path.join(test_dir, "link")
        os.mkdir(real_dir)
        symlink.symlink(real_dir, link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(link_dir)
        assert symlink.islink(link_dir)
        assert os.path.islink(link_dir)
        assert not symlink._windows_is_hardlink(link_dir)
        assert not symlink._windows_is_junction(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_junction(tmpdir):
    """Test the symlink._windows_create_junction method"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        junction_real_dir = os.path.join(test_dir, "real_dir")
        junction_link_dir = os.path.join(test_dir, "link_dir")
        os.mkdir(junction_real_dir)
        symlink._windows_create_junction(junction_real_dir, junction_link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(junction_link_dir)
        assert symlink._windows_is_junction(junction_link_dir)
        assert symlink.islink(junction_link_dir)
        assert not os.path.islink(junction_link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_hard_link(tmpdir):
    """Test the symlink._windows_create_hard_link method"""
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmpdir.join("link.txt"))
        symlink._windows_create_hard_link(real_file, link_file)
        # Verify that all expected conditions are met
        assert os.path.exists(link_file)
        assert symlink._windows_is_hardlink(real_file)
        assert symlink._windows_is_hardlink(link_file)
        assert symlink.islink(link_file)
        assert not os.path.islink(link_file)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_link_dir(tmpdir):
    """Test the functionality of the windows_create_link method with a directory
    which should result in making a junction.
    """
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        real_dir = os.path.join(test_dir, "real")
        link_dir = os.path.join(test_dir, "link")
        os.mkdir(real_dir)
        symlink._windows_create_link(real_dir, link_dir)
        # Verify that all expected conditions are met
        assert os.path.exists(link_dir)
        assert symlink.islink(link_dir)
        assert not symlink._windows_is_hardlink(link_dir)
        assert symlink._windows_is_junction(link_dir)
        assert not os.path.islink(link_dir)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_create_link_file(tmpdir):
    """Test the functionality of the windows_create_link method with a file
    which should result in the creation of a hard link. It also tests the
    functionality of the symlink islink infrastructure.
    """
    with tmpdir.as_cwd():
        test_dir = str(tmpdir)
        fd, real_file = tempfile.mkstemp(prefix="real", suffix=".txt", dir=test_dir)
        link_file = str(tmpdir.join("link.txt"))
        symlink._windows_create_link(real_file, link_file)
        # Verify that all expected conditions are met
        assert symlink._windows_is_hardlink(link_file)
        assert symlink.islink(link_file)
        assert not symlink._windows_is_junction(link_file)


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_read_link(tmpdir):
    """Makes sure symlink.readlink can read the link source for hard links and
    junctions on windows."""
    with tmpdir.as_cwd():
        real_dir_1 = "real_dir_1"
        real_dir_2 = "real_dir_2"
        link_dir_1 = "link_dir_1"
        link_dir_2 = "link_dir_2"
        os.mkdir(real_dir_1)
        os.mkdir(real_dir_2)

        # Create a file and a directory
        _, real_file_1 = tempfile.mkstemp(prefix="real_1", suffix=".txt", dir=".")
        _, real_file_2 = tempfile.mkstemp(prefix="real_2", suffix=".txt", dir=".")
        link_file_1 = "link_1.txt"
        link_file_2 = "link_2.txt"

        # Make hard link/junction
        symlink._windows_create_hard_link(real_file_1, link_file_1)
        symlink._windows_create_hard_link(real_file_2, link_file_2)
        symlink._windows_create_junction(real_dir_1, link_dir_1)
        symlink._windows_create_junction(real_dir_2, link_dir_2)

        assert symlink.readlink(link_file_1) == os.path.abspath(real_file_1)
        assert symlink.readlink(link_file_2) == os.path.abspath(real_file_2)
        assert symlink.readlink(link_dir_1) == os.path.abspath(real_dir_1)
        assert symlink.readlink(link_dir_2) == os.path.abspath(real_dir_2)
