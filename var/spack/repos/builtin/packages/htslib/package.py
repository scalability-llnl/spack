# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Htslib(AutotoolsPackage):
    """C library for high-throughput sequencing data formats."""

    homepage = "https://github.com/samtools/htslib"
    url = "https://github.com/samtools/htslib/releases/download/1.10.2/htslib-1.10.2.tar.bz2"

    version('1.12', sha256='2280141b46e953ba4ae01b98335a84f8e6ccbdb6d5cdbab7f70ee4f7e3b6f4ca')
    version('1.10.2', sha256='e3b543de2f71723830a1e0472cf5489ec27d0fbeb46b1103e14a11b7177d1939')
    version('1.9', sha256='e04b877057e8b3b8425d957f057b42f0e8509173621d3eccaedd0da607d9929a')
    version('1.8', sha256='c0ef1eec954a98cc708e9f99f6037db85db45670b52b6ab37abcc89b6c057ca1')
    version('1.7', sha256='be3d4e25c256acdd41bebb8a7ad55e89bb18e2fc7fc336124b1e2c82ae8886c6')
    version('1.6', sha256='9588be8be0c2390a87b7952d644e7a88bead2991b3468371347965f2e0504ccb')
    version('1.5', sha256='a02b515ea51d86352b089c63d778fb5e8b9d784937cf157e587189cb97ad922d')
    version('1.4', sha256='5cfc8818ff45cd6e924c32fec2489cb28853af8867a7ee8e755c4187f5883350')
    version('1.3.1', sha256='49d53a2395b8cef7d1d11270a09de888df8ba06f70fe68282e8235ee04124ae6')
    version('1.2', sha256='125c01421d5131afb4c3fd2bc9c7da6f4f1cd9ab5fc285c076080b9aca24bffc')

    variant('libcurl',
            default=True,
            description='Enable libcurl-based support for http/https/etc URLs,'
            ' for versions >= 1.3. This also enables S3 and GCS support.')

    depends_on('zlib')
    depends_on('bzip2', when='@1.4:')
    depends_on('xz', when='@1.4:')
    depends_on('curl', when='@1.3:+libcurl')

    depends_on('m4', when="@1.2")
    depends_on('autoconf', when="@1.2")
    depends_on('automake', when="@1.2")
    depends_on('libtool', when="@1.2")

    # v1.2 uses the automagically assembled tarball from .../archive/...
    # everything else uses the tarballs uploaded to the release
    def url_for_version(self, version):
        if version.string == '1.2':
            return 'https://github.com/samtools/htslib/archive/1.2.tar.gz'
        else:
            url = "https://github.com/samtools/htslib/releases/download/{0}/htslib-{0}.tar.bz2"
            return url.format(version.dotted)

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('@1.3:'):
            args.extend(self.enable_or_disable('libcurl'))

        return args
