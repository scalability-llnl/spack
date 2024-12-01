# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import platform

import pytest

import spack
import spack.platforms
import spack.spec
from spack.main import SpackCommand
from spack.util.executable import which

debug = SpackCommand("debug")


@pytest.mark.db
def test_create_db_tarball(tmpdir, database):
    with tmpdir.as_cwd():
        debug("create-db-tarball")

        # get the first non-dotfile to avoid coverage files in the directory
        files = os.listdir(os.getcwd())
        tarball_name = next(
            f for f in files if not f.startswith(".") and not f.startswith("tests")
        )

        # debug command made an archive
        assert os.path.exists(tarball_name)

        # print contents of archive
        tar = which("tar")
        contents = tar("tzf", tarball_name, output=str)

        # DB file is included
        assert "index.json" in contents

        # specfiles from all installs are included
        for spec in database.query():
            # externals won't have a specfile
            if spec.external:
                continue

            spec_suffix = "%s/.spack/spec.json" % spec.dag_hash()
            assert spec_suffix in contents


def test_report():
    out = debug("report")
    host_platform = spack.platforms.host()
    host_os = host_platform.operating_system("frontend")
    host_target = host_platform.target("frontend")
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))

    assert spack.get_version() in out
    assert platform.python_version() in out
    assert str(architecture) in out
