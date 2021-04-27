# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hipfft(CMakePackage):
    """hipFFT is an FFT marshalling library. Currently,
       hipFFT supports either rocFFT or cuFFT as backends."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipFFT"
    url      = "https://github.com/ROCmSoftwarePlatform/hipFFT/archive/refs/tags/rocm-4.1.0.tar.gz"

    maintainers = ['arjun-raj-kuppala', 'sreekolam']

    version('4.1.0', sha256='885ffd4813f2c271150f1b8b386f0af775b38fc82b96ce6fd94eb4ba0c0180be')

    depends_on('hip@4.1.0')
    depends_on('hip-rocclr@4.1.0')
    depends_on('rocfft@4.1.0')
    depends_on('rocm-cmake@4.1.0', type='build')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
