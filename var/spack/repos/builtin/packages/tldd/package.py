# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tldd(MakefilePackage):
    """A program similar to ldd(1) but showing the output as a tree."""

    homepage = "https://gitlab.com/miscripts/tldd"
    git      = "https://gitlab.com/miscripts/tldd.git"

    version('2018-10-05', commit='61cb512cc992ea6cbb7239e99ec7ac92ea072507')
    version('master', branch='master')

    depends_on('pstreams@0.8.0:')

    def patch(self):
        filter_file(
            r'#include <pstreams/pstream.h>',
            r'#include <pstream.h>',
            'tldd.cc')

    @property
    def install_targets(self):
        return ['install', 'PREFIX={0}'.format(self.prefix)]
