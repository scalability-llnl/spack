# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycifrw(PythonPackage):
    """Python library for interacting with Crystallographic Information
    Framework (CIF) files."""

    homepage = "https://bitbucket.org/jamesrhester/pycifrw/src/development/"
    pypi = "PyCifRW/PyCifRW-4.4.1.tar.gz"

    license("Python-2.0")

    version("4.4.6", sha256="02bf5975e70ab71540bff62fbef3e8354ac707a0f0ab914a152047962891ef15")
    version("4.4.1", sha256="cef7662f475e0eb78a55c2d55774d474e888c96b0539e5f08550afa902cdc4e1")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
