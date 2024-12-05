# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGtdbtk(PythonPackage):
    """GTDB-Tk is a software toolkit for assigning objective taxonomic
    classifications to bacterial and archaeal genomes based on the Genome
    Database Taxonomy (GTDB)."""

    homepage = "https://github.com/Ecogenomics/GTDBTk"
    pypi = "gtdbtk/gtdbtk-2.1.0.tar.gz"

    license("GPL-3.0-only")

    version("2.3.2", sha256="80efd31e10007d835f56a3d6fdf039a59db3b6ba4be26b234692da5e688aa99f")
    version("2.3.0", sha256="4f237a03657be4540ac653c276fe31c002b6923af0411316719a9541d6e97d4b")
    version("2.1.0", sha256="980885141f13502afdf05e720871427e3de4fe27f4f3f97e74af6fed87eb50a7")

    depends_on("py-setuptools", type=("build"))
    depends_on("py-dendropy@4.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.9.0:", type=("build", "run"))
    depends_on("py-tqdm@4.35.0:", type=("build", "run"))
    depends_on("py-pydantic@1.9.2:1", type=("build", "run"), when="@2.3.0:")
    depends_on("prodigal@2.6.2:", type=("build", "run"))
    depends_on("hmmer@3.1b2:", type=("build", "run"))
    depends_on("pplacer@1.1alpha:", type=("build", "run"))
    depends_on("fastani@1.32:", type=("build", "run"))
    depends_on("fasttree@2.1.9:", type=("build", "run"))
    depends_on("mash@2.2:", type=("build", "run"))
