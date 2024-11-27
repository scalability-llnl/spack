# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpendatalab(PythonPackage):
    """OpenDataLab Python SDK"""

    homepage = "https://github.com/opendatalab/opendatalab-python-sdk"
    pypi = "opendatalab/opendatalab-0.0.9.tar.gz"

    license("MIT")

    version("0.0.9", sha256="4648b66d5be096ba38fa087b6c7906c24218d02a49906c8b41c069b9a8747530")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pycryptodome", type=("build", "run"))
    depends_on("py-click@7:", type=("build", "run"))
    depends_on("py-requests@2.4.2:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    # depends_on("py-pywin32", when="platform=windows", type=("build", "run"))
    conflicts("platform=windows", msg="Requires py-pywin32 to be packaged")
