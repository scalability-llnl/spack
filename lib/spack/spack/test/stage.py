# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test that the Stage class works correctly."""
import collections
import errno
import getpass
import os
import shutil
import stat
import sys

import pytest

from llnl.util.filesystem import getuid, mkdirp, partition_path, touch, working_dir
from llnl.util.symlink import readlink

import spack.config
import spack.error
import spack.fetch_strategy
import spack.stage
import spack.util.executable
import spack.util.url as url_util
from spack.resource import Resource
from spack.stage import DevelopStage, ResourceStage, Stage, StageComposite
from spack.util.path import canonicalize_path

# The following values are used for common fetch and stage mocking fixtures:
_archive_base = "test-files"
_archive_fn = "%s.tar.gz" % _archive_base
_extra_fn = "extra.sh"
_hidden_fn = ".hidden"
_readme_fn = "README.txt"

_extra_contents = "#!/bin/sh\n"
_hidden_contents = ""
_readme_contents = "hello world!\n"

# TODO: Replace the following with an enum once guarantee supported (or
# include enum34 for python versions < 3.4.
_include_readme = 1
_include_hidden = 2
_include_extra = 3


# Mock fetch directories are expected to appear as follows:
#
# TMPDIR/
#     _archive_fn     archive_url = file:///path/to/_archive_fn
#
# Mock expanded stage directories are expected to have one of two forms,
# depending on how the tarball expands.  Non-exploding tarballs are expected
# to have the following structure:
#
# TMPDIR/                 temp stage dir
#     spack-src/          well-known stage source directory
#         _readme_fn      Optional test_readme (contains _readme_contents)
#     _hidden_fn          Optional hidden file (contains _hidden_contents)
#     _archive_fn         archive_url = file:///path/to/_archive_fn
#
# while exploding tarball directories are expected to be structured as follows:
#
# TMPDIR/                 temp stage dir
#     spack-src/          well-known stage source directory
#         archive_name/   archive dir
#             _readme_fn  test_readme (contains _readme_contents)
#         _extra_fn       test_extra file (contains _extra_contents)
#     _archive_fn         archive_url = file:///path/to/_archive_fn
#


@pytest.fixture
def clear_stage_root(monkeypatch):
    """Ensure spack.stage._stage_root is not set at test start."""
    monkeypatch.setattr(spack.stage, "_stage_root", None)
    yield


def check_expand_archive(stage, stage_name, expected_file_list):
    """
    Ensure the expanded archive directory contains the expected structure and
    files as described in the module-level comments above.
    """
    stage_path = get_stage_path(stage, stage_name)
    archive_dir = spack.stage._source_path_subdir

    stage_contents = os.listdir(stage_path)
    assert _archive_fn in stage_contents
    assert archive_dir in stage_contents

    source_path = os.path.join(stage_path, archive_dir)
    assert source_path == stage.source_path

    source_contents = os.listdir(source_path)

    for _include in expected_file_list:
        if _include == _include_hidden:
            # The hidden file represent the HFS metadata associated with Mac
            # OS X tar files so is expected to be in the same directory as
            # the archive directory.
            assert _hidden_fn in stage_contents

            fn = os.path.join(stage_path, _hidden_fn)
            contents = _hidden_contents

        elif _include == _include_readme:
            # The standard README.txt file will be in the source directory if
            # the tarball didn't explode; otherwise, it will be in the
            # original archive subdirectory of it.
            if _archive_base in source_contents:
                fn = os.path.join(source_path, _archive_base, _readme_fn)
            else:
                fn = os.path.join(source_path, _readme_fn)
            contents = _readme_contents

        elif _include == _include_extra:
            assert _extra_fn in source_contents

            fn = os.path.join(source_path, _extra_fn)
            contents = _extra_contents

        else:
            assert False

        assert os.path.isfile(fn)
        with open(fn) as _file:
            _file.read() == contents


def check_fetch(stage, stage_name):
    """
    Ensure the fetch resulted in a properly placed archive file as described in
    the module-level comments.
    """
    stage_path = get_stage_path(stage, stage_name)
    assert _archive_fn in os.listdir(stage_path)
    assert os.path.join(stage_path, _archive_fn) == stage.fetcher.archive_file


def check_destroy(stage, stage_name):
    """Figure out whether a stage was destroyed correctly."""
    stage_path = get_stage_path(stage, stage_name)

    # check that the stage dir/link was removed.
    assert not os.path.exists(stage_path)

    # tmp stage needs to remove tmp dir too.
    target = os.path.realpath(stage_path)
    assert not os.path.exists(target)


def check_setup(stage, stage_name, archive):
    """Figure out whether a stage was set up correctly."""
    stage_path = get_stage_path(stage, stage_name)

    # Ensure stage was created in the spack stage directory
    assert os.path.isdir(stage_path)

    # Make sure it points to a valid directory
    target = os.path.realpath(stage_path)
    assert os.path.isdir(target)
    assert not os.path.islink(target)

    # Make sure the directory is in the place we asked it to
    # be (see setUp, tearDown, and use_tmp)
    assert target.startswith(str(archive.stage_path))


def get_stage_path(stage, stage_name):
    """Figure out where a stage should be living. This depends on
    whether it's named.
    """
    stage_path = spack.stage.get_stage_root()
    if stage_name is not None:
        # If it is a named stage, we know where the stage should be
        return os.path.join(stage_path, stage_name)
    else:
        # If it's unnamed, ensure that we ran mkdtemp in the right spot.
        assert stage.path is not None
        assert stage.path.startswith(stage_path)
        return stage.path


# TODO: Revisit use of the following fixture (and potentially leveraging
#       the `mock_stage` path in `mock_stage_archive`) per discussions in
#       #12857.  See also #13065.
@pytest.fixture
def tmp_build_stage_dir(tmpdir, clear_stage_root):
    """Use a temporary test directory for the stage root."""
    test_path = str(tmpdir.join("stage"))
    with spack.config.override("config:build_stage", test_path):
        yield tmpdir, spack.stage.get_stage_root()

    shutil.rmtree(test_path)


@pytest.fixture
def mock_stage_archive(tmp_build_stage_dir):
    """Create the directories and files for the staged mock archive."""

    # Mock up a stage area that looks like this:
    #
    # tmpdir/                test_files_dir
    #     stage/             test_stage_path (where stage should be)
    #     <_archive_base>/   archive_dir_path
    #         <_readme_fn>   Optional test_readme (contains _readme_contents)
    #     <_extra_fn>        Optional extra file (contains _extra_contents)
    #     <_hidden_fn>       Optional hidden file (contains _hidden_contents)
    #     <_archive_fn>      archive_url = file:///path/to/<_archive_fn>
    #
    def create_stage_archive(expected_file_list=[_include_readme]):
        tmpdir, test_stage_path = tmp_build_stage_dir
        mkdirp(test_stage_path)

        # Create the archive directory and associated file
        archive_dir = tmpdir.join(_archive_base)
        archive = tmpdir.join(_archive_fn)
        archive_url = url_util.path_to_file_url(str(archive))
        archive_dir.ensure(dir=True)

        # Create the optional files as requested and make sure expanded
        # archive peers are included.
        tar_args = ["czf", str(_archive_fn), _archive_base]
        for _include in expected_file_list:
            if _include == _include_hidden:
                # The hidden file case stands in for the way Mac OS X tar files
                # represent HFS metadata.  Locate in the same directory as the
                # archive file.
                tar_args.append(_hidden_fn)
                fn, contents = (tmpdir.join(_hidden_fn), _hidden_contents)

            elif _include == _include_readme:
                # The usual README.txt file is contained in the archive dir.
                fn, contents = (archive_dir.join(_readme_fn), _readme_contents)

            elif _include == _include_extra:
                # The extra file stands in for exploding tar files so needs
                # to be in the same directory as the archive file.
                tar_args.append(_extra_fn)
                fn, contents = (tmpdir.join(_extra_fn), _extra_contents)
            else:
                break

            fn.write(contents)

        # Create the archive file
        with tmpdir.as_cwd():
            tar = spack.util.executable.which("tar", required=True)
            tar(*tar_args)

        Archive = collections.namedtuple("Archive", ["url", "tmpdir", "stage_path", "archive_dir"])
        return Archive(
            url=archive_url, tmpdir=tmpdir, stage_path=test_stage_path, archive_dir=archive_dir
        )

    return create_stage_archive


@pytest.fixture
def mock_noexpand_resource(tmpdir):
    """Set up a non-expandable resource in the tmpdir prior to staging."""
    test_resource = tmpdir.join("resource-no-expand.sh")
    test_resource.write("an example resource")
    return str(test_resource)


@pytest.fixture
def mock_expand_resource(tmpdir):
    """Sets up an expandable resource in tmpdir prior to staging."""
    # Mock up an expandable resource:
    #
    # tmpdir/                    test_files_dir
    #     resource-expand/       resource source dir
    #         resource-file.txt  resource contents (contains 'test content')
    #     resource.tar.gz        archive of resource content
    #
    subdir = "resource-expand"
    resource_dir = tmpdir.join(subdir)
    resource_dir.ensure(dir=True)

    archive_name = "resource.tar.gz"
    archive = tmpdir.join(archive_name)
    archive_url = url_util.path_to_file_url(str(archive))

    filename = "resource-file.txt"
    test_file = resource_dir.join(filename)
    test_file.write("test content\n")

    with tmpdir.as_cwd():
        tar = spack.util.executable.which("tar", required=True)
        tar("czf", str(archive_name), subdir)

    MockResource = collections.namedtuple("MockResource", ["url", "files"])

    return MockResource(archive_url, [filename])


@pytest.fixture
def composite_stage_with_expanding_resource(mock_stage_archive, mock_expand_resource):
    """Sets up a composite for expanding resources prior to staging."""
    composite_stage = StageComposite()
    archive = mock_stage_archive()
    root_stage = Stage(archive.url)
    composite_stage.append(root_stage)

    test_resource_fetcher = spack.fetch_strategy.from_kwargs(url=mock_expand_resource.url)
    # Specify that the resource files are to be placed in the 'resource-dir'
    # directory
    test_resource = Resource("test_resource", test_resource_fetcher, "", "resource-dir")
    resource_stage = ResourceStage(test_resource_fetcher, root_stage, test_resource)
    composite_stage.append(resource_stage)
    return composite_stage, root_stage, resource_stage, mock_expand_resource


@pytest.fixture
def failing_search_fn():
    """Returns a search function that fails! Always!"""

    def _mock():
        raise Exception("This should not have been called")

    return _mock


class FailingFetchStrategy(spack.fetch_strategy.FetchStrategy):
    def fetch(self):
        raise spack.fetch_strategy.FailedDownloadError(
            "<non-existent URL>", "This implementation of FetchStrategy always fails"
        )


@pytest.fixture
def search_fn():
    """Returns a search function that always succeeds."""

    class _Mock:
        performed_search = False

        def __call__(self):
            self.performed_search = True
            return []

    return _Mock()


def check_stage_dir_perms(prefix, path):
    """Check the stage directory perms to ensure match expectations."""
    # Ensure the path's subdirectories -- to `$user` -- have their parent's
    # perms while those from `$user` on are owned and restricted to the
    # user.
    assert path.startswith(prefix)

    user = getpass.getuser()
    prefix_status = os.stat(prefix)
    uid = getuid()

    # Obtain lists of ancestor and descendant paths of the $user node, if any.
    #
    # Skip processing prefix ancestors since no guarantee they will be in the
    # required group (e.g. $TEMPDIR on HPC machines).
    skip = prefix if prefix.endswith(os.sep) else prefix + os.sep
    group_paths, user_node, user_paths = partition_path(path.replace(skip, ""), user)

    for p in group_paths:
        p_status = os.stat(os.path.join(prefix, p))
        assert p_status.st_gid == prefix_status.st_gid
        assert p_status.st_mode == prefix_status.st_mode

    # Add the path ending with the $user node to the user paths to ensure paths
    # from $user (on down) meet the ownership and permission requirements.
    if user_node:
        user_paths.insert(0, user_node)

    for p in user_paths:
        p_status = os.stat(os.path.join(prefix, p))
        assert uid == p_status.st_uid
        assert p_status.st_mode & stat.S_IRWXU == stat.S_IRWXU


@pytest.mark.usefixtures("mock_packages")
class TestStage:
    stage_name = "spack-test-stage"

    def test_setup_and_destroy_name_with_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            check_setup(stage, self.stage_name, archive)
        check_destroy(stage, self.stage_name)

    def test_setup_and_destroy_name_without_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            check_setup(stage, self.stage_name, archive)
        check_destroy(stage, self.stage_name)

    def test_setup_and_destroy_no_name_with_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url) as stage:
            check_setup(stage, None, archive)
        check_destroy(stage, None)

    def test_noexpand_stage_file(self, mock_stage_archive, mock_noexpand_resource):
        """When creating a stage with a nonexpanding URL, the 'archive_file'
        property of the stage should refer to the path of that file.
        """
        test_noexpand_fetcher = spack.fetch_strategy.from_kwargs(
            url=url_util.path_to_file_url(mock_noexpand_resource), expand=False
        )
        with Stage(test_noexpand_fetcher) as stage:
            stage.fetch()
            stage.expand_archive()
            assert os.path.exists(stage.archive_file)

    @pytest.mark.disable_clean_stage_check
    def test_composite_stage_with_noexpand_resource(
        self, mock_stage_archive, mock_noexpand_resource
    ):
        archive = mock_stage_archive()
        composite_stage = StageComposite()
        root_stage = Stage(archive.url)
        composite_stage.append(root_stage)

        resource_dst_name = "resource-dst-name.sh"
        test_resource_fetcher = spack.fetch_strategy.from_kwargs(
            url=url_util.path_to_file_url(mock_noexpand_resource), expand=False
        )
        test_resource = Resource("test_resource", test_resource_fetcher, resource_dst_name, None)
        resource_stage = ResourceStage(test_resource_fetcher, root_stage, test_resource)
        composite_stage.append(resource_stage)

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.expand_archive()
        assert composite_stage.expanded  # Archive is expanded

        assert os.path.exists(os.path.join(composite_stage.source_path, resource_dst_name))

    @pytest.mark.disable_clean_stage_check
    def test_composite_stage_with_expand_resource(self, composite_stage_with_expanding_resource):
        (composite_stage, root_stage, resource_stage, mock_resource) = (
            composite_stage_with_expanding_resource
        )

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.expand_archive()

        assert composite_stage.expanded  # Archive is expanded

        for fname in mock_resource.files:
            file_path = os.path.join(root_stage.source_path, "resource-dir", fname)
            assert os.path.exists(file_path)

        # Perform a little cleanup
        shutil.rmtree(root_stage.path)

    @pytest.mark.disable_clean_stage_check
    def test_composite_stage_with_expand_resource_default_placement(
        self, composite_stage_with_expanding_resource
    ):
        """For a resource which refers to a compressed archive which expands
        to a directory, check that by default the resource is placed in
        the source_path of the root stage with the name of the decompressed
        directory.
        """

        (composite_stage, root_stage, resource_stage, mock_resource) = (
            composite_stage_with_expanding_resource
        )

        resource_stage.resource.placement = None

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.expand_archive()

        for fname in mock_resource.files:
            file_path = os.path.join(root_stage.source_path, "resource-expand", fname)
            assert os.path.exists(file_path)

        # Perform a little cleanup
        shutil.rmtree(root_stage.path)

    def test_setup_and_destroy_no_name_without_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url) as stage:
            check_setup(stage, None, archive)
        check_destroy(stage, None)

    @pytest.mark.parametrize("debug", [False, True])
    def test_fetch(self, mock_stage_archive, debug):
        archive = mock_stage_archive()
        with spack.config.override("config:debug", debug):
            with Stage(archive.url, name=self.stage_name) as stage:
                stage.fetch()
                check_setup(stage, self.stage_name, archive)
                check_fetch(stage, self.stage_name)
            check_destroy(stage, self.stage_name)

    def test_no_search_if_default_succeeds(self, mock_stage_archive, failing_search_fn):
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, search_fn=failing_search_fn)
        with stage:
            stage.fetch()
        check_destroy(stage, self.stage_name)

    def test_no_search_mirror_only(self, failing_search_fn):
        stage = Stage(FailingFetchStrategy(), name=self.stage_name, search_fn=failing_search_fn)
        with stage:
            try:
                stage.fetch(mirror_only=True)
            except spack.error.FetchError:
                pass
        check_destroy(stage, self.stage_name)

    @pytest.mark.parametrize(
        "err_msg,expected",
        [
            ("Fetch from fetch.test.com", "Fetch from fetch.test.com"),
            (None, "All fetchers failed"),
        ],
    )
    def test_search_if_default_fails(self, search_fn, err_msg, expected):
        stage = Stage(FailingFetchStrategy(), name=self.stage_name, search_fn=search_fn)

        with stage:
            with pytest.raises(spack.error.FetchError, match=expected):
                stage.fetch(mirror_only=False, err_msg=err_msg)

        check_destroy(stage, self.stage_name)
        assert search_fn.performed_search

    def test_ensure_one_stage_entry(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            stage_path = get_stage_path(stage, self.stage_name)
            spack.fetch_strategy._ensure_one_stage_entry(stage_path)
        check_destroy(stage, self.stage_name)

    @pytest.mark.parametrize(
        "expected_file_list",
        [
            [],
            [_include_readme],
            [_include_extra, _include_readme],
            [_include_hidden, _include_readme],
        ],
    )
    def test_expand_archive(self, expected_file_list, mock_stage_archive):
        archive = mock_stage_archive(expected_file_list)
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            check_setup(stage, self.stage_name, archive)
            check_fetch(stage, self.stage_name)
            stage.expand_archive()
            check_expand_archive(stage, self.stage_name, expected_file_list)
        check_destroy(stage, self.stage_name)

    def test_expand_archive_extra_expand(self, mock_stage_archive):
        """Test expand with an extra expand after expand (i.e., no-op)."""
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            check_setup(stage, self.stage_name, archive)
            check_fetch(stage, self.stage_name)
            stage.expand_archive()
            stage.fetcher.expand()
            check_expand_archive(stage, self.stage_name, [_include_readme])
        check_destroy(stage, self.stage_name)

    def test_restage(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            stage.expand_archive()

            with working_dir(stage.source_path):
                check_expand_archive(stage, self.stage_name, [_include_readme])

                # Try to make a file in the old archive dir
                with open("foobar", "w") as file:
                    file.write("this file is to be destroyed.")

            assert "foobar" in os.listdir(stage.source_path)

            # Make sure the file is not there after restage.
            stage.restage()
            check_fetch(stage, self.stage_name)
            assert "foobar" not in os.listdir(stage.source_path)
        check_destroy(stage, self.stage_name)

    def test_no_keep_without_exceptions(self, mock_stage_archive):
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=False)
        with stage:
            pass
        check_destroy(stage, self.stage_name)

    @pytest.mark.disable_clean_stage_check
    def test_keep_without_exceptions(self, mock_stage_archive):
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=True)
        with stage:
            pass
        path = get_stage_path(stage, self.stage_name)
        assert os.path.isdir(path)

    @pytest.mark.disable_clean_stage_check
    def test_no_keep_with_exceptions(self, mock_stage_archive):
        class ThisMustFailHere(Exception):
            pass

        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=False)
        try:
            with stage:
                raise ThisMustFailHere()

        except ThisMustFailHere:
            path = get_stage_path(stage, self.stage_name)
            assert os.path.isdir(path)

    @pytest.mark.disable_clean_stage_check
    def test_keep_exceptions(self, mock_stage_archive):
        class ThisMustFailHere(Exception):
            pass

        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=True)
        try:
            with stage:
                raise ThisMustFailHere()

        except ThisMustFailHere:
            path = get_stage_path(stage, self.stage_name)
            assert os.path.isdir(path)

    def test_source_path_available(self, mock_stage_archive):
        """Ensure source path available but does not exist on instantiation."""
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name)

        source_path = stage.source_path
        assert source_path
        assert source_path.endswith(spack.stage._source_path_subdir)
        assert not os.path.exists(source_path)

    @pytest.mark.not_on_windows("Windows file permission erroring is not yet supported")
    @pytest.mark.skipif(getuid() == 0, reason="user is root")
    def test_first_accessible_path(self, tmpdir):
        """Test _first_accessible_path names."""
        spack_dir = tmpdir.join("paths")
        name = str(spack_dir)
        files = [os.path.join(os.path.sep, "no", "such", "path"), name]

        # Ensure the tmpdir path is returned since the user should have access
        path = spack.stage._first_accessible_path(files)
        assert path == name
        assert os.path.isdir(path)
        check_stage_dir_perms(str(tmpdir), path)

        # Ensure an existing path is returned
        spack_subdir = spack_dir.join("existing").ensure(dir=True)
        subdir = str(spack_subdir)
        path = spack.stage._first_accessible_path([subdir])
        assert path == subdir

        # Ensure a path with a `$user` node has the right permissions
        # for its subdirectories.
        user = getpass.getuser()
        user_dir = spack_dir.join(user, "has", "paths")
        user_path = str(user_dir)
        path = spack.stage._first_accessible_path([user_path])
        assert path == user_path
        check_stage_dir_perms(str(tmpdir), path)

        # Cleanup
        shutil.rmtree(str(name))

    def test_create_stage_root(self, tmpdir, no_path_access):
        """Test create_stage_root permissions."""
        test_dir = tmpdir.join("path")
        test_path = str(test_dir)

        try:
            if getpass.getuser() in str(test_path).split(os.sep):
                # Simply ensure directory created if tmpdir includes user
                spack.stage.create_stage_root(test_path)
                assert os.path.exists(test_path)

                p_stat = os.stat(test_path)
                assert p_stat.st_mode & stat.S_IRWXU == stat.S_IRWXU
            else:
                # Ensure an OS Error is raised on created, non-user directory
                with pytest.raises(OSError) as exc_info:
                    spack.stage.create_stage_root(test_path)

                assert exc_info.value.errno == errno.EACCES
        finally:
            try:
                shutil.rmtree(test_path)
            except OSError:
                pass

    def test_resolve_paths(self):
        """Test _resolve_paths."""
        assert spack.stage._resolve_paths([]) == []

        # resolved path without user appends user
        paths = [os.path.join(os.path.sep, "a", "b", "c")]
        can_paths = [paths[0]]
        user = getpass.getuser()

        if sys.platform != "win32":
            can_paths = [os.path.join(paths[0], user)]
        assert spack.stage._resolve_paths(paths) == can_paths

        # resolved path with node including user does not append user
        paths = [os.path.join(os.path.sep, "spack-{0}".format(user), "stage")]
        assert spack.stage._resolve_paths(paths) == paths

        tempdir = "$tempdir"
        can_tempdir = canonicalize_path(tempdir)
        user = getpass.getuser()
        temp_has_user = user in can_tempdir.split(os.sep)
        paths = [
            os.path.join(tempdir, "stage"),
            os.path.join(tempdir, "$user"),
            os.path.join(tempdir, "$user", "$user"),
            os.path.join(tempdir, "$user", "stage", "$user"),
        ]

        res_paths = [canonicalize_path(p) for p in paths]
        if temp_has_user:
            res_paths[1] = can_tempdir
            res_paths[2] = os.path.join(can_tempdir, user)
            res_paths[3] = os.path.join(can_tempdir, "stage", user)
        elif sys.platform != "win32":
            res_paths[0] = os.path.join(res_paths[0], user)

        assert spack.stage._resolve_paths(paths) == res_paths

    @pytest.mark.not_on_windows("Windows file permission erroring is not yet supported")
    @pytest.mark.skipif(getuid() == 0, reason="user is root")
    def test_get_stage_root_bad_path(self, clear_stage_root):
        """Ensure an invalid stage path root raises a StageError."""
        with spack.config.override("config:build_stage", "/no/such/path"):
            with pytest.raises(spack.stage.StageError, match="No accessible stage paths in"):
                spack.stage.get_stage_root()

        # Make sure the cached stage path values are unchanged.
        assert spack.stage._stage_root is None

    @pytest.mark.parametrize(
        "path,purged",
        [
            ("spack-stage-1234567890abcdef1234567890abcdef", True),
            ("spack-stage-anything-goes-here", True),
            ("stage-spack", False),
        ],
    )
    def test_stage_purge(self, tmpdir, clear_stage_root, path, purged):
        """Test purging of stage directories."""
        stage_dir = tmpdir.join("stage")
        stage_path = str(stage_dir)

        test_dir = stage_dir.join(path)
        test_dir.ensure(dir=True)
        test_path = str(test_dir)

        with spack.config.override("config:build_stage", stage_path):
            stage_root = spack.stage.get_stage_root()
            assert stage_path == stage_root

            spack.stage.purge()

            if purged:
                assert not os.path.exists(test_path)
            else:
                assert os.path.exists(test_path)
                shutil.rmtree(test_path)

    def test_stage_constructor_no_fetcher(self):
        """Ensure Stage constructor with no URL or fetch strategy fails."""
        with pytest.raises(ValueError):
            with Stage(None):
                pass

    def test_stage_constructor_with_path(self, tmpdir):
        """Ensure Stage constructor with a path uses it."""
        testpath = str(tmpdir)
        with Stage("file:///does-not-exist", path=testpath) as stage:
            assert stage.path == testpath


def _create_files_from_tree(base, tree):
    for name, content in tree.items():
        sub_base = os.path.join(base, name)
        if isinstance(content, dict):
            os.mkdir(sub_base)
            _create_files_from_tree(sub_base, content)
        else:
            assert (content is None) or (isinstance(content, str))
            with open(sub_base, "w") as f:
                if content:
                    f.write(content)


def _create_tree_from_dir_recursive(path):
    if os.path.islink(path):
        return readlink(path)
    elif os.path.isdir(path):
        tree = {}
        for name in os.listdir(path):
            sub_path = os.path.join(path, name)
            tree[name] = _create_tree_from_dir_recursive(sub_path)
        return tree
    else:
        with open(path, "r") as f:
            content = f.read() or None
        return content


@pytest.fixture
def develop_path(tmpdir):
    dir_structure = {"a1": {"b1": None, "b2": "b1content"}, "a2": None}
    srcdir = str(tmpdir.join("test-src"))
    os.mkdir(srcdir)
    _create_files_from_tree(srcdir, dir_structure)
    yield dir_structure, srcdir


class TestDevelopStage:
    def test_sanity_check_develop_path(self, develop_path):
        _, srcdir = develop_path
        with open(os.path.join(srcdir, "a1", "b2")) as f:
            assert f.read() == "b1content"

        assert os.path.exists(os.path.join(srcdir, "a2"))

    def test_develop_stage(self, develop_path, tmp_build_stage_dir):
        """Check that (a) develop stages update the given
        `dev_path` with a symlink that points to the stage dir and
        (b) that destroying the stage does not destroy `dev_path`
        """
        devtree, srcdir = develop_path
        stage = DevelopStage("test-stage", srcdir, reference_link="link-to-stage")
        assert not os.path.exists(stage.reference_link)
        stage.create()
        assert os.path.exists(stage.reference_link)
        srctree1 = _create_tree_from_dir_recursive(stage.source_path)
        assert os.path.samefile(srctree1["link-to-stage"], stage.path)
        del srctree1["link-to-stage"]
        assert srctree1 == devtree

        stage.destroy()
        assert not os.path.exists(stage.reference_link)
        # Make sure destroying the stage doesn't change anything
        # about the path
        assert not os.path.exists(stage.path)
        srctree2 = _create_tree_from_dir_recursive(srcdir)
        assert srctree2 == devtree


def test_stage_create_replace_path(tmp_build_stage_dir):
    """Ensure stage creation replaces a non-directory path."""
    _, test_stage_path = tmp_build_stage_dir
    mkdirp(test_stage_path)

    nondir = os.path.join(test_stage_path, "afile")
    touch(nondir)
    path = url_util.path_to_file_url(str(nondir))

    stage = Stage(path, name="afile")
    stage.create()

    # Ensure the stage path is "converted" to a directory
    assert os.path.isdir(nondir)


def test_cannot_access(capsys):
    """Ensure can_access dies with the expected error."""
    with pytest.raises(SystemExit):
        # It's far more portable to use a non-existent filename.
        spack.stage.ensure_access("/no/such/file")

    captured = capsys.readouterr()
    assert "Insufficient permissions" in str(captured)


def test_override_keep_in_composite_stage():
    stage_1 = Stage("file:///does-not-exist", keep=True)
    stage_2 = Stage("file:///does-not-exist", keep=False)
    stage_3 = Stage("file:///does-not-exist", keep=True)
    stages = spack.stage.StageComposite.from_iterable((stage_1, stage_2, stage_3))

    # The getter for the composite stage just returns the value of the first stage
    # its just there so we have a setter too.
    assert stages.keep
    assert stage_1.keep
    assert not stage_2.keep
    assert stage_3.keep

    # This should override all stages
    stages.keep = False
    assert not stages.keep
    assert not stage_1.keep
    assert not stage_2.keep
    assert not stage_3.keep
