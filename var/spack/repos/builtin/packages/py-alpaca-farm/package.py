# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAlpacaFarm(PythonPackage):
    """AlpacaFarm is a simulator that enables research and development on learning
    from feedback at a fraction of the usual cost, promoting accessible research on
    instruction following and alignment."""

    homepage = "https://github.com/tatsu-lab/alpaca_farm"
    pypi = "alpaca_farm/alpaca_farm-0.1.9.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version("0.1.9", sha256="1039d33c814d0bbbcab6a0e77ed8e897992ad7107d5c4999d56bdad7e0b0a59f")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-datasets", type=("build", "run"))
    depends_on("py-einops", type=("build", "run"))
    depends_on("py-nltk", type=("build", "run"))
    depends_on("py-accelerate@0.18.0:", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-transformers@4.26.0:", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
    depends_on("py-tiktoken@0.3.2:", type=("build", "run"))
    depends_on("py-markdown", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-sentencepiece", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-wandb", type=("build", "run"))
    depends_on("py-torch@1.13.1:", type=("build", "run"))
    depends_on("py-fire", type=("build", "run"))
    depends_on("py-openai", type=("build", "run"))
    depends_on("py-alpaca-eval@0.2.8:", type=("build", "run"))
