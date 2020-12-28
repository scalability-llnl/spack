# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcgroup(AutotoolsPackage):
    """Library of control groups."""

    homepage = "https://sourceforge.net/projects/libcg/"
    url      = "https://sourceforge.net/projects/libcg/files/libcgroup/v0.41/libcgroup-0.41.tar.bz2"

    version('0.41', sha256='e4e38bdc7ef70645ce33740ddcca051248d56b53283c0dc6d404e17706f6fb51')
    version('0.37', sha256='15c8f3febb546530d3495af4e4904b3189c273277ca2d8553dec882cde1cd0f6')
    version('0.36', sha256='8dcd2ae220435b3de736d3efb0023fdf1192d7a7f4032b439f3cf5342cff7b4c')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('bison',    type='build')
    depends_on('flex',     type='build')
    depends_on('linux-pam')
