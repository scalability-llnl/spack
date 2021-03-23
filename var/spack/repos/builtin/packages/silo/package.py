# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Silo(AutotoolsPackage):
    """Silo is a library for reading and writing a wide variety of scientific
       data to binary, disk files."""

    homepage = "https://wci.llnl.gov/simulation/computer-codes/silo"
    url      = "https://wci.llnl.gov/sites/wci/files/2021-01/silo-4.10.2.tgz"

    version('4.10.2', sha256='3af87e5f0608a69849c00eb7c73b11f8422fa36903dd14610584506e7f68e638', preferred=True)
    version('4.10.2-bsd', sha256='4b901dfc1eb4656e83419a6fde15a2f6c6a31df84edfad7f1dc296e01b20140e',
            url="https://wci.llnl.gov/sites/wci/files/2021-01/silo-4.10.2-bsd.tgz")
    version('4.9', sha256='90f3d069963d859c142809cfcb034bc83eb951f61ac02ccb967fc8e8d0409854')
    version('4.8', sha256='c430c1d33fcb9bc136a99ad473d535d6763bd1357b704a915ba7b1081d58fb21')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('shared', default=True, description='Build shared libraries')
    variant('silex', default=False,
            description='Builds Silex, a GUI for viewing Silo files')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('mpi', default=True,
            description='Compile with MPI Compatibility')

    depends_on('mpi', when='+mpi')
    depends_on('hdf5@:1.10.999', when='@:4.10.2')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('qt+gui~framework@4.8:4.9', when='+silex')
    depends_on('libx11', when='+silex')
    # Xmu dependency is required on Ubuntu 18-20
    depends_on('libxmu', when='+silex')
    depends_on('readline')
    depends_on('zlib')

    patch('remove-mpiposix.patch', when='@4.8:4.10.2')
    patch('H5FD_class_t-terminate.patch', when='^hdf5@1.10.0:')

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == 'ldflags':
            if spec['hdf5'].satisfies('~shared'):
                flags.append('-ldl')
            flags.append(spec['readline'].libs.search_flags)

        if '+pic' in spec:
            if name == 'cflags':
                flags.append(self.compiler.cc_pic_flag)
            elif name == 'cxxflags':
                flags.append(self.compiler.cxx_pic_flag)
            elif name == 'fcflags':
                flags.append(self.compiler.fc_pic_flag)
        return (flags, None, None)

    @when('%clang@9:')
    def patch(self):
        self.clang_9_patch()

    @when('%apple-clang@11.0.3:')
    def patch(self):
        self.clang_9_patch()

    def clang_9_patch(self):
        # Clang 9 and later include macro definitions in <math.h> that conflict
        # with typedefs DOMAIN and RANGE used in Silo plugins.
        # It looks like the upstream fpzip repo has been fixed, but that change
        # hasn't yet made it into silo.
        # https://github.com/LLNL/fpzip/blob/master/src/pcmap.h

        def repl(match):
            # Change macro-like uppercase to title-case.
            return match.group(1).title()

        files_to_filter = [
            "src/fpzip/codec.h",
            "src/fpzip/pcdecoder.inl",
            "src/fpzip/pcencoder.inl",
            "src/fpzip/pcmap.h",
            "src/fpzip/pcmap.inl",
            "src/fpzip/read.cpp",
            "src/fpzip/write.cpp",
            "src/hzip/hzmap.h",
            "src/hzip/hzresidual.h",
        ]

        filter_file(r'\b(DOMAIN|RANGE|UNION)\b', repl, *files_to_filter)

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--with-hdf5=%s,%s' % (spec['hdf5'].prefix.include,
                                   spec['hdf5'].prefix.lib),
            '--with-zlib=%s,%s' % (spec['zlib'].prefix.include,
                                   spec['zlib'].prefix.lib),
            '--enable-install-lite-headers',
            '--enable-fortran' if '+fortran' in spec else '--disable-fortran',
            '--enable-silex' if '+silex' in spec else '--disable-silex',
            '--enable-shared' if '+shared' in spec else '--disable-shared',
        ]

        if '+silex' in spec:
            x = spec['libx11']
            config_args.extend([
                '--with-Qt-dir=' + spec['qt'].prefix,
                '--with-Qt-lib=QtGui -lQtCore',
                '--x-includes=' + x.prefix.include,
                '--x-libraries=' + x.prefix.lib,
            ])

        if '+mpi' in spec:
            config_args.append('CC=%s' % spec['mpi'].mpicc)
            config_args.append('CXX=%s' % spec['mpi'].mpicxx)
            config_args.append('FC=%s' % spec['mpi'].mpifc)

        return config_args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            "libsilo*", root=self.prefix, shared=shared, recursive=True
        )
