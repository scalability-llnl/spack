# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDrmaa(PythonPackage):
    """Python wrapper around the C DRMAA library."""

    homepage = "https://github.com/pygridtools/drmaa-python"
    pypi = "drmaa/drmaa-0.7.9.tar.gz"

    license("BSD-3-Clause")

    version("0.7.9", sha256="12540cd98afc40d5c0b2f38d7b0e46468d1c45192a2f401f41fc2eda9c9f5542")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
