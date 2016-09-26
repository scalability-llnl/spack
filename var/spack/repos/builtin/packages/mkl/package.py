from spack import *
import os

from spack.pkg.builtin.intel import IntelInstaller


class Mkl(IntelInstaller):
    """Intel Math Kernel Library.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html.

    To set the threading layer at run time set MKL_THREADING_LAYER
    variable to one of the following values: INTEL (default), SEQUENTIAL, PGI.
    To set interface layer at run time, use set the MKL_INTERFACE_LAYER
    variable to LP64 (default) or ILP64.
    """

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="file://%s/l_mkl_11.3.2.181.tgz" % os.getcwd())
    version('11.3.3.210', 'f72546df27f5ebb0941b5d21fd804e34',
            url="file://%s/l_mkl_11.3.3.210.tgz" % os.getcwd())

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False, description='64 bit integers')
    variant('openmp', default=False, description='OpenMP multithreading layer')

    # virtual dependency
    provides('blas')
    provides('lapack')
    # TODO: MKL also provides implementation of Scalapack.

    @property
    def blas_libs(self):
        shared = True if '+shared' in self.spec else False
        suffix = dso_suffix if '+shared' in self.spec else 'a'
        mkl_integer = ['libmkl_intel_ilp64'] if '+ilp64' in self.spec else ['libmkl_intel_lp64']  # NOQA: ignore=E501
        mkl_threading = ['libmkl_sequential']
        if '+openmp' in self.spec:
            mkl_threading = ['libmkl_intel_thread', 'libiomp5'] if '%intel' in self.spec else ['libmkl_gnu_thread']  # NOQA: ignore=E501
        # TODO: TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']
        mkl_libs = find_libraries(
            mkl_integer + ['libmkl_core'] + mkl_threading,
            root=join_path(self.prefix.lib, 'intel64'),
            shared=shared
        )
        system_libs = [
            'libpthread.{0}'.format(suffix),
            'libm.{0}'.format(suffix),
            'libdl.{0}'.format(suffix)
        ]
        return mkl_libs + system_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    def install(self, spec, prefix):
        self.intel_prefix = os.path.join(prefix, "pkg")
        IntelInstaller.install(self, spec, prefix)

        mkl_dir = os.path.join(self.intel_prefix, "mkl")
        for f in os.listdir(mkl_dir):
            os.symlink(os.path.join(mkl_dir, f), os.path.join(self.prefix, f))

        # Unfortunately MKL libs are natively distrubted in prefix/lib/intel64.
        # To make MKL play nice with Spack, symlink all files to prefix/lib:
        mkl_lib_dir = os.path.join(prefix, "lib", "intel64")
        for f in os.listdir(mkl_lib_dir):
            os.symlink(os.path.join(mkl_lib_dir, f),
                       os.path.join(self.prefix, "lib", f))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # set up MKLROOT for everyone using MKL package
        spack_env.set('MKLROOT', self.prefix)

    def setup_environment(self, spack_env, env):
        env.set('MKLROOT', self.prefix)
