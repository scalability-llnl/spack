# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpacyLoggers(PythonPackage):
    """Logging utilities for SpaCy"""

    homepage = "https://github.com/explosion/spacy-loggers"
    pypi = "spacy-loggers/spacy-loggers-1.0.4.tar.gz"

    license("MIT")

    version("1.0.4", sha256="e6f983bf71230091d5bb7b11bf64bd54415eca839108d5f83d9155d0ba93bf28")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
