# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAlpacaEval(PythonPackage):
    """An automatic evaluator for instruction-following language models.
    Human-validated, high-quality, cheap, and fast."""

    homepage = "https://github.com/tatsu-lab/alpaca_eval"
    pypi = "alpaca_eval/alpaca_eval-0.2.8.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version("0.2.8", sha256="5b21b74d7362ee229481b6a6d826dd620b2ef6b82e4f5470645e0a4b696a31e6")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-python-dotenv", type=("build", "run"))
    depends_on("py-datasets", type=("build", "run"))
    depends_on("py-openai", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-tiktoken@0.3.2:", type=("build", "run"))
    depends_on("py-fire", type=("build", "run"))
