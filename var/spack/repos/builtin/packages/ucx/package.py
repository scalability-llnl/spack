# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ucx(AutotoolsPackage, CudaPackage):
    """a communication library implementing high-performance messaging for
    MPI/PGAS frameworks"""

    homepage = "http://www.openucx.org"
    url      = "https://github.com/openucx/ucx/releases/download/v1.3.1/ucx-1.3.1.tar.gz"
    git      = "https://github.com/openucx/ucx.git"

    maintainers = ['hppritcha']

    # Development
    version('1.9-dev', branch='v1.9.x')

    # Current
    version('1.9.0', sha256='a7a2c8841dc0d5444088a4373dc9b9cc68dbffcd917c1eba92ca8ed8e5e635fb', preferred=True)
    version('1.8.1', sha256='a48820cb8d0761b5ccf3e7ba03a7c8c1dde6276017657178829e07ffc35b556a')
    version('1.8.0', sha256='e400f7aa5354971c8f5ac6b881dc2846143851df868088c37d432c076445628d')
    version('1.7.0', sha256='6ab81ee187bfd554fe7e549da93a11bfac420df87d99ee61ffab7bb19bdd3371')
    version('1.6.1', sha256='1425648aa03f5fa40e4bc5c4a5a83fe0292e2fe44f6054352fbebbf6d8f342a1')
    version('1.6.0', sha256='360e885dd7f706a19b673035a3477397d100a02eb618371697c7f3ee4e143e2c')
    version('1.5.2', sha256='1a333853069860e86ba69b8d071ccc9871209603790e2b673ec61f8086913fad')
    version('1.5.1', sha256='567119cd80ad2ae6968ecaa4bd1d2a80afadd037ccc988740f668de10d2fdb7e')
    version('1.5.0', sha256='84f6e4fa5740afebb9b1c8bb405c07206e58c56f83120dcfcd8dc89e4b7d7458')
    version('1.4.0', sha256='99891a98476bcadc6ac4ef9c9f083bc6ffb188a96b3c3bc89c8bbca64de2c76e')

    # Still supported
    version('1.3.1', sha256='e058c8ec830d2f50d9db1e3aaaee105cd2ad6c1e6df20ae58b9b4179de7a8992')
    version('1.3.0', sha256='71e69e6d78a4950cc5a1edcbe59bf7a8f8e38d59c9f823109853927c4d442952')
    version('1.2.2', sha256='914d10fee8f970d4fb286079dd656cf8a260ec7d724d5f751b3109ed32a6da63')
    version('1.2.1', sha256='fc63760601c03ff60a2531ec3c6637e98f5b743576eb410f245839c84a0ad617')
    version('1.2.0', sha256='1e1a62d6d0f89ce59e384b0b5b30b416b8fd8d7cedec4182a5319d0dfddf649c')

    variant('thread_multiple', default=False,
            description='Enable thread support in UCP and UCT')
    variant('optimizations', default=True,
            description='Enable optimizations')
    variant('logging', default=False,
            description='Enable logging')
    variant('debug', default=False,
            description='Enable debugging')
    variant('assertions', default=False,
            description='Enable assertions')
    variant('parameter_checking', default=False,
            description='Enable parameter checking')
    variant('pic', default=True,
            description='Builds with PIC support')
    variant('java', default=False,
            description='Builds with Java bindings')
    variant('gdrcopy', default=False,
            description='Enable gdrcopy support')
    variant('knem', default=False,
            description='Enable KNEM support')
    variant('xpmem', default=False,
            description='Enable XPMEM support')
    variant('cma', default=False,
            description="nable Cross Memory Attach")
    variant('rc', default=False,
            description="Compile with IB Reliable Connection support")
    variant('dc', default=False,
            description="Compile with IB Dynamic Connection support")
    variant('ud', default=False,
            description="Compile with IB Unreliable Datagram support")
    variant('mlx5-dv', default=False,
            description="Compile with mlx5 Direct Verbs support")
    variant('ib-hw-tm', default=False,
            description="Compile with IB Tag Matching support")
    variant('dm', default=False,
            description="Compile with Device Memory support")
    variant('cm', default=False,
            description="Compile with IB Connection Manager support")

    depends_on('numactl')
    depends_on('rdma-core')
    depends_on('pkgconfig', type='build')
    depends_on('java@8', when='+java')
    depends_on('maven', when='+java')
    depends_on('gdrcopy', when='@1.7:+gdrcopy')
    depends_on('gdrcopy@1.3', when='@:1.6+gdrcopy')
    conflicts('+gdrcopy', when='~cuda',
              msg='gdrcopy currently requires cuda support')
    depends_on('xpmem', when='+xpmem')
    depends_on('knem', when='+knem')

    configure_abs_path = 'contrib/configure-release'

    @when('@1.9-dev')
    def autoreconf(self, spec, prefix):
        Executable('./autogen.sh')()

    def configure_args(self):
        spec = self.spec
        config_args = []

        if '+thread_multiple' in spec:
            config_args.append('--enable-mt')
        else:
            config_args.append('--disable-mt')

        if '+cma' in spec:
            config_args.append('--enable-cma')
        else:
            config_args.append('--disable-cma')

        if '+paramter_checking' in spec:
            config_args.append('--enable-params-check')
        else:
            config_args.append('--disable-params-check')

        # Activate SIMD based on properties of the target
        if 'avx' in self.spec.target:
            config_args.append('--with-avx')
        else:
            config_args.append('--without-avx')

        config_args.extend(self.enable_or_disable('optimizations'))
        config_args.extend(self.enable_or_disable('assertions'))
        config_args.extend(self.enable_or_disable('logging'))

        config_args.extend(self.with_or_without('pic'))
        config_args.extend(self.with_or_without('rc'))
        config_args.extend(self.with_or_without('ud'))
        config_args.extend(self.with_or_without('dc'))
        config_args.extend(self.with_or_without('mlx5-dv'))
        config_args.extend(self.with_or_without('ib-hw-tm'))
        config_args.extend(self.with_or_without('dm'))
        config_args.extend(self.with_or_without('cm'))
        config_args.extend(self.with_or_without('java',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('cuda',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('gdrcopy',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('knem',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('xpmem',
                                                activation_value='prefix'))

        return config_args
