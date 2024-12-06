# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiosqlite(PythonPackage):
    """asyncio bridge to the standard sqlite3 module"""

    homepage = "https://aiosqlite.omnilib.dev"
    pypi = "aiosqlite/aiosqlite-0.17.0.tar.gz"

    license("MIT")

    version("0.17.0", sha256="f0e6acc24bc4864149267ac82fb46dfb3be4455f99fe21df82609cc6e6baee51")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.2:", type=("build", "run"))
    depends_on("py-flit-core@2:3", type="build")

    # aiosqlite.test requires aiounittests, not yet in spack
    import_modules = ["aiosqlite"]
