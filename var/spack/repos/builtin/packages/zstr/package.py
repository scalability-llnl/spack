# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zstr(Package):
    """This C++ header-only library enables the use of C++ standard
    iostreams to access ZLib-compressed streams."""

    homepage = "https://github.com/mateidavid/zstr"
    url = "https://github.com/mateidavid/zstr/archive/v1.0.4.tar.gz"

    maintainers("bvanessen")

    license("MIT")

    version("1.0.7", sha256="8d2ddae68ff7bd0a6fce6150a8f52ad9ce1bed2c4056c8846f4dec4f2dc60819")
    version("1.0.4", sha256="a594a3a9c192a6d9e93f9585910d41f7ee6791eb7c454d40c922656324b3058e")
    version("1.0.3", sha256="d42f1b08e4c3a26e3b42433691d32765015cf89f089ae075b1acb819ccba585f")
    version("1.0.2", sha256="b4c2d72f0f222b72985fc6c2bd2bd9c1fc353d2e4c8c12186fd87229107a442b")
    version("1.0.1", sha256="e17e67e00ede182504b3165cebd802420770541465d4ba41df1a15bf4c2a63b7")
    version("1.0.0", sha256="9f4fa8cb0d2cbba03dfe67900c48b6e75c8380d9263a0ac71d795f11e0224b96")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        """Make the install targets - Note that this package
        keeps it's headers in the src directory"""
        install_tree(join_path(self.stage.source_path, "src"), prefix.include)
