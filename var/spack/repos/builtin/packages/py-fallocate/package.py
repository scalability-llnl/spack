# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFallocate(PythonPackage):
    """Module to expose posix_fallocate(3), posix_fadvise(3) and fallocate(2)
    """

    homepage = "https://github.com/trbs/fallocate"
    url      = "https://pypi.io/packages/source/f/fallocate/fallocate-1.6.4.tar.gz"

    version('1.6.4', sha256='85ebeb2786761fbe80d88c52590a610bd3425fc89e188c208a3f261a5bd6acb3')
