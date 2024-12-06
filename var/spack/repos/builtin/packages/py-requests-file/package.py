# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsFile(PythonPackage):
    """File transport adapter for Requests."""

    homepage = "https://github.com/dashea/requests-file"
    pypi = "requests-file/requests-file-1.5.1.tar.gz"

    maintainers("LydDeb")

    license("Apache-2.0")

    version("1.5.1", sha256="07d74208d3389d01c38ab89ef403af0cfec63957d53a0081d8eca738d0247d8e")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@1.0.0:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
