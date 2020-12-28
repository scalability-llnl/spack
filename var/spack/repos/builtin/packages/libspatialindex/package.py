# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libspatialindex(CMakePackage):
    """C++ implementation of R*-tree, an MVR-tree and a TPR-tree with C API."""

    homepage = "https://libspatialindex.org/"
    url      = "https://github.com/libspatialindex/libspatialindex/tarball/1.8.5"

    version('1.8.5', sha256='271f0d1425c527fd7d8b4be45b27e9383b244047b5918225877105616e7c0ad2')
