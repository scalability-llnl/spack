# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvplFft(Package):
    """NVPL FFT (NVIDIA Performance Libraries FFT) is part of NVIDIA Performance Libraries
    and provides Fast Fourier Transform (FFT) calculations on ARM CPUs.
    """

    homepage = "https://docs.nvidia.com/nvpl/_static/blas/index.html"
    url = (
        "https://developer.download.nvidia.com/compute/nvpl/redist"
        "/nvpl_fft/linux-sbsa/nvpl_fft-linux-sbsa-0.1.0-archive.tar.xz"
    )

    license("UNKNOWN")

    version("0.3.0", sha256="e20791b77fa705e5a4f7aa5dada39b2a41e898189e0e60e680576128d532269b")
    version("0.2.0.2", sha256="264343405aad6aca451bf8bd0988b6217b2bb17fd8f99394b83e04d9ab2f7f91")
    version("0.1.0", sha256="0344f8e15e5b40f4d552f7013fe04a32e54a092cc3ebede51ddfce74b44c6e7d")

    provides("fftw-api@3")

    requires("target=armv8.2a:", msg="Any CPU with Arm-v8.2a+ microarch")

    conflicts("%gcc@:7")
    conflicts("%clang@:13")

    def url_for_version(self, version):
        url = "https://developer.download.nvidia.com/compute/nvpl/redist/nvpl_fft/linux-sbsa/nvpl_fft-linux-sbsa-{0}-archive.tar.xz"
        return url.format(version)

    def install(self, spec, prefix):
        install_tree(".", prefix)
