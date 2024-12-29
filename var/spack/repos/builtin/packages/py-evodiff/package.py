# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEvodiff(PythonPackage):
    """Python package for generation of protein sequences and evolutionary alignments via \
        discrete diffusion models"""

    homepage = "https://github.com/microsoft/evodiff"
    pypi = "evodiff/evodiff-1.1.0.tar.gz"

    license("MIT", checked_by="ashim-mahara")

    version("1.1.0", sha256="c1f2d7bd0e46ad244f1c55066caefc5ad9b1bcf4e836be1832311b8cd74e923f")

    depends_on("py-setuptools@61.0:", type=("build"))

    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-lmdb", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-sequence-models", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-blosum", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-fair-esm", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-biotite", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-mdanalysis", type=("build", "run"))
    depends_on("py-pdb-tools", type=("build", "run"))

    # listed in the file setup.py but is not used anywhere in the source code
    # depends_on("py-mlflow", type=("build", "run"))
