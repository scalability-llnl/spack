# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RequiresVirtual(Package):
    """Package that requires a virtual dependency and is registered
    as an external.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version('2.0', '2.0_a_hash')

    depends_on('stuff')
