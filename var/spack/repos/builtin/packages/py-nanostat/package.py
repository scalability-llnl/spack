# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNanostat(PythonPackage):
    """Calculate statistics for Oxford Nanopore sequencing data and alignments"""

    homepage = "https://github.com/wdecoster/nanostat"
    pypi = "NanoStat/NanoStat-1.6.0.tar.gz"

    maintainers("Pandapip1")

    version("1.6.0", sha256="e45fa8d1ab49bdaed17596c26c0af148b44e4af46238391a8bb7a1b4cc940079")

    depends_on("py-setuptools", type=("build",))
    depends_on("py-nanoget@1.13.2:", type=("build", "run"))
    depends_on("py-nanomath@1.0.0:", type=("build", "run"))
