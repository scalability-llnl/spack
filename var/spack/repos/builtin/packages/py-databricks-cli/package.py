# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatabricksCli(PythonPackage):
    """A command line interface for Databricks."""

    homepage = "https://pypi.org/project/databricks-cli/"
    pypi = "databricks-cli/databricks-cli-0.17.4.tar.gz"

    version("0.17.4", sha256="bc0c4dd082f033cb6d7978cacaca5261698efe3a4c70f52f98762c38db925ce0")
    version("0.14.3", sha256="bdf89a3917a3f8f8b99163e38d40e66dc478c7408954747f145cd09816b05e2c")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-pyjwt@1.7.0:", type=("build", "run"))
    depends_on("py-oauthlib@3.1.0:", type=("build", "run"))
    depends_on("py-requests@2.17.3:", type=("build", "run"))
    depends_on("py-tabulate@0.7.7:", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
