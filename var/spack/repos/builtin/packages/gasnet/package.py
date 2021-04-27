# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Gasnet(AutotoolsPackage):
    """GASNet is a language-independent, low-level networking layer
       that provides network-independent, high-performance communication
       primitives tailored for implementing parallel global address space
       SPMD languages and libraries such as UPC, Co-Array Fortran, SHMEM,
       Cray Chapel, and Titanium.
    """
    homepage = "https://gasnet.lbl.gov"
    url      = "https://gasnet.lbl.gov/EX/GASNet-2020.3.0.tar.gz"

    maintainers = ['PHHargrove', 'bonachea']

    version('2020.3.0', sha256='019eb2d2284856e6fabe6c8c0061c874f10e95fa0265245f227fd3497f1bb274')
    version('2019.9.0', sha256='117f5fdb16e53d0fa8a47a1e28cccab1d8020ed4f6e50163d985dc90226aaa2c')
    version('2019.6.0', sha256='839ba115bfb48083c66b4c1c27703d73063b75d2f1e0501d5eab2ad7f0f776c8')
    version('2019.3.2', sha256='9e2175047879f1e8c7c4b0a9db3c2cd20c978371cd7f209cf669d402119b6fdb')
    version('2019.3.0', sha256='97fe19bb5ab32d14a96d2dd19d0f03048f68bb20ca83abe0c00cdab40e86eba5')
    version('1.32.0', sha256='42e4774b3bbc7c142f77c41b6ce86b594f579073f46c31f47f424c7e31ee1511')
    version('1.30.0', sha256='b5d8c98c53174a98a41efb4ec9dedb62c0a9e8fa111bb6460cd4493beb80d497')
    version('1.28.2', sha256='7903fd8ebdd03bcda20a66e3fcedef2f8b384324591aa91b8370f3360f6384eb')
    version('1.28.0', sha256='a7999fbaa1f220c2eb9657279c7e7cccd1b21865d5383c9a5685cfe05a0702bc')
    version('1.24.0', sha256='76b4d897d5e2261ef83d0885c192e8ac039e32cb2464f11eb64eb3f9f2df38c0')

    variant('mpi', default=True, description="Support MPI")
    variant('ibv', default=False, description="Support InfiniBand")
    variant('udp', default=False, description="Support UDP")
    variant('aligned-segments', default=False,
            description="Requirement to achieve aligned VM segments")
    variant('pshm', default=True,
            description="Support inter-process shared memory support")
    variant('segment-mmap-max', default='16GB',
            description="Upper bound for mmap-based GASNet segments")

    conflicts('+aligned-segments', when='+pshm')

    depends_on('mpi', when='+mpi')

    def url_for_version(self, version):
        url = "https://gasnet.lbl.gov/"
        if version >= Version('2019'):
            url += "EX/GASNet-{0}.tar.gz".format(version)
        else:
            url += "download/GASNet-{0}.tar.gz".format(version)

        return url

    def configure_args(self):
        args = [
            # TODO: factor IB suport out into architecture description.
            '--enable-par',
            '--enable-mpi-compat',
            '--enable-segment-fast',
            '--disable-parsync',
            '--with-segment-mmap-max=%s '
            % (self.spec.variants['segment-mmap-max'].value),
            # for consumers with shared libs
            "CC=%s %s" % (spack_cc, self.compiler.cc_pic_flag),
            "CXX=%s %s" % (spack_cxx, self.compiler.cxx_pic_flag),
        ]

        if '+aligned-segments' in self.spec:
            args.append('--enable-aligned-segments')
        else:
            args.append('--disable-aligned-segments')

        if '+pshm' in self.spec:
            args.append('--enable-pshm')
        else:
            args.append('--disable-pshm')

        if '+mpi' in self.spec:
            args.extend(['--enable-mpi',
                         '--disable-udp',
                         '--disable-ibv',
                         '--disable-seq',
                         'MPI_CC=%s %s'
                        % (self.spec['mpi'].mpicc, self.compiler.cc_pic_flag)])

        if '+ibv' in self.spec:
            args.extend(['--enable-ibv',
                         '--with-ibv-max-hcas=1',
                         '--enable-pthreads',
                         '--disable-udp',
                         '--disable-mpi',
                         '--disable-seq',
                         '--disable-smp',
                         '--disable-portals'])

        if '+udp' in self.spec:
            args.extend(['--enable-udp',
                         '--disable-ibv',
                         '--disable-mpi',
                         '--disable-seq'])

        return args
