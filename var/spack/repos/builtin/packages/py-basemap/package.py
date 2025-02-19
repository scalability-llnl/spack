# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    homepage = "https://matplotlib.org/basemap/"
    url = "https://github.com/matplotlib/basemap/archive/refs/tags/v1.4.1.tar.gz"

    license("MIT")

    version("1.4.1", sha256="730b1e2ff5eb31c73680bd8ebabc6b11adfc587cfa6832c528a8a82822e5a490")

    variant("hires", default=False, description="Install hi-res data.")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("py-cython@0.29:3.0", type="build")

    depends_on("python@3.10:3", type=("build", "run"))
    depends_on("py-numpy@1.21:1.26", type=("build", "run"))
    depends_on("py-matplotlib@1.5:3.8", type=("build", "run"))
    depends_on("py-pyproj@1.9.3:3.6", type=("build", "run"))
    depends_on("py-pyshp@1.2:2.3", type=("build", "run"))
    depends_on("py-packaging@16.0:23", type=("build", "run"))

    depends_on("geos", type=("build", "run"))
    # Per Github issue #3813, setuptools is required at runtime in order
    # to make mpl_toolkits a namespace package that can span multiple
    # directories (i.e., matplotlib and basemap)
    depends_on("py-setuptools", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("GEOS_DIR", self.spec["geos"].prefix)

    def install(self, spec, prefix):
        with working_dir("packages/basemap"):
            python("setup.py", "install", "--prefix={0}".format(prefix))

        with working_dir("packages/basemap_data"):
            python("setup.py", "install", "--prefix={0}".format(prefix))

        if "+hires" in spec:
            with working_dir("packages/basemap_data_hires"):
                python("setup.py", "install", "--prefix={0}".format(prefix))
