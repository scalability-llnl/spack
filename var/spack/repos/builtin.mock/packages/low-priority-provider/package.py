# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LowPriorityProvider(Package):
    """Provides multiple virtuals but is low in the priority of clingo"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    # A low priority provider that provides both these specs together
    provides("mpi", "lapack")
