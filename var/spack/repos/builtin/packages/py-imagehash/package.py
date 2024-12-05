# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImagehash(PythonPackage):
    """A Python Perceptual Image Hashing Module"""

    homepage = "https://github.com/JohannesBuchner/imagehash"
    pypi = "ImageHash/ImageHash-4.3.1.tar.gz"

    maintainers("thomas-bouvier")

    license("BSD-2-Clause")

    version("4.3.1", sha256="7038d1b7f9e0585beb3dd8c0a956f02b95a346c0b5f24a9e8cc03ebadaf0aa70")

    depends_on("py-setuptools", type="build")
    depends_on("pil", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pywavelets", type=("build", "run"))
