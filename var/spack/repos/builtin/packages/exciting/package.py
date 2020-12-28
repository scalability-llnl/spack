# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exciting(MakefilePackage):
    """
    exciting is a full-potential all-electron density-functional-theory package
    implementing the families of linearized augmented planewave methods. It can
    be applied to all kinds of materials, irrespective of the atomic species in
    volved, and also allows for exploring the physics of core electrons. A
    particular focus are excited states within many-body perturbation theory.
    """

    homepage = "http://exciting-code.org/"
    url      = "http://exciting.wdfiles.com/local--files/nitrogen-14/exciting.nitrogen-14.tar.gz"

    version('14', sha256='a7feaffdc23881d6c0737d2f79f94d9bf073e85ea358a57196d7f7618a0a3eff')

    # as-of-yet unpublished fix to version 14
    patch('dfgather.patch', when='@14', working_dir='src/src_xs', level=0)
    variant('mpi', default=False, description='Use MPI')
    variant('mkl', default=False, description='Use MKL')
    variant('omp', default=True, description='Use OpenMP')
    variant('scalapack', default=False, description='Use ScaLAPACK')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw', when='~mkl')
    depends_on('mkl', when='+mkl')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack')
    conflicts('%gcc@10:', msg='exciting cannot be built with GCC 10')

    for __compiler in spack.compilers.supported_compilers():
        if __compiler != 'intel':
            conflicts('%{0}'.format(__compiler), when='^mkl',
                      msg='MKL only works with the Intel compiler')

    def edit(self, spec, prefix):
        opts = {}
        opts['BUILDSMP'] = 'true'
        opts['F90_OPTS'] = '-cpp '
        opts['F77_OPTS'] = '-cpp -O3 '
        opts['CPP_ON_OPTS'] = '-cpp -DXS -DISO -DLIBXC'
        opts['LIB_ARP'] = 'libarpack.a'
        opts['F90'] = spack_fc
        opts['F77'] = spack_f77
        if '+omp' in spec:
            opts['LDFLAGS'] = self.compiler.openmp_flag + ' -DUSEOMP'
            opts['F90_OPTS'] += self.compiler.openmp_flag + ' -DUSEOMP'
            opts['F77_OPTS'] += self.compiler.openmp_flag + ' -DUSEOMP'
        if '%intel' in spec:
            opts['F90_OPTS'] += ' -O3 -cpp -ip -unroll -scalar_rep '
            opts['CPP_ON_OPTS'] += ' -DIFORT -DFFTW'
        if '%gcc' in spec:
            opts['F90_OPTS'] += '-O3 -march=native -ffree-line-length-0'
        filter_file('FCFLAGS = @FCFLAGS@',
                    ' '.join(['FCFLAGS = @FCFLAGS@', '-cpp',
                              self.compiler.openmp_flag]),
                    'src/libXC/src/Makefile.in')
        if '+mkl' in spec:
            if '%intel' in spec:
                opts['LIB_LPK'] = '-mkl=parallel'
            opts['INC_MKL'] = spec['mkl'].headers.include_flags
            opts['LIB_MKL'] = spec['mkl'].libs.ld_flags
        else:
            opts['LIB_LPK'] = ' '.join([spec['lapack'].libs.ld_flags,
                                        spec['blas'].libs.ld_flags,
                                        self.compiler.openmp_flag])
        if '+mpi' in spec:
            opts['BUILDMPI'] = 'true'
            opts['MPIF90'] = spec['mpi'].mpifc
            opts['MPIF90_CPP_OPTS'] = self.compiler.openmp_flag
            opts['MPIF90_CPP_OPTS'] += ' -DMPI -DMPIRHO -DMPISEC '
            opts['MPIF90_OPTS'] = ' '.join(['$(F90_OPTS)', '$(CPP_ON_OPTS) '
                                            '$(MPIF90_CPP_OPTS)'])
            opts['MPIF90MT'] = '$(MPIF90)'
        else:
            opts['BUILDMPI'] = 'false'

        if '+scalapack' in spec:
            opts['LIB_SCLPK'] = spec['scalapack'].libs.ld_flags
            opts['LIB_SCLPK'] += ' ' + self.compiler.openmp_flag
            opts['CPP_SCLPK'] = ' -DSCAL '
            opts['LIBS_MPI'] = '$(LIB_SCLPK)'
            opts['MPIF90_CPP_OPTS'] += ' $(CPP_SCLPK) '

        opts['USE_SYS_LAPACK'] = 'true'
        opts['LIB_FFT'] = 'fftlib.a'
        opts['LIB_BZINT'] = 'libbzint.a'
        opts['LIBS'] = '$(LIB_ARP) $(LIB_LPK) $(LIB_FFT) $(LIB_BZINT)'
        with open('build/make.inc', 'a') as inc:
            for key in opts:
                inc.write('{0} = {1}\n'.format(key, opts[key]))

    def install(self, spec, prefix):
        install_tree('bin', prefix)
        install_tree('species', prefix.species)
        install_tree('tools', prefix.tools)

    def setup_run_environment(self, env):
        env.set('WNHOME', self.prefix)
        env.set('EXCITINGROOT', self.prefix)
        env.set('EXCITINGBIN', self.prefix.bin)
        env.set('EXCITINGTOOLS', self.prefix.tools)
        env.set('EXCITINGSTM', self.prefix.tools.stm)
        env.set('EXCITINGVISUAL', self.prefix.xml.visualizationtemplates)
        env.set('EXCITINGCONVERT', self.prefix.xml.inputfileconverter)
        env.set('TIMEFORMAT', ' Elapsed time = %0lR')
        env.set('WRITEMINMAX', '1')
        env.append_path('PYTHONPATH', self.prefix.tools.stm)
        env.append_path('PATH', self.prefix.tools)
        env.append_path('PATH', self.prefix)
        env.append_path('PATH', self.prefix.tools.stm)
