# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psrdada(AutotoolsPackage, CudaPackage):
    """Open source software to process some types of astronomy data."""

    homepage = "https://psrdada.sourceforge.net/"
    git = "https://git.code.sf.net/p/psrdada/code"

    maintainers("aweaver1fandm")

    version("master", branch="master", preferred=True)

    depends_on("c", type="build")  # generated

    conflicts("~cuda", msg="You must specify +cuda")
    conflicts("cuda@11.8")
    conflicts("cuda_arch=none", msg="You must specify the CUDA architecture")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("nasm", type="build")
    depends_on("pkgconf", type="build")
    depends_on("fftw@3.3:", type="build")
    depends_on("python")
    depends_on("cuda", type="build")
