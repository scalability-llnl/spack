# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFilterpy(PythonPackage):
    """This library provides Kalman filtering and various
    related optimal and non-optimal filtering software written
    in Python."""

    homepage = "https://github.com/rlabbe/filterpy/"
    pypi = "filterpy/filterpy-1.4.5.zip"

    license("MIT")

    version("1.4.5", sha256="4f2a4d39e4ea601b9ab42b2db08b5918a9538c168cff1c6895ae26646f3d73b1")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
