# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PreferredTest(Package):
    """Dummy package with develop version and preffered version"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('develop', git='https://github.com/dummy/repo.git')
    version('0.2.16', 'b1190f3d3471685f17cfd1ec1d252ac9')
    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9', preferred=True)
    version('0.2.14', 'b1190f3d3471685f17cfd1ec1d252ac9')
