# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytng(PythonPackage):
    """Provides the TNGFileIterator object to allow simple Pythonic
    access to data contained within TNG files.
    """

    homepage = "https://pypi.org/project/pytng/"
    pypi = "pytng/pytng-0.3.0.tar.gz"

    maintainers("RMeli")

    license("BSD-3-Clause")

    version("0.3.0", sha256="f563f9ea260ca8c8e17b3bcf9458bae35aedd5c58e1c5ac4dfff77a1e036506e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-cython@0.28:2", type="build")
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.20.0:", type=("build", "run"))
