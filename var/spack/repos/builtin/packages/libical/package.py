# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libical(CMakePackage):
    """Libical - an implementation of iCalendar protocols and data formats."""

    homepage = "https://github.com/libical/libical"
    url = "https://github.com/libical/libical/archive/v3.0.8.tar.gz"

    version('3.0.8', sha256='09fecacaf75ba5a242159e3a9758a5446b5ce4d0ab684f98a7040864e1d1286f')

    depends_on('cmake@3.11.0:', type='build')
    depends_on('perl', type='build')
    depends_on('icu4c')

    def cmake_args(self):
        return ['-DENABLE_GTK_DOC=OFF']
