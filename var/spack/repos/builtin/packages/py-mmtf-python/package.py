# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMmtfPython(PythonPackage):
    """The macromolecular transmission format (MMTF) is a binary encoding of
    biological structures."""

    homepage = "https://github.com/rcsb/mmtf-python"
    pypi = "mmtf-python/mmtf-python-1.1.2.tar.gz"

    license("Apache-2.0")

    version("1.1.2", sha256="a5caa7fcd2c1eaa16638b5b1da2d3276cbd3ed3513f0c2322957912003b6a8df")

    depends_on("py-setuptools", type="build")
    depends_on("py-msgpack@0.5.6:", type=("build", "run"))
