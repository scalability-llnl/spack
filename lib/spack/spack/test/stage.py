##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Test that the Stage class works correctly."""
import os
import collections

import pytest

from llnl.util.filesystem import working_dir

import spack.paths
import spack.stage
import spack.util.executable

from spack.resource import Resource
from spack.stage import Stage, StageComposite, ResourceStage


def check_setup_source(stage, stage_name, mock_archive):
    stage_path = get_stage_path(stage, stage_name)
    archive_name = 'test-files.tar.gz'
    archive_dir = 'test-files'
    assert archive_name in os.listdir(stage_path)
    assert archive_dir in os.listdir(stage_path)

    assert os.path.join(stage_path, archive_dir) == stage.source_path

    readme = os.path.join(stage_path, archive_dir, 'README.txt')
    assert os.path.isfile(readme)
    with open(readme) as file:
        'hello world!\n' == file.read()


def check_fetch(stage, stage_name):
    archive_name = 'test-files.tar.gz'
    stage_path = get_stage_path(stage, stage_name)
    assert archive_name in os.listdir(stage_path)
    assert os.path.join(stage_path, archive_name) == stage.fetcher.archive_file


def check_destroy(stage, stage_name):
    """Figure out whether a stage was destroyed correctly."""
    stage_path = get_stage_path(stage, stage_name)

    # check that the stage dir/link was removed.
    assert not os.path.exists(stage_path)

    # tmp stage needs to remove tmp dir too.
    if spack.stage._use_tmp_stage:
        target = os.path.realpath(stage_path)
        assert not os.path.exists(target)


def check_setup(stage, stage_name, archive):
    """Figure out whether a stage was set up correctly."""
    stage_path = get_stage_path(stage, stage_name)

    # Ensure stage was created in the spack stage directory
    assert os.path.isdir(stage_path)

    if spack.stage.get_tmp_root():
        # Check that the stage dir is really a symlink.
        assert os.path.islink(stage_path)

        # Make sure it points to a valid directory
        target = os.path.realpath(stage_path)
        assert os.path.isdir(target)
        assert not os.path.islink(target)

        # Make sure the directory is in the place we asked it to
        # be (see setUp, tearDown, and use_tmp)
        assert target.startswith(str(archive.test_tmp_dir))

    else:
        # Make sure the stage path is NOT a link for a non-tmp stage
        assert os.path.islink(stage_path)


def get_stage_path(stage, stage_name):
    """Figure out where a stage should be living. This depends on
    whether it's named.
    """
    if stage_name is not None:
        # If it is a named stage, we know where the stage should be
        return os.path.join(spack.paths.stage_path, stage_name)
    else:
        # If it's unnamed, ensure that we ran mkdtemp in the right spot.
        assert stage.path is not None
        assert stage.path.startswith(spack.paths.stage_path)
        return stage.path


@pytest.fixture()
def tmpdir_for_stage(mock_archive):
    """Uses a temporary directory for staging"""
    current = spack.paths.stage_path
    spack.config.set(
        'config',
        {'build_stage': [str(mock_archive.test_tmp_dir)]},
        scope='user')
    yield
    spack.config.set('config', {'build_stage': [current]}, scope='user')


@pytest.fixture()
def mock_archive(tmpdir, monkeypatch):
    """Creates a mock archive with the structure expected by the tests"""
    # Mock up a stage area that looks like this:
    #
    # TMPDIR/                    test_files_dir
    #     tmp/                   test_tmp_path (where stage should be)
    #     test-files/            archive_dir_path
    #         README.txt         test_readme (contains "hello world!\n")
    #     test-files.tar.gz      archive_url = file:///path/to/this
    #
    test_tmp_path = tmpdir.join('tmp')
    # set _test_tmp_path as the default test directory to use for stages.
    spack.config.set(
        'config', {'build_stage': [str(test_tmp_path)]}, scope='user')

    archive_dir = tmpdir.join('test-files')
    archive_name = 'test-files.tar.gz'
    archive = tmpdir.join(archive_name)
    archive_url = 'file://' + str(archive)
    test_readme = archive_dir.join('README.txt')
    archive_dir.ensure(dir=True)
    test_tmp_path.ensure(dir=True)
    test_readme.write('hello world!\n')

    with tmpdir.as_cwd():
        tar = spack.util.executable.which('tar', required=True)
        tar('czf', str(archive_name), 'test-files')

    # Make spack use the test environment for tmp stuff.
    monkeypatch.setattr(spack.stage, '_tmp_root', None)
    monkeypatch.setattr(spack.stage, '_use_tmp_stage', True)

    Archive = collections.namedtuple(
        'Archive', ['url', 'tmpdir', 'test_tmp_dir', 'archive_dir']
    )
    yield Archive(
        url=archive_url,
        tmpdir=tmpdir,
        test_tmp_dir=test_tmp_path,
        archive_dir=archive_dir
    )


@pytest.fixture()
def mock_noexpand_resource(tmpdir):
    test_resource = tmpdir.join('resource-no-expand.sh')
    test_resource.write("an example resource")
    return str(test_resource)


@pytest.fixture()
def mock_expand_resource(tmpdir):
    resource_dir = tmpdir.join('resource-expand')
    archive_name = 'resource.tar.gz'
    archive = tmpdir.join(archive_name)
    archive_url = 'file://' + str(archive)
    test_file = resource_dir.join('resource-file.txt')
    resource_dir.ensure(dir=True)
    test_file.write('test content\n')
    current = tmpdir.chdir()
    tar = spack.util.executable.which('tar', required=True)
    tar('czf', str(archive_name), 'resource-expand')
    current.chdir()

    MockResource = collections.namedtuple(
        'MockResource', ['url', 'files'])

    return MockResource(archive_url, ['resource-file.txt'])


@pytest.fixture()
def composite_stage_with_expanding_resource(
        mock_archive, mock_expand_resource):
    composite_stage = StageComposite()
    root_stage = Stage(mock_archive.url)
    composite_stage.append(root_stage)

    test_resource_fetcher = spack.fetch_strategy.from_kwargs(
        url=mock_expand_resource.url)
    # Specify that the resource files are to be placed in the 'resource-dir'
    # directory
    test_resource = Resource(
        'test_resource', test_resource_fetcher, None, 'resource-dir')
    resource_stage = ResourceStage(
        test_resource_fetcher, root_stage, test_resource)
    composite_stage.append(resource_stage)
    return composite_stage, root_stage, resource_stage


@pytest.fixture()
def failing_search_fn():
    """Returns a search function that fails! Always!"""
    def _mock():
        raise Exception("This should not have been called")
    return _mock


@pytest.fixture()
def failing_fetch_strategy():
    """Returns a fetch strategy that fails."""
    class FailingFetchStrategy(spack.fetch_strategy.FetchStrategy):
        def fetch(self):
            raise spack.fetch_strategy.FailedDownloadError(
                "<non-existent URL>",
                "This implementation of FetchStrategy always fails"
            )
    return FailingFetchStrategy()


@pytest.fixture()
def search_fn():
    """Returns a search function that always succeeds."""
    class _Mock(object):
        performed_search = False

        def __call__(self):
            self.performed_search = True
            return []

    return _Mock()


@pytest.mark.usefixtures('mock_packages')
class TestStage(object):

    stage_name = 'spack-test-stage'

    @pytest.mark.usefixtures('tmpdir_for_stage')
    def test_setup_and_destroy_name_with_tmp(self, mock_archive):
        with Stage(mock_archive.url, name=self.stage_name) as stage:
            check_setup(stage, self.stage_name, mock_archive)
        check_destroy(stage, self.stage_name)

    def test_setup_and_destroy_name_without_tmp(self, mock_archive):
        with Stage(mock_archive.url, name=self.stage_name) as stage:
            check_setup(stage, self.stage_name, mock_archive)
        check_destroy(stage, self.stage_name)

    @pytest.mark.usefixtures('tmpdir_for_stage')
    def test_setup_and_destroy_no_name_with_tmp(self, mock_archive):
        with Stage(mock_archive.url) as stage:
            check_setup(stage, None, mock_archive)
        check_destroy(stage, None)

    @pytest.mark.disable_clean_stage_check
    @pytest.mark.usefixtures('tmpdir_for_stage')
    def test_composite_stage_with_noexpand_resource(
            self, mock_archive, mock_noexpand_resource):
        composite_stage = StageComposite()
        root_stage = Stage(mock_archive.url)
        composite_stage.append(root_stage)

        resource_dst_name = 'resource-dst-name.sh'
        test_resource_fetcher = spack.fetch_strategy.from_kwargs(
            url='file://' + mock_noexpand_resource, expand=False)
        test_resource = Resource(
            'test_resource', test_resource_fetcher, None, resource_dst_name)
        resource_stage = ResourceStage(
            test_resource_fetcher, root_stage, test_resource)
        composite_stage.append(resource_stage)

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.setup_source()
        assert os.path.exists(
            os.path.join(composite_stage.source_path, resource_dst_name))

    @pytest.mark.disable_clean_stage_check
    @pytest.mark.usefixtures('tmpdir_for_stage')
    def test_composite_stage_with_expand_resource_empty_existing_destination(
            self, mock_archive, mock_expand_resource,
            composite_stage_with_expanding_resource):

        composite_stage, root_stage, resource_stage = (
            composite_stage_with_expanding_resource)
        composite_stage.create()
        composite_stage.fetch()
        root_stage.setup_source()
        os.mkdir(os.path.join(root_stage.source_path, 'resource-dir'))

        resource_stage.setup_source()
        for fname in mock_expand_resource.files:
            file_path = os.path.join(
                root_stage.source_path, 'resource-dir', fname)
            assert os.path.exists(file_path)

    @pytest.mark.disable_clean_stage_check
    @pytest.mark.usefixtures('tmpdir_for_stage')
    def test_composite_stage_with_expand_resource_nonempty_existing_dest(
            self, mock_archive, mock_expand_resource,
            composite_stage_with_expanding_resource):

        composite_stage, root_stage, resource_stage = (
            composite_stage_with_expanding_resource)
        composite_stage.create()
        composite_stage.fetch()
        root_stage.setup_source()
        os.mkdir(os.path.join(root_stage.source_path, 'resource-dir'))
        preexisting_file = os.path.join(
            root_stage.source_path, 'resource-dir/non-conflicting-file')
        with open(preexisting_file, 'w'):
            pass

        resource_stage.setup_source()
        for fname in mock_expand_resource.files:
            file_path = os.path.join(
                root_stage.source_path, 'resource-dir', fname)
            assert os.path.exists(file_path)

    def test_setup_and_destroy_no_name_without_tmp(self, mock_archive):
        with Stage(mock_archive.url) as stage:
            check_setup(stage, None, mock_archive)
        check_destroy(stage, None)

    def test_fetch(self, mock_archive):
        with Stage(mock_archive.url, name=self.stage_name) as stage:
            stage.fetch()
            check_setup(stage, self.stage_name, mock_archive)
            check_fetch(stage, self.stage_name)
        check_destroy(stage, self.stage_name)

    def test_no_search_if_default_succeeds(
            self, mock_archive, failing_search_fn):
        stage = Stage(mock_archive.url,
                      name=self.stage_name,
                      search_fn=failing_search_fn)
        with stage:
            stage.fetch()
        check_destroy(stage, self.stage_name)

    def test_no_search_mirror_only(
            self, failing_fetch_strategy, failing_search_fn):
        stage = Stage(failing_fetch_strategy,
                      name=self.stage_name,
                      search_fn=failing_search_fn)
        with stage:
            try:
                stage.fetch(mirror_only=True)
            except spack.fetch_strategy.FetchError:
                pass
        check_destroy(stage, self.stage_name)

    def test_search_if_default_fails(self, failing_fetch_strategy, search_fn):
        stage = Stage(failing_fetch_strategy,
                      name=self.stage_name,
                      search_fn=search_fn)
        with stage:
            try:
                stage.fetch(mirror_only=False)
            except spack.fetch_strategy.FetchError:
                pass
        check_destroy(stage, self.stage_name)
        assert search_fn.performed_search

    def test_setup_source(self, mock_archive):
        with Stage(mock_archive.url, name=self.stage_name) as stage:
            stage.fetch()
            check_setup(stage, self.stage_name, mock_archive)
            check_fetch(stage, self.stage_name)
            stage.setup_source()
            check_setup_source(stage, self.stage_name, mock_archive)
        check_destroy(stage, self.stage_name)

    def test_restage(self, mock_archive):
        with Stage(mock_archive.url, name=self.stage_name) as stage:
            stage.fetch()
            stage.setup_source()

            with working_dir(stage.source_path):
                check_setup_source(stage, self.stage_name, mock_archive)

                # Try to make a file in the old archive dir
                with open('foobar', 'w') as file:
                    file.write("this file is to be destroyed.")

            assert 'foobar' in os.listdir(stage.source_path)

            # Make sure the file is not there after restage.
            stage.restage()
            check_fetch(stage, self.stage_name)
            assert 'foobar' not in os.listdir(stage.source_path)
        check_destroy(stage, self.stage_name)

    @pytest.mark.disable_clean_stage_check
    @pytest.mark.usefixtures('tmpdir_for_stage')
    def test_restage_with_resource(
            self, mock_archive, mock_expand_resource,
            composite_stage_with_expanding_resource):

        composite_stage, root_stage, resource_stage = (
            composite_stage_with_expanding_resource)

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.setup_source()

        resource_file = os.path.join(
            root_stage.source_path, 'resource-dir', 'resource-file.txt')
        assert os.path.exists(resource_file)

        composite_stage.restage()

        assert os.path.exists(resource_file)

    def test_no_keep_without_exceptions(self, mock_archive):
        stage = Stage(mock_archive.url, name=self.stage_name, keep=False)
        with stage:
            pass
        check_destroy(stage, self.stage_name)

    @pytest.mark.disable_clean_stage_check
    def test_keep_without_exceptions(self, mock_archive):
        stage = Stage(mock_archive.url, name=self.stage_name, keep=True)
        with stage:
            pass
        path = get_stage_path(stage, self.stage_name)
        assert os.path.isdir(path)

    @pytest.mark.disable_clean_stage_check
    def test_no_keep_with_exceptions(self, mock_archive):
        class ThisMustFailHere(Exception):
            pass

        stage = Stage(mock_archive.url, name=self.stage_name, keep=False)
        try:
            with stage:
                raise ThisMustFailHere()

        except ThisMustFailHere:
            path = get_stage_path(stage, self.stage_name)
            assert os.path.isdir(path)

    @pytest.mark.disable_clean_stage_check
    def test_keep_exceptions(self, mock_archive):
        class ThisMustFailHere(Exception):
            pass

        stage = Stage(mock_archive.url, name=self.stage_name, keep=True)
        try:
            with stage:
                raise ThisMustFailHere()

        except ThisMustFailHere:
            path = get_stage_path(stage, self.stage_name)
            assert os.path.isdir(path)
