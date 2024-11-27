# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Jali(CMakePackage):
    """Jali is a parallel, unstructured mesh infrastructure library designed
    for use by multi-physics simulations.
    """

    homepage = "https://github.com/lanl/jali"
    git = "https://github.com/lanl/jali"
    url = "https://github.com/lanl/jali/archive/1.1.6.tar.gz"

    maintainers("raovgarimella")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.1.6", sha256="a2f4e4f238c60ea78486e0c9ea5b3e2cdd9d91c2ae5ea006a1d33a12e9eafa3a")
    version("1.1.5", sha256="4f18f3e8b50f20a89918e99596a7226c215944d84df642bc1fb2d6c31464b95b")
    version("1.1.4", sha256="135ab02be1487fcdfb039613cbed630bce336d581a66468c66209db0a9d8a104")
    version("1.1.1", sha256="c96c000b3893ea7f15bbc886524476dd466ae145e77deedc27e412fcc3541207")
    version("1.1.0", sha256="783dfcd6a9284af83bb380ed257fa8b0757dc2f7f9196d935eb974fb6523c644")
    version("1.0.5", sha256="979170615d33a7bf20c96bd4d0285e05a2bbd901164e377a8bccbd9af9463801")

    depends_on("cxx", type="build")  # generated

    variant("mstk", default=True, description="Enable MSTK")

    # dependencies
    depends_on("cmake@3.13:", type="build")

    depends_on("mpi")

    # Fixme: Can the maintainers please confirm if this is a required dependency
    depends_on("boost")
    depends_on(Boost.with_default_variants)
    depends_on("mstk@3.3.5: +exodusii+parallel~use_markers partitioner=all", when="+mstk")

    depends_on("zoltan -fortran")
    depends_on("metis")
    depends_on("exodusii")

    # Unit testing variant
    depends_on("unittest-cpp", type="test")

    def cmake_args(self):
        options = []

        # Turn MSTK ON/OFF
        options.append(self.define_from_variant("ENABLE_MSTK_Mesh", "mstk"))

        # Unit test variant
        options.append(self.define("ENABLE_TESTS", self.run_tests))

        return options
