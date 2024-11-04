# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``llnl/util/filesystem.py``"""
import filecmp
import os
import shutil
import stat
import sys
from contextlib import contextmanager

import pytest

import llnl.util.filesystem as fs
from llnl.util.symlink import islink, readlink, symlink

import spack.paths


@pytest.fixture()
def stage(tmpdir_factory):
    """Creates a stage with the directory structure for the tests."""

    s = tmpdir_factory.mktemp("filesystem_test")

    with s.as_cwd():
        # Create source file hierarchy
        fs.touchp("source/1")
        fs.touchp("source/a/b/2")
        fs.touchp("source/a/b/3")
        fs.touchp("source/c/4")
        fs.touchp("source/c/d/5")
        fs.touchp("source/c/d/6")
        fs.touchp("source/c/d/e/7")
        fs.touchp("source/g/h/i/8")
        fs.touchp("source/g/h/i/9")
        fs.touchp("source/g/i/j/10")

        # Create symlinks
        symlink(os.path.abspath("source/1"), "source/2")
        symlink("b/2", "source/a/b2")
        symlink("a/b", "source/f")

        # Create destination directory
        fs.mkdirp("dest")

    yield s


class TestCopy:
    """Tests for ``filesystem.copy``"""

    def test_file_dest(self, stage):
        """Test using a filename as the destination."""

        with fs.working_dir(str(stage)):
            fs.copy("source/1", "dest/1")

            assert os.path.exists("dest/1")

    def test_dir_dest(self, stage):
        """Test using a directory as the destination."""

        with fs.working_dir(str(stage)):
            fs.copy("source/1", "dest")

            assert os.path.exists("dest/1")

    def test_glob_src(self, stage):
        """Test using a glob as the source."""

        with fs.working_dir(str(stage)):
            fs.copy("source/a/*/*", "dest")

            assert os.path.exists("dest/2")
            assert os.path.exists("dest/3")

    def test_non_existing_src(self, stage):
        """Test using a non-existing source."""

        with fs.working_dir(str(stage)):
            with pytest.raises(IOError, match="No such file or directory"):
                fs.copy("source/none", "dest")

    def test_multiple_src_file_dest(self, stage):
        """Test a glob that matches multiple source files and a dest
        that is not a directory."""

        with fs.working_dir(str(stage)):
            match = ".* matches multiple files but .* is not a directory"
            with pytest.raises(ValueError, match=match):
                fs.copy("source/a/*/*", "dest/1")


def check_added_exe_permissions(src, dst):
    src_mode = os.stat(src).st_mode
    dst_mode = os.stat(dst).st_mode
    for perm in [stat.S_IXUSR, stat.S_IXGRP, stat.S_IXOTH]:
        if src_mode & perm:
            assert dst_mode & perm


class TestInstall:
    """Tests for ``filesystem.install``"""

    def test_file_dest(self, stage):
        """Test using a filename as the destination."""

        with fs.working_dir(str(stage)):
            fs.install("source/1", "dest/1")

            assert os.path.exists("dest/1")
            check_added_exe_permissions("source/1", "dest/1")

    def test_dir_dest(self, stage):
        """Test using a directory as the destination."""

        with fs.working_dir(str(stage)):
            fs.install("source/1", "dest")

            assert os.path.exists("dest/1")
            check_added_exe_permissions("source/1", "dest/1")

    def test_glob_src(self, stage):
        """Test using a glob as the source."""

        with fs.working_dir(str(stage)):
            fs.install("source/a/*/*", "dest")

            assert os.path.exists("dest/2")
            assert os.path.exists("dest/3")
            check_added_exe_permissions("source/a/b/2", "dest/2")
            check_added_exe_permissions("source/a/b/3", "dest/3")

    def test_non_existing_src(self, stage):
        """Test using a non-existing source."""

        with fs.working_dir(str(stage)):
            with pytest.raises(IOError, match="No such file or directory"):
                fs.install("source/none", "dest")

    def test_multiple_src_file_dest(self, stage):
        """Test a glob that matches multiple source files and a dest
        that is not a directory."""

        with fs.working_dir(str(stage)):
            match = ".* matches multiple files but .* is not a directory"
            with pytest.raises(ValueError, match=match):
                fs.install("source/a/*/*", "dest/1")


class TestCopyTree:
    """Tests for ``filesystem.copy_tree``"""

    def test_existing_dir(self, stage):
        """Test copying to an existing directory."""

        with fs.working_dir(str(stage)):
            fs.copy_tree("source", "dest")

            assert os.path.exists("dest/a/b/2")

    def test_non_existing_dir(self, stage):
        """Test copying to a non-existing directory."""

        with fs.working_dir(str(stage)):
            fs.copy_tree("source", "dest/sub/directory")

            assert os.path.exists("dest/sub/directory/a/b/2")

    def test_symlinks_true(self, stage):
        """Test copying with symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.copy_tree("source", "dest", symlinks=True)

            assert os.path.exists("dest/2")
            assert islink("dest/2")

            assert os.path.exists("dest/a/b2")
            with fs.working_dir("dest/a"):
                assert os.path.exists(readlink("b2"))

            assert os.path.realpath("dest/f/2") == os.path.abspath("dest/a/b/2")
            assert os.path.realpath("dest/2") == os.path.abspath("dest/1")

    def test_symlinks_true_ignore(self, stage):
        """Test copying when specifying relative paths that should be ignored"""
        with fs.working_dir(str(stage)):
            ignore = lambda p: p in [os.path.join("c", "d", "e"), "a"]
            fs.copy_tree("source", "dest", symlinks=True, ignore=ignore)
            assert not os.path.exists("dest/a")
            assert os.path.exists("dest/c/d")
            assert not os.path.exists("dest/c/d/e")

    def test_symlinks_false(self, stage):
        """Test copying without symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.copy_tree("source", "dest", symlinks=False)

            assert os.path.exists("dest/2")
            if sys.platform != "win32":
                assert not os.path.islink("dest/2")

    def test_glob_src(self, stage):
        """Test using a glob as the source."""

        with fs.working_dir(str(stage)):
            fs.copy_tree("source/g/*", "dest")

            assert os.path.exists("dest/i/8")
            assert os.path.exists("dest/i/9")
            assert os.path.exists("dest/j/10")

    def test_non_existing_src(self, stage):
        """Test using a non-existing source."""

        with fs.working_dir(str(stage)):
            with pytest.raises(IOError, match="No such file or directory"):
                fs.copy_tree("source/none", "dest")

    def test_parent_dir(self, stage):
        """Test source as a parent directory of destination."""

        with fs.working_dir(str(stage)):
            match = "Cannot copy ancestor directory"
            with pytest.raises(ValueError, match=match):
                fs.copy_tree("source", "source/sub/directory")


class TestInstallTree:
    """Tests for ``filesystem.install_tree``"""

    def test_existing_dir(self, stage):
        """Test installing to an existing directory."""

        with fs.working_dir(str(stage)):
            fs.install_tree("source", "dest")

            assert os.path.exists("dest/a/b/2")
            check_added_exe_permissions("source/a/b/2", "dest/a/b/2")

    def test_non_existing_dir(self, stage):
        """Test installing to a non-existing directory."""

        with fs.working_dir(str(stage)):
            fs.install_tree("source", "dest/sub/directory")

            assert os.path.exists("dest/sub/directory/a/b/2")
            check_added_exe_permissions("source/a/b/2", "dest/sub/directory/a/b/2")

    def test_symlinks_true(self, stage):
        """Test installing with symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.install_tree("source", "dest", symlinks=True)

            assert os.path.exists("dest/2")
            if sys.platform != "win32":
                assert os.path.islink("dest/2")
            check_added_exe_permissions("source/2", "dest/2")

    def test_symlinks_false(self, stage):
        """Test installing without symlink preservation."""

        with fs.working_dir(str(stage)):
            fs.install_tree("source", "dest", symlinks=False)

            assert os.path.exists("dest/2")
            if sys.platform != "win32":
                assert not os.path.islink("dest/2")
            check_added_exe_permissions("source/2", "dest/2")

    @pytest.mark.not_on_windows("Broken symlinks not allowed on Windows")
    def test_allow_broken_symlinks(self, stage):
        """Test installing with a broken symlink."""
        with fs.working_dir(str(stage)):
            symlink("nonexistant.txt", "source/broken")
            fs.install_tree("source", "dest", symlinks=True)
            assert os.path.islink("dest/broken")
            assert not os.path.exists(readlink("dest/broken"))

    def test_glob_src(self, stage):
        """Test using a glob as the source."""

        with fs.working_dir(str(stage)):
            fs.install_tree("source/g/*", "dest")

            assert os.path.exists("dest/i/8")
            assert os.path.exists("dest/i/9")
            assert os.path.exists("dest/j/10")
            check_added_exe_permissions("source/g/h/i/8", "dest/i/8")
            check_added_exe_permissions("source/g/h/i/9", "dest/i/9")
            check_added_exe_permissions("source/g/i/j/10", "dest/j/10")

    def test_non_existing_src(self, stage):
        """Test using a non-existing source."""

        with fs.working_dir(str(stage)):
            with pytest.raises(IOError, match="No such file or directory"):
                fs.install_tree("source/none", "dest")

    def test_parent_dir(self, stage):
        """Test source as a parent directory of destination."""

        with fs.working_dir(str(stage)):
            match = "Cannot copy ancestor directory"
            with pytest.raises(ValueError, match=match):
                fs.install_tree("source", "source/sub/directory")


def test_paths_containing_libs(dirs_with_libfiles):
    lib_to_dirs, all_dirs = dirs_with_libfiles

    assert set(fs.paths_containing_libs(all_dirs, ["libgfortran"])) == set(
        lib_to_dirs["libgfortran"]
    )

    assert set(fs.paths_containing_libs(all_dirs, ["libirc"])) == set(lib_to_dirs["libirc"])


def test_move_transaction_commit(tmpdir):
    fake_library = tmpdir.mkdir("lib").join("libfoo.so")
    fake_library.write("Just some fake content.")

    with fs.replace_directory_transaction(str(tmpdir.join("lib"))) as backup:
        assert os.path.isdir(backup)
        fake_library = tmpdir.mkdir("lib").join("libfoo.so")
        fake_library.write("Other content.")

    assert not os.path.lexists(backup)
    with open(str(tmpdir.join("lib", "libfoo.so")), "r") as f:
        assert "Other content." == f.read()


def test_move_transaction_rollback(tmpdir):
    fake_library = tmpdir.mkdir("lib").join("libfoo.so")
    fake_library.write("Initial content.")

    try:
        with fs.replace_directory_transaction(str(tmpdir.join("lib"))) as backup:
            assert os.path.isdir(backup)
            fake_library = tmpdir.mkdir("lib").join("libfoo.so")
            fake_library.write("New content.")
            raise RuntimeError("")
    except RuntimeError:
        pass

    assert not os.path.lexists(backup)
    with open(str(tmpdir.join("lib", "libfoo.so")), "r") as f:
        assert "Initial content." == f.read()


@pytest.mark.regression("10601")
@pytest.mark.regression("10603")
def test_recursive_search_of_headers_from_prefix(installation_dir_with_headers):
    # Try to inspect recursively from <prefix> and ensure we don't get
    # subdirectories of the '<prefix>/include' path
    prefix = str(installation_dir_with_headers)
    header_list = fs.find_all_headers(prefix)

    include_dirs = header_list.directories

    if sys.platform == "win32":
        header_list = [header.replace("/", "\\") for header in header_list]
        include_dirs = [dir.replace("/", "\\") for dir in include_dirs]

    # Check that the header files we expect are all listed
    assert os.path.join(prefix, "include", "ex3.h") in header_list
    assert os.path.join(prefix, "include", "boost", "ex3.h") in header_list
    assert os.path.join(prefix, "path", "to", "ex1.h") in header_list
    assert os.path.join(prefix, "path", "to", "subdir", "ex2.h") in header_list

    # Check that when computing directories we exclude <prefix>/include/boost
    assert os.path.join(prefix, "include") in include_dirs
    assert os.path.join(prefix, "include", "boost") not in include_dirs
    assert os.path.join(prefix, "path", "to") in include_dirs
    assert os.path.join(prefix, "path", "to", "subdir") in include_dirs


if sys.platform == "win32":
    dir_list = [
        (["C:/pfx/include/foo.h", "C:/pfx/include/subdir/foo.h"], ["C:/pfx/include"]),
        (["C:/pfx/include/foo.h", "C:/pfx/subdir/foo.h"], ["C:/pfx/include", "C:/pfx/subdir"]),
        (
            ["C:/pfx/include/subdir/foo.h", "C:/pfx/subdir/foo.h"],
            ["C:/pfx/include", "C:/pfx/subdir"],
        ),
    ]
else:
    dir_list = [
        (["/pfx/include/foo.h", "/pfx/include/subdir/foo.h"], ["/pfx/include"]),
        (["/pfx/include/foo.h", "/pfx/subdir/foo.h"], ["/pfx/include", "/pfx/subdir"]),
        (["/pfx/include/subdir/foo.h", "/pfx/subdir/foo.h"], ["/pfx/include", "/pfx/subdir"]),
    ]


@pytest.mark.parametrize("list_of_headers,expected_directories", dir_list)
def test_computation_of_header_directories(list_of_headers, expected_directories):
    hl = fs.HeaderList(list_of_headers)
    assert hl.directories == expected_directories


def test_headers_directory_setter():
    if sys.platform == "win32":
        root = r"C:\pfx\include\subdir"
    else:
        root = "/pfx/include/subdir"
    hl = fs.HeaderList([root + "/foo.h", root + "/bar.h"])

    # Set directories using a list
    hl.directories = [root]
    assert hl.directories == [root]

    # If it's a single directory it's fine to not wrap it into a list
    # when setting the property
    hl.directories = root
    assert hl.directories == [root]

    # Paths are normalized, so it doesn't matter how many backslashes etc.
    # are present in the original directory being used
    if sys.platform == "win32":
        # TODO: Test with \\'s
        hl.directories = "C:/pfx/include//subdir"
    else:
        hl.directories = "/pfx/include//subdir/"
    assert hl.directories == [root]

    # Setting an empty list is allowed and returns an empty list
    hl.directories = []
    assert hl.directories == []

    # Setting directories to None also returns an empty list
    hl.directories = None
    assert hl.directories == []


if sys.platform == "win32":
    # TODO: Test \\s
    paths = [
        (r"C:\user\root", None, (["C:\\", r"C:\user", r"C:\user\root"], "", [])),
        (r"C:\user\root", "C:\\", ([], "C:\\", [r"C:\user", r"C:\user\root"])),
        (r"C:\user\root", r"user", (["C:\\"], r"C:\user", [r"C:\user\root"])),
        (r"C:\user\root", r"root", (["C:\\", r"C:\user"], r"C:\user\root", [])),
        (r"relative\path", None, ([r"relative", r"relative\path"], "", [])),
        (r"relative\path", r"relative", ([], r"relative", [r"relative\path"])),
        (r"relative\path", r"path", ([r"relative"], r"relative\path", [])),
    ]
else:
    paths = [
        ("/tmp/user/root", None, (["/tmp", "/tmp/user", "/tmp/user/root"], "", [])),
        ("/tmp/user/root", "tmp", ([], "/tmp", ["/tmp/user", "/tmp/user/root"])),
        ("/tmp/user/root", "user", (["/tmp"], "/tmp/user", ["/tmp/user/root"])),
        ("/tmp/user/root", "root", (["/tmp", "/tmp/user"], "/tmp/user/root", [])),
        ("relative/path", None, (["relative", "relative/path"], "", [])),
        ("relative/path", "relative", ([], "relative", ["relative/path"])),
        ("relative/path", "path", (["relative"], "relative/path", [])),
    ]


@pytest.mark.parametrize("path,entry,expected", paths)
def test_partition_path(path, entry, expected):
    assert fs.partition_path(path, entry) == expected


if sys.platform == "win32":
    path_list = [
        ("", []),
        (r".\some\sub\dir", [r".\some", r".\some\sub", r".\some\sub\dir"]),
        (r"another\sub\dir", [r"another", r"another\sub", r"another\sub\dir"]),
    ]
else:
    path_list = [
        ("", []),
        ("/tmp/user/dir", ["/tmp", "/tmp/user", "/tmp/user/dir"]),
        ("./some/sub/dir", ["./some", "./some/sub", "./some/sub/dir"]),
        ("another/sub/dir", ["another", "another/sub", "another/sub/dir"]),
    ]


@pytest.mark.parametrize("path,expected", path_list)
def test_prefixes(path, expected):
    assert fs.prefixes(path) == expected


@pytest.mark.regression("7358")
@pytest.mark.parametrize(
    "regex,replacement,filename,keyword_args",
    [
        (r"\<malloc\.h\>", "<stdlib.h>", "x86_cpuid_info.c", {}),
        (r"CDIR", "CURRENT_DIRECTORY", "selfextract.bsx", {"stop_at": "__ARCHIVE_BELOW__"}),
    ],
)
def test_filter_files_with_different_encodings(regex, replacement, filename, tmpdir, keyword_args):
    # All files given as input to this test must satisfy the pre-requisite
    # that the 'replacement' string is not present in the file initially and
    # that there's at least one match for the regex
    original_file = os.path.join(spack.paths.test_path, "data", "filter_file", filename)
    target_file = os.path.join(str(tmpdir), filename)
    shutil.copy(original_file, target_file)
    # This should not raise exceptions
    fs.filter_file(regex, replacement, target_file, **keyword_args)
    # Check the strings have been replaced
    extra_kwargs = {"errors": "surrogateescape"}

    with open(target_file, mode="r", **extra_kwargs) as f:
        assert replacement in f.read()


@pytest.mark.not_on_windows("chgrp isn't used on Windows")
def test_chgrp_dont_set_group_if_already_set(tmpdir, monkeypatch):
    with fs.working_dir(tmpdir):
        os.mkdir("test-dir_chgrp_dont_set_group_if_already_set")

    def _fail(*args, **kwargs):
        raise Exception("chrgrp should not be called")

    class FakeStat(object):
        def __init__(self, gid):
            self.st_gid = gid

    original_stat = os.stat

    def _stat(*args, **kwargs):
        path = args[0]
        if path == "test-dir_chgrp_dont_set_group_if_already_set":
            return FakeStat(gid=1001)
        else:
            # Monkeypatching stat can interfere with post-test cleanup, so for
            # paths that aren't part of the test, we want the original behavior
            # of stat
            return original_stat(*args, **kwargs)

    monkeypatch.setattr(os, "chown", _fail)
    monkeypatch.setattr(os, "lchown", _fail)
    monkeypatch.setattr(os, "stat", _stat)

    with fs.working_dir(tmpdir):
        with pytest.raises(Exception):
            fs.chgrp("test-dir_chgrp_dont_set_group_if_already_set", 1002)
        fs.chgrp("test-dir_chgrp_dont_set_group_if_already_set", 1001)


def test_filter_files_multiple(tmpdir):
    # All files given as input to this test must satisfy the pre-requisite
    # that the 'replacement' string is not present in the file initially and
    # that there's at least one match for the regex
    original_file = os.path.join(spack.paths.test_path, "data", "filter_file", "x86_cpuid_info.c")
    target_file = os.path.join(str(tmpdir), "x86_cpuid_info.c")
    shutil.copy(original_file, target_file)
    # This should not raise exceptions
    fs.filter_file(r"\<malloc.h\>", "<unistd.h>", target_file)
    fs.filter_file(r"\<string.h\>", "<unistd.h>", target_file)
    fs.filter_file(r"\<stdio.h\>", "<unistd.h>", target_file)
    # Check the strings have been replaced
    extra_kwargs = {"errors": "surrogateescape"}

    with open(target_file, mode="r", **extra_kwargs) as f:
        assert "<malloc.h>" not in f.read()
        assert "<string.h>" not in f.read()
        assert "<stdio.h>" not in f.read()


def test_filter_files_start_stop(tmpdir):
    original_file = os.path.join(spack.paths.test_path, "data", "filter_file", "start_stop.txt")
    target_file = os.path.join(str(tmpdir), "start_stop.txt")
    shutil.copy(original_file, target_file)
    # None of the following should happen:
    #   - filtering starts after A is found in the file:
    fs.filter_file("A", "X", target_file, string=True, start_at="B")
    #   - filtering starts exactly when B is found:
    fs.filter_file("B", "X", target_file, string=True, start_at="B")
    #   - filtering stops before D is found:
    fs.filter_file("D", "X", target_file, string=True, stop_at="C")

    assert filecmp.cmp(original_file, target_file)

    # All of the following should happen:
    fs.filter_file("A", "X", target_file, string=True)
    fs.filter_file("B", "X", target_file, string=True, start_at="X", stop_at="C")
    fs.filter_file(r"C|D", "X", target_file, start_at="X", stop_at="E")

    with open(target_file, mode="r") as f:
        assert all("X" == line.strip() for line in f.readlines())


# Each test input is a tuple of entries which prescribe
# - the 'subdirs' to be created from tmpdir
# - the 'files' in that directory
# - what is to be removed
@pytest.mark.parametrize(
    "files_or_dirs",
    [
        # Remove a file over the two that are present
        [{"subdirs": None, "files": ["spack.lock", "spack.yaml"], "remove": ["spack.lock"]}],
        # Remove the entire directory where two files are stored
        [{"subdirs": "myenv", "files": ["spack.lock", "spack.yaml"], "remove": ["myenv"]}],
        # Combine a mix of directories and files
        [
            {"subdirs": None, "files": ["spack.lock", "spack.yaml"], "remove": ["spack.lock"]},
            {"subdirs": "myenv", "files": ["spack.lock", "spack.yaml"], "remove": ["myenv"]},
        ],
        # Multiple subdirectories, remove root
        [
            {"subdirs": "work/myenv1", "files": ["spack.lock", "spack.yaml"], "remove": []},
            {"subdirs": "work/myenv2", "files": ["spack.lock", "spack.yaml"], "remove": ["work"]},
        ],
        # Multiple subdirectories, remove each one
        [
            {
                "subdirs": "work/myenv1",
                "files": ["spack.lock", "spack.yaml"],
                "remove": ["work/myenv1"],
            },
            {
                "subdirs": "work/myenv2",
                "files": ["spack.lock", "spack.yaml"],
                "remove": ["work/myenv2"],
            },
        ],
        # Remove files with the same name in different directories
        [
            {
                "subdirs": "work/myenv1",
                "files": ["spack.lock", "spack.yaml"],
                "remove": ["work/myenv1/spack.lock"],
            },
            {
                "subdirs": "work/myenv2",
                "files": ["spack.lock", "spack.yaml"],
                "remove": ["work/myenv2/spack.lock"],
            },
        ],
        # Remove first the directory, then a file within the directory
        [
            {
                "subdirs": "myenv",
                "files": ["spack.lock", "spack.yaml"],
                "remove": ["myenv", "myenv/spack.lock"],
            }
        ],
        # Remove first a file within a directory, then the directory
        [
            {
                "subdirs": "myenv",
                "files": ["spack.lock", "spack.yaml"],
                "remove": ["myenv/spack.lock", "myenv"],
            }
        ],
    ],
)
@pytest.mark.regression("18441")
def test_safe_remove(files_or_dirs, tmpdir):
    # Create a fake directory structure as prescribed by test input
    to_be_removed, to_be_checked = [], []
    for entry in files_or_dirs:
        # Create relative dir
        subdirs = entry["subdirs"]
        dir = tmpdir if not subdirs else tmpdir.ensure(*subdirs.split("/"), dir=True)

        # Create files in the directory
        files = entry["files"]
        for f in files:
            abspath = str(dir.join(f))
            to_be_checked.append(abspath)
            fs.touch(abspath)

        # List of things to be removed
        for r in entry["remove"]:
            to_be_removed.append(str(tmpdir.join(r)))

    # Assert that files are deleted in the context block,
    # mock a failure by raising an exception
    with pytest.raises(RuntimeError):
        with fs.safe_remove(*to_be_removed):
            for entry in to_be_removed:
                assert not os.path.exists(entry)
            raise RuntimeError("Mock a failure")

    # Assert that files are restored
    for entry in to_be_checked:
        assert os.path.exists(entry)


@pytest.mark.regression("18441")
def test_content_of_files_with_same_name(tmpdir):
    # Create two subdirectories containing a file with the same name,
    # differentiate the files by their content
    file1 = tmpdir.ensure("myenv1/spack.lock")
    file2 = tmpdir.ensure("myenv2/spack.lock")
    file1.write("file1"), file2.write("file2")

    # Use 'safe_remove' to remove the two files
    with pytest.raises(RuntimeError):
        with fs.safe_remove(str(file1), str(file2)):
            raise RuntimeError("Mock a failure")

    # Check both files have been restored correctly
    # and have not been mixed
    assert file1.read().strip() == "file1"
    assert file2.read().strip() == "file2"


def test_keep_modification_time(tmpdir):
    file1 = tmpdir.ensure("file1")
    file2 = tmpdir.ensure("file2")

    # Shift the modification time of the file 10 seconds back:
    mtime1 = file1.mtime() - 10
    file1.setmtime(mtime1)

    with fs.keep_modification_time(file1.strpath, file2.strpath, "non-existing-file"):
        file1.write("file1")
        file2.remove()

    # Assert that the modifications took place the modification time has not
    # changed;
    assert file1.read().strip() == "file1"
    assert not file2.exists()
    assert int(mtime1) == int(file1.mtime())


def test_temporary_dir_context_manager():
    previous_dir = os.path.realpath(os.getcwd())
    with fs.temporary_dir() as tmp_dir:
        assert previous_dir != os.path.realpath(os.getcwd())
        assert os.path.realpath(str(tmp_dir)) == os.path.realpath(os.getcwd())


@pytest.mark.not_on_windows("No shebang on Windows")
def test_is_nonsymlink_exe_with_shebang(tmpdir):
    with tmpdir.as_cwd():
        # Create an executable with shebang.
        with open("executable_script", "wb") as f:
            f.write(b"#!/interpreter")
        os.chmod("executable_script", 0o100775)

        with open("executable_but_not_script", "wb") as f:
            f.write(b"#/not-a-shebang")
        os.chmod("executable_but_not_script", 0o100775)

        with open("not_executable_with_shebang", "wb") as f:
            f.write(b"#!/interpreter")
        os.chmod("not_executable_with_shebang", 0o100664)

        os.symlink("executable_script", "symlink_to_executable_script")

        assert fs.is_nonsymlink_exe_with_shebang("executable_script")
        assert not fs.is_nonsymlink_exe_with_shebang("executable_but_not_script")
        assert not fs.is_nonsymlink_exe_with_shebang("not_executable_with_shebang")
        assert not fs.is_nonsymlink_exe_with_shebang("symlink_to_executable_script")


class RegisterVisitor(fs.BaseDirectoryVisitor):
    """A directory visitor that keeps track of all visited paths"""

    def __init__(self, root, follow_dirs=True, follow_symlink_dirs=True):
        self.files = []
        self.dirs_before = []
        self.symlinked_dirs_before = []
        self.dirs_after = []
        self.symlinked_dirs_after = []

        self.root = root
        self.follow_dirs = follow_dirs
        self.follow_symlink_dirs = follow_symlink_dirs

    def check(self, root, rel_path, depth):
        # verify the (root, rel_path, depth) make sense.
        assert root == self.root and depth + 1 == len(rel_path.split(os.sep))

    def visit_file(self, root, rel_path, depth):
        self.check(root, rel_path, depth)
        self.files.append(rel_path)

    def visit_symlinked_file(self, root, rel_path, depth):
        self.visit_file(root, rel_path, depth)

    def before_visit_dir(self, root, rel_path, depth):
        self.check(root, rel_path, depth)
        self.dirs_before.append(rel_path)
        return self.follow_dirs

    def before_visit_symlinked_dir(self, root, rel_path, depth):
        self.check(root, rel_path, depth)
        self.symlinked_dirs_before.append(rel_path)
        return self.follow_symlink_dirs

    def after_visit_dir(self, root, rel_path, depth):
        self.check(root, rel_path, depth)
        self.dirs_after.append(rel_path)

    def after_visit_symlinked_dir(self, root, rel_path, depth):
        self.check(root, rel_path, depth)
        self.symlinked_dirs_after.append(rel_path)


@pytest.mark.not_on_windows("Requires symlinks")
def test_visit_directory_tree_follow_all(noncyclical_dir_structure):
    root = str(noncyclical_dir_structure)
    visitor = RegisterVisitor(root, follow_dirs=True, follow_symlink_dirs=True)
    fs.visit_directory_tree(root, visitor)
    j = os.path.join
    assert visitor.files == [
        j("a", "file_1"),
        j("a", "to_c", "dangling_link"),
        j("a", "to_c", "file_2"),
        j("a", "to_file_1"),
        j("b", "file_1"),
        j("b", "to_c", "dangling_link"),
        j("b", "to_c", "file_2"),
        j("b", "to_file_1"),
        j("c", "dangling_link"),
        j("c", "file_2"),
        j("file_3"),
    ]
    assert visitor.dirs_before == [j("a"), j("a", "d"), j("b", "d"), j("c")]
    assert visitor.dirs_after == [j("a", "d"), j("a"), j("b", "d"), j("c")]
    assert visitor.symlinked_dirs_before == [j("a", "to_c"), j("b"), j("b", "to_c")]
    assert visitor.symlinked_dirs_after == [j("a", "to_c"), j("b", "to_c"), j("b")]


@pytest.mark.not_on_windows("Requires symlinks")
def test_visit_directory_tree_follow_dirs(noncyclical_dir_structure):
    root = str(noncyclical_dir_structure)
    visitor = RegisterVisitor(root, follow_dirs=True, follow_symlink_dirs=False)
    fs.visit_directory_tree(root, visitor)
    j = os.path.join
    assert visitor.files == [
        j("a", "file_1"),
        j("a", "to_file_1"),
        j("c", "dangling_link"),
        j("c", "file_2"),
        j("file_3"),
    ]
    assert visitor.dirs_before == [j("a"), j("a", "d"), j("c")]
    assert visitor.dirs_after == [j("a", "d"), j("a"), j("c")]
    assert visitor.symlinked_dirs_before == [j("a", "to_c"), j("b")]
    assert not visitor.symlinked_dirs_after


@pytest.mark.not_on_windows("Requires symlinks")
def test_visit_directory_tree_follow_none(noncyclical_dir_structure):
    root = str(noncyclical_dir_structure)
    visitor = RegisterVisitor(root, follow_dirs=False, follow_symlink_dirs=False)
    fs.visit_directory_tree(root, visitor)
    j = os.path.join
    assert visitor.files == [j("file_3")]
    assert visitor.dirs_before == [j("a"), j("c")]
    assert not visitor.dirs_after
    assert visitor.symlinked_dirs_before == [j("b")]
    assert not visitor.symlinked_dirs_after


@pytest.mark.regression("29687")
@pytest.mark.parametrize("initial_mode", [stat.S_IRUSR | stat.S_IXUSR, stat.S_IWGRP])
@pytest.mark.not_on_windows("Windows might change permissions")
def test_remove_linked_tree_doesnt_change_file_permission(tmpdir, initial_mode):
    # Here we test that a failed call to remove_linked_tree, due to passing a file
    # as an argument instead of a directory, doesn't leave the file with different
    # permissions as a side effect of trying to handle the error.
    file_instead_of_dir = tmpdir.ensure("foo")
    file_instead_of_dir.chmod(initial_mode)
    initial_stat = os.stat(str(file_instead_of_dir))
    fs.remove_linked_tree(str(file_instead_of_dir))
    final_stat = os.stat(str(file_instead_of_dir))
    assert final_stat == initial_stat


def test_filesummary(tmpdir):
    p = str(tmpdir.join("xyz"))
    with open(p, "wb") as f:
        f.write(b"abcdefghijklmnopqrstuvwxyz")

    assert fs.filesummary(p, print_bytes=8) == (26, b"abcdefgh...stuvwxyz")
    assert fs.filesummary(p, print_bytes=13) == (26, b"abcdefghijklmnopqrstuvwxyz")
    assert fs.filesummary(p, print_bytes=100) == (26, b"abcdefghijklmnopqrstuvwxyz")


@pytest.mark.parametrize("bfs_depth", [1, 2, 10])
def test_find_first_file(tmpdir, bfs_depth):
    # Create a structure: a/a/a/{file1,file2}, b/a, c/a, d/{a,file1}
    tmpdir.join("a", "a", "a").ensure(dir=True)
    tmpdir.join("b", "a").ensure(dir=True)
    tmpdir.join("c", "a").ensure(dir=True)
    tmpdir.join("d", "a").ensure(dir=True)
    tmpdir.join("e").ensure(dir=True)

    fs.touch(tmpdir.join("a", "a", "a", "file1"))
    fs.touch(tmpdir.join("a", "a", "a", "file2"))
    fs.touch(tmpdir.join("d", "file1"))

    root = str(tmpdir)

    # Iterative deepening: should find low-depth file1.
    assert os.path.samefile(
        fs.find_first(root, "file*", bfs_depth=bfs_depth), os.path.join(root, "d", "file1")
    )

    assert fs.find_first(root, "nonexisting", bfs_depth=bfs_depth) is None

    assert os.path.samefile(
        fs.find_first(root, ["nonexisting", "file2"], bfs_depth=bfs_depth),
        os.path.join(root, "a", "a", "a", "file2"),
    )

    # Should find first dir
    assert os.path.samefile(fs.find_first(root, "a", bfs_depth=bfs_depth), os.path.join(root, "a"))


def test_rename_dest_exists(tmpdir):
    @contextmanager
    def setup_test_files():
        a = tmpdir.join("a", "file1")
        b = tmpdir.join("a", "file2")
        fs.touchp(a)
        fs.touchp(b)
        with open(a, "w") as oa, open(b, "w") as ob:
            oa.write("I am A")
            ob.write("I am B")
        yield a, b
        shutil.rmtree(tmpdir.join("a"))

    @contextmanager
    def setup_test_dirs():
        a = tmpdir.join("d", "a")
        b = tmpdir.join("d", "b")
        fs.mkdirp(a)
        fs.mkdirp(b)
        yield a, b
        shutil.rmtree(tmpdir.join("d"))

    # test standard behavior of rename
    # smoke test
    with setup_test_files() as files:
        a, b = files
        fs.rename(str(a), str(b))
        assert os.path.exists(b)
        assert not os.path.exists(a)
        with open(b, "r") as ob:
            content = ob.read()
        assert content == "I am A"

    # test relatitve paths
    # another sanity check/smoke test
    with setup_test_files() as files:
        a, b = files
        with fs.working_dir(str(tmpdir)):
            fs.rename(os.path.join("a", "file1"), os.path.join("a", "file2"))
            assert os.path.exists(b)
            assert not os.path.exists(a)
            with open(b, "r") as ob:
                content = ob.read()
            assert content == "I am A"

    # Test rename symlinks to same file
    c = tmpdir.join("a", "file1")
    a = tmpdir.join("a", "link1")
    b = tmpdir.join("a", "link2")
    fs.touchp(c)
    symlink(c, a)
    symlink(c, b)
    fs.rename(str(a), str(b))
    assert os.path.exists(b)
    assert not os.path.exists(a)
    assert os.path.realpath(b) == c
    shutil.rmtree(tmpdir.join("a"))

    # test rename onto itself
    a = tmpdir.join("a", "file1")
    b = a
    fs.touchp(a)
    with open(a, "w") as oa:
        oa.write("I am A")
    fs.rename(str(a), str(b))
    # check a, or b, doesn't matter, same file
    assert os.path.exists(a)
    # ensure original file was not duplicated
    assert len(os.listdir(tmpdir.join("a"))) == 1
    with open(a, "r") as oa:
        assert oa.read()
    shutil.rmtree(tmpdir.join("a"))

    # test rename onto symlink
    # to directory from symlink to directory
    # (this is something spack does when regenerating views)
    with setup_test_dirs() as dirs:
        a, b = dirs
        link1 = tmpdir.join("f", "link1")
        link2 = tmpdir.join("f", "link2")
        fs.mkdirp(tmpdir.join("f"))
        symlink(a, link1)
        symlink(b, link2)
        fs.rename(str(link1), str(link2))
        assert os.path.exists(link2)
        assert os.path.realpath(link2) == a
        shutil.rmtree(tmpdir.join("f"))


@pytest.mark.only_windows("Test is for Windows specific behavior")
def test_windows_sfn(tmpdir):
    # first check some standard Windows locations
    # we know require sfn names
    # this is basically a smoke test
    # ensure spaces are replaced + path abbreviated
    assert fs.windows_sfn("C:\\Program Files (x86)") == "C:\\PROGRA~2"
    # ensure path without spaces is still properly shortened
    assert fs.windows_sfn("C:\\ProgramData") == "C:\\PROGRA~3"

    # test user created paths
    # ensure longer path with spaces is properly abbreviated
    a = tmpdir.join("d", "this is a test", "a", "still test")
    # ensure longer path is properly abbreviated
    b = tmpdir.join("d", "long_path_with_no_spaces", "more_long_path")
    # ensure path not in need of abbreviation is properly roundtripped
    c = tmpdir.join("d", "this", "is", "short")
    # ensure paths that are the same in the first six letters
    # are incremented post tilde
    d = tmpdir.join("d", "longerpath1")
    e = tmpdir.join("d", "longerpath2")
    fs.mkdirp(a)
    fs.mkdirp(b)
    fs.mkdirp(c)
    fs.mkdirp(d)
    fs.mkdirp(e)
    # check only for path of path we can control,
    # pytest prefix may or may not be mangled by windows_sfn
    # based on user/pytest config
    assert "d\\THISIS~1\\a\\STILLT~1" in fs.windows_sfn(a)
    assert "d\\LONG_P~1\\MORE_L~1" in fs.windows_sfn(b)
    assert "d\\this\\is\\short" in fs.windows_sfn(c)
    assert "d\\LONGER~1" in fs.windows_sfn(d)
    assert "d\\LONGER~2" in fs.windows_sfn(e)
    shutil.rmtree(tmpdir.join("d"))
