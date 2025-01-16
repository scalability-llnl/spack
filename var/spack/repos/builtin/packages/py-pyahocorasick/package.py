# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyahocorasick(PythonPackage):
    """pyahocorasick is a fast and memory efficient library for exact or approximate
    multi-pattern string search meaning that you can find multiple key strings
    occurrences at once in some input text. The strings 'index' can be built ahead
    of time and saved (as a pickle) to disk to reload and reuse later."""

    homepage = "http://github.com/WojciechMula/pyahocorasick"
    pypi = "pyahocorasick/pyahocorasick-2.0.0.tar.gz"

    maintainers("meyersbs")

    version("2.0.0", sha256="2985cac6d99c0e9165617fe154b4db0b50c4c2819791c2ad5f0aac0c6a6e58c5")

    # From setup.py
    depends_on("py-setuptools", type="build")
    depends_on("python@3.6:", type=("build", "run"))
