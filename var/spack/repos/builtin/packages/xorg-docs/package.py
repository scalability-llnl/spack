# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XorgDocs(AutotoolsPackage, XorgPackage):
    """This package provides miscellaneous documentation for the X Window
    System that doesn't better fit into other packages.

    The preferred documentation format for these documents is DocBook XML."""

    homepage = "http://cgit.freedesktop.org/xorg/doc/xorg-docs"
    xorg_mirror_path = "doc/xorg-docs-1.7.1.tar.gz"

    version('1.7.1', sha256='360707db2ba48f6deeb53d570deca9fa98218af48ead4a726a67f63e3ef63816')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
    depends_on('xorg-sgml-doctools@1.8:', type='build')
    depends_on('xmlto', type='build')
