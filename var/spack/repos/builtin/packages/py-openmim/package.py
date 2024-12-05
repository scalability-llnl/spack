# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenmim(PythonPackage):
    """MIM Installs OpenMMLab packages"""

    homepage = "https://github.com/open-mmlab/mim"
    pypi = "openmim/openmim-0.3.9.tar.gz"

    license("Apache-2.0")

    version("0.3.9", sha256="b3977b92232b4b8c4d987cbc73e4515826d5543ccd3a66d49fcfc602cc5b3352")

    depends_on("py-setuptools", type="build")
    depends_on("py-click", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-model-index", type=("build", "run"))
    depends_on("py-opendatalab", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pip@19.3:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
