# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladMetalad(PythonPackage):
    """DataLad extension for semantic metadata handling"""

    homepage = "https://github.com/datalad/datalad-metalad/"
    pypi = "datalad_metalad/datalad_metalad-0.2.1.tar.gz"

    license("MIT")

    version("0.4.17", sha256="8854d5b8bc8387eff27639510f10c3cffe9cd76be018512a5d451be9708242b9")
    version("0.4.5", sha256="db1a0675e3c67fe2d9093e7098b142534f49588dea5ee048ee962422a9927fbf")
    version("0.2.1", sha256="70fe423136a168f7630b3e0ff1951e776d61e7d5f36670bddf24299ac0870285")

    depends_on("py-setuptools@30.3:", type=("build"))
    depends_on("py-setuptools", type=("build"))

    depends_on("py-six", when="@0.3.1:", type=("build", "run"))
    depends_on("py-datalad@0.18:", when="@0.4.11:", type=("build", "run"))
    depends_on("py-datalad@0.15.6:", when="@0.3:", type=("build", "run"))
    depends_on("py-datalad@0.12.3:", type=("build", "run"))
    depends_on("py-datalad-metadata-model@0.3.10:", when="@0.4.12:", type=("build", "run"))
    depends_on("py-datalad-metadata-model@0.3.5:0.3", when="@:0.4.9", type=("build", "run"))
    depends_on("py-datalad-deprecated", when="@0.4.17:", type=("build", "run"))
    depends_on("py-pytest", when="@0.4.11:", type=("build", "run"))
    depends_on("py-pyyaml", when="@0.3.1:", type=("build", "run"))
    depends_on("git-annex", type=("run"))
