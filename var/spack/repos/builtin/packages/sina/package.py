# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sina(CachedCMakePackage):
    """Sina C++ Library"""

    homepage = "https://github.com/LLNL/Sina"
    url = "https://github.com/LLNL/Sina/releases/download/v1.10.0/sina-cpp-1.10.0.tar.gz"

    maintainers("estebanpauli", "HaluskaR", "murray55")

    version("1.13.0", sha256="4087fc63ea054fd5d6cfcd2223d33edcb910df1fad5936301591e1a9aa4d6bac")
    version("1.11.0", sha256="a080f6583101696a6354940f00646ef892e1b2f8fc3f1b1907ba1c3ade6d4b47")
    version("1.10.0", sha256="b34379ce8cc5eca5a0f16893053fac75be14c2109d1beed4c6d48e11f9b281c7")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("docs", default=False, description="Allow generating documentation")
    variant("adiak", default=False, description="Create interface for calling Sina through Adiak")
    variant("test", default=False, description="Build tests")

    depends_on("cmake@3.8.0:", type="build")
    depends_on("adiak", when="+adiak")
    depends_on("doxygen", type="build", when="+docs")
    depends_on("conduit")

    def cmake_args(self):
        return [
            self.define_from_variant("-DSINA_BUILD_ADIAK_BINDINGS", "adiak"),
            self.define_from_variant("-DSINA_BUILD_TESTS", "test"),
            self.define_from_variant("-DSINA_BUILD_DOCS", "docs"),
        ]

    def initconfig_package_entries(self):
        entries = ["#" + 78 * "-", "# Library Dependencies", "#" + 78 * "-"]

        conduit_dir = self.spec["conduit"].prefix
        entries.append(cmake_cache_path("Conduit_DIR", "%s/lib/cmake/conduit" % conduit_dir))

        use_adiak = self.spec.satisfies("^adiak")
        entries.append(cmake_cache_option("SINA_BUILD_ADIAK_BINDINGS", use_adiak))
        if use_adiak:
            adiak_dir = self.spec["adiak"].prefix
            entries.append(cmake_cache_path("adiak_DIR", "%s/lib/cmake/adiak/" % adiak_dir))

        entries.append("#" + 78 * "-")
        entries.append("# Devtools")
        entries.append("#" + 78 * "-")

        build_tests = self.spec.satisfies("+test")
        entries.append(cmake_cache_option("SINA_BUILD_TESTS", build_tests))

        build_docs = self.spec.satisfies("+docs")
        entries.append(cmake_cache_option("SINA_BUILD_DOCS", build_docs))
        if build_docs:
            doxygen_bin_dir = self.spec["doxygen"].prefix.bin
            entries.append(
                cmake_cache_path("DOXYGEN_EXECUTABLE", os.path.join(doxygen_bin_dir, "doxygen"))
            )

        return entries
