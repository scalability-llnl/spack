# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os

from spack.main import SpackCommand
from spack.stage import Stage
import spack.environment as ev
import spack.config

mirror = SpackCommand('mirror')
env = SpackCommand('env')
add = SpackCommand('add')
concretize = SpackCommand('concretize')
fetch = SpackCommand('fetch')


@pytest.mark.disable_clean_stage_check
@pytest.mark.regression('8083')
def test_regression_8083(tmpdir, capfd, mock_packages, mock_fetch, config):
    with capfd.disabled():
        output = mirror('create', '-d', str(tmpdir), 'externaltool')
    assert 'Skipping' in output
    assert 'as it is an external spec' in output


@pytest.mark.regression('12345')
def test_mirror_from_env(tmpdir, mock_packages, mock_fetch, config,
                         mutable_mock_env_path):
    mirror_dir = str(tmpdir)
    env_name = 'test'

    env('create', env_name)
    with ev.read(env_name):
        add('trivial-install-test-package')
        add('git-test')
        concretize()
        with spack.config.override('config:checksum', False):
            mirror('create', '-d', mirror_dir)

    e = ev.read(env_name)
    assert set(os.listdir(mirror_dir)) == set([s.name for s in e.user_specs])
    for spec in e.specs_by_hash.values():
        mirror_res = os.listdir(os.path.join(mirror_dir, spec.name))
        expected = ['%s.tar.gz' % spec.format('{name}-{version}')]
        assert mirror_res == expected


@pytest.mark.disable_clean_stage_check
@pytest.mark.regression('12710')
def test_mirror_paths(tmpdir, capfd, mock_packages, mock_archive):
    # handle mirrors added via relative paths

    with tmpdir.as_cwd():
        with Stage('spack-mirror-test') as stage:
            mirror_root = os.path.join(stage.path, 'test-mirror')

            # register mirror with spack config
            # use relative path here!
            mirrors = {'spack-mirror-test': 'file://' + 
                                            os.path.relpath(mirror_root)}
            spack.config.set('mirrors', mirrors)

            with spack.config.override('config:checksum', False):
                mirror('create', '-d', mirror_root, 'libdwarf')

            with capfd.disabled():
                output = fetch('-n', 'libdwarf')

            for fetch_line in output.split('==>'):
                if mirror_root.split(os.sep)[-2] in fetch_line:
                    # various possible markers of fetch failure
                    # from relative mirror path
                    for bad_entry in ['curl', '503', 'error', 'failed']:
                        assert bad_entry not in fetch_line
