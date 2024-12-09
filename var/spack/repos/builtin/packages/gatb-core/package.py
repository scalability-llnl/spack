# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GatbCore(CMakePackage):
    """GATB - The Genome Analysis Toolbox with de-Bruijn graph"""

    homepage = "https://gatb.inria.fr/software/gatb-core/"
    git = "https://github.com/GATB/gatb-core.git"

    depends_on("cmake@3.1.0:", type="build")

    version("1.4.2", tag="v1.4.2", commit="99f573a465beb30acc22ab20be458d2ea0277684")
    version("1.4.1", tag="v1.4.1", commit="b45a6c213597b23f8f5221902e2b86b4009c11d9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    root_cmakelists_dir = "gatb-core"
