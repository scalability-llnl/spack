# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Salmon(CMakePackage):
    """Salmon is a tool for quantifying the expression of transcripts using
       RNA-seq data."""

    homepage = "http://combine-lab.github.io/salmon/"
    url      = "https://github.com/COMBINE-lab/salmon/archive/v0.8.2.tar.gz"

    version('1.4.0', sha256='6d3e25387450710f0aa779a1e9aaa9b4dec842324ff8551d66962d7c7606e71d')
    version('0.14.1', sha256='05289170e69b5f291a8403b40d6b9bff54cc38825e9f721c210192b51a19273e')
    version('0.12.0', sha256='91ebd1efc5b0b4c12ec6babecf3c0b79f7102e42b8895ca07c8c8fea869fefa3')
    version('0.9.1', sha256='3a32c28d217f8f0af411c77c04144b1fa4e6fd3c2f676661cc875123e4f53520')
    version('0.8.2', sha256='299168e873e71e9b07d63a84ae0b0c41b0876d1ad1d434b326a5be2dce7c4b91')

    variant('build_type', default='RELEASE',
            description='CMake build type',
            values=('DEBUG', 'RELEASE'))

    depends_on('tbb')
    depends_on('boost@:1.66.0', when='@:0.14.1')
    depends_on('boost@1.72.0:', when='@1.4.0:')
    depends_on('cereal')
    depends_on('jemalloc')
    depends_on('xz')
    depends_on('zlib')
    depends_on('bzip2')
    depends_on('libdivsufsort')
    depends_on('staden-io-lib~curl')
    depends_on('libgff')
    depends_on('pkgconfig')
    depends_on('curl', when='@0.14.1:')

    conflicts('%gcc@:5.1', when='@0.14.1:')

    resources = [
        ('1.4.0', 'pufferfish', '059207e8d3134060ed70595e53f4189954c9e5edfaa6361b46304f55d1b71bc7'),
        ('0.14.1', 'RapMap', 'fabac2f360513b803aa3567415eddcd97261ab8a23d4f600af5f98ee8ffd944b'),
        ('0.12.0', 'RapMap', '05102c0bbc8a0c0056a01cd0e8788fa5b504aee58ac226ab8c0e3ffec8019790'),
        ('0.9.1', 'RapMap', '8975e5a1ed61ed9354ba776272927545f417ecdce95823e71ba1e7b61de7d380'),
        ('0.8.2', 'RapMap', '1691f4bca2b604f05f36772ae45faf0842ab4809843df770bd10366a5cfd6822'),
    ]

    for ver, repo, checksum in resources:
        resource(name='rapmap',
                 url='https://github.com/COMBINE-lab/{0}/archive/salmon-v{1}.zip'.format(repo, ver),
                 sha256=checksum,
                 placement='external',
                 expand=False,
                 when='@{0}'.format(ver))

    def patch(self):
        # remove static linking to libstdc++
        filter_file('-static-libstdc++', '', 'CMakeLists.txt', string=True)
        if self.spec.satisfies('@0.8.2:0.9.1'):
            filter_file('${FAST_MALLOC_LIB}',
                        '${FAST_MALLOC_LIB}\n'
                        '${CMAKE_DL_LIBS}',
                        'src/CMakeLists.txt',
                        string=True)

        if self.spec.satisfies('@:0.14.1'):
            filter_file('curl -k.*',
                        '',
                        'scripts/fetchRapMap.sh')
            symlink('./salmon-v{0}.zip'.format(self.version),
                    './external/rapmap.zip')

        if self.spec.satisfies('@1.4.0:'):
            filter_file('curl -k.*',
                        '',
                        'scripts/fetchPufferfish.sh')
            symlink('./salmon-v{0}.zip'.format(self.version),
                    './external/pufferfish.zip')
            # Fix issues related to lto-wrapper during install
            filter_file('INTERPROCEDURAL_OPTIMIZATION True',
                        'INTERPROCEDURAL_OPTIMIZATION False',
                        'src/CMakeLists.txt', string=True)
            filter_file('curl -k.*', '', 'scripts/fetchPufferfish.sh')

    def cmake_args(self):
        args = [
            '-DBOOST_ROOT=%s' % self.spec['boost'].prefix,
        ]

        return args
