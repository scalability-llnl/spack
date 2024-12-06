# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spectra(CMakePackage):
    """
    Spectra stands for Sparse Eigenvalue Computation Toolkit as a Redesigned
    ARPACK. It is a C++ library for large scale eigenvalue problems,
    built on top of Eigen, an open source linear algebra library.

    Spectra is implemented as a header-only C++ library, whose only
    dependency, Eigen, is also header-only. Hence Spectra can be easily
    embedded in C++ projects that require calculating eigenvalues of
    large matrices.
    """

    homepage = "https://spectralib.org/"
    url = "https://github.com/yixuan/spectra/archive/refs/tags/v1.0.1.tar.gz"
    maintainers("snehring")

    license("MPL-2.0")

    version("1.0.1", sha256="919e3fbc8c539a321fd5a0766966922b7637cc52eb50a969241a997c733789f3")
    version("1.0.0", sha256="45228b7d77b916b5384245eb13aa24bc994f3b0375013a8ba6b85adfd2dafd67")
    version("0.9.0", sha256="2966757d432e8fba5958c2a05ad5674ce34eaae3718dd546c1ba8760b80b7a3d")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.5:")
    depends_on("eigen")
