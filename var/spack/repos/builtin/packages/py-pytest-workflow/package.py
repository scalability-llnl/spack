# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestWorkflow(PythonPackage):
    """A workflow-system agnostic testing framework
    that aims to make pipeline/workflow testing easy
    by using YAML files for the test configuration.
    """

    homepage = "https://github.com/LUMC/pytest-workflow"
    pypi = "pytest-workflow/pytest-workflow-1.6.0.tar.gz"

    license("AGPL-3.0-or-later")

    version("1.6.0", sha256="8fb9fb31a6132c783231afbbbb92941297a42713dcd459694b5efe4a13b8cba7")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@51:", type="build")

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pytest@5.4.0:", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
