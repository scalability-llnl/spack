# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTopiaryAsr(PythonPackage):
    """Python framework for doing ancestral sequence reconstruction."""

    homepage = "https://github.com/harmslab/topiary"

    url = "https://github.com/harmslab/topiary/archive/refs/tags/v0.9.9.tar.gz"
    git = "https://github.com/harmslab/topiary.git"

    maintainers("snehring")

    license("MIT")

    version("main", branch="main")
    version("0.9.9", sha256="5601fba92e7add33a3732482426b2c7ef46b0fccc4a4ea11357537e1b937903c")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-numpy@:1.21", type=("build", "run"), when="@0.9.9")
    depends_on("py-numpy", type=("build", "run"), when="@main")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-ete3", type=("build", "run"))
    depends_on("py-toytree", type=("build", "run"))
    depends_on("py-dendropy", type=("build", "run"))
    depends_on("py-pastml", type=("build", "run"))
    depends_on("py-openpyxl", type=("build", "run"))
    depends_on("py-opentree", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-xlrd", type=("build", "run"))
    # while undocumented, this requires mpi4py to run
    depends_on("py-mpi4py", type=("build", "run"))

    # runtime deps from https://topiary-asr.readthedocs.io/en/latest/installation.html#required-libraries
    depends_on("blast-plus", type="run")
    depends_on("muscle5@5.0:", type="run")
    depends_on("generax@2.0:+mpi", type="run")
    depends_on("raxml-ng@1.1:", type="run")

    depends_on("mpi", type="run")
    depends_on(
        "openmpi+legacylaunchers", type="run", when="^[virtuals=mpi] openmpi schedulers=slurm"
    )

    conflicts("^mpich")

    def patch(self):
        if self.spec.satisfies("^raxml-ng+mpi"):
            filter_file(
                r"RAXML_BINARY\s*=\s*\"raxml-ng\"$",
                'RAXML_BINARY = "raxml-ng-mpi"',
                join_path("topiary", "raxml", "_raxml.py"),
            )
            filter_file(
                r"binary\s*=\s*\"raxml-ng\"",
                'binary = "raxml-ng-mpi"',
                join_path("topiary", "_private", "installed.py"),
            )
