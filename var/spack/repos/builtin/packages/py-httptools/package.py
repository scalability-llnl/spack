# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttptools(PythonPackage):
    """httptools is a Python binding for the nodejs HTTP parser."""

    homepage = "https://github.com/MagicStack/httptools"
    pypi = "httptools/httptools-0.1.1.tar.gz"

    license("MIT")

    version("0.5.0", sha256="295874861c173f9101960bba332429bb77ed4dcd8cdf5cee9922eb00e4f6bc09")
    version("0.1.1", sha256="41b573cf33f64a8f8f3400d0a7faf48e1888582b6f6e02b82b9bd4f0bf7497ce")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.24:0.29", type="build")
