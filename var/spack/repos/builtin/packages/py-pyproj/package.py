# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyproj(PythonPackage):
    """Python interface to PROJ (cartographic projections and
    coordinate transformations library)."""

    homepage = "https://github.com/pyproj4/pyproj"
    pypi = "pyproj/pyproj-2.2.0.tar.gz"
    git = "https://github.com/pyproj4/pyproj.git"

    license("MIT")
    maintainers("citibeth", "adamjstewart")

    version("3.7.0", sha256="bf658f4aaf815d9d03c8121650b6f0b8067265c36e31bc6660b98ef144d81813")
    version("3.6.1", sha256="44aa7c704c2b7d8fb3d483bbf75af6cb2350d30a63b144279a09b75fead501bf")
    version("3.6.0", sha256="a5b111865b3f0f8b77b3983f2fbe4dd6248fc09d3730295949977c8dcd988062")
    version("3.5.0", sha256="9859d1591c1863414d875ae0759e72c2cffc01ab989dc64137fbac572cc81bf6")
    version("3.4.1", sha256="261eb29b1d55b1eb7f336127344d9b31284d950a9446d1e0d1c2411f7dd8e3ac")
    version("3.4.0", sha256="a708445927ace9857f52c3ba67d2915da7b41a8fdcd9b8f99a4c9ed60a75eb33")
    version("3.3.1", sha256="b3d8e14d91cc95fb3dbc03a9d0588ac58326803eefa5bbb0978d109de3304fbe")
    version("3.3.0", sha256="ce8bfbc212729e9a643f5f5d77f7a93394e032eda1e2d8799ae902d08add747e")
    version("3.2.1", sha256="4a936093825ff55b24c1fc6cc093541fcf6d0f6d406589ed699e62048ebf3877")
    version("3.2.0", sha256="48df0d5ab085bd2dc6db3bca79e20bf15b08ffca4f4e42df6d87b566633b800c")
    version("3.1.0", sha256="67b94f4e694ae33fc90dfb7da0e6b5ed5f671dd0acc2f6cf46e9c39d56e16e1a")
    version("3.0.1", sha256="bfbac35490dd17f706700673506eeb8170f8a2a63fb5878171d4e6eef242d141")
    version("3.0.0", sha256="539e320d06e5441edadad2e2ab276e1877445eca384fc1c056b5501453d433c2")
    version("2.6.1", sha256="52556f245f1112f121091937b47738d1fbcbd0f13be6fb32689de31ab0975d24")
    version("2.6.0", sha256="977542d2f8cf2981cf3ad72cedfebcd6ac56977c7aa830d9b49fa7888b56e83d")
    version("2.2.0", sha256="0a4f793cc93539c2292638c498e24422a2ec4b25cb47545addea07724b2a56e5")
    version("2.1.3", sha256="99c52788b01a7bb9a88024bf4d40965c0a66a93d654600b5deacf644775f424d")

    # In pyproject.toml
    with default_args(type="build"):
        depends_on("py-setuptools@61:", when="@3.4:")
        depends_on("py-setuptools")
        depends_on("py-cython@3:", when="@3.6.1:")
        depends_on("py-cython@0.28.4:2", when="@2:3.6.0")

    with default_args(type=("build", "link", "run")):
        depends_on("python@3.10:", when="@3.7:")
        depends_on("python@3.9:", when="@3.6:")
        depends_on("python@3.8:", when="@3.3:")

    with default_args(type=("build", "run")):
        depends_on("py-certifi", when="@3:")

    # In setup.py (PROJ_MIN_VERSION)
    # https://pyproj4.github.io/pyproj/stable/installation.html#installing-from-source
    depends_on("proj@9.2:", when="@3.7:")
    depends_on("proj@9:", when="@3.5:")
    depends_on("proj@8.2:", when="@3.4")
    depends_on("proj@8.0:9.1", when="@3.3")
    depends_on("proj@7.2:9.1", when="@3.0.1:3.2")
    depends_on("proj@7.2", when="@3.0.0")
    depends_on("proj@6.2:7", when="@2.4:2.6")
    depends_on("proj@6.1:7", when="@2.2:2.3")
    depends_on("proj@6.0:7", when="@2.0:2.1")
    depends_on("proj")

    def setup_build_environment(self, env):
        # https://pyproj4.github.io/pyproj/stable/installation.html#pyproj-build-environment-variables
        env.set("PROJ_VERSION", self.spec["proj"].version)
        env.set("PROJ_DIR", self.spec["proj"].prefix)
        env.set("PROJ_LIBDIR", self.spec["proj"].libs.directories[0])
        env.set("PROJ_INCDIR", self.spec["proj"].headers.directories[0])
