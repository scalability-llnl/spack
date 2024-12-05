# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlymur(PythonPackage):
    """glymur contains a Python interface to the OpenJPEG
    library which allows one to read and write JPEG 2000 files.
    glymur works on Python 3.7, 3.8, 3.9, and 3.10."""

    homepage = "https://github.com/quintusdias/glymur"
    pypi = "Glymur/Glymur-0.9.9.tar.gz"

    license("MIT")

    version("0.9.9", sha256="25b8a6ac07892c98b4613f959295ada9ca5e76b27bfa25069ab0a8a5bb4048f4")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-setuptools", type="build")
