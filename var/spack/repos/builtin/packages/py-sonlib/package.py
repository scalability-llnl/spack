# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySonlib(PythonPackage):
    """Small general purpose library for C and
    Python with focus on bioinformatics."""

    # Note that there are a few versions of sonLib floating around
    # the one from the ComparativeGenomicsToolkit seems to be the
    # actively developed version

    # There are no releases so we have devel and a commit
    # to fix the code at one point in time (1st April)

    homepage = "https://github.com/ComparativeGenomicsToolkit/sonLib"
    url = "https://github.com/ComparativeGenomicsToolkit/sonLib"
    git = "https://github.com/ComparativeGenomicsToolkit/sonLib.git"

    license("MIT")

    version("devel", branch="master")
    version("20200401", commit="7ebe2ede05a6ee366d93a7a993db69a99943a68f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
