# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQudida(PythonPackage):
    """QuDiDA is a micro library for very naive though quick
    pixel level image domain adaptation via scikit-learn
    transformers."""

    homepage = "https://github.com/arsenyinfo/qudida"
    pypi = "qudida/qudida-0.0.4.tar.gz"

    version("0.0.4", sha256="db198e2887ab0c9aa0023e565afbff41dfb76b361f85fd5e13f780d75ba18cc8")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@0.18:", type=("build", "run"))
    depends_on("py-scikit-learn@0.19.1:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("opencv@4.0.1:+python3", type=("build", "run"))
