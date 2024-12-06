# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySacrebleu(PythonPackage):
    """SacreBLEU is a standard BLEU implementation that downloads and manages
    WMT datasets, produces scores on detokenized outputs, and reports a string
    encapsulating BLEU parameters, facilitating the production of shareable,
    comparable BLEU scores."""

    homepage = "https://github.com/mjpost/sacrebleu"
    pypi = "sacrebleu/sacrebleu-2.0.0.tar.gz"

    license("Apache-2.0")

    version("2.0.0", sha256="51fb69b6683f1b9999cd180143bb6b21d7841744537c9aab235cfe676550f0cf")

    depends_on("python@3.6.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-portalocker", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-tabulate@0.8.9:", type=("build", "run"))
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))

    def patch(self):
        touch("CHANGELOG.md")
