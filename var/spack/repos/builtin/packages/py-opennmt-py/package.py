# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpennmtPy(PythonPackage):
    """OpenNMT-py is the PyTorch version of the OpenNMT project, an open-source
    (MIT) neural machine translation (and beyond!) framework. It is designed to be
    research friendly to try out new ideas in translation, language modeling,
    summarization, and many other NLP tasks."""

    homepage = "https://github.com/OpenNMT/OpenNMT-py/"
    pypi = "OpenNMT-py/OpenNMT-py-3.1.1.tar.gz"

    maintainers("meyersbs")

    version("3.1.1", sha256="2191d17df6872ebc0e4f5886a35eb22d49c92528bd6eb019d01b2c46247dcc71")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-torch@1.13:1", type=("build", "run"))
    depends_on("py-configargparse", type=("build", "run"))
    depends_on("py-ctranslate2@3.2:3", type=("build", "run"))
    depends_on("py-tensorboard@2.3:", type=("build", "run"))
    depends_on("py-flask", type=("build", "run"))
    depends_on("py-waitress", type=("build", "run"))
    depends_on("py-pyonmttok@1.35:1", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-sacrebleu", type=("build", "run"))
    depends_on("py-rapidfuzz", type=("build", "run"))
    depends_on("py-pyahocorasick", type=("build", "run"))
