# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInquirerpy(PythonPackage):
    """Python port of Inquirer.js
    (A collection of common interactive command-line user interfaces).
    """

    homepage = "https://github.com/kazhala/InquirerPy"
    pypi = "inquirerpy/InquirerPy-0.3.4.tar.gz"

    license("MIT")

    version("0.3.4", sha256="89d2ada0111f337483cb41ae31073108b2ec1e618a49d7110b0d7ade89fc197e")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-prompt-toolkit@3.0.1:3", type=("build", "run"))
    depends_on("py-pfzy@0.3.1:0.3", type=("build", "run"))
