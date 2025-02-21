# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMemray(PythonPackage):
    """A memory profiler for Python applications."""

    homepage = "https://github.com/bloomberg/memray"
    pypi = "memray/memray-1.1.0.tar.gz"

    license("Apache-2.0")

    version("1.15.0", sha256="1beffa2bcba3dbe0f095d547927286eca46e272798b83026dd1b5db58e16ed56")
    version("1.1.0", sha256="876e46e0cd42394be48b33f81314bc946f4eb023b04bf1def084c25ccf1d2bb6")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("python@3.7:", type=("build", "link", "run"))

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-pkgconfig", when="@1.10:")
        depends_on("py-cython@0.29.31:", when="@1.10:")
        depends_on("py-cython")

    with default_args(type=("build", "run")):
        depends_on("py-jinja2@2.9:", when="@1.10:")
        depends_on("py-jinja2")
        depends_on("py-rich@11.2:", when="@1.10:")
        depends_on("py-rich")
        depends_on("py-textual@0.41:", when="@1.12:")
        depends_on("py-textual@0.34:", when="@1.11:")

    # https://github.com/bloomberg/memray#building-from-source
    depends_on("elfutils", when="platform=linux @1.13:")
    depends_on("libunwind", when="platform=linux")
    depends_on("lz4")

    conflicts("platform=darwin", when="@:1.9", msg="Memray only works on Linux")
    conflicts("platform=windows", msg="Memray only works on Linux and macOS")
