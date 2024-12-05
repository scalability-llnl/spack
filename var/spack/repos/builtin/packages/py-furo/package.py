# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuro(PythonPackage):
    """A clean customisable Sphinx documentation theme.."""

    homepage = "https://github.com/pradyunsg/furo"
    pypi = "furo/furo-2023.5.20.tar.gz"

    license("MIT")

    version("2024.7.18", sha256="37b08c5fccc95d46d8712c8be97acd46043963895edde05b0f4f135d58325c83")
    version("2024.5.6", sha256="81f205a6605ebccbb883350432b4831c0196dd3d1bc92f61e1f459045b3d2b0b")
    version("2024.4.27", sha256="15a9b65269038def2cefafb86c71c6616e3969b8f07ba231f588c10c4aee6d88")
    version("2024.1.29", sha256="4d6b2fe3f10a6e36eb9cc24c1e7beb38d7a23fc7b3c382867503b7fcac8a1e02")
    version("2023.9.10", sha256="5707530a476d2a63b8cad83b4f961f3739a69f4b058bcf38a03a39fa537195b2")
    version("2023.5.20", sha256="40e09fa17c6f4b22419d122e933089226dcdb59747b5b6c79363089827dea16f")

    depends_on("py-sphinx-theme-builder@0.2.0a10:", type="build")

    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-sphinx@6:7", type=("build", "run"))
    depends_on("py-sphinx-basic-ng@1.0.0b2:", type=("build", "run"))
    depends_on("py-pygments@2.7:", type=("build", "run"))
