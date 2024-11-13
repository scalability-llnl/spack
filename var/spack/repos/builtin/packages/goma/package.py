# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Goma(CMakePackage):
    """A Full-Newton Finite Element Program for Free and Moving Boundary Problems with
    Coupled Fluid/Solid Momentum, Energy, Mass, and Chemical Species Transport"""

    homepage = "https://www.gomafem.com"
    url = "https://github.com/goma/goma/archive/v7.0.0.tar.gz"
    git = "https://github.com/goma/goma.git"

    maintainers("wortiz")

    license("GPL-2.0-or-later")

    version("7.8.2", commit="968790728b7544f6e362792748c3842d6c5e2bd9")
    version("7.7.0", commit="936caf27cab74023d8dfd792cc5411b8c92f2a04")
    version("7.6.1", commit="c799e935009b85e00979fa8b248952194f6ade7a")
    version("7.4.3", commit="bb0cf8030f9e8d61066d052ea6fad67fe49651f8")
    version("7.3.0", commit="415f442953e2171afae1f8ad55868052c6f511ce")
    version("7.2.0", commit="814f433aa5674c07274fffd4a619d80cd31f71ab")
    version("7.1.3", commit="8e8ffbe872f41ca4675e1588140c5b9dfe17e9e4")
    version("7.1.1", commit="4bebca85ab3840709b44f63502893af6453710e8")
    version("7.0.4", commit="27b2cb2477fa92f9457597f588c137de2572ef69")
    version("7.0.0", commit="5166896f273e5853e1f32885e20f68317b24979c")
    version("release", branch="release")
    version("main", branch="main")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Problem size variants
    variant(
        "max_conc",
        default="4",
        values=("4", "8", "10", "15", "20"),
        description="Set internal maximum number of species",
    )
    variant(
        "max_external_field",
        default="4",
        values=("4", "8", "10", "15", "20"),
        description="Set internal maximum number of external fields",
    )
    variant(
        "max_prob_var",
        default="15",
        values=("10", "15", "20", "25", "28", "34", "40", "46", "64"),
        description="Set internal maximum number of active equations",
    )
    variant(
        "mde",
        default="27",
        values=("8", "9", "10", "16", "20", "27", "54"),
        description="Set internal maximum DOF per element",
    )
    variant(
        "max_number_matls",
        default="9",
        values=("9", "10", "15", "20", "25", "30", "45", "50", "55"),
        description="Set internal maximum number of materials",
    )

    # Floating point checks
    variant("check_finite", default=False, description="Enable finite computation check")
    variant("fpe", default=False, description="Enable floating point exception")

    # Optional third party libraries
    variant("arpack-ng", default=True, description="Build with ARPACK support")
    variant("metis", default=True, description="Build with metis decomposition")
    variant("omega-h", default=True, description="Build with Omega_h support")
    variant("petsc", default=True, description="Build with PETSc solver support")
    variant("sparse", default=True, description="Build with legacy sparse solver")
    variant("suite-sparse", default=True, description="Build with UMFPACK support")

    # Required dependencies
    depends_on("mpi")
    depends_on("seacas+applications")
    depends_on("trilinos+mpi+epetra+aztec+amesos+stratimikos+teko+mumps+superlu-dist+ml~exodus")

    # Optional dependencies
    depends_on("arpack-ng", when="+arpack-ng")
    depends_on("metis", when="+metis")
    depends_on("omega-h+mpi", when="+omega-h")
    depends_on("petsc+hypre+mpi~exodusii", when="+petsc")
    depends_on("sparse", when="+sparse")
    depends_on("suite-sparse", when="+suite-sparse")

    def cmake_args(self):
        args = []

        # Problem sizes
        args.append(self.define_from_variant("MAX_CONC", "max_conc"))
        args.append(self.define_from_variant("MAX_EXTERNAL_FIELD", "max_external_field"))
        args.append(self.define_from_variant("MAX_PROB_VAR", "max_prob_var"))
        args.append(self.define_from_variant("MDE", "mde"))
        args.append(self.define_from_variant("MAX_NUMBER_MATLS", "max_number_matls"))

        # Floating point error checks
        args.append(self.define_from_variant("CHECK_FINITE", "check_finite"))
        args.append(self.define_from_variant("FP_EXCEPT", "fpe"))

        # Configure optional libraries
        args.append(self.define_from_variant("ENABLE_ARPACK", "arpack-ng"))
        args.append(self.define_from_variant("ENABLE_METIS", "metis"))
        args.append(self.define_from_variant("ENABLE_OMEGA_H", "omega-h"))
        args.append(self.define_from_variant("ENABLE_PETSC", "petsc"))
        args.append(self.define_from_variant("ENABLE_SPARSE", "sparse"))
        args.append(self.define_from_variant("ENABLE_UMFPACK", "suite-sparse"))

        return args
