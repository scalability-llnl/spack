# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTreehash(PythonPackage):
    """Calculates a SHA256 (or, potentially, any other hashlib supported
    function) "tree" hash, as used by e.g. Amazon Glacier."""

    homepage = "https://github.com/jdswinbank/treehash"
    pypi = "treehash/TreeHash-1.0.2.tar.gz"

    version("1.0.2", sha256="fefcadd6a1e8ba2808897d776d5ae8bdae56ec3fe90ed385c1322357269f27a4")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
