# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JsonCwx(AutotoolsPackage):
    """JSON-C with Extensions"""

    homepage = "https://github.com/LLNL/json-cwx"
    url = "https://github.com/LLNL/json-cwx/archive/0.12.tar.gz"

    license("JSON")

    version("0.12", sha256="3bfae1f23eacba53ee130dbd1a6acf617af4627a9b4e4581d64b20a99b4e2b60")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    parallel = False

    configure_directory = "json-cwx"

    def autoreconf(self, spec, prefix):
        with working_dir("json-cwx"):
            autogen = Executable("./autogen.sh")
            autogen()

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file(
                "-Wno-error=deprecated-declarations -Wextra "
                "-Wwrite-strings -Wno-unused-parameter -std=gnu99",
                "",
                "json-cwx/Makefile.am.inc",
            )
