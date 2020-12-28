# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class OpenclHeaders(BundlePackage):
    """Bundled OpenCL (Open Computing Language) header files"""

    homepage = "https://www.khronos.org/registry/OpenCL/"

    version('2.2')
    version('2.1')
    version('2.0')

    depends_on('opencl-c-headers@2020.03.13:')
    depends_on('opencl-clhpp@2.0.11:', when='@2.1:')
    depends_on('opencl-clhpp@2.0.9:', when='@2.0')
