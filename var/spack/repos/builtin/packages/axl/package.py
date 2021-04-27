# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.error import SpackError


def async_api_validator(pkg_name, variant_name, values):
    if 'none' in values and len(values) != 1:
        raise SpackError("The value 'none' is not usable"
                         " with other async_api values.")
    if 'intel_cppr' in values and 'cray_dw' in values:
        raise SpackError("The 'intel_cppr' and 'cray_dw' asynchronous"
                         " APIs are incompatible.")


class Axl(CMakePackage):
    """Asynchronous transfer library"""

    homepage = "https://github.com/ecp-veloc/AXL"
    url      = "https://github.com/ecp-veloc/AXL/archive/v0.4.0.tar.gz"
    git      = "https://github.com/ecp-veloc/axl.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.4.0', sha256='0530142629d77406a00643be32492760c2cf12d1b56c6b6416791c8ff5298db2')
    version('0.3.0', sha256='737d616b669109805f7aed1858baac36c97bf0016e1115b5c56ded05d792613e', deprecated=True)
    version('0.2.0', sha256='d04a445f102b438fe96a1ff3429790b0c035f0d23c2797bb5601a00b582a71fc', deprecated=True)
    version('0.1.1', sha256='36edac007938fe47d979679414c5c27938944d32536e2e149f642916c5c08eaa', deprecated=True)

    variant('async_api', default='daemon',
            description="Set of async transfer APIs to enable",
            values=['cray_dw', 'intel_cppr', 'daemon', 'none'], multi=True,
            validator=async_api_validator)

    variant('bbapi_fallback', default='False',
            description='Using BBAPI, if source or destination don\'t support \
            file extents then fallback to pthreads')

    depends_on('kvtree')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('platform=cray'):
            args.append("-DAXL_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)

        if self.spec.satisfies('@:0.3.0'):
            apis = list(self.spec.variants['async_api'].value)
            if 'daemon' in apis:
                args.append('-DAXL_ASYNC_DAEMON=ON')
                apis.remove('daemon')

            for api in apis:
                args.append('-DAXL_ASYNC_API={0}'.format(api.upper()))

        if self.spec.satisfies('@0.4.0:'):
            if '+bbapi_fallback' in self.spec:
                args.append('-DENABLE_BBAPI_FALLBACK=ON')
            else:
                args.append('-DENABLE_BBAPI_FALLBACK=OFF')

        return args
