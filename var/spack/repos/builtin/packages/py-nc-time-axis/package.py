# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNcTimeAxis(PythonPackage):
    """cftime support for matplotlib axis."""

    homepage = "https://github.com/scitools/nc-time-axis"
    pypi = "nc-time-axis/nc-time-axis-1.1.0.tar.gz"

    license("BSD-3-Clause")

    version("1.4.1", sha256="72d80f492f34bbf59490838d8cb3d92f14e88900b0ee35498b2b33c82795eb81")
    version("1.1.0", sha256="ea9d4f7f9e9189c96f7d320235ac6c4be7f63dc5aa256b3ee5d5cca5845e6e26")

    depends_on("python@3.7:", when="@1.4.1:")
    depends_on("python@3.7:3.11", when="@1.1.0")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@42:", type="build", when="@1.4.1:")
    depends_on("py-setuptools-scm@6.0: +toml", type="build", when="@1.4.1:")
    depends_on("py-cftime", type=("build", "run"))
    depends_on("py-cftime@1.5:", type="build", when="@1.4.1:")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"), when="@1.1.0")

    requires("@1.4.1:", when="^python@3.12:")
