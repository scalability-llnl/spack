# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    homepage = "https://matplotlib.org/basemap/"
    pypi = "basemap/basemap-1.4.1.zip"

    license("MIT")

    version("1.4.1", sha256="730b1e2ff5eb31c73680bd8ebabc6b11adfc587cfa6832c528a8a82822e5a490")

    variant("hires", default=False, description="Install hi-res data.")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.10:3.11", type=("build", "run"))
    # Per Github issue #3813, setuptools is required at runtime in order
    # to make mpl_toolkits a namespace package that can span multiple
    # directories (i.e., matplotlib and basemap)
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy@1.2.1:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    # 1.2.1 is PROJ6 compatible
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=939022
    depends_on("py-pyproj", type=("build", "run"))

    depends_on("py-cython", type=("build", "run"))
    depends_on("py-pyshp", type=("build", "run"))
    depends_on("geos", type=("build", "run"))

    def url_for_version(self, version):
        if version >= Version("1.3.2"):
            return "https://github.com/matplotlib/basemap/archive/v{0}.tar.gz".format(version)
        elif version >= Version("1.2.0"):
            return "https://github.com/matplotlib/basemap/archive/v{0}rel.tar.gz".format(version)
        else:
            return "https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-{0}/basemap-{0}.tar.gz".format(
                version
            )

    def setup_build_environment(self, env):
        env.set("GEOS_DIR", self.spec["geos"].prefix)

    def install(self, spec, prefix):
        with working_dir("packages/basemap"):
            pip("install", ".", "--prefix={0}".format(prefix))

        with working_dir("packages/basemap_data"):
            pip("install", ".", "--prefix={0}".format(prefix))

        if "+hires" in spec:
            with working_dir("packages/basemap_data_hires"):
                pip("install", ".", "--prefix={0}".format(prefix))
