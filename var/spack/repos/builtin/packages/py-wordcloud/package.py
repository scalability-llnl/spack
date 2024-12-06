# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWordcloud(PythonPackage):
    """A little word cloud generator in Python."""

    homepage = "https://github.com/amueller/word_cloud"
    pypi = "wordcloud/wordcloud-1.8.1.tar.gz"

    license("MIT")

    version("1.8.1", sha256="e6ef771aac17c1cf8558c8d5ef025796184066d7b78f8118aefe011fb0d22952")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.6.1:", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
