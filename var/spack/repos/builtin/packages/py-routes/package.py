# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRoutes(PythonPackage):
    """Routing Recognition and Generation Tools"""

    homepage = "https://routes.readthedocs.io/"
    pypi = "routes/Routes-2.5.1.tar.gz"

    license("MIT")

    version("2.5.1", sha256="b6346459a15f0cbab01a45a90c3d25caf980d4733d628b4cc1952b865125d053")

    depends_on("py-setuptools", type="build")

    depends_on("py-six", type=("build", "run"))
    depends_on("py-repoze-lru@0.3:", type=("build", "run"))
