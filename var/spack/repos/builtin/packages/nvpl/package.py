# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvpl(Package):
    """
    NVPL (NVIDIA Performance Libraries) is  are a collection of 
    essential math libraries optimized for Arm 64-bit architectures.
    """

    homepage = "https://docs.nvidia.com/nvpl/"
    url = (
        "https://developer.download.nvidia.com/compute/nvpl/24.7/local_installers/nvpl-linux-sbsa-24.7.tar.gz"
    )

    maintainers("fspiga")

    skip_version_audit = ["platform=darwin", "platform=windows"]

    redistribute(source=False, binary=False)

    version("24.7", sha256="25362d64629fcf85fcb4b2ad59f7d492dc5f14dca2c9e35e822063a9b39507fc")

    # TODO: add "fftw" when Fortran FFTW API completed
    provides("blas")
    provides("lapack")
    #provides("fftw-api@3")

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    requires("target=armv8.2a:", msg="Any CPU with Arm-v8.2a+ microarch")

    conflicts("target=x86:", msg="Only available on Aarch64")
    conflicts("target=ppc64:", msg="Only available on Aarch64")
    conflicts("target=ppc64le:", msg="Only available on Aarch64")

    requires("target=armv8.2a:", msg="Any CPU with Arm-v8.2a+ microarch")

    conflicts("%gcc@:7")
    conflicts("%clang@:13")
    conflicts("threads=openmp", when="%clang")

    def url_for_version(self, version):
        url = "https://developer.download.nvidia.com/compute/nvpl/{0}/local_installers/nvpl-linux-sbsa-{0}.tar.gz"
        return url.format(version)

    @property
    def blas_headers(self):
        return find_all_headers(self.spec.prefix.include)

    @property
    def blas_libs(self):
        spec = self.spec

        if "+ilp64" in spec:
            int_type = "ilp64"
        else:
            int_type = "lp64"

        if spec.satisfies("threads=openmp"):
            threading_type = "gomp"
        else:
            # threads=none
            threading_type = "seq"

        name = ["libnvpl_blas_core", f"libnvpl_blas_{int_type}_{threading_type}"]

        return find_libraries(name, spec.prefix.lib, shared=True, recursive=True)

    @property
    def lapack_headers(self):
        return find_all_headers(self.spec.prefix.include)

    @property
    def lapack_libs(self):
        spec = self.spec

        if "+ilp64" in spec:
            int_type = "ilp64"
        else:
            int_type = "lp64"

        if spec.satisfies("threads=openmp"):
            threading_type = "gomp"
        else:
            # threads=none
            threading_type = "seq"

        name = ["libnvpl_lapack_core", f"libnvpl_lapack_{int_type}_{threading_type}"]

        return find_libraries(name, spec.prefix.lib, shared=True, recursive=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)

