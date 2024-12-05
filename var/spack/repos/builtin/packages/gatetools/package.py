# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gatetools(PythonPackage):
    """Python tools for GATE, see https://github.com/OpenGATE/Gate"""

    homepage = "https://github.com/OpenGATE/GateTools"
    pypi = "gatetools/gatetools-0.9.14.tar.gz"

    license("LGPL-3.0-only")

    version("0.12.1", sha256="eb4847442594e466f0fc01eb5ff1eb89f1dfc4e4b5968d611dacb75a88d24013")
    version("0.11.2", sha256="6eef8a779278b862823ae79d6aab210db4f7889c9127b2c2e4c3a4195f9a9928")
    version("0.9.14", sha256="78fe864bb52fd4c6aeeee90d8f6c1bc5406ce02ac6f48712379efac606b5c006")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pydicom", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-colored", type=("build", "run"))
    depends_on("py-itk@5.1.0:", type=("build", "run"))
    depends_on("py-uproot3", type=("build", "run"))
    depends_on("py-wget", type=("build", "run"))
    depends_on("py-python-box", type=("build", "run"), when="@0.11.2:")
    depends_on("py-lz4", type=("build", "run"), when="@0.11.2:")
    depends_on("py-colorama", type=("build", "run"), when="@0.11.2:")
    depends_on("py-xxhash", type=("build", "run"), when="@0.11.2:")
    depends_on("gate+rtk", type="run")

    # The readme.md file is not in the distribution, so fake it.
    @run_before("install")
    def readme(self):
        touch("readme.md")
