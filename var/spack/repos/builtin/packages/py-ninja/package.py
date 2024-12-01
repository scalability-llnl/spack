# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyNinja(PythonPackage):
    """Ninja is a small build system with a focus on speed.

    Deprecated: use ninja instead.
    """

    homepage = "https://ninja-build.org"
    pypi = "ninja/ninja-1.10.2.tar.gz"

    license("Apache-2.0")

    version(
        "1.10.2",
        sha256="bb5e54b9a7343b3a8fc6532ae2c169af387a45b0d4dd5b72c2803e21658c5791",
        deprecated=True,
    )

    depends_on("cmake@3.6:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("ninja@1.10.2", type=("build", "run"), when="@1.10.2")

    def patch(self):
        os.unlink(join_path(self.stage.source_path, "CMakeLists.txt"))

    @run_after("install")
    def installit(self):
        syntax_file = os.path.join(self.spec["ninja"].prefix.misc, "ninja_syntax.py")
        bin_file = os.path.join(self.spec["ninja"].prefix.bin, "ninja")
        dst = os.path.join(python_platlib, "ninja")
        dstbin = os.path.join(dst, "data", "bin")
        mkdirp(dstbin)
        os.symlink(bin_file, os.path.join(dstbin, "ninja"))
        os.symlink(syntax_file, os.path.join(dst, "ninja_syntax.py"))
