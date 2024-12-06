# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyspellchecker(PythonPackage):
    """Pure python spell checker based on work by Peter Norvig"""

    homepage = "https://github.com/barrust/pyspellchecker"
    pypi = "pyspellchecker/pyspellchecker-0.6.2.tar.gz"

    license("MIT")

    version("0.6.2", sha256="af6a1d0393a175499475a873f31e52135f1efd5fc912c979101b795b3c2ee77f")

    depends_on("python@3.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
