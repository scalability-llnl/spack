# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import numbers

from spack.package import *


def is_integral(x):
    """Any integer value"""
    try:
        return isinstance(int(x), numbers.Integral) and not isinstance(x, bool)
    except ValueError:
        return False


class Npb(MakefilePackage):
    """The NAS Parallel Benchmarks (NPB) are a small set of programs
    designed to help evaluate the performance of parallel supercomputers.

    The benchmarks are derived from computational fluid dynamics (CFD)
    applications and consist of five kernels and three pseudo-applications
    in the original "pencil-and-paper" specification (NPB 1). The benchmark
    suite has been extended to include new benchmarks for unstructured
    adaptive mesh, parallel I/O, multi-zone applications, and computational
    grids. Problem sizes in NPB are predefined and indicated as different
    classes. Reference implementations of NPB are available in commonly-used
    programming models like MPI and OpenMP (NPB 2 and NPB 3).
    """

    homepage = "https://www.nas.nasa.gov/publications/npb.html"
    url = "https://www.nas.nasa.gov/assets/npb/NPB3.3.1.tar.gz"

    version("3.3.1", sha256="4a8ea679b1df69f583c544c47198b3c26a50ec2bb6f8f69aef66c04c9a747d2d")
    version("3.4.1", sha256="f3a43467da6e84a829ea869156d3ea86c17932136bb413a4b6dab23018a28881")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Valid Benchmark Names
    valid_names = (
        "is",  # Integer Sort, random memory access
        "ep",  # Embarrassingly Parallel
        "cg",  # Conjugate Gradient, irregular memory access and communication
        "mg",  # Multi-Grid on a sequence of meshes, long- and short-distance
        # communication, memory intensive
        "ft",  # discrete 3D fast Fourier Transform, all-to-all communication
        "bt",  # Block Tri-diagonal solver
        "sp",  # Scalar Penta-diagonal solver
        "lu",  # Lower-Upper Gauss-Seidel solver
    )

    # Valid Benchmark Classes
    valid_classes = (
        "S",  # Small for quick test purposes
        "W",  # Workstation size
        "A",
        "B",
        "C",  # standard test problems
        # ~4X size increase going from one class to the next
        "D",
        "E",
        "F",  # large test problems
        # ~16X size increase from each of the previous classes
    )

    # TODO: Combine these into a single mutually exclusive variant
    variant(
        "implementation",
        default="mpi",
        values=("serial", "mpi", "openmp"),
        description="Selects one among the available implementations",
    )

    variant(
        "names",
        default=",".join(valid_names),
        values=valid_names,
        multi=True,
        description="Benchmark names (comma separated list)",
    )

    variant(
        "classes",
        default=",".join(valid_classes),
        values=valid_classes,
        multi=True,
        description="Benchmark classes (comma separated list)",
    )

    # This variant only applies to the MPI implementation
    variant(
        "nprocs",
        default="1,2,4,8,16,32,64,128",
        values=is_integral,
        multi=True,
        description="Number of processes (comma separated list)",
    )

    depends_on("mpi@2:", when="implementation=mpi")

    # Cannot be built in parallel
    parallel = False

    @property
    def build_directory(self):
        if "implementation=mpi" in self.spec:
            implementation = "MPI"
        elif "implementation=openmp" in self.spec:
            implementation = "OMP"
        elif "implementation=serial" in self.spec:
            implementation = "SER"
        else:
            raise RuntimeError("You must choose an implementation to build")

        return "NPB{0}-{1}".format(self.version.up_to(2), implementation)

    def edit(self, spec, prefix):
        names = spec.variants["names"].value
        classes = spec.variants["classes"].value
        nprocs = spec.variants["nprocs"].value

        if "implementation=mpi" in spec:
            fflags = fflags = ["-O3"]
            if spec.satisfies("%gcc@10:"):
                fflags.append("-fallow-argument-mismatch")

            definitions = {
                # Parallel Fortran
                "MPIFC": spec["mpi"].mpifc,
                "MPIF77": spec["mpi"].mpif77,
                "FLINK": spec["mpi"].mpif77,
                "FMPI_LIB": spec["mpi"].libs.ld_flags,
                "FMPI_INC": "-I" + spec["mpi"].prefix.include,
                "FFLAGS": " ".join(fflags),
                "FLINKFLAGS": "-O3",
                # Parallel C
                "MPICC": spec["mpi"].mpicc,
                "CLINK": spec["mpi"].mpicc,
                "CMPI_LIB": spec["mpi"].libs.ld_flags,
                "CMPI_INC": "-I" + spec["mpi"].prefix.include,
                "CFLAGS": "-O3",
                "CLINKFLAGS": "-O3",
                # Utilities C
                "CC": spack_cc + " -g",
                "BINDIR": prefix.bin,
                "RAND": "randi8",
            }
        elif "implementation=openmp" in spec:
            definitions = {
                # Parallel Fortran
                "FC": spack_fc,
                "F77": spack_f77,
                "FLINK": spack_f77,
                "F_LIB": "",
                "F_INC": "",
                "FFLAGS": "-O3 " + self.compiler.openmp_flag,
                "FLINKFLAGS": "-O3 " + self.compiler.openmp_flag,
                # Parallel C
                "CC": spack_cc,
                "CLINK": spack_cc,
                "C_LIB": "-lm",
                "C_INC": "",
                "CFLAGS": "-O3 " + self.compiler.openmp_flag,
                "CLINKFLAGS": "-O3 " + self.compiler.openmp_flag,
                # Utilities C
                "UCC": spack_cc,
                "BINDIR": prefix.bin,
                "RAND": "randi8",
                "WTIME": "wtime.c",
            }
        elif "implementation=serial" in spec:
            definitions = {
                # Parallel Fortran
                "F77": spack_f77,
                "FLINK": spack_f77,
                "F_LIB": "",
                "F_INC": "",
                "FFLAGS": "-O3",
                "FLINKFLAGS": "-O3",
                # Parallel C
                "CC": spack_cc,
                "CLINK": spack_cc,
                "C_LIB": "-lm",
                "C_INC": "",
                "CFLAGS": "-O3",
                "CLINKFLAGS": "-O3",
                # Utilities C
                "UCC": spack_cc,
                "BINDIR": prefix.bin,
                "RAND": "randi8",
                "WTIME": "wtime.c",
            }

        with working_dir(self.build_directory):
            with open("config/make.def", "w") as make_def:
                for key in definitions:
                    make_def.write("{0} = {1}\n".format(key, definitions[key]))

            with open("config/suite.def", "w") as suite_def:
                for name in names:
                    for classname in classes:
                        # Classes C, D, E  and F are not available for DT
                        if name == "dt" and classname in ("C", "D", "E", "F"):
                            continue

                        # Class E, F is not available for IS at @3.3.1
                        # Class F is not available for IS at @3.4.1
                        if name == "is":
                            if classname == "E":
                                if spec.satisfies("@3.3.1"):
                                    continue
                            if classname == "F":
                                continue

                        if "implementation=mpi" in spec and spec.satisfies("@3.3.1"):
                            for nproc in nprocs:
                                suite_def.write("{0}\t{1}\t{2}\n".format(name, classname, nproc))
                        else:
                            suite_def.write("{0}\t{1}\n".format(name, classname))

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        with working_dir(self.build_directory):
            make("suite")
