# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsharp(AutotoolsPackage):
    """Libsharp is a code library for spherical harmonic transforms (SHTs) and
    spin-weighted spherical harmonic transforms, which evolved from the libpsht
    library."""

    variant("openmp", default=True, description="Build with openmp support")
    variant("mpi", default=True, description="Build with MPI support")
    variant("pic", default=True, description="Generate position-independent code (PIC)")

    homepage = "https://github.com/Libsharp/libsharp"
    git = "https://github.com/Libsharp/libsharp.git"

    license("GPL-2.0-or-later")

    version("1.0.0", commit="cc4753ff4b0ef393f0d4ada41a175c6d1dd85d71", preferred=True)
    version("2018-01-17", commit="593d4eba67d61827191c32fb94bf235cb31205e1")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("mpi", when="+mpi")

    patch("arm.patch", when="@2018-01-17 target=aarch64:")
    patch("1.0.0-arm.patch", when="@1.0.0 target=aarch64:")

    def autoreconf(self, spec, prefix):
        """Generate autotools configuration"""
        bash = which("bash")
        bash("autoconf")

    def configure_args(self):
        args = []
        if "+openmp" not in self.spec:
            args.append("--disable-openmp")
        if "+mpi" not in self.spec:
            args.append("--disable-mpi")
        if self.spec.satisfies("+pic"):
            args.append("--enable-pic")
        return args

    def install(self, spec, prefix):
        # Libsharp's only caller healpix include headers like 'libsharp/xxx.h'
        # Install xxx.h to include/libsharp
        install_tree("auto/include", prefix.include.libsharp)
        install_tree("auto/lib", prefix.lib)
