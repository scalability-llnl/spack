# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class PyShapely(PythonPackage):
    """Manipulation and analysis of geometric objects in the Cartesian plane."""

    homepage = "https://github.com/shapely/shapely"
    pypi = "shapely/shapely-1.7.1.tar.gz"
    git = "https://github.com/shapely/shapely.git"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("2.0.6", sha256="997f6159b1484059ec239cacaa53467fd8b5564dabe186cd84ac2944663b0bf6")
    version("2.0.5", sha256="bff2366bc786bfa6cb353d6b47d0443c570c32776612e527ee47b6df63fcfe32")
    version("2.0.4", sha256="5dc736127fac70009b8d309a0eeb74f3e08979e530cf7017f2f507ef62e6cfb8")
    version("2.0.3", sha256="4d65d0aa7910af71efa72fd6447e02a8e5dd44da81a983de9d736d6e6ccbe674")
    version("2.0.2", sha256="1713cc04c171baffc5b259ba8531c58acc2a301707b7f021d88a15ed090649e7")
    version("2.0.1", sha256="66a6b1a3e72ece97fc85536a281476f9b7794de2e646ca8a4517e2e3c1446893")
    version("2.0.0", sha256="11f1b1231a6c04213fb1226c6968d1b1b3b369ec42d1e9655066af87631860ea")
    version("1.8.5", sha256="e82b6d60ecfb124120c88fe106a478596bbeab142116d7e7f64a364dac902a92")
    version("1.8.4", sha256="a195e51caafa218291f2cbaa3fef69fd3353c93ec4b65b2a4722c4cf40c3198c")
    version("1.8.3", sha256="1ce9da186d48efc50130af96d62ffb4d2e175235143d804ef395aad156d45bb3")
    version("1.8.2", sha256="572af9d5006fd5e3213e37ee548912b0341fb26724d6dc8a4e3950c10197ebb6")
    version("1.8.1", sha256="0956a3aced40c31a957a52aa1935467334926844a6776b469acb0760a5e6aba8")
    version("1.8.0", sha256="f5307ee14ba4199f8bbcf6532ca33064661c1433960c432c84f0daa73b47ef9c")
    version("1.7.1", sha256="1641724c1055459a7e2b8bbe47ba25bdc89554582e62aec23cb3f3ca25f9b129")
    version("1.7.0", sha256="e21a9fe1a416463ff11ae037766fe410526c95700b9e545372475d2361cc951e")
    version(
        "1.6.4",
        sha256="b10bc4199cfefcf1c0e5d932eac89369550320ca4bdf40559328d85f1ca4f655",
        deprecated=True,
    )

    depends_on("c", type="build")

    # pyproject.toml
    with default_args(type="build"):
        depends_on("py-cython", when="@2.0.2:")
        depends_on("py-cython@0.29:0", when="@2.0.0:2.0.1")
        depends_on("py-cython@0.29.24:2", when="@:1")
        depends_on("py-setuptools@61:", when="@2:")
        depends_on("py-setuptools@:63", when="@:1")

    with default_args(type=("build", "link", "run")):
        depends_on("py-numpy@1.14:2", when="@2.0.6:")
        # https://github.com/shapely/shapely/issues/2098
        depends_on("py-numpy@1.14:2.0", when="@2.0.4:2.0.5")
        # https://github.com/shapely/shapely/issues/1972
        depends_on("py-numpy@1.14:1", when="@2.0.0:2.0.3")
        depends_on("py-numpy@:1", when="@1")

    # setup.py
    depends_on("geos@3.5:", when="@2:")
    depends_on("geos@3.3:", when="@:1")

    # https://github.com/shapely/shapely/pull/891
    patch(
        "https://github.com/shapely/shapely/commit/98f6b36710bbe05b4ab59231cb0e08b06fe8b69c.patch?full_index=1",
        sha256="8583cdc97648277fa4faea8bd88d49e43390e87f697b966bd2b4290fba945ba0",
        when="@:1.7.0",
    )

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/{0}/{0}hapely/{0}hapely-{1}.tar.gz"
        if version >= Version("2"):
            letter = "s"
        else:
            letter = "S"
        return url.format(letter, version)

    @when("@:1.8.1")
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
        # https://github.com/shapely/shapely/issues/909
        libs = ":".join(self.spec["geos"].libs.directories)
        if sys.platform == "darwin":
            env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", libs)
        else:
            env.prepend_path("LD_LIBRARY_PATH", libs)

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_build_environment(env)
