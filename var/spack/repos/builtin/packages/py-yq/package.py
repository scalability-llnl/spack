# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYq(PythonPackage):
    """yq takes YAML input, converts it to JSON, and pipes it to jq"""

    homepage = "https://github.com/kislyuk/yq"
    pypi = "yq/yq-2.12.2.tar.gz"

    maintainers("qwertos")

    license("Apache-2.0")

    version("2.12.2", sha256="2f156d0724b61487ac8752ed4eaa702a5737b804d5afa46fa55866951cd106d2")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-toml@0.10.0:", type=("build", "run"))
    depends_on("py-pyyaml@3.11:", type=("build", "run"))
    depends_on("py-argcomplete@1.8.1:", type=("build", "run"))
    depends_on("py-xmltodict@0.11.0:", type=("build", "run"))
