# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    url = "https://github.com/matplotlib/basemap/archive/v1.2.0rel.tar.gz"
    homepage = "https://matplotlib.org/basemap/"

    license("MIT")

    version("1.2.1", sha256="3fb30424f18cd4ffd505e30fd9c810ae81b999bb92f950c76553e1abc081faa7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Per Github issue #3813, setuptools is required at runtime in order
    # to make mpl_toolkits a namespace package that can span multiple
    # directories (i.e., matplotlib and basemap)
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy@1.2.1:", type=("build", "run"))
    depends_on("py-matplotlib@1.0.0:3.0.0,3.0.2:", type=("build", "run"))
    # 1.2.1 is PROJ6 compatible
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=939022
    depends_on("py-pyproj@1.9.3:", type=("build", "run"), when="@1.2.1:")

    depends_on("py-pyshp@1.2.0:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("geos")

    def url_for_version(self, version):
        if version >= Version("1.2.0"):
            return "https://github.com/matplotlib/basemap/archive/v{0}rel.tar.gz".format(version)
        else:
            return "https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-{0}/basemap-{0}.tar.gz".format(
                version
            )

    def setup_build_environment(self, env):
        env.set("GEOS_DIR", self.spec["geos"].prefix)
