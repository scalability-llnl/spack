# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNanomath(PythonPackage):
    """A few simple math function for other Oxford Nanopore processing scripts"""

    homepage = "https://github.com/wdecoster/nanomath"
    pypi = "nanomath/nanomath-1.3.0.tar.gz"

    maintainers("Pandapip1")

    version("1.4.0", sha256="ed7a38fbb156d9a68a95c2570fe3c2035321d0a3e234580496750afca4927ced")
    version("1.3.0", sha256="c35a024b10b34dd8f539cefed1fd69e0a46d18037ca48bed63c7941c67ae028e")

    depends_on("py-setuptools", type=("build",))
    depends_on("py-python-deprecated", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-numpy@1.9:", type=("build", "run"))
