# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class DirectMpich(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/direct_mpich-1.0.tar.gz"

    version('1.0', 'foobarbaz')

    depends_on('mpich')
