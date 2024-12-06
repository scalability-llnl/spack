# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRatelim(PythonPackage):
    """Makes it easy to respect rate limits."""

    homepage = "https://github.com/themiurgo/ratelim"
    pypi = "ratelim/ratelim-0.1.6.tar.gz"

    license("MIT")

    version("0.1.6", sha256="826d32177e11f9a12831901c9fda6679fd5bbea3605910820167088f5acbb11d")

    depends_on("py-setuptools", type="build")
    depends_on("py-decorator", type=("build", "run"))
