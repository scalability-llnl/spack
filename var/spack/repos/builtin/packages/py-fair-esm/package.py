# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFairEsm(PythonPackage):
    """Evolutionary Scale Modeling"""

    homepage = "https://github.com/facebookresearch/esm"
    pypi = "fair-esm/fair-esm-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="4ed34d4598ec75ed6550a4e581d023bf8d4a8375317ecba6269bb68135f80c85")

    depends_on("py-setuptools@59.5.0:", type=("build"))

    variant("esmfold", default=True, description="Enable dependencies for OpenFold")
    depends_on("py-biopython@1.79:", when="+esmfold", type=("build", "run"))

    depends_on("py-deepspeed", type=("build", "run"))
    depends_on("py-dm-tree", type=("build", "run"))
    depends_on("py-pytorch-lightning", type=("build", "run"))
    depends_on("py-omegaconf", type=("build", "run"))
    depends_on("py-ml-collections", type=("build", "run"))
    depends_on("py-einops", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
