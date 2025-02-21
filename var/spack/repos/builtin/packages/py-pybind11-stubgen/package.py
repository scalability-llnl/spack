# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybind11Stubgen(PythonPackage):
    """Generates stubs for pybind11-wrapped python modules"""

    homepage = "https://github.com/sizmailov/pybind11-stubgen"
    pypi = "pybind11-stubgen/pybind11-stubgen-2.5.1.tar.gz"

    version("2.5.1", sha256="4427a67038a00c5ac1637ffa6c65728c67c5b1251ecc23c7704152be0b14cc0b")
    version("0.8.7", sha256="79e24009137cd51ef7201c5b9f4d0d072824b260cff751ec8200a8886e06adbf")
    version("0.3.0", sha256="fb9bc977df46d7f1aecd33258e34abbbd01f1f461862c8a2a85341b96e6e6bdf")

    depends_on("py-setuptools", type="build")
