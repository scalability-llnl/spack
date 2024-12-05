# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpglib(PythonPackage):
    """Python bindings for C library for finding and handling
    crystal symmetries."""

    homepage = "https://spglib.readthedocs.io/en/latest/"
    pypi = "spglib/spglib-1.9.9.18.tar.gz"
    git = "https://github.com/spglib/spglib.git"

    license("BSD-3-Clause")

    version("2.0.2", sha256="1d081ec22da4ab4fc3198e9445ddad6dec2261c43927831151d93e39422610aa")
    version("1.16.1", sha256="9fd2fefbd83993b135877a69c498d8ddcf20a9980562b65b800cfb4cdadad003")
    version("1.9.9.18", sha256="cbbb8383320b500dc6100b83d5e914a26a97ef8fc97c82d8921b10220e4126cd")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@18.0:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    # https://github.com/spglib/spglib/issues/407
    depends_on("py-numpy@:1", type=("build", "run"))
