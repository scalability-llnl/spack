# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIgraph(PythonPackage):
    """Python interface to the igraph high performance graph library,
    primarily aimed at complex network research and analysis."""

    homepage = "https://github.com/igraph/python-igraph"
    pypi = "igraph/igraph-0.10.6.tar.gz"

    license("GPL-2.0-or-later")

    version("0.11.6", sha256="837f233256c3319f2a35a6a80d94eafe47b43791ef4c6f9e9871061341ac8e28")
    version("0.10.6", sha256="76f7aad294514412f835366a7d9a9c1e7a34c3e6ef0a6c3a1a835234323228e8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("matplotlib", default=False, description="Enable plotting with Matplotlib")

    depends_on("cmake", type="build")
    depends_on("igraph+shared@0.10.6", when="@0.10.6")
    depends_on("igraph+shared@0.10.13", when="@0.11.6")
    depends_on("pkgconfig", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-texttable@1.6.2:", type=("build", "run"))
    depends_on("py-matplotlib@3.5:", type="run", when="+matplotlib")

    def setup_build_environment(self, env):
        env.set("IGRAPH_USE_PKG_CONFIG", "1")
