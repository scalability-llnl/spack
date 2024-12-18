# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyPycairo(PythonPackage):
    """Pycairo is a set of Python bindings for the cairo graphics library."""

    homepage = "https://www.cairographics.org/pycairo/"
    pypi = "pycairo/pycairo-1.17.1.tar.gz"
    git = "https://github.com/pygobject/pycairo.git"

    license("MPL-1.1")

    version("1.24.0", sha256="1444d52f1bb4cc79a4a0c0fe2ccec4bd78ff885ab01ebe1c0f637d8392bcafb6")
    version("1.20.0", sha256="5695a10cb7f9ae0d01f665b56602a845b0a8cb17e2123bfece10c2e58552468c")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:", when="@1.23:", type=("build", "run"))
    depends_on("python@3.6:3", when="@1.20:1.22", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    # https://github.com/pygobject/pycairo/blob/main/docs/getting_started.rst
    depends_on("pkgconfig", type="build")
    # version requirements from setup.py
    depends_on("cairo@1.15.10: +pdf")

    @run_after("install")
    def post_install(self):
        src = self.prefix.lib + "/pkgconfig/py3cairo.pc"
        dst = self.prefix.lib + "/pkgconfig/pycairo.pc"
        if os.path.exists(src) and not os.path.exists(dst):
            copy(src, dst)
