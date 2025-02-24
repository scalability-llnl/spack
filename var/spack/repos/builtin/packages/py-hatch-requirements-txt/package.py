# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchRequirementsTxt(PythonPackage):
    """Hatchling plugin to read project dependencies from requirements.txt"""

    homepage = "https://github.com/repo-helper/hatch-requirements-txt"
    pypi = "hatch_requirements_txt/hatch_requirements_txt-0.4.0.tar.gz"

    license("MIT")

    version("0.4.1", sha256="2c686e5758fd05bb55fa7d0c198fdd481f8d3aaa3c693260f5c0d74ce3547d20")
    version("0.4.0", sha256="800509946e85d9e56d73242fab223ec36db50372e870a04e2dd1fd9bad98455d")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-hatchling@0.21:", type=("build", "run"))
    depends_on("py-packaging@21.3:", type=("build", "run"))
