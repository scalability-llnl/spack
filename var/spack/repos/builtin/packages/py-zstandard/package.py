# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyZstandard(PythonPackage):
    """Python bindings to the Zstandard (zstd) compression library."""

    homepage = "https://github.com/indygreg/python-zstandard"
    pypi = "zstandard/zstandard-0.22.0.tar.gz"

    license("BSD", checked_by="teaguesterling")

    version("0.22.0", sha256="8226a33c542bcb54cd6bd0a366067b610b41713b64c9abec1bc4533d69f51e70")

    depends_on("py-cffi@1.16.0:")
    depends_on("py-setuptools@:68", type="build")
    depends_on("zstd")
