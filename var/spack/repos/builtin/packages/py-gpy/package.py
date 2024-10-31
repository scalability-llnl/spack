# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGpy(PythonPackage):
    """The Gaussian Process Toolbox."""

    homepage = "https://sheffieldml.github.io/GPy/"
    pypi = "gpy/GPy-1.9.9.tar.gz"
    maintainers("liuyangzhuan")

    license("BSD-3-Clause")

    version("1.10.0", sha256="a2b793ef8d0ac71739e7ba1c203bc8a5afa191058b42caa617e0e29aa52aa6fb")
    version("1.9.9", sha256="04faf0c24eacc4dea60727c50a48a07ddf9b5751a3b73c382105e2a31657c7ed")
    version("0.8.8", sha256="e135d928cf170e2ec7fb058a035b5a7e334dc6b84d0bfb981556782528341988")

    depends_on("c", type="build")  # generated

    variant("plotting", default=False, description="Enable plotting")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scipy@0.16:", type=("build", "run"))
    depends_on("py-scipy@1.3:", when="@1.10.0:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-paramz@0.9.0:", type=("build", "run"))
    # cython is install_requires, but not used at runtime, so stick to build type
    depends_on("py-cython@0.29:", type="build")

    with when("+plotting"):
        depends_on("py-matplotlib@3.0:", type=("build", "run"))
        depends_on("py-plotly@1.8.6:", type=("build", "run"))

    @run_before("install")
    def touch_sources(self):
        # This packages uses deprecated build_ext, for which we cannot
        # automatically force recythonization.
        # See also https://github.com/SheffieldML/GPy/pull/1020
        for src in find(".", "*.pyx"):
            touch(src)
