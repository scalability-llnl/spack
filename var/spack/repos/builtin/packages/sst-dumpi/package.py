# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstDumpi(AutotoolsPackage):
    """The DUMPI package provides libraries to collect and read traces of MPI
    applications. Traces are created by linking an application with a library
    that uses the PMPI interface to intercept MPI calls. DUMPI records
    signatures of all MPI-1 and MPI-2 subroutine calls, return values, request
    information, and PAPI counters.
    """

    homepage = "http://sst.sandia.gov/about_dumpi.html"
    url = "https://github.com/sstsimulator/sst-dumpi/archive/refs/tags/v13.0.0_Final.tar.gz"
    git = "https://github.com/sstsimulator/sst-dumpi.git"

    maintainers("berquist", "jpkenny", "calewis")

    license("BSD-3-Clause")

    version("13.0.0", sha256="0eaa5cf5826c9fbba6cfeed42f52af67c5a7d45bc8cbb485c2a3867b7438229b")
    version("12.1.0", sha256="b718658cbb0be957d28883f7cc914617bff97b3629fad7017cd62e14ed667d9d")
    version("12.0.1", sha256="6e74e5f16ee26c83b17ecd5c272a61ec37977f07f531066533dd610805f9117b")
    version("12.0.0", sha256="04989c900adb253262808e59897d9f9b8df5dbd497a03820c3340640055dcf4f")
    version("11.1.0", sha256="58144b4b7543705ef648ca86ea4ebf3c739554ea8a472123aadc2967a8201cdd")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf@1.68:", type="build")
    depends_on("automake@1.11.1:", type="build")
    depends_on("libtool@1.2.4:", type="build")
    depends_on("m4", type="build")
