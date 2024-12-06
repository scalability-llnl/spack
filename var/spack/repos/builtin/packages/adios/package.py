# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Adios(AutotoolsPackage):
    """The Adaptable IO System (ADIOS) provides a simple,
    flexible way for scientists to describe the
    data in their code that may need to be written,
    read, or processed outside of the running simulation.
    """

    homepage = "https://www.olcf.ornl.gov/center-projects/adios/"
    url = "https://github.com/ornladios/ADIOS/archive/v1.12.0.tar.gz"
    git = "https://github.com/ornladios/ADIOS.git"

    maintainers("ax3l")

    version("develop", branch="master")
    version("1.13.1", sha256="b1c6949918f5e69f701cabfe5987c0b286793f1057d4690f04747852544e157b")
    version("1.13.0", sha256="7b5ee8ff7a5f7215f157c484b20adb277ec0250f87510513edcc25d2c4739f50")
    version("1.12.0", sha256="22bc22c157322abec2d1a0817a259efd9057f88c2113e67d918a9a5ebcb3d88d")
    version("1.11.1", sha256="9f5c10b9471a721ba57d1cf6e5a55a7ad139a6c12da87b4dc128539e9eef370e")
    version("1.11.0", sha256="e89d14ccbe7181777225e0ba6c272c0941539b8ccd440e72ed5a9457441dae83")
    version("1.10.0", sha256="6713069259ee7bfd4d03f47640bf841874e9114bab24e7b0c58e310c42a0ec48")
    version("1.9.0", sha256="23b2bb70540d51ab0855af0b205ca484fd1bd963c39580c29e3133f9e6fffd46")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Builds a shared version of the library")

    variant("fortran", default=False, description="Enable Fortran bindings support")

    variant("mpi", default=True, description="Enable MPI support")
    variant("infiniband", default=False, description="Enable infiniband support")

    # transforms
    variant("zlib", default=True, description="Enable zlib transform support")
    variant("bzip2", default=False, description="Enable bzip2 transform support")
    variant("szip", default=False, description="Enable szip transform support")
    variant("zfp", default=True, description="Enable ZFP transform support")
    variant("sz", default=True, description="Enable SZ transform support")
    variant("lz4", default=True, description="Enable LZ4 transform support")
    variant("blosc", default=True, description="Enable Blosc transform support")
    # transports and serial file converters
    variant(
        "hdf5",
        default=False,
        description="Enable parallel HDF5 transport and serial bp2h5 " + "converter",
    )
    variant("netcdf", default=False, description="Enable netcdf support")

    variant(
        "staging",
        values=any_combination_of("flexpath", "dataspaces"),
        description="Enable dataspaces and/or flexpath staging transports",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")
    depends_on("python", type="build")

    depends_on("mpi", when="+mpi")
    # optional transformations
    depends_on("zlib-api", when="+zlib")
    depends_on("bzip2", when="+bzip2")
    depends_on("szip", when="+szip")
    depends_on("sz@:1.4.10", when="@:1.12.0 +sz")
    depends_on("sz@1.4.11.0:1.4.11", when="@1.13.0 +sz")
    depends_on("sz@1.4.12.3:1.4.12", when="@1.13.1: +sz")
    depends_on("zfp@0.5.1:0.5", when="+zfp")
    depends_on("lz4", when="+lz4")
    depends_on("c-blosc@1.12.0:", when="+blosc")
    # optional transports & file converters
    depends_on("hdf5@1.8:+hl+mpi", when="+hdf5")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("libevpath", when="staging=flexpath")
    depends_on("dataspaces+mpi", when="staging=dataspaces")

    for p in ["+hdf5", "+netcdf", "staging=flexpath", "staging=dataspaces"]:
        conflicts(p, when="~mpi")

    build_directory = "spack-build"

    # ADIOS uses the absolute Python path, which is too long and results in
    # "bad interpreter" errors - but not applicable for 1.9.0
    patch("python.patch", when="@1.10.0:")
    # Fix ADIOS <=1.10.0 compile error on HDF5 1.10+
    #   https://github.com/ornladios/ADIOS/commit/3b21a8a41509
    #   https://github.com/spack/spack/issues/1683
    patch("adios_1100.patch", when="@:1.10.0^hdf5@1.10:")

    # ADIOS 1.13.1 is written for ZFP 0.5.0 interfaces
    #   https://github.com/ornladios/ADIOS/pull/204
    patch("zfp051.patch", when="@1.11.0:1.13.1")

    # Fix a bug in configure.ac that causes automake issues on RHEL 7.7
    patch(
        "https://github.com/ornladios/ADIOS/pull/207.patch?full_index=1",
        when="@1.12.0: +mpi",
        sha256="aea47e56013b57c2d5d36e23e0ae6010541c3333a84003784437768c2e350b05",
    )

    def validate(self, spec):
        """Checks if incompatible variants have been activated at the same time

        Args:
            spec: spec of the package

        Raises:
            RuntimeError: in case of inconsistencies
        """
        if "+fortran" in spec and not self.compiler.fc:
            msg = "cannot build a fortran variant without a fortran compiler"
            raise RuntimeError(msg)

    def with_or_without_hdf5(self, activated):
        if activated:
            return f"--with-phdf5={self.spec['hdf5'].prefix}"

        return "--without-phdf5"

    def setup_build_environment(self, env):
        # https://github.com/ornladios/ADIOS/issues/206
        if self.spec.satisfies("%gcc@10: +fortran"):
            env.set("FCFLAGS", "-fallow-argument-mismatch")

    def configure_args(self):
        spec = self.spec
        self.validate(spec)

        extra_args = [
            # required, otherwise building its python bindings will fail
            f"CFLAGS={self.compiler.cc_pic_flag}"
        ]

        extra_args += self.enable_or_disable("shared")
        extra_args += self.enable_or_disable("fortran")

        if spec.satisfies("+mpi"):
            env["MPICC"] = spec["mpi"].mpicc
            env["MPICXX"] = spec["mpi"].mpicxx

        extra_args += self.with_or_without("mpi", activation_value="prefix")
        extra_args += self.with_or_without("infiniband")

        if spec.satisfies("+zlib"):
            extra_args.append(f"--with-zlib={spec['zlib-api'].prefix}")
        else:
            extra_args.append("--without-zlib")

        # Transforms
        variants = ["bzip2", "szip"]
        if spec.satisfies("@1.11.0:"):
            variants += ["zfp"]
        if spec.satisfies("@1.12.0:"):
            variants += ["sz", "lz4"]
        if spec.satisfies("@1.13.0:"):
            extra_args += self.with_or_without(
                "blosc", activation_value=lambda x: spec["c-blosc"].prefix
            )

        # External I/O libraries
        variants += ["hdf5", "netcdf"]

        for x in variants:
            extra_args += self.with_or_without(x, activation_value="prefix")

        # Staging transports
        def with_staging(name):
            if name == "flexpath":
                return spec["libevpath"].prefix
            return spec[name].prefix

        extra_args += self.with_or_without("staging", activation_value=with_staging)

        return extra_args
