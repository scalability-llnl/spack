# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonXmpToolkit(PythonPackage):
    """Python XMP Toolkit for working with metadata."""

    homepage = "https://github.com/python-xmp-toolkit/python-xmp-toolkit"
    pypi = "python-xmp-toolkit/python-xmp-toolkit-2.0.1.tar.gz"

    license("BSD-3-Clause")

    version("2.0.1", sha256="f8d912946ff9fd46ed5c7c355aa5d4ea193328b3f200909ef32d9a28a1419a38")

    depends_on("python@2.6:2.7,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytz", type=("build", "run"))
    depends_on("exempi@2.2.0:", type=("build", "run"))
