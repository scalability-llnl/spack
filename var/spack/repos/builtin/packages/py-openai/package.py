# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenai(PythonPackage):
    """The OpenAI Python library provides convenient access to the OpenAI API
    from applications written in the Python language. It includes a pre-defined
    set of classes for API resources that initialize themselves dynamically from
    API responses which makes it compatible with a wide range of versions of the
    OpenAI API."""

    homepage = "https://github.com/openai/openai-python"
    pypi = "openai/openai-0.27.8.tar.gz"

    license("MIT")

    version("0.27.8", sha256="2483095c7db1eee274cebac79e315a986c4e55207bb4fa7b82d185b3a2ed9536")

    variant("datalib", default=False, description="facilities for data loading")
    variant(
        "wandb",
        default=False,
        description="keeps track of hyperparameters, system metrics, and predictions",
    )
    variant("embeddings", default=False, description="represents a text string vector")

    depends_on("python@3.7.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.20:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@3.7", type=("build", "run"))
    depends_on("py-aiohttp", type=("build", "run"))

    with when("+datalib"):
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-pandas@1.2.3:", type=("build", "run"))
        depends_on("py-pandas-stubs@1.1.0.11:", type=("build", "run"))
        depends_on("py-openpyxl@3.0.7:", type=("build", "run"))

    with when("+wandb"):
        depends_on("py-wandb", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-pandas@1.2.3:", type=("build", "run"))
        depends_on("py-pandas-stubs@1.1.0.11:", type=("build", "run"))
        depends_on("py-openpyxl@3.0.7:", type=("build", "run"))

    with when("+embeddings"):
        depends_on("py-scikit-learn@1.0.2:", type=("build", "run"))
        depends_on("py-tenacity@8.0.1:", type=("build", "run"))
        depends_on("py-matplotlib", type=("build", "run"))
        depends_on("py-plotly", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-scipy", type=("build", "run"))
        depends_on("py-pandas@1.2.3:", type=("build", "run"))
        depends_on("py-pandas-stubs@1.1.0.11:", type=("build", "run"))
        depends_on("py-openpyxl@3.0.7:", type=("build", "run"))
