# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrieregex(PythonPackage):
    """Build efficient trie-based regular expressions from large word lists"""

    homepage = "https://github.com/ermanh/trieregex"
    pypi = "trieregex/trieregex-1.0.0.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("1.0.0", sha256="a34dd31d04aa169e1989971a315fcbd524126330c7f2f9f16991b0a8c9084eaf")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
