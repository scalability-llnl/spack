# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUcMicroPy(PythonPackage):
    """Micro subset of unicode data files for linkify-it-py projects."""

    homepage = "https://github.com/tsutsu3/uc.micro-py"
    pypi = "uc-micro-py/uc-micro-py-1.0.2.tar.gz"

    license("MIT")

    version("1.0.2", sha256="30ae2ac9c49f39ac6dce743bd187fcd2b574b16ca095fa74cd9396795c954c54")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
