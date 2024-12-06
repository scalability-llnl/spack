# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAffine(PythonPackage):
    """Matrices describing affine transformation of the plane."""

    homepage = "https://github.com/sgillies/affine"
    url = "https://github.com/sgillies/affine/archive/2.1.0.zip"

    depends_on("py-setuptools", type="build")

    license("BSD-3-Clause")

    version("2.1.0", sha256="b67b7dee9a9865185a931758a3e347ad8583d0ac985895b90985a477ccfa4745")
