# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBrotlipy(PythonPackage):
    """Python binding to the Brotli library."""

    homepage = "https://github.com/python-hyper/brotlipy/"
    pypi = "brotlipy/brotlipy-0.7.0.tar.gz"

    license("MIT")

    version("0.7.0", sha256="36def0b859beaf21910157b4c33eb3b06d8ce459c942102f16988cca6ea164df")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.0.0:", type=("build", "run"))

    # TODO: Builds against internal copy of headers, doesn't seem to be a way
    # to use external brotli installation
    # depends_on('brotli')
