# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Regcm(AutotoolsPackage):
    """RegCM, ICTP Regional Climate Model (https://ictp.it)."""

    homepage = "https://gforge.ictp.it/gf/project/regcm/"

    license("AFL-1.1")

    version(
        "4.7.0",
        sha256="456631c10dcb83d70e51c3babda2f7a1aa41ed9e60cb4209deb3764655267519",
        url="https://gforge.ictp.it/gf/download/frsrelease/259/1845/RegCM-4.7.0.tar.gz",
    )

    variant("debug", default=False, description="Build RegCM using debug options.")
    variant("profile", default=False, description="Build RegCM using profiling options.")
    variant(
        "singleprecision",
        default=False,
        description="Build RegCM using single precision float type.",
    )

    # On Intel and PGI compilers, multiple archs can be built at the same time,
    # producing a so-called fat binary. Unfortunately, gcc builds only the last
    # architecture provided at the configure line.
    # For this reason, we allow a single arch when using GCC (checks are
    # performed below in the configure_args).
    # Moreover, RegCM supports optimizations only for GCC and Intel compilers.
    # To sum up:
    # - intel: a user is able to build a single executables for all the
    #   combinations of architectures (e.g. `--extension=knl,skl,bdw,nhl`);
    # - gcc: a user is allowed to build an executable using a single
    #   optimization/extension;
    # - other compilers: no extensions/optimizations are supported.
    #
    # See also discussions: #974, #9934, #10797.
    extensions = ("knl", "skl", "bdw", "nhl")
    variant(
        "extension",
        values=any_combination_of(*extensions),
        description="Build extensions for a specific architecture. Only "
        "available for GCC and Intel compilers; moreover, "
        "GCC builds only one architecture optimization.",
    )

    variant(
        "pnetcdf",
        default=False,
        description="Build NetCDF using the high performance parallel " "NetCDF implementation.",
    )

    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("hdf5")
    depends_on("mpi")
    depends_on("netcdf-c +parallel-netcdf", when="+pnetcdf")

    intel_msg = (
        "Intel compiler not working with this specific version of "
        "RegCM (generates a bug at runtime): please install a newer "
        "version of RegCM or use a different compiler."
    )
    conflicts("%intel", when="@4.7.0", msg=intel_msg)

    # 'make' sometimes crashes when compiling with more than 10-12 cores.
    # Moreover, parallel compile time is ~ 1m 30s, while serial is ~ 50s.
    parallel = False

    def flag_handler(self, name, flags):
        if name == "fflags" and self.compiler.fc.endswith("gfortran"):
            flags.extend(
                [
                    "-Wall",
                    "-Wextra",
                    "-Warray-temporaries",
                    "-Wconversion",
                    "-fimplicit-none",
                    "-fbacktrace",
                    "-ffree-line-length-0",
                    "-finit-real=nan",
                    "-ffpe-trap=zero,overflow,underflow",
                    "-fcheck=all",
                ]
            )

        elif name == "ldlibs":
            flags.extend(["-lnetcdff", "-lnetcdf"])
            if self.compiler.fc.endswith("gfortran"):
                flags.extend(["-lm", "-ldl"])
            else:
                flags.extend(["-lhdf5_hl", "-lhdf5", "-lz"])

        return (None, None, flags)

    def configure_args(self):
        args = ["--enable-shared"]

        optimizations = self.spec.variants["extension"].value
        first_optim = optimizations[0]

        if first_optim != "none":
            if not (self.spec.satisfies(r"%gcc") or self.spec.satisfies(r"%intel")):
                # This means the user chose some optimizations on a different
                # compiler from GCC and Intel, which are the only compiler
                # supported by RegCM 4.7.x.
                raise InstallError(
                    "Architecture optimizations are available " "only for GCC and Intel compilers."
                )

            if len(optimizations) > 1 and self.spec.satisfies(r"%gcc"):
                # https://github.com/spack/spack/issues/974
                raise InstallError(
                    "The GCC compiler does not support " "multiple architecture optimizations."
                )

            # RegCM configure script treats --disable-X as --enable-X, so we
            # cannot use enable_or_disable; enable only the flags requested.
            args += ("--enable-" + ext for ext in optimizations)

        for opt in ("debug", "profile", "singleprecision"):
            if ("+" + opt) in self.spec:
                args.append("--enable-" + opt)

        # RegCM SVN6916 introduced a specific flag to use some pnetcdf calls.
        if "+pnetcdf" in self.spec and "@4.7.0-SVN6916:" in self.spec:
            args.append("--enable-parallel-nc")

        # RegCM doesn't listen to the FFLAGS variable, so we have to route
        # flags to FCFLAGS.
        fcflags = list(self.spec.compiler_flags["fflags"])

        # RegCM complains when compiled with gfortran.
        if self.compiler.fc.endswith("gfortran"):
            fcflags.append("-fno-range-check")

        args.append("FCFLAGS=" + " ".join(fcflags))

        # The configure needs a hint on the MPI Fortran compiler, otherwise it
        # doesn't find it and tries to compile MPI Fortran code with the system
        # Fortran non-MPI compiler.
        args.append("MPIFC=" + self.spec["mpi"].mpifc)

        return args
