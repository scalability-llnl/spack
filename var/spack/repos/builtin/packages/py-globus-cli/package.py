# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlobusCli(PythonPackage):
    """Globus CLI is a standalone application that can be installed on the user's machine
    and is used to access the Globus service. The CLI provides an interface to Globus
    services from the shell, and is suited to both interactive and simple scripting use cases."""

    homepage = "https://docs.globus.org/cli"
    git = "https://github.com/globus/globus-cli.git"
    url = "https://github.com/globus/globus-cli/archive/refs/tags/3.16.0.zip"

    maintainers("climbfuji")

    version("3.16.0", sha256="0ef721060870d9346505e52b9bf30c7bed6ae136cc08762deb2f8893bd25d8c5")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-globus-sdk@3.25.0", type=("build", "run"))
    depends_on("py-click@8", type=("build", "run"))
    depends_on("py-jmespath@1.0.1", type=("build", "run"))
    depends_on("py-packaging@17:", type=("build", "run"))
