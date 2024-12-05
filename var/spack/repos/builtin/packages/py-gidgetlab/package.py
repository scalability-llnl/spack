# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGidgetlab(PythonPackage):
    """An asynchronous GitLab API library."""

    homepage = "https://gitlab.com/beenje/gidgetlab"
    pypi = "gidgetlab/gidgetlab-1.1.0.tar.gz"
    git = "https://gitlab.com/beenje/gidgetlab.git"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("main", branch="main")
    version("1.1.0", sha256="314ec2cddc898317ec45d99068665dbf33c0fee1f52df6671f28ad35bb51f902")

    variant(
        "aiohttp", default=False, description="Enable aiohttp functionality through dependency."
    )

    depends_on("py-setuptools@45:", type=("build", "run"))
    depends_on("py-setuptools-scm@6.2:", type="build")

    depends_on("py-aiohttp", type=("build", "run"), when="+aiohttp")
    depends_on("py-cachetools", type=("build", "run"), when="+aiohttp")
