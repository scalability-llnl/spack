# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

import pytest

import os
import os.path

import spack.architecture as architecture
import spack.config
from spack.main import SpackCommand, get_version
from spack.util.executable import which

debug = SpackCommand('debug')


@pytest.mark.db
def test_create_db_tarball(tmpdir, database):
    with tmpdir.as_cwd():
        debug('create-db-tarball')

        # get the first non-dotfile to avoid coverage files in the directory
        files = os.listdir(os.getcwd())
        tarball_name = next(f for f in files if not f.startswith('.'))

        # debug command made an archive
        assert os.path.exists(tarball_name)

        # print contents of archive
        tar = which('tar')
        contents = tar('tzf', tarball_name, output=str)

        # DB file is included
        assert 'index.json' in contents

        # spec.yamls from all installs are included
        for spec in database.query():
            # externals won't have a spec.yaml
            if spec.external:
                continue

            spec_suffix = '%s/.spack/spec.yaml' % spec.dag_hash()
            assert spec_suffix in contents


def test_report():
    out = debug('report')
    arch = architecture.Arch(architecture.platform(), 'frontend', 'frontend')

    assert get_version() in out
    assert platform.python_version() in out
    assert str(arch) in out
    assert spack.config.get('config:concretizer', 'original') in out
