# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCwlUpgrader(PythonPackage):
    """Common Workflow Language standalone document upgrader"""

    homepage = "https://github.com/common-workflow-language/cwl-upgrader"
    pypi = "cwl-upgrader/cwl-upgrader-1.2.4.tar.gz"

    license("Apache-2.0")

    version("1.2.4", sha256="b25fc236407343d44cc830ac3f63eed395b8d872fc7e17db92cde583d4a3b2ec")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-ruamel-yaml@0.16.0:0.17.21", when="^python@3.10:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.15.98:0.17.21", when="^python@3.9:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.15.78:0.17.21", when="^python@3.8:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.15.71:0.17.21", type=("build", "run"))
    depends_on("py-schema-salad", type=("build", "run"))
