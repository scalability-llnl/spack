# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Fargparse(CMakePackage):
    """Command line argument parsing for Fortran"""

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/fArgParse"
    url = "https://github.com/Goddard-Fortran-Ecosystem/fArgParse/archive/refs/tags/v1.4.1.tar.gz"
    list_url = "https://github.com/Goddard-Fortran-Ecosystem/fArgParse/tags"
    git = "https://github.com/Goddard-Fortran-Ecosystem/fArgParse.git"

    maintainers("mathomp4", "tclune")

    version("develop", branch="develop")
    version("main", branch="main")

    version("1.8.0", sha256="37108bd3c65d892d8c24611ce4d8e5451767e4afe81445fde67eab652178dd01")
    version("1.7.0", sha256="9889e7eca9c020b742787fba2be0ba16edcc3fcf52929261ccb7d09996a35f89")
    version("1.6.0", sha256="055a0af44f50c302f8f20a8bcf3d26c5bbeacf5222cdbaa5b19da4cff56eb9c0")
    version("1.5.0", sha256="1c16ead5f1bacb9c2f33aab99a0889c68c1a1ece754ddc3fd340f10a0d5da2f7")
    version("1.4.2", sha256="2cd3f14845235407c6a4171ab4602499dade045e3f9b7dc75190f4a315ac8b44")
    version("1.4.1", sha256="8f9b92a80f05b0a8ab2dd5cd309ad165041c7fcdd589b96bf75c7dd889b9b584")
    version("1.3.1", sha256="65d168696762b53f9a34fac8a82527fb602372f47be05018ebb382ec27b52c6c")
    version("1.3.0", sha256="08fde5fb1b739b69203ac336fe7b39915cfc7f52e068e564b9b6d905d79fc93d")
    version("1.2.0", sha256="4d14584d2bd5406267e3eacd35b50548dd9e408526465e89514690774217da70")
    version("1.1.2", sha256="89f63f181ccf183ca6212aee7ed7e39d510e3df938b0b16d487897ac9a61647f")

    depends_on("fortran", type="build")

    depends_on("gftl-shared")
    depends_on("gftl")
    depends_on("cmake@3.12:", type="build")

    # fargparse only works with the Fujitsu compiler from 1.7.0 onwards
    conflicts(
        "%fj",
        when="@:1.6.0",
        msg="fargparse only works with the Fujitsu compiler from 1.7.0 onwards",
    )

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
