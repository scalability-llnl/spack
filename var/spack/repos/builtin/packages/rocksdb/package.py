# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rocksdb(MakefilePackage):
    """RocksDB: A Persistent Key-Value Store for Flash and RAM Storage"""

    homepage = "https://github.com/facebook/rocksdb"
    url      = 'https://github.com/facebook/rocksdb/archive/v5.17.2.tar.gz'
    git      = 'https://github.com/facebook/rocksdb.git'

    version('develop', git=git, branch='master', submodules=True)
    version('5.17.2',  sha256='101f05858650a810c90e4872338222a1a3bf3b24de7b7d74466814e6a95c2d28')
    version('5.16.6',  sha256='f0739edce1707568bdfb36a77638fd5bae287ca21763ce3e56cf0bfae8fff033')
    version('5.15.10', sha256='26d5d4259fa352ae1604b5b4d275f947cacc006f4f7d2ef0b815056601b807c0')

    variant('bz2', default=False, description='Enable bz2 compression support')
    variant('lz4', default=True, description='Enable lz4 compression support')
    variant('snappy', default=False, description='Enable snappy compression support')
    variant('static', default=True, description='Build static library')
    variant('zlib', default=True, description='Enable zlib compression support')
    variant('zstd', default=False, description='Enable zstandard compression support')
    variant('tbb', default=False, description='Enable Intel TBB support')


    depends_on('bzip2', when='+bzip2')
    depends_on('gflags')
    depends_on('lz4', when='+lz4')
    depends_on('snappy', when='+snappy')
    depends_on('zlib', when='+zlib')
    depends_on('zstd', when='+zstd')
    depends_on('tbb', when='+tbb')

    phases = ['install']

    def patch(self):
        filter_file(
            '-march=native', '',
            join_path('build_tools', 'build_detect_platform')
        )

    def install(self, spec, prefix):
        cflags = []
        ldflags = []

        if spec.satisfies('%gcc@9:'):
            cflags.append('-Wno-error=deprecated-copy')
            cflags.append('-Wno-error=pessimizing-move')
            cflags.append('-Wno-error=redundant-move')

        if '+zlib' in self.spec:
            cflags.append('-I' + self.spec['zlib'].prefix.include)
            ldflags.append(self.spec['zlib'].libs.ld_flags)
        else:
            env['ROCKSDB_DISABLE_ZLIB'] = 'YES'

        if '+bz2' in self.spec:
            cflags.append('-I' + self.spec['bz2'].prefix.include)
            ldflags.append(self.spec['bz2'].libs.ld_flags)
        else:
            env['ROCKSDB_DISABLE_BZIP'] = 'YES'

        if '+tbb' in self.spec:
            cflags.append(spec['tbb'].headers.cpp_flags)
            ldflags.append('-L' + spec['tbb'].prefix.lib)
        else:
            env['ROCKSDB_DISABLE_TBB'] = 'YES'

        for pkg in ['lz4', 'snappy', 'zstd']:
            if '+' + pkg in self.spec:
                cflags.append(self.spec[pkg].headers.cpp_flags)
                ldflags.append(self.spec[pkg].libs.ld_flags)
            else:
                env['ROCKSDB_DISABLE_' + pkg.upper()] = 'YES'

        cflags.append(self.spec['gflags'].headers.cpp_flags)
        ldflags.append(self.spec['gflags'].libs.ld_flags)

        env['CFLAGS'] = ' '.join(cflags)
        env['PLATFORM_FLAGS'] = ' '.join(ldflags)
        env['INSTALL_PATH'] = self.spec.prefix

        buildtype = 'install-static' if '+static' in spec else 'install-shared'
        make(buildtype)
