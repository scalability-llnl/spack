# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCmake(PythonPackage):
    """CMake is an open-source, cross-platform family of tools designed to
    build, test and package software
    """

    homepage = "https://cmake.org/"
    url      = "https://pypi.io/packages/source/c/cmake/cmake-3.18.0.tar.gz"

    version('3.18.0', sha256='52b98c5ee70b5fa30a8623e96482227e065292f78794eb085fdf0fecb204b79b')

    depends_on('cmake@3.18.0', type=('build', 'link', 'run'), when='@3.18.0')
    depends_on('py-scikit-build', type='build')
