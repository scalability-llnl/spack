# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys
import os
from spack import *
import llnl.util.tty as tty


class Namd(MakefilePackage):
    """NAMDis a parallel molecular dynamics code designed for
    high-performance simulation of large biomolecular systems."""

    homepage = "http://www.ks.uiuc.edu/Research/namd/"
    url      = "file://{0}/NAMD_2.12_Source.tar.gz".format(os.getcwd())
    git      = "https://charm.cs.illinois.edu/gerrit/namd.git"
    manual_download = True

    version("master", branch="master")
    version('2.15a1', branch="master", tag='release-2-15-alpha-1')
    version('2.14', sha256='34044d85d9b4ae61650ccdba5cda4794088c3a9075932392dd0752ef8c049235',
            preferred=True)
    version('2.13', '9e3323ed856e36e34d5c17a7b0341e38')
    version('2.12', '2a1191909b1ab03bf0205971ad4d8ee9')

    variant('fftw', default='3', values=('none', '2', '3', 'mkl'),
            description='Enable the use of FFTW/FFTW3/MKL FFT')

    variant('interface', default='none', values=('none', 'tcl', 'python'),
            description='Enables TCL and/or python interface')

    # init_tcl_pointers() declaration and implementation are inconsistent
    # "src/colvarproxy_namd.C", line 482: error: inherited member is not
    # allowed
    patch('inherited-member-2.13.patch', when='@2.13')
    patch('inherited-member-2.14.patch', when='@2.14')

    depends_on('charmpp@6.10.1:', when="@2.14:")
    depends_on('charmpp@6.8.2', when="@2.13")
    depends_on('charmpp@6.7.1', when="@2.12")

    depends_on('fftw@:2.99', when="fftw=2")
    depends_on('fftw@3:', when="fftw=3")

    depends_on('intel-mkl', when="fftw=mkl")

    depends_on('tcl', when='interface=tcl')

    depends_on('tcl', when='interface=python')
    depends_on('python', when='interface=python')

    def _copy_arch_file(self, lib):
        config_filename = 'arch/{0}.{1}'.format(self.arch, lib)
        copy('arch/Linux-x86_64.{0}'.format(lib),
             config_filename)
        if lib == 'tcl':
            filter_file(r'-ltcl8\.5',
                        '-ltcl{0}'.format(self.spec['tcl'].version.up_to(2)),
                        config_filename)

    def _append_option(self, opts, lib):
        if lib != 'python':
            self._copy_arch_file(lib)
        spec = self.spec
        opts.extend([
            '--with-{0}'.format(lib),
            '--{0}-prefix'.format(lib), spec[lib].prefix
        ])

    @property
    def arch(self):
        plat = sys.platform
        if plat.startswith("linux"):
            plat = "linux"
        march = platform.machine()
        return '{0}-{1}'.format(plat, march)

    @property
    def build_directory(self):
        return '{0}-spack'.format(self.arch)

    def _edit_arch_generic(self, spec, prefix):
        """Generic arch makefile generation"""
        m64 = '-m64 ' if not spec.satisfies('arch=aarch64:') else ''
        with working_dir('arch'):
            with open('{0}.arch'.format(self.build_directory), 'w') as fh:
                # this options are take from the default provided
                # configuration files
                # https://github.com/UIUC-PPL/charm/pull/2778
                archopt = spec.target.optimization_flags(
                    spec.compiler.name, spec.compiler.version)

                if self.spec.satisfies('^charmpp@:6.10.1'):
                    optims_opts = {
                        'gcc': m64 + '-O3 -fexpensive-optimizations \
                                        -ffast-math -lpthread ' + archopt,
                        'intel': '-O2 -ip -qopenmp-simd' + archopt}
                else:
                    optims_opts = {
                        'gcc': m64 + '-O3 -fexpensive-optimizations \
                                        -ffast-math ' + archopt,
                        'intel': '-O2 -ip ' + archopt}

                optim_opts = optims_opts[self.compiler.name] \
                    if self.compiler.name in optims_opts else ''

                fh.write('\n'.join([
                    'NAMD_ARCH = {0}'.format(self.arch),
                    'CHARMARCH = {0}'.format(self.spec['charmpp'].charmarch),
                    'CXX = {0.cxx} {0.cxx11_flag}'.format(
                        self.compiler),
                    'CXXOPTS = {0}'.format(optim_opts),
                    'CC = {0}'.format(self.compiler.cc),
                    'COPTS = {0}'.format(optim_opts),
                    ''
                ]))

    def _edit_arch_target_based(self, spec, prefix):
        """Try to use target base arch file return True if succeed"""
        if spec.version < Version("2.14"):
            return False

        found_special_opt = False
        with working_dir('arch'):
            arch_filename = '{0}.arch'.format(self.build_directory)

            replace = [
                [
                    r"^CHARMARCH = .*$",
                    'CHARMARCH = {0}'.format(self.spec['charmpp'].charmarch)
                ],
                [
                    r"^NAMD_ARCH = .*$",
                    'NAMD_ARCH = {0}'.format(self.arch)
                ]
            ]

            # Optimizations for skylake_avx512
            if spec.platform == "linux" and \
                    self.compiler.name == "intel" and \
                    'avx512' in spec.target and \
                    spec.target >= 'skylake_avx512':
                if spec.version >= Version("2.15") and \
                        os.path.exists("Linux-AVX512-icc.arch"):
                    tty.info("Building binaries with AVX512-tile optimization")
                    copy("Linux-AVX512-icc.arch", arch_filename)
                elif spec.version >= Version("2.14") and \
                        os.path.exists("Linux-SKX-icc.arch"):
                    tty.info("Building binaries with Skylake-X"
                             "AVX512 optimization")
                    copy("Linux-SKX-icc.arch", arch_filename)
                else:
                    return False

                replace.append([
                    r"^CXX = icpc",
                    'CXX = {0}'.format(self.compiler.cxx)
                ])
                replace.append([
                    r"^CC = icc",
                    'CC = {0}'.format(self.compiler.cc)
                ])
                found_special_opt = True

            if found_special_opt:
                for pattern, replacement in replace:
                    filter_file(pattern, replacement, arch_filename)

        return found_special_opt

    def _edit_arch(self, spec, prefix):
        """Try to use target base arch file, if not make generic"""
        if not self._edit_arch_target_based(spec, prefix):
            self._edit_arch_generic(spec, prefix)

    def edit(self, spec, prefix):
        self._edit_arch(spec, prefix)

        self._copy_arch_file('base')

        opts = ['--charm-base', spec['charmpp'].prefix]
        fftw_version = spec.variants['fftw'].value
        if fftw_version == 'none':
            opts.append('--without-fftw')
        elif fftw_version == 'mkl':
            self._append_option(opts, 'mkl')
        else:
            _fftw = 'fftw{0}'.format('' if fftw_version == '2' else '3')

            self._copy_arch_file(_fftw)
            opts.extend(['--with-{0}'.format(_fftw),
                         '--fftw-prefix', spec['fftw'].prefix])

        interface_type = spec.variants['interface'].value
        if interface_type != 'none':
            self._append_option(opts, 'tcl')

            if interface_type == 'python':
                self._append_option(opts, 'python')
        else:
            opts.extend([
                '--without-tcl',
                '--without-python'
            ])

        config = Executable('./config')

        config(self.build_directory, *opts)

        # patch Make.config if needed
        # spack install charmpp straight to prefix
        # (not to $(CHARMBASE)/$(CHARMARCH))
        if not os.path.exists(join_path(
                self.spec['charmpp'].prefix, self.spec['charmpp'].charmarch)):
            filter_file(r"^CHARM = \$\(CHARMBASE\)/\$\(CHARMARCH\)",
                        "CHARM = $(CHARMBASE)",
                        join_path(self.build_directory, "Make.config"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install('namd2', prefix.bin)

            # I'm not sure this is a good idea or if an autoload of the charm
            # module would not be better.
            install('charmrun', prefix.bin)
