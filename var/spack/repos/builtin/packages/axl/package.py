# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.error import SpackError
from spack.package import *


def async_api_validator(pkg_name, variant_name, values):
    if 'none' in values and len(values) != 1:
        raise SpackError("The value 'none' is not usable"
                         " with other async_api values.")
    if 'ibm_bbapi' in values and 'cray_dw' in values:
        raise SpackError("The 'ibm_bbapi' and 'cray_dw' asynchronous"
                         " APIs are incompatible.")


class Axl(CMakePackage):
    """Asynchronous transfer library"""

    homepage = "https://github.com/ecp-veloc/AXL"
    url      = "https://github.com/ecp-veloc/AXL/archive/v0.1.1.zip"
    git      = "https://github.com/ecp-veloc/axl.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.3.0', sha256='3f5efff87be700a5792a0ee9a7aeae45c640e2936623b024e8bc1056f7952a46')
    version('0.2.0', sha256='a0babe3576da30919f89df2f83c76bd01d06345919f2e54d4dddcd6f73faedcc')
    version('0.1.1', sha256='ebbf231bb542a6c91efb79fce05d4c8a346d5506d88ae1899fb670be52e81933')

    variant('async_api', default='daemon',
            description="Set of async transfer APIs to enable",
            values=['cray_dw', 'ibm_bbapi', 'daemon', 'none'], multi=True,
            validator=async_api_validator)

    # not-yet implemented functionality
    conflicts('async_api=cray_dw', when='@0.1.0')
    conflicts('async_api=ibm_bbapi', when='@0.1.0')

    depends_on('kvtree')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('platform=cray'):
            args.append("-DAXL_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)

        apis = list(self.spec.variants['async_api'].value)
        if 'daemon' in apis:
            args.append('-DAXL_ASYNC_DAEMON=ON')
            apis.remove('daemon')

        for api in apis:
            args.append('-DAXL_ASYNC_API={0}'.format(api))

        return args
