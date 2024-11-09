# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcdf(CMakePackage):
    """Binary data format designed to store data fields with user-specified accuracy."""

    homepage = "https://github.com/jimbraun/XCDF"
    url = "https://github.com/jimbraun/XCDF/archive/refs/tags/v3.00.03.tar.gz"

    license("BSD-2-Clause")

    version("3.01", sha256="39fe816f40d6af18e16e71ffcf958258fdac4959ac894a60d1b863efaa57754e")
    version("3.00.03", sha256="4e445a2fea947ba14505d08177c8d5b55856f8411f28de1fe4d4c00f6824b711")

    depends_on("cxx", type="build")  # generated

    patch("remove_python_support.patch", when="@3.00.03")

    depends_on("python@3.7:", when="@3.01:")
    depends_on("py-pybind11", when="@3.01:", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.lib)
