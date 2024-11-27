# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExifread(PythonPackage):
    """Read Exif metadata from tiff and jpeg files."""

    homepage = "https://github.com/ianare/exif-py"
    pypi = "ExifRead/ExifRead-2.3.2.tar.gz"

    license("BSD-3-Clause")

    version("3.0.0", sha256="0ac5a364169dbdf2bd62f94f5c073970ab6694a3166177f5e448b10c943e2ca4")
    version("2.3.2", sha256="a0f74af5040168d3883bbc980efe26d06c89f026dc86ba28eb34107662d51766")

    depends_on("py-setuptools", type="build")
