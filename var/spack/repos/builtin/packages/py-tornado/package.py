# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTornado(PythonPackage):
    """Tornado is a Python web framework and asynchronous networking
    library."""

    homepage = "https://github.com/tornadoweb/tornado"
    pypi = "tornado/tornado-6.1.tar.gz"

    license("Apache-2.0")

    version("6.3.3", sha256="e7d8db41c0181c80d76c982aacc442c0783a2c54d6400fe028954201a2e032fe")
    version("6.2", sha256="9b630419bde84ec666bfd7ea0a4cb2a8a651c2d5cccdbdd1972a0c859dfc3c13")
    version("6.1", sha256="33c6e81d7bd55b468d2e793517c909b139960b6c790a60b7991b9b6b76fb9791")
    version("6.0.3", sha256="c845db36ba616912074c5b1ee897f8e0124df269468f25e4fe21fe72f6edd7a9")
    version("5.1.1", sha256="4e5158d97583502a7e2739951553cbd88a72076f152b4b11b64b9a10c4c49409")
    version("4.4", sha256="3176545b6cb2966870db4def4f646da6ab7a0c19400576969c57279a7561ab02")

    depends_on("c", type="build")  # generated

    depends_on("python@3.8:", when="@6.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
