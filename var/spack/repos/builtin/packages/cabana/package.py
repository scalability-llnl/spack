# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cabana(CMakePackage):
    """The Exascale Co-Design Center for Particle Applications Toolkit
    """
    homepage = "https://github.com/ECP-copa/Cabana"
    git      = "https://github.com/ECP-copa/Cabana.git"
    url      = "https://github.com/ECP-copa/Cabana/archive/0.1.0.tar.gz"

    version('master', branch='master')
    version('0.3.0', sha256='fb67ab9aaf254b103ae0eb5cc913ddae3bf3cd0cf6010e9686e577a2981ca84f')
    version('0.2.0', sha256='3e0c0e224e90f4997f6c7e2b92f00ffa18f8bcff72f789e0908cea0828afc2cb')
    version('0.1.0', sha256='3280712facf6932b9d1aff375b24c932abb9f60a8addb0c0a1950afd0cb9b9cf')
    version('0.1.0-rc0', sha256='73754d38aaa0c2a1e012be6959787108fec142294774c23f70292f59c1bdc6c5')

    variant('serial', default=True, description="enable Serial backend (default)")
    variant('openmp', default=False, description="enable OpenMP backend")
    variant('cuda', default=False, description="enable Cuda backend")
    variant('shared', default=True, description='Build shared libraries')
    variant('mpi', default=True, description='Build with mpi support')

    depends_on("cmake@3.9:", type='build')
    depends_on("kokkos-legacy+serial", when="@:0.2.0+serial")
    depends_on("kokkos-legacy+openmp", when="@:0.2.0+openmp")
    depends_on("kokkos-legacy+cuda", when="@:0.2.0+cuda")
    depends_on("kokkos@3.1:+serial", when="@0.3.0:+serial")
    depends_on("kokkos@3.1:+openmp", when="@0.3.0:+openmp")
    depends_on("kokkos@3.1:+cuda", when="@0.3.0:+cuda")
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        options = [
            '-DCabana_ENABLE_TESTING=ON',
            '-DCabana_ENABLE_Serial=%s'  % (
                'On' if '+serial'  in self.spec else 'Off'),
            '-DCabana_ENABLE_OpenMP=%s'  % (
                'On' if '+openmp'  in self.spec else 'Off'),
            '-DCabana_ENABLE_Cuda=%s'  % (
                'On' if '+cuda'  in self.spec else 'Off'),
            '-DCabana_ENABLE_MPI=%s'  % (
                'On' if '+mpi'  in self.spec else 'Off'),
            '-DBUILD_SHARED_LIBS=%s' % (
                'On' if '+shared'  in self.spec else 'Off')
        ]

        return options
