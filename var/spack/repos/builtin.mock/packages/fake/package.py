# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fake(Package):
    homepage = "http://www.fake-spack-example.org"
    url      = "http://www.fake-spack-example.org/downloads/fake-1.0.tar.gz"

    version('1.0', 'foobarbaz')
