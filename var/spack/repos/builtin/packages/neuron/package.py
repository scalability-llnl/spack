# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Neuron(Package):
    """NEURON is a simulation environment for single and networks of neurons.

    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments. The primary scripting
    language is hoc but a Python interface is also available.
    """

    homepage = "https://www.neuron.yale.edu/"
    url      = "http://www.neuron.yale.edu/ftp/neuron/versions/v7.5/nrn-7.5.tar.gz"
    git      = "https://github.com/nrnhines/nrn.git"

    version('develop', branch='master')
    version('7.5', sha256='67642216a969fdc844da1bd56643edeed5e9f9ab8c2a3049dcbcbcccba29c336')
    version('7.4', sha256='1403ba16b2b329d2376f4bf007d96e6bf2992fa850f137f1068ad5b22b432de6')
    version('7.3', sha256='71cff5962966c5cd5d685d90569598a17b4b579d342126b31e2d431128cc8832')
    version('7.2', sha256='c777d73a58ff17a073e8ea25f140cb603b8b5f0df3c361388af7175e44d85b0e')

    variant('mpi',           default=True,  description='Enable MPI parallelism')
    variant('python',        default=True,  description='Enable python')
    variant('shared',        default=False, description='Build shared libraries')
    variant('cross-compile', default=False, description='Build for cross-compile environment')
    variant('multisend',     default=True,  description="Enable multi-send spike exchange")
    variant('rx3d',          default=False, description="Enable cython translated 3-d rxd")

    depends_on('flex',       type='build')
    depends_on('bison',      type='build')
    depends_on('automake',   type='build')
    depends_on('automake',   type='build')
    depends_on('autoconf',   type='build')
    depends_on('libtool',    type='build')
    depends_on('pkgconfig',  type='build')

    depends_on('mpi',         when='+mpi')
    depends_on('python@2.6:', when='+python')
    depends_on('ncurses',     when='~cross-compile')

    conflicts('~shared', when='+python')

    filter_compiler_wrappers('*/bin/nrniv_makefile')

    def get_neuron_archdir(self):
        """Determine the architecture-specific neuron base directory.

        Instead of recreating the logic of the neuron's configure
        we dynamically find the architecture-specific directory by
        looking for a specific binary.
        """
        file_list = find(self.prefix, '*/bin/nrniv_makefile')
        # check needed as when initially evaluated the prefix is empty
        if file_list:
            neuron_archdir = os.path.dirname(os.path.dirname(file_list[0]))
        else:
            neuron_archdir = self.prefix

        return neuron_archdir

    def patch(self):
        # aclocal need complete include path (especially on os x)
        pkgconf_inc = '-I %s/share/aclocal/' % (self.spec['pkgconfig'].prefix)
        libtool_inc = '-I %s/share/aclocal/' % (self.spec['libtool'].prefix)
        newpath = 'aclocal -I m4 %s %s' % (pkgconf_inc, libtool_inc)
        filter_file(r'aclocal -I m4', r'%s' % newpath, "build.sh")

    def get_arch_options(self, spec):
        options = []

        if spec.satisfies('+cross-compile'):
            options.extend(['cross_compiling=yes',
                            '--without-memacs',
                            '--without-nmodl'])

        # on os-x disable building carbon 'click' utility
        if 'darwin' in self.spec.architecture:
            options.append('macdarwin=no')

        return options

    def get_python_options(self, spec):
        options = []

        if spec.satisfies('+python'):
            python_exec = spec['python'].command.path
            py_inc = spec['python'].headers.directories[0]
            py_lib = spec['python'].prefix.lib

            if not os.path.isdir(py_lib):
                py_lib = spec['python'].prefix.lib64

            options.extend(['--with-nrnpython=%s' % python_exec,
                            '--disable-pysetup',
                            'PYINCDIR=%s' % py_inc,
                            'PYLIBDIR=%s' % py_lib])

            if spec.satisfies('~cross-compile'):
                options.append('PYTHON_BLD=%s' % python_exec)

        else:
            options.append('--without-nrnpython')

        return options

    def get_compiler_options(self, spec):
        flags = '-O2 -g'

        if self.spec.satisfies('%pgi'):
            flags += ' ' + self.compiler.cc_pic_flag

        return ['CFLAGS=%s' % flags,
                'CXXFLAGS=%s' % flags]

    def build_nmodl(self, spec, prefix):
        # build components for front-end arch in cross compiling environment
        options = ['--prefix=%s' % prefix,
                   '--with-nmodl-only',
                   '--without-x']

        if 'cray' in self.spec.architecture:
            flags = '-target-cpu=x86_64 -target-network=none'
            options.extend(['CFLAGS=%s' % flags,
                            'CXXFLAGS=%s' % flags])

        configure = Executable(join_path(self.stage.source_path, 'configure'))
        configure(*options)
        make()
        make('install')

    def install(self, spec, prefix):

        options = ['--prefix=%s' % prefix,
                   '--without-iv',
                   '--without-x',
                   '--without-readline']

        if spec.satisfies('+multisend'):
            options.append('--with-multisend')

        if spec.satisfies('~rx3d'):
            options.append('--disable-rx3d')

        if spec.satisfies('+mpi'):
            options.extend(['MPICC=%s' % spec['mpi'].mpicc,
                            'MPICXX=%s' % spec['mpi'].mpicxx,
                            '--with-paranrn'])
        else:
            options.append('--without-paranrn')

        if spec.satisfies('~shared'):
            options.extend(['--disable-shared',
                            'linux_nrnmech=no'])

        options.extend(self.get_arch_options(spec))
        options.extend(self.get_python_options(spec))
        options.extend(self.get_compiler_options(spec))

        build = Executable('./build.sh')
        build()

        with working_dir('build', create=True):
            if spec.satisfies('+cross-compile'):
                self.build_nmodl(spec, prefix)
            srcpath = self.stage.source_path
            configure = Executable(join_path(srcpath, 'configure'))
            configure(*options)
            make('VERBOSE=1')
            make('install')

    def setup_run_environment(self, env):
        neuron_archdir = self.get_neuron_archdir()
        env.prepend_path('PATH', join_path(neuron_archdir, 'bin'))
        env.prepend_path('LD_LIBRARY_PATH', join_path(neuron_archdir, 'lib'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        neuron_archdir = self.get_neuron_archdir()
        env.prepend_path('PATH', join_path(neuron_archdir, 'bin'))
        env.prepend_path('LD_LIBRARY_PATH', join_path(neuron_archdir, 'lib'))
