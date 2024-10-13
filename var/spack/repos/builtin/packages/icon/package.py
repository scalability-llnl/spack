# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from collections import defaultdict

from spack.package import *


class Icon(AutotoolsPackage):
    """ICON - is a modeling framework for weather, climate, and environmental prediction. It solves
    the full three-dimensional non-hydrostatic and compressible Navier-Stokes equations on an
    icosahedral grid and allows seamless predictions from local to global scales."""

    homepage = "https://www.icon-model.org"
    url = "https://gitlab.dkrz.de/icon/icon-model/-/archive/icon-2024.01-public/icon-model-icon-2024.01-public.tar.gz"

    maintainers("skosukhin")

    license("BSD-3-Clause", checked_by="skosukhin")

    version("2024.01-1", sha256="3e57608b7e1e3cf2f4cb318cfe2fdb39678bd53ca093955d99570bd6d7544184")
    version("2024.01", sha256="d9408fdd6a9ebf5990298e9a09c826e8c15b1e79b45be228f7a5670a3091a613")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Model Features:
    variant("atmo", default=True, description="Enable the atmosphere component")
    variant("les", default=True, description="Enable the Large-Eddy Simulation component")
    variant("upatmo", default=True, description="Enable the upper atmosphere component")
    variant("ocean", default=True, description="Enable the ocean component")
    variant("jsbach", default=True, description="Enable the land component JSBACH")
    variant("waves", default=True, description="Enable the ocean surface wave component")
    variant("coupling", default=True, description="Enable the coupling")
    variant("aes", default=True, description="Enable the AES physics package")
    variant("nwp", default=True, description="Enable the NWP physics package")
    variant(
        "ecrad", default=False, description="Enable usage of the ECMWF radiation scheme (ECRAD)"
    )
    variant(
        "rte-rrtmgp",
        default=True,
        description="Enable usage of the RTE+RRTMGP toolbox for radiation calculations",
    )
    variant(
        "art", default=False, description="Enable the aerosols and reactive trace component ART"
    )

    # Infrastructural Features:
    variant("mpi", default=True, description="Enable MPI (parallelization) support")
    variant("openmp", default=False, description="Enable OpenMP support")

    nvidia_targets = {"nvidia-{0}".format(cc): cc for cc in CudaPackage.cuda_arch_values}
    # TODO: add AMD GPU support

    variant(
        "gpu",
        default="none",
        values=("none",) + tuple(nvidia_targets.keys()),
        description="Enable GPU support for the specified architecture",
    )
    for __x in nvidia_targets.keys():
        # Other compilers are not yet tested or supported, older NVHPC versions are not supported:
        requires("%nvhpc@21.3:", when="gpu={0}".format(__x))

    variant("mpi-gpu", default=True, description="Enable usage of the GPU-aware MPI features")
    requires("+mpi", when="+mpi-gpu")
    conflicts("gpu=none", when="+mpi-gpu")

    variant("grib2", default=False, description="Enable GRIB2 I/O")

    variant(
        "parallel-netcdf",
        default=False,
        description="Enable usage of the parallel features of NetCDF",
    )
    requires("+mpi", when="+parallel-netcdf")

    variant("cdi-pio", default=False, description="Enable usage of the parallel features of CDI")
    requires("+mpi", when="+cdi-pio")

    variant("yaxt", default=False, description="Enable the YAXT data exchange")
    requires("+mpi", when="+yaxt")

    serialization_values = ("read", "perturb", "create")
    variant(
        "serialization",
        default="none",
        values=("none",) + serialization_values,
        description="Enable the Serialbox2 serialization",
    )

    variant("comin", default=False, description="Enable the ICON community interfaces")

    # Optimization Features:
    variant("mixed-precision", default=False, description="Enable mixed-precision dynamical core")

    depends_on("python", type="build")
    depends_on("perl", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("gmake@3.81:", type="build")
    depends_on("findutils", type="build")

    depends_on("libxml2", when="+art")
    depends_on("libfyaml@0.6:", when="+coupling")
    for __x in serialization_values:
        depends_on("serialbox+fortran", when="serialization={0}".format(__x))
    depends_on("eccodes", when="+grib2")
    depends_on("lapack")
    depends_on("blas")
    depends_on("netcdf-fortran")
    depends_on("netcdf-c")
    depends_on("netcdf-c+mpi", when="+parallel-netcdf")
    depends_on("mpi", when="+mpi")

    for __x in nvidia_targets.keys():
        depends_on("cuda", when="gpu={0}".format(__x))

    def configure_args(self):
        args = ["--disable-rpaths"]
        flags = defaultdict(list)
        libs = LibraryList([])

        for x in [
            "atmo",
            "les",
            "upatmo",
            "jsbach",
            "waves",
            "aes",
            "nwp",
            "ecrad",
            "rte-rrtmgp",
            "openmp",
            "mpi-gpu",
            "parallel-netcdf",
            "cdi-pio",
            "yaxt",
            "mixed-precision",
            "comin",
        ]:
            args += self.enable_or_disable(x)

        if self.spec.satisfies("+art"):
            args.append("--enable-art")
            libs += self.spec["libxml2"].libs
        else:
            args.append("--disable-art")

        if self.spec.satisfies("+coupling"):
            args.append("--enable-coupling")
            libs += self.spec["libfyaml"].libs
        else:
            args.append("--disable-coupling")

        serialization = self.spec.variants["serialization"].value
        if serialization == "none":
            args.append("--disable-serialization")
        else:
            args.extend(
                [
                    "--enable-serialization={0}".format(serialization),
                    "SB2PP={0}".format(self.spec["serialbox"].pp_ser),
                ]
            )
            libs += self.spec["serialbox:fortran"].libs

        if self.spec.satisfies("+grib2"):
            args.append("--enable-grib2")
            libs += self.spec["eccodes:c"].libs
        else:
            args.append("--disable-grib2")

        libs += self.spec["lapack:fortran"].libs
        libs += self.spec["blas:fortran"].libs
        libs += self.spec["netcdf-fortran"].libs
        libs += self.spec["netcdf-c"].libs

        if self.spec.satisfies("+mpi"):
            args.extend(
                [
                    "--enable-mpi",
                    # We cannot provide a universal value for MPI_LAUNCH, therefore we have to
                    # disable the MPI checks:
                    "--disable-mpi-checks",
                    "CC=" + self.spec["mpi"].mpicc,
                    "FC=" + self.spec["mpi"].mpifc,
                ]
            )
        else:
            args.append("--disable-mpi")

        gpu = self.spec.variants["gpu"].value

        if gpu in self.nvidia_targets:
            args.append("--enable-gpu=openacc+cuda")
            flags["CUDAFLAGS"] = [
                "-g",
                "-O3",
                "-arch=sm_{0}".format(self.nvidia_targets[gpu]),
                "-ccbin={0}".format(spack_cxx),
            ]
            flags["ICON_LDFLAGS"].extend(self.compiler.stdcxx_libs)
            libs += self.spec["cuda"].libs
        else:
            args.append("--disable-gpu")

        if self.compiler.name == "gcc":
            flags["CFLAGS"].append("-g")
            flags["ICON_CFLAGS"].append("-O3")
            flags["ICON_BUNDLED_CFLAGS"].append("-O2")
            flags["FCFLAGS"].append("-g")
            flags["ICON_FCFLAGS"].append("-O2")
            if self.spec.satisfies("+ocean"):
                flags["ICON_OCEAN_FCFLAGS"].extend(["-O3", "-fno-tree-loop-vectorize"])
                args.extend(
                    ["--enable-fcgroup-OCEAN", "ICON_OCEAN_PATH=src/hamocc:src/ocean:src/sea_ice"]
                )

        elif self.compiler.name in ["intel", "oneapi"]:
            args.append("--enable-intel-consistency")

            flags["CFLAGS"].extend(["-g", "-ftz", "-fma", "-ip", "-qno-opt-dynamic-align"])
            flags["ICON_CFLAGS"].append("-O3")
            flags["ICON_BUNDLED_CFLAGS"].append("-O2")
            flags["FCFLAGS"].extend(["-g", "-fp-model source"])
            flags["ICON_FCFLAGS"].extend(
                [
                    "-O3",
                    "-ftz",
                    "-qoverride-limits",
                    "-assume realloc_lhs",
                    "-align array64byte",
                    "-fma",
                    "-ip",
                ]
            )

            if self.spec.satisfies("%oneapi+coupling"):
                flags["ICON_YAC_CFLAGS"].extend(["-O2", "-fp-model precise"])

            if self.spec.satisfies("+ocean"):
                flags["ICON_OCEAN_FCFLAGS"].extend(
                    ["-O3", "-assume norealloc_lhs", "-reentrancy threaded"]
                )
                args.extend(
                    ["--enable-fcgroup-OCEAN", "ICON_OCEAN_PATH=src/hamocc:src/ocean:src/sea_ice"]
                )

                if self.spec.satisfies("+openmp"):
                    flags["ICON_OCEAN_FCFLAGS"].extend(["-DOCE_SOLVE_OMP"])

            if self.spec.satisfies("+ecrad"):
                flags["ICON_ECRAD_FCFLAGS"].extend(["-qno-opt-dynamic-align", "-no-fma", "-fpe0"])

        elif self.compiler.name == "nvhpc":
            flags["CFLAGS"].extend(["-g", "-O2"])
            flags["FCFLAGS"].extend(
                ["-g", "-O2", "-Mrecursive", "-Mallocatable=03", "-Mstack_arrays"]
            )

            if gpu in self.nvidia_targets:
                flags["FCFLAGS"].extend(
                    ["-acc=gpu", "-gpu=cc{0}".format(self.nvidia_targets[gpu])]
                )

            if self.spec.satisfies("%nvhpc@:23.9+coupling"):
                args.append("yac_cv_fc_is_contiguous_works=yes")

        else:
            flags["CFLAGS"].extend(["-g", "-O2"])
            flags["FCFLAGS"].extend(["-g", "-O2"])

        args.extend(["{0}={1}".format(name, " ".join(value)) for name, value in flags.items()])
        args.append("LIBS={0}".format(libs.link_flags))

        return args
