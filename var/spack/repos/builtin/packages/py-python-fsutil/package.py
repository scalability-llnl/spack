# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonFsutil(PythonPackage):
    """file-system utilities for lazy devs."""

    homepage = "https://github.com/fabiocaccamo/python-fsutil"
    pypi = "python-fsutil/python-fsutil-0.4.0.tar.gz"

    license("MIT")

    version("0.4.0", sha256="873eceb11fb488fc2d7675cd1bc74a743502f674f0be88f5e7b920c7baeefed6")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-setuptools", type="build")
