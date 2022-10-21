# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyInstrain(PythonPackage):
    """inStrain is python program for analysis of co-occurring genome
    populations from metagenomes that allows highly accurate genome
    comparisons, analysis of coverage, microdiversity, and linkage, and
    sensitive SNP detection with gene localization and synonymous
    non-synonymous identification."""

    homepage = "https://github.com/MrOlm/instrain"
    pypi = "inStrain/inStrain-1.5.7.tar.gz"

    variant(
        "coverm",
        default=False,
        description="Enables quick_profile operation"
    )
    variant(
        "prodigal",
        default=False,
        description="Enables profiling on a gene by gene level"
    )

    version("1.5.7", sha256="c5dcb01dae244927fe987b5f0695d895ccf521c9dfd87a2cb59057ad50bd9bfa")

    depends_on("python@3.4.0:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@0.25:1.1.2,1.1.4:", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-biopython@:1.74", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-pytest", type=("build"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pysam@0.15:", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-lmfit", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("samtools", type=("build", "run"))
    # Optional dependencies
    depends_on("coverm", type=("build", "run"), when="+coverm")
    depends_on("prodigal", type=("build", "run"), when="+prodigal")
