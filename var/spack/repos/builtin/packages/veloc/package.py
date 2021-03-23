# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Veloc(CMakePackage):
    """Very-Low Overhead Checkpointing System. VELOC is a multi-level
    checkpoint-restart runtime for HPC supercomputing infrastructures"""

    homepage = "https://github.com/ECP-VeloC/VELOC"
    url      = "https://github.com/ECP-VeloC/VELOC/archive/veloc-1.0rc1.zip"
    git      = "https://github.com/ecp-veloc/veloc.git"

    tags = ['ecp']

    version('master', branch='master')
    version('1.4',    sha256='d5d12aedb9e97f079c4428aaa486bfa4e31fe1db547e103c52e76c8ec906d0a8')
    version('1.1',    sha256='2bbdacf3e0ce4e7c9e360874d8d85b405525bdc7bd992bdb1f1ba49218072160')
    version('1.0',    sha256='d594b73d6549a61fce8e67b8984a17cebc3e766fc520ed1636ae3683cdde77cb')
    version('1.0rc1', sha256='81686ca0994a22475911d38d21c7c74b64ffef4ca872fd01f76d155c5124b0bc')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('libpthread-stubs')
    depends_on('mpi')
    depends_on('er')
    depends_on('axl')
    depends_on('openssl')  # Relies on the OpenSSL crypto library for checksums
    depends_on('pdsh', when='@master')
    depends_on('cmake@3.9:', type='build')

    conflicts('%gcc@:4.9.3')

    # requires C++11
    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)

    def cmake_args(self):
        args = [
            "-DWITH_AXL_PREFIX=%s" % self.spec['axl'].prefix,
            "-DWITH_ER_PREFIX=%s" % self.spec['er'].prefix,
            "-DBOOST_ROOT=%s" % self.spec['boost'].prefix,
            "-DMPI_CXX_COMPILER=%s" % self.spec['mpi'].mpicxx
        ]

        return args
