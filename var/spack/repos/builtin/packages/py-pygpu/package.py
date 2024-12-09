# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygpu(PythonPackage):
    """Python packge for the libgpuarray C library."""

    homepage = "https://github.com/Theano/libgpuarray"
    url = "https://github.com/Theano/libgpuarray/archive/v0.6.1.tar.gz"

    version("0.7.6", sha256="ad1c00dd47c3d36ee1708e5167377edbfcdb7226e837ef9c68b841afbb4a4f6a")
    version("0.7.5", sha256="39c4d2e743848be43c8819c736e089ae51b11aa446cc6ee05af945c2dfd63420")
    version("0.7.2", sha256="ef11ee6f8d62d53831277fd3dcab662aa770a5b5de2d30fe3018c4af959204da")
    version("0.7.1", sha256="4d0f9dd63b0595a8c04d8cee91b2619847c033b011c71d776caa784322382ed6")
    version("0.7.0", sha256="afe7907435dcbf78b3ea9b9f6c97e5a0d4a219a7170f5025ca0db1c289bb88df")
    version("0.6.9", sha256="689716feecb4e495f4d383ec1518cf3ba70a2a642a903cc445b6b6ffc119bc25")
    version("0.6.2", sha256="04756c6270c0ce3b91a9bf01be38c4fc743f5356acc18d9f807198021677bcc8")
    version("0.6.1", sha256="b2466311e0e3bacdf7a586bba0263f6d232bf9f8d785e91ddb447653741e6ea5")
    version("0.6.0", sha256="a58a0624e894475a4955aaea25e82261c69b4d22c8f15ec07041a4ba176d35af")

    depends_on("c", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    depends_on("libgpuarray@0.7.6", when="@0.7.6")
    depends_on("libgpuarray@0.7.5", when="@0.7.5")
    depends_on("libgpuarray")
    # not just build-time, requires pkg_resources
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-cython@0.25:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("py-mako@0.7:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
