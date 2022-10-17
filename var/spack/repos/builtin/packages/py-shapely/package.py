# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class PyShapely(PythonPackage):
    """Manipulation and analysis of geometric objects in the Cartesian plane."""

    homepage = "https://github.com/Toblerity/Shapely"
    pypi = "Shapely/Shapely-1.7.1.tar.gz"
    git = "https://github.com/Toblerity/Shapely.git"

    maintainers = ["adamjstewart"]

    version("main", branch="main")
    version("master", branch="main", deprecated=True)
    version("1.8.5", sha256="e82b6d60ecfb124120c88fe106a478596bbeab142116d7e7f64a364dac902a92")
    version("1.8.4", sha256="a195e51caafa218291f2cbaa3fef69fd3353c93ec4b65b2a4722c4cf40c3198c")
    version("1.8.3", sha256="1ce9da186d48efc50130af96d62ffb4d2e175235143d804ef395aad156d45bb3")
    version("1.8.2", sha256="572af9d5006fd5e3213e37ee548912b0341fb26724d6dc8a4e3950c10197ebb6")
    version("1.8.1", sha256="0956a3aced40c31a957a52aa1935467334926844a6776b469acb0760a5e6aba8")
    version("1.8.0", sha256="f5307ee14ba4199f8bbcf6532ca33064661c1433960c432c84f0daa73b47ef9c")
    version("1.7.1", sha256="1641724c1055459a7e2b8bbe47ba25bdc89554582e62aec23cb3f3ca25f9b129")
    version("1.7.0", sha256="e21a9fe1a416463ff11ae037766fe410526c95700b9e545372475d2361cc951e")
    version("1.6.4", sha256="b10bc4199cfefcf1c0e5d932eac89369550320ca4bdf40559328d85f1ca4f655")

    depends_on("python@3.6:", when="@1.8:", type=("build", "link", "run"))
    depends_on("python@2.7:2.8,3.4:", when="@1.7", type=("build", "link", "run"))
    depends_on("python@2.6:", when="@:1.6", type=("build", "link", "run"))
    depends_on("py-setuptools@:63", type="build")
    depends_on("py-cython@0.29.24:2", type="build")
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("geos@3.3:3.10", when="@:1.7")
    depends_on("geos@3.6:3.10", when="@1.8:")
    depends_on("py-pytest", type="test")
    depends_on("py-pytest-cov", type="test")

    # https://github.com/Toblerity/Shapely/pull/891
    patch(
        "https://github.com/Toblerity/Shapely/commit/98f6b36710bbe05b4ab59231cb0e08b06fe8b69c.patch?full_index=1",
        sha256="8583cdc97648277fa4faea8bd88d49e43390e87f697b966bd2b4290fba945ba0",
        when="@:1.7.0",
    )

    @when("^python@3.7:")
    def patch(self):
        # Python 3.7 changed the thread storage API, precompiled *.c files
        # need to be re-cythonized
        if os.path.exists("shapely/speedups/_speedups.c"):
            os.remove("shapely/speedups/_speedups.c")
        if os.path.exists("shapely/vectorized/_vectorized.c"):
            os.remove("shapely/vectorized/_vectorized.c")

    def setup_build_environment(self, env):
        env.set("GEOS_CONFIG", join_path(self.spec["geos"].prefix.bin, "geos-config"))

        # Shapely uses ctypes.util.find_library, which searches LD_LIBRARY_PATH
        # Our RPATH logic works fine, but the unit tests fail without this
        # https://github.com/Toblerity/Shapely/issues/909
        libs = ":".join(self.spec["geos"].libs.directories)
        if sys.platform == "darwin":
            env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", libs)
        else:
            env.prepend_path("LD_LIBRARY_PATH", libs)

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest")
