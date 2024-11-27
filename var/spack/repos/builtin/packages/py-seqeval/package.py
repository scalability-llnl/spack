# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySeqeval(PythonPackage):
    """seqeval is a Python framework for sequence labeling
    evaluation. seqeval can evaluate the performance of
    chunking tasks such as named-entity recognition,
    part-of-speech tagging, semantic role labeling and so on."""

    homepage = "https://github.com/chakki-works/seqeval"
    pypi = "seqeval/seqeval-1.2.2.tar.gz"

    license("MIT")

    version("1.2.2", sha256="f28e97c3ab96d6fcd32b648f6438ff2e09cfba87f05939da9b3970713ec56e6f")

    depends_on("python@2.6:2,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.14:", type=("build", "run"))
    depends_on("py-scikit-learn@0.21.3:", type=("build", "run"))
