# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Advancecomp(AutotoolsPackage):
    """AdvanceCOMP contains recompression utilities for your .zip archives,
    .png images, .mng video clips and .gz files."""

    homepage = "http://www.advancemame.it"
    url      = "https://github.com/amadvance/advancecomp/archive/v2.1.tar.gz"

    version('2.1',  sha256='6113c2b6272334af710ba486e8312faa3cee5bd6dc8ca422d00437725e2b602a')
    version('2.0',  sha256='caa63332cd141db17988eb89c662cf76bdde72f60d4de7cb0fe8c7e51eb40eb7')
    version('1.23', sha256='fe89d6ab382efc6b6be536b8d58113f36b83d82783d5215c261c14374cba800a')
    version('1.22', sha256='b8c482027a5f78d9a7f871cbba19cc896ed61653d1d93034c9dbe55484952605')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('zlib',      type='link')
