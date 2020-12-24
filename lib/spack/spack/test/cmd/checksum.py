# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.main
import spack.stage

zlib_sha256 = 'c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1'

checksum  = spack.main.SpackCommand('checksum')


def test_checksum():

    output = checksum('zlib@1.2.11')

    assert "('1.2.11', sha256='{0}')".format(zlib_sha256) in output


@pytest.mark.disable_clean_stage_check
def test_checksum_keep_stage(config):

    path = spack.stage.get_stage_root()
    file_list = os.listdir(path)

    for file_name in file_list:
        if file_name.startswith('spack-stage-'):
            assert os.path.exists(os.path.join(path,
                                  file_name, 'zlib-1.2.11.tar.gz'))
