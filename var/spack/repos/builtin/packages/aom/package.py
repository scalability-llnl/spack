# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Darach Golden <dgolden@tchpc.tcd.ie>,
# Institution: Trinity Centre for High Performance Computing, https://www.tchpc.tcd.ie/  # noqa: E501
# Date: May 09, 2019
# Author: Sean McGrath <smcgrat@tchpc.tcd.ie>
# Institution: Trinity Centre for High Performance Computing, https://www.tchpc.tcd.ie/  # noqa: E501
# Date: May 09, 2019
#
from spack.package import *


class Aom(CMakePackage):
    """Alliance for Open Media AOM AV1 Codec Library"""
    homepage = "https://aomedia.googlesource.com/aom"
    git      = "https://aomedia.googlesource.com/aom"
    version('v1.0.0-errata1', commit='29d8ce4836630df5cc7ab58f1afc4836765fc212')
    depends_on('yasm')

    def cmake_args(self):
        args = []
        args.append('-DBUILD_SHARED_LIBS=ON')
        return args
