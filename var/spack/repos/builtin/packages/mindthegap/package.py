# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mindthegap(CMakePackage):
    """MindTheGap is a software that performs integrated detection and
       assembly of genomic insertion variants in NGS read datasets with
       respect to a reference genome."""

    homepage = "https://gatb.inria.fr/software/mind-the-gap/"
    git      = "https://github.com/GATB/MindTheGap.git"

    version('2.0.2', tags='v2.0.2', submodules=True)

    depends_on('zlib')
