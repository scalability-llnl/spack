# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyedr(PythonPackage):
    """Pyedr provides a means of reading a Gromacs EDR binary XDR file and return
    its contents as a dictionary of NumPy arrays"""

    homepage = "https://github.com/MDAnalysis/panedr"
    pypi = "pyedr/pyedr-0.7.1.tar.gz"

    maintainers("RMeli")

    license("LGPL-2.1-or-later")

    version("0.7.2", sha256="8a02b7d94f97f99083c489568f7816ee8ed37e2efca0c1ba3a2e4b83e932d5b9")
    version("0.7.1", sha256="ad7ccdeb739399acd11a25f2d2413ebb46a54223059a2b902ac604d29fabd767")

    # Minimal NumPy version only specified in requirements.txt
    depends_on("py-numpy@1.19.0:", type=("build", "run"))
    depends_on("py-pbr", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-mda-xdrlib", when="@0.7.2:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
