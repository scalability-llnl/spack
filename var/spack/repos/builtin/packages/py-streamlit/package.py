# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStreamlit(PythonPackage):
    """The fastest way to build data apps in Python."""

    homepage = "https://streamlit.io/"
    pypi = "streamlit/streamlit-1.20.0.tar.gz"

    version("1.20.0", sha256="f6e257e033a2532ce9b37c425717a4e885fa4d0e339fa5dcdbbda8d75ec191e9")

    depends_on("py-setuptools", type="build")
    depends_on("py-altair@3.2:4", type=("build", "run"))
    depends_on("py-blinker@1:", type=("build", "run"))
    depends_on("py-cachetools@4:", type=("build", "run"))
    depends_on("py-click@7:", type=("build", "run"))
    depends_on("py-importlib-metadata@1.4:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging@14.1:", type=("build", "run"))
    depends_on("py-pandas@0.25:1", type=("build", "run"))
    depends_on("pil@6.2:", type=("build", "run"))
    depends_on("py-protobuf@3.12:3", type=("build", "run"))
    depends_on("py-pyarrow@4:", type=("build", "run"))
    depends_on("py-pympler@0.9:", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-requests@2.4:", type=("build", "run"))
    depends_on("py-rich@10.11:", type=("build", "run"))
    depends_on("py-semver", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", type=("build", "run"))
    depends_on("py-tzlocal@1.1:", type=("build", "run"))
    depends_on("py-validators@0.2:", type=("build", "run"))
    depends_on("py-watchdog", when="platform=linux", type=("build", "run"))
    depends_on("py-watchdog", when="platform=windows", type=("build", "run"))
