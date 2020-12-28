# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpmemobjCpp(CMakePackage):
    """C++ bindings for libpmemobj (https://github.com/pmem/pmdk)"""

    homepage = "https://github.com/pmem/libpmemobj-cpp"
    url      = "https://github.com/pmem/libpmemobj-cpp/archive/1.6.tar.gz"
    git      = "https://github.com/pmem/libpmemobj-cpp.git"

    version('develop', branch='master')
    version('1.6', sha256='791bf86c6b9401451e3d20f19cb8799d312b9d58659cb93aa532cd724db554ae')
    version('1.5.1', sha256='0448bac4697f6563789e5bf22b8556288ae67ab916608bc45d0a3baa24c67985')
    version('1.5', sha256='6254aa2fb77977f8b91998eb866216d2af22f4ccbffdfc7932df1dff151da61e')

    # libpmemobj only supports 'Debug' and 'Release'
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release'))

    depends_on('pmdk')
