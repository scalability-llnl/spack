# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import sys

import pytest

import llnl.util.symlink
from llnl.util.filesystem import mkdirp, touchp, visit_directory_tree, working_dir
from llnl.util.link_tree import DestinationMergeVisitor, LinkTree, SourceMergeVisitor
from llnl.util.symlink import _windows_can_symlink, islink, readlink, symlink

from spack.stage import Stage


@pytest.fixture()
def stage():
    """Creates a stage with the directory structure for the tests."""
    s = Stage("link-tree-test")
    s.create()

    with working_dir(s.path):
        touchp("source/1")
        touchp("source/a/b/2")
        touchp("source/a/b/3")
        touchp("source/c/4")
        touchp("source/c/d/5")
        touchp("source/c/d/6")
        touchp("source/c/d/e/7")

    yield s

    s.destroy()


@pytest.fixture()
def link_tree(stage):
    """Return a properly initialized LinkTree instance."""
    source_path = os.path.join(stage.path, "source")
    return LinkTree(source_path)


def check_file_link(filename, expected_target):
    assert os.path.isfile(filename)
    assert islink(filename)
    if sys.platform != "win32" or llnl.util.symlink._windows_can_symlink():
        assert os.path.abspath(os.path.realpath(filename)) == os.path.abspath(expected_target)


def check_dir(filename):
    assert os.path.isdir(filename)


@pytest.mark.parametrize("run_as_root", [True, False])
def test_merge_to_new_directory(stage, link_tree, monkeypatch, run_as_root):
    if sys.platform != "win32":
        if run_as_root:
            pass
        else:
            pytest.skip("Skipping duplicate test.")
    elif _windows_can_symlink() or not run_as_root:
        monkeypatch.setattr(llnl.util.symlink, "_windows_can_symlink", lambda: run_as_root)
    else:
        # Skip if trying to run as dev-mode without having dev-mode.
        pytest.skip("Skipping portion of test which required dev-mode privileges.")

    with working_dir(stage.path):
        link_tree.merge("dest")

        files = [
            ("dest/1", "source/1"),
            ("dest/a/b/2", "source/a/b/2"),
            ("dest/a/b/3", "source/a/b/3"),
            ("dest/c/4", "source/c/4"),
            ("dest/c/d/5", "source/c/d/5"),
            ("dest/c/d/6", "source/c/d/6"),
            ("dest/c/d/e/7", "source/c/d/e/7"),
        ]

        for dest, source in files:
            check_file_link(dest, source)
            assert os.path.isabs(readlink(dest))

        link_tree.unmerge("dest")

        assert not os.path.exists("dest")


@pytest.mark.parametrize("run_as_root", [True, False])
def test_merge_to_new_directory_relative(stage, link_tree, monkeypatch, run_as_root):
    if sys.platform != "win32":
        if run_as_root:
            pass
        else:
            pytest.skip("Skipping duplicate test.")
    elif _windows_can_symlink() or not run_as_root:
        monkeypatch.setattr(llnl.util.symlink, "_windows_can_symlink", lambda: run_as_root)
    else:
        # Skip if trying to run as dev-mode without having dev-mode.
        pytest.skip("Skipping portion of test which required dev-mode privileges.")

    with working_dir(stage.path):
        link_tree.merge("dest", relative=True)

        files = [
            ("dest/1", "source/1"),
            ("dest/a/b/2", "source/a/b/2"),
            ("dest/a/b/3", "source/a/b/3"),
            ("dest/c/4", "source/c/4"),
            ("dest/c/d/5", "source/c/d/5"),
            ("dest/c/d/6", "source/c/d/6"),
            ("dest/c/d/e/7", "source/c/d/e/7"),
        ]

        for dest, source in files:
            check_file_link(dest, source)
            # Hard links/junctions are inherently absolute.
            if sys.platform != "win32" or run_as_root:
                assert not os.path.isabs(readlink(dest))

        link_tree.unmerge("dest")

        assert not os.path.exists("dest")


@pytest.mark.parametrize("run_as_root", [True, False])
def test_merge_to_existing_directory(stage, link_tree, monkeypatch, run_as_root):
    if sys.platform != "win32":
        if run_as_root:
            pass
        else:
            pytest.skip("Skipping duplicate test.")
    elif _windows_can_symlink() or not run_as_root:
        monkeypatch.setattr(llnl.util.symlink, "_windows_can_symlink", lambda: run_as_root)
    else:
        # Skip if trying to run as dev-mode without having dev-mode.
        pytest.skip("Skipping portion of test which required dev-mode privileges.")

    with working_dir(stage.path):
        touchp("dest/x")
        touchp("dest/a/b/y")

        link_tree.merge("dest")

        files = [
            ("dest/1", "source/1"),
            ("dest/a/b/2", "source/a/b/2"),
            ("dest/a/b/3", "source/a/b/3"),
            ("dest/c/4", "source/c/4"),
            ("dest/c/d/5", "source/c/d/5"),
            ("dest/c/d/6", "source/c/d/6"),
            ("dest/c/d/e/7", "source/c/d/e/7"),
        ]
        for dest, source in files:
            check_file_link(dest, source)

        assert os.path.isfile("dest/x")
        assert os.path.isfile("dest/a/b/y")

        link_tree.unmerge("dest")

        assert os.path.isfile("dest/x")
        assert os.path.isfile("dest/a/b/y")

        for dest, _ in files:
            assert not os.path.isfile(dest)


def test_merge_with_empty_directories(stage, link_tree):
    with working_dir(stage.path):
        mkdirp("dest/f/g")
        mkdirp("dest/a/b/h")

        link_tree.merge("dest")
        link_tree.unmerge("dest")

        assert not os.path.exists("dest/1")
        assert not os.path.exists("dest/a/b/2")
        assert not os.path.exists("dest/a/b/3")
        assert not os.path.exists("dest/c/4")
        assert not os.path.exists("dest/c/d/5")
        assert not os.path.exists("dest/c/d/6")
        assert not os.path.exists("dest/c/d/e/7")

        assert os.path.isdir("dest/a/b/h")
        assert os.path.isdir("dest/f/g")


def test_ignore(stage, link_tree):
    with working_dir(stage.path):
        touchp("source/.spec")
        touchp("dest/.spec")

        link_tree.merge("dest", ignore=lambda x: x == ".spec")
        link_tree.unmerge("dest", ignore=lambda x: x == ".spec")

        assert not os.path.exists("dest/1")
        assert not os.path.exists("dest/a")
        assert not os.path.exists("dest/c")

        assert os.path.isfile("source/.spec")
        assert os.path.isfile("dest/.spec")


def test_source_merge_visitor_does_not_follow_symlinked_dirs_at_depth(tmpdir):
    """Given an dir structure like this::

        .
        `-- a
            |-- b
            |   |-- c
            |   |   |-- d
            |   |   |   `-- file
            |   |   `-- symlink_d -> d
            |   `-- symlink_c -> c
            `-- symlink_b -> b

    The SoureMergeVisitor will expand symlinked dirs to directories, but only
    to fixed depth, to avoid exponential explosion. In our current defaults,
    symlink_b will be expanded, but symlink_c and symlink_d will not.
    """
    j = os.path.join
    with tmpdir.as_cwd():
        os.mkdir(j("a"))
        os.mkdir(j("a", "b"))
        os.mkdir(j("a", "b", "c"))
        os.mkdir(j("a", "b", "c", "d"))
        symlink(j("b"), j("a", "symlink_b"))
        symlink(j("c"), j("a", "b", "symlink_c"))
        symlink(j("d"), j("a", "b", "c", "symlink_d"))
        with open(j("a", "b", "c", "d", "file"), "wb"):
            pass

    visitor = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir), visitor)
    assert [p for p in visitor.files.keys()] == [
        j("a", "b", "c", "d", "file"),
        j("a", "b", "c", "symlink_d"),  # treated as a file, not expanded
        j("a", "b", "symlink_c"),  # treated as a file, not expanded
        j("a", "symlink_b", "c", "d", "file"),  # symlink_b was expanded
        j("a", "symlink_b", "c", "symlink_d"),  # symlink_b was expanded
        j("a", "symlink_b", "symlink_c"),  # symlink_b was expanded
    ]
    assert [p for p in visitor.directories.keys()] == [
        j("a"),
        j("a", "b"),
        j("a", "b", "c"),
        j("a", "b", "c", "d"),
        j("a", "symlink_b"),
        j("a", "symlink_b", "c"),
        j("a", "symlink_b", "c", "d"),
    ]


def test_source_merge_visitor_cant_be_cyclical(tmpdir):
    """Given an dir structure like this::

        .
        |-- a
        |   `-- symlink_b -> ../b
        |   `-- symlink_symlink_b -> symlink_b
        `-- b
            `-- symlink_a -> ../a

    The SoureMergeVisitor will not expand `a/symlink_b`, `a/symlink_symlink_b` and
    `b/symlink_a` to avoid recursion. The general rule is: only expand symlinked dirs
    pointing deeper into the directory structure.
    """
    j = os.path.join
    with tmpdir.as_cwd():
        os.mkdir(j("a"))
        os.mkdir(j("b"))

        symlink(j("..", "b"), j("a", "symlink_b"))
        symlink(j("symlink_b"), j("a", "symlink_b_b"))
        symlink(j("..", "a"), j("b", "symlink_a"))

    visitor = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir), visitor)
    assert [p for p in visitor.files.keys()] == [
        j("a", "symlink_b"),
        j("a", "symlink_b_b"),
        j("b", "symlink_a"),
    ]
    assert [p for p in visitor.directories.keys()] == [j("a"), j("b")]


def test_destination_merge_visitor_always_errors_on_symlinked_dirs(tmpdir):
    """When merging prefixes into a non-empty destination folder, and
    this destination folder has a symlinked dir where the prefix has a dir,
    we should never merge any files there, but register a fatal error."""
    j = os.path.join

    # Here example_a and example_b are symlinks.
    with tmpdir.mkdir("dst").as_cwd():
        os.mkdir("a")
        os.symlink("a", "example_a")
        os.symlink("a", "example_b")

    # Here example_a is a directory, and example_b is a (non-expanded) symlinked
    # directory.
    with tmpdir.mkdir("src").as_cwd():
        os.mkdir("example_a")
        with open(j("example_a", "file"), "wb"):
            pass
        os.symlink("..", "example_b")

    visitor = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir.join("src")), visitor)
    visit_directory_tree(str(tmpdir.join("dst")), DestinationMergeVisitor(visitor))

    assert visitor.fatal_conflicts
    conflicts = [c.dst for c in visitor.fatal_conflicts]
    assert "example_a" in conflicts
    assert "example_b" in conflicts


def test_destination_merge_visitor_file_dir_clashes(tmpdir):
    """Tests whether non-symlink file-dir and dir-file clashes as registered as fatal
    errors"""
    with tmpdir.mkdir("a").as_cwd():
        os.mkdir("example")

    with tmpdir.mkdir("b").as_cwd():
        with open("example", "wb"):
            pass

    a_to_b = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir.join("a")), a_to_b)
    visit_directory_tree(str(tmpdir.join("b")), DestinationMergeVisitor(a_to_b))
    assert a_to_b.fatal_conflicts
    assert a_to_b.fatal_conflicts[0].dst == "example"

    b_to_a = SourceMergeVisitor()
    visit_directory_tree(str(tmpdir.join("b")), b_to_a)
    visit_directory_tree(str(tmpdir.join("a")), DestinationMergeVisitor(b_to_a))
    assert b_to_a.fatal_conflicts
    assert b_to_a.fatal_conflicts[0].dst == "example"


def test_source_merge_visitor_does_not_register_identical_file_conflicts(tmp_path: pathlib.Path):
    """Tests whether the SourceMergeVisitor does not register identical file conflicts.
    but instead registers the file that triggers the potential conflict."""
    (tmp_path / "dir_bottom").mkdir()
    (tmp_path / "dir_bottom" / "file").write_bytes(b"hello")

    (tmp_path / "dir_top").mkdir()
    (tmp_path / "dir_top" / "file").symlink_to(tmp_path / "dir_bottom" / "file")
    (tmp_path / "dir_top" / "zzzz").write_bytes(b"hello")

    visitor = SourceMergeVisitor()
    visitor.set_projection(str(tmp_path / "view"))

    visit_directory_tree(str(tmp_path / "dir_top"), visitor)

    # After visiting the top dir, we should have `file` and `zzzz` listed, in that order. Using
    # .items() to test order.
    assert list(visitor.files.items()) == [
        (str(tmp_path / "view" / "file"), (str(tmp_path / "dir_top"), "file")),
        (str(tmp_path / "view" / "zzzz"), (str(tmp_path / "dir_top"), "zzzz")),
    ]

    # Then after visiting the bottom dir, the "conflict" should be resolved, and `file` should
    # come from the bottom dir.
    visit_directory_tree(str(tmp_path / "dir_bottom"), visitor)
    assert not visitor.file_conflicts
    assert list(visitor.files.items()) == [
        (str(tmp_path / "view" / "zzzz"), (str(tmp_path / "dir_top"), "zzzz")),
        (str(tmp_path / "view" / "file"), (str(tmp_path / "dir_bottom"), "file")),
    ]


def test_source_merge_visitor_does_deals_with_dangling_symlinks(tmp_path: pathlib.Path):
    """When a file and a dangling symlink conflict, this should be handled like a file conflict."""
    (tmp_path / "dir_a").mkdir()
    os.symlink("non-existent", str(tmp_path / "dir_a" / "file"))

    (tmp_path / "dir_b").mkdir()
    (tmp_path / "dir_b" / "file").write_bytes(b"data")

    visitor = SourceMergeVisitor()
    visitor.set_projection(str(tmp_path / "view"))

    visit_directory_tree(str(tmp_path / "dir_a"), visitor)
    visit_directory_tree(str(tmp_path / "dir_b"), visitor)

    # Check that a conflict was registered.
    assert len(visitor.file_conflicts) == 1
    conflict = visitor.file_conflicts[0]
    assert conflict.src_a == str(tmp_path / "dir_a" / "file")
    assert conflict.src_b == str(tmp_path / "dir_b" / "file")
    assert conflict.dst == str(tmp_path / "view" / "file")

    # The first file encountered should be listed.
    assert visitor.files == {str(tmp_path / "view" / "file"): (str(tmp_path / "dir_a"), "file")}
