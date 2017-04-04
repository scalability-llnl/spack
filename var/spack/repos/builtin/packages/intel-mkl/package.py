##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os

from spack.pkg.builtin.intel import IntelInstaller


class IntelMkl(IntelInstaller):
    """Intel Math Kernel Library."""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('2017.2.174', 'ef39a12dcbffe5f4a0ef141b8759208c',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11306/l_mkl_2017.2.174.tgz")
    version('2017.0.098', '3cdcb739ab5ab1e047eb130b9ffdd8d0',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9662/l_mkl_2017.0.098.tgz")
    version('11.3.3.210', 'f72546df27f5ebb0941b5d21fd804e34',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9068/l_mkl_11.3.3.210.tgz")
    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8711/l_mkl_11.3.2.181.tgz")

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False, description='64 bit integers')
    variant('openmp', default=False, description='OpenMP multithreading layer')

    # virtual dependency
    provides('blas')
    provides('lapack')
    provides('scalapack')
    provides('mkl')

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
        return self.libs

    @property
    def scalapack_libs(self):
        libnames = ['libmkl_scalapack']
        if self.spec.satisfies('^openmpi'):
            libnames.append('libmkl_blacs_openmpi')
        elif self.spec.satisfies('^mpich@1'):
            libnames.append('libmkl_blacs')
        elif self.spec.satisfies('^mpich@2:'):
            libnames.append('libmkl_blacs_intelmpi')
        elif self.spec.satisfies('^mvapich2'):
            libnames.append('libmkl_blacs_intelmpi')
        elif self.spec.satisfies('^mpt'):
            libnames.append('libmkl_blacs_sgimpt')
        # TODO: ^intel-parallel-studio can mean intel mpi, a compiler or a lib
        # elif self.spec.satisfies('^intel-parallel-studio'):
        #     libnames.append('libmkl_blacs_intelmpi')
        else:
            raise InstallError("No MPI found for scalapack")

        shared = True if '+shared' in self.spec else False
        integer = 'ilp64' if '+ilp64' in self.spec else 'lp64'
        libs = find_libraries(
            ['{0}_{1}'.format(l, integer) for l in libnames],
            root=join_path(self.prefix.lib, 'intel64'),
            shared=shared
        )
        return libs

    def install(self, spec, prefix):
        self.intel_prefix = os.path.join(prefix, "pkg")
        IntelInstaller.install(self, spec, prefix)

        mkl_dir = os.path.join(self.intel_prefix, "mkl")
        for f in os.listdir(mkl_dir):
            os.symlink(os.path.join(mkl_dir, f), os.path.join(self.prefix, f))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # set up MKLROOT for everyone using MKL package
        spack_env.set('MKLROOT', self.prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.set('MKLROOT', self.prefix)
