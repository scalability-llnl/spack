# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonEngineio(PythonPackage):
    """Engine.IO is the implementation of transport-based
    cross-browser/cross-device bi-directional communication
    layer for Socket.IO."""

    homepage = "https://python-engineio.readthedocs.io/en/latest/"
    url = "https://github.com/miguelgrinberg/python-engineio/archive/v2.0.2.tar.gz"

    version("2.0.2", sha256="9fbe531108a95bc61518b61c4718e2661fc81d32b54fd6af34799bf10a367a6b")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.9.0:", type=("build", "run"))
