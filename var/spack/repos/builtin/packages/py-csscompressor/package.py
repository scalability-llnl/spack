# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCsscompressor(PythonPackage):
    """Port of YUI CSS Compressor to Python."""

    pypi = "csscompressor/csscompressor-0.9.5.tar.gz"
    homepage = "https://github.com/sprymix/csscompressor"

    license("BSD", checked_by="lizzyd710")

    version("0.9.5", sha256="afa22badbcf3120a4f392e4d22f9fff485c044a1feda4a950ecc5eba9dd31a05")

    depends_on("py-setuptools", type="build")
