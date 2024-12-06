# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycorenlp(PythonPackage):
    """Python wrapper for Stanford CoreNLP. This simply wraps the API from the server
    included with CoreNLP."""

    homepage = "https://github.com/smilli/py-corenlp"
    pypi = "pycorenlp/pycorenlp-0.3.0.tar.gz"

    maintainers("meyersbs")

    version("0.3.0", sha256="3af60c557b23868659c0784efa1818f4c57c7b826b3e8f000d508aa17e62b67a")

    # From setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-requests", type=("build", "run"))
    # From README
    depends_on("corenlp@3.6.0:", type=("build", "run"))
