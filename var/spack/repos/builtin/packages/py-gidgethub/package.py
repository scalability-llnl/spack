# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGidgethub(PythonPackage):
    """An async GitHub API library for Python."""

    homepage = "https://github.com/gidgethub/gidgethub"
    pypi = "gidgethub/gidgethub-5.3.0.tar.gz"
    git = "https://github.com/gidgethub/gidgethub.git"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("main", branch="main")
    version("5.3.0", sha256="9ece7d37fbceb819b80560e7ed58f936e48a65d37ec5f56db79145156b426a25")

    variant(
        "aiohttp", default=False, description="Enable aiohttp functionality through dependency."
    )
    variant(
        "tornado", default=False, description="Enable tornado functionality through dependency."
    )

    depends_on("py-flit", type="build", when="@:5.3.0")
    depends_on("py-flit-core", type="build", when="@5.3.1:")

    depends_on("py-uritemplate@3.0.1:", type=("build", "run"))
    depends_on("py-pyjwt+crypto@2.4.0:", type=("build", "run"))

    depends_on("py-aiohttp", type=("build", "run"), when="+aiohttp")
    depends_on("py-tornado", type=("build", "run"), when="+tornado")
