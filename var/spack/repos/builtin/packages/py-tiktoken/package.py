# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTiktoken(PythonPackage):
    """tiktoken is a fast BPE tokeniser for use with OpenAI's models."""

    homepage = "https://github.com/openai/tiktoken"
    pypi = "tiktoken/tiktoken-0.4.0.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("0.4.0", sha256="59b20a819969735b48161ced9b92f05dc4519c17be4015cfb73b65270a243620")
    version("0.3.1", sha256="8295912429374f5f3c6c6bf053a091ce1de8c1792a62e3b30d4ad36f47fa8b52")

    # From pyproject.toml
    depends_on("py-setuptools@62.4:", type="build")
    depends_on("py-setuptools-rust@1.5.2:", type="build")
    depends_on("py-wheel", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-regex@2022.1.18:", type=("build", "run"))
    depends_on("py-requests@2.26.0:", type=("build", "run"))
