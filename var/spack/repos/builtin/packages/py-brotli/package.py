# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBrotli(PythonPackage):
    """Python bindings for the Brotli compression library."""

    homepage = "https://github.com/google/brotli"
    pypi = "Brotli/Brotli-1.1.0.tar.gz"

    license("MIT")

    version("1.1.0", sha256="81de08ac11bcb85841e440c13611c00b67d3bf82698314928d0b676362546724")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
