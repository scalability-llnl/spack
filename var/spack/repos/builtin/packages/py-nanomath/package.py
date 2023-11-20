# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class PyNanomath(PythonPackage):
    """A few simple math function for other Oxford Nanopore processing scripts"""

    homepage = "https://github.com/wdecoster/nanomath"
    pypi = "nanomath/nanomath-1.3.0.tar.gz"

    version("1.3.0", sha256="c35a024b10b34dd8f539cefed1fd69e0a46d18037ca48bed63c7941c67ae028e")

    depends_on("python@3")
    depends_on("py-pandas")
    depends_on("py-numpy@1.8:")
