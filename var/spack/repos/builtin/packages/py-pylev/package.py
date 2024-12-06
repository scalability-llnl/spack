# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylev(PythonPackage):
    """A pure Python Levenshtein implementation that's not freaking GPL'd."""

    homepage = "https://github.com/toastdriven/pylev"
    pypi = "pylev/pylev-1.4.0.tar.gz"

    license("BSD-3-Clause")

    version("1.4.0", sha256="9e77e941042ad3a4cc305dcdf2b2dec1aec2fbe3dd9015d2698ad02b173006d1")

    depends_on("python@2.7,3.3:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
