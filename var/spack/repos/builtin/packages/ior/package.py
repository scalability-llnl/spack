# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ior(AutotoolsPackage):
    """The IOR software is used for benchmarking parallel file systems
    using POSIX, MPI-IO, or HDF5 interfaces."""

    homepage = "https://github.com/hpc/ior"
    url = "https://github.com/hpc/ior/archive/3.2.1.tar.gz"

    version("develop", git="https://github.com/hpc/ior.git", branch="main")
    version("4.0.0", sha256="cb17f6b0d17fb98dae28abaa116fd3adde411f52d45ff9efb125efc791b97463")
    version(
        "3.3.0",
        sha256="701f2167f81ef963e227d4c036c4a947a98b5642b7c14c87c8ae657849891528",
        preferred=True,
    )
    version("3.3.0rc1", sha256="0e42ebf5b5adae60625bf97989c8e2519d41ea2e3d18561d7d5b945625317aa5")
    version("3.2.1", sha256="ebcf2495aecb357370a91a2d5852cfd83bba72765e586bcfaf15fb79ca46d00e")
    version("3.2.0", sha256="91a766fb9c34b5780705d0997b71b236a1120da46652763ba11d9a8c44251852")
    version("3.0.1", sha256="0cbefbcdb02fb13ba364e102f9e7cc2dcf761698533dac25de446a3a3e81390d")

    depends_on("c", type="build")  # generated

    variant("hdf5", default=False, description="support IO with HDF5 backend")
    variant("ncmpi", default=False, description="support IO with NCMPI backend")
    variant("lustre", default=False, description="support configurable Lustre striping values")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("mpi")
    depends_on("hdf5+mpi", when="+hdf5")
    depends_on("parallel-netcdf", when="+ncmpi")
    depends_on("lustre", when="+lustre")

    # The build for 3.2.0 fails if hdf5 is enabled
    # See https://github.com/hpc/ior/pull/124
    patch(
        "https://github.com/hpc/ior/commit/1dbca5c293f95074f9887ddb2043fa984670fb4d.patch?full_index=1",
        sha256="ce7fa0eabf408f9b712c478a08aa62d68737d213901707ef8cbfc3aec02e2713",
        when="@3.2.0 +hdf5",
    )

    # Needs patch to make Lustre variant work
    # See https://github.com/hpc/ior/issues/353
    patch(
        "https://github.com/glennklockwood/ior/commit/e49476be64d4100c2da662ea415f327348b3d11d.patch?full_index=1",
        sha256="ee3527023ef70ea9aee2e6208f8be7126d5a48f26c587deed3d6238b4f848a06",
        when="+lustre",
    )

    @run_before("autoreconf")
    def bootstrap(self):
        Executable("./bootstrap")()

    def configure_args(self):
        spec = self.spec
        config_args = []

        env["CC"] = spec["mpi"].mpicc

        if spec.satisfies("+hdf5"):
            config_args.append("--with-hdf5")
            config_args.append("CFLAGS=-D H5_USE_16_API")
        else:
            config_args.append("--without-hdf5")

        if spec.satisfies("+ncmpi"):
            config_args.append("--with-ncmpi")
        else:
            config_args.append("--without-ncmpi")

        if spec.satisfies("+lustre"):
            config_args.append("--with-lustre")
        else:
            config_args.append("--without-lustre")

        return config_args
