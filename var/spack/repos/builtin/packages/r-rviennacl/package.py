# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRviennacl(RPackage):
    """'ViennaCL' C++ Header Files.

    'ViennaCL' is a free open-source linear algebra library for computations on
    many-core architectures (GPUs, MIC) and multi-core CPUs. The library is
    written in C++ and supports 'CUDA', 'OpenCL', and 'OpenMP' (including
    switches at runtime). I have placed these libraries in this package as a
    more efficient distribution system for CRAN. The idea is that you can write
    a package that depends on the 'ViennaCL' library and yet you do not need to
    distribute a copy of this code with your package."""

    cran = "RViennaCL"

    version("1.7.1.8", sha256="adcc74537337582153d5b11d281e391e91a7f3afae116aa1b9a034ffd11b0252")

    depends_on("cxx", type="build")  # generated
