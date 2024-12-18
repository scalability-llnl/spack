# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HackrfHost(CMakePackage):
    """Software for HackRF, a low cost, open source Software Defined
    Radio platform."""

    homepage = "https://github.com/mossmann/hackrf"
    url = "https://github.com/mossmann/hackrf/archive/v2018.01.1.tar.gz"

    maintainers("aweits")

    root_cmakelists_dir = "host"

    license("GPL-2.0-only")

    version("2018.01.1", sha256="84dbb5536d3aa5bd6b25d50df78d591e6c3431d752de051a17f4cb87b7963ec3")

    depends_on("c", type="build")  # generated

    depends_on("cmake@2.8.12:", type="build")
    depends_on("libusb@1.0.18:")
    depends_on("fftw@3.3.5:")
