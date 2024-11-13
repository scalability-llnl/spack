# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libspatialindex(CMakePackage):
    """C++ implementation of R*-tree, an MVR-tree and a TPR-tree with C API."""

    homepage = "https://libspatialindex.org/"
    url = "https://github.com/libspatialindex/libspatialindex/archive/refs/tags/1.8.5.tar.gz"

    license("MIT")

    version("1.9.3", sha256="7b44340a3edc55c11abfc453bb60f148b29f569cef9e1148583e76132e9c7379")
    version("1.8.5", sha256="93cce77269612f45287b521d5afdfb245be2b93b8b6438d92f8b9e0bdb37059d")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5.0:", type="build")

    @property
    def libs(self):
        return find_libraries(["libspatialindex_c"], root=self.prefix, recursive=True, shared=True)
