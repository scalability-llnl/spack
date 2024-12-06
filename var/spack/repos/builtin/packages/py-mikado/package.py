# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMikado(PythonPackage):
    """Mikado is a lightweight Python3 pipeline whose purpose is to facilitate
    the identification of expressed loci from RNA-Seq data * and to select
    the best models in each locus."""

    homepage = "https://github.com/EI-CoreBioinformatics/mikado"
    pypi = "Mikado/Mikado-1.2.4.tar.gz"

    version("1.2.4", sha256="c0485dba3b7c285599809e058c83f33b5efa9522d20d9f980423410604207f61")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel@0.28.0:", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-cython@0.25:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-networkx@1.10:", type=("build", "run"))
    depends_on("py-sqlalchemy@1:", type=("build", "run"))
    depends_on("py-sqlalchemy-utils", type=("build", "run"))
    depends_on("py-biopython@1.66:", type=("build", "run"))
    depends_on("py-intervaltree", type=("build", "run"))
    depends_on("py-nose", type=("build", "run"))
    depends_on("py-pyfaidx", type=("build", "run"))
    depends_on("py-scikit-learn@0.17.0:", type=("build", "run"))
    depends_on("py-scipy@0.15.0:", type=("build", "run"))
    depends_on("py-python-magic", type=("build", "run"))
    depends_on("py-drmaa", type=("build", "run"))
    depends_on("snakemake", type=("build", "run"))
    depends_on("py-docutils@:0.13.0,0.13.2:", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-ujson", type=("build", "run"))
    depends_on("py-simplejson", type=("build", "run"))
    depends_on("python@3.4:", type=("build", "run"))
