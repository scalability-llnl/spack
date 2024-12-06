# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRtree(PythonPackage):
    """R-Tree spatial index for Python GIS."""

    homepage = "https://github.com/Toblerity/rtree"
    pypi = "Rtree/rtree-1.3.0.tar.gz"

    maintainers("adamjstewart", "hobu")

    license("MIT")

    version("1.3.0", sha256="b36e9dd2dc60ffe3d02e367242d2c26f7281b00e1aaf0c39590442edaaadd916")
    version("1.2.0", sha256="f5145f7852bf7f95c126fb16bf1a4c2ca9300ae151b07f8a0f7083ea47912675")
    version("1.1.0", sha256="6f8ee504dde5d005b25b08aaf5be0b3404af3ad5fece6e1ddcde35908a798a95")
    version("1.0.1", sha256="222121699c303a64065d849bf7038b1ecabc37b65c7fa340bedb38ef0e805429")
    version("1.0.0", sha256="d0483482121346b093b9a42518d40f921adf445915b7aea307eb26768c839682")
    version("0.9.7", sha256="be8772ca34699a9ad3fb4cfe2cfb6629854e453c10b3328039301bbfc128ca3e")
    version("0.8.3", sha256="6cb9cf3000963ea6a3db777a597baee2bc55c4fc891e4f1967f262cc96148649")

    depends_on("python@3.8:", when="@1.1:", type=("build", "run"))
    depends_on("py-setuptools@61:", when="@1.1:", type="build")
    depends_on("py-setuptools@39.2:", when="@1:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-typing-extensions@3.7:", when="@1: ^python@:3.7", type=("build", "run"))
    depends_on("libspatialindex@1.8.5:")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/R/Rtree/{}-{}.tar.gz"
        name = "Rtree"
        if version >= Version("1.3.0"):
            name = name.lower()
        return url.format(name, version)

    def setup_build_environment(self, env):
        env.set("SPATIALINDEX_C_LIBRARY", self.spec["libspatialindex"].libs[0])

    def setup_run_environment(self, env):
        self.setup_build_environment(env)
