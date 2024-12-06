# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Akantu(CMakePackage):
    """
    Akantu means a little element in Kinyarwanda, a Bantu language. From now
    on it is also an opensource object-oriented Finite Element library which
    has the ambition to be generic and efficient.

    """

    homepage = "https://akantu.ch"
    url = "https://gitlab.com/akantu/akantu/-/archive/v3.0.0/akantu-v3.0.0.tar.gz"
    git = "https://gitlab.com/akantu/akantu.git"

    maintainers("nrichart")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("3.0.0", sha256="7e8f64e25956eba44def1b2d891f6db8ba824e4a82ff0d51d6b585b60ab465db")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "external_solvers",
        values=any_combination_of("mumps", "petsc"),
        description="Activates the implicit solver",
    )
    variant("mpi", default=True, description="Activates parallel capabilities")
    variant("python", default=False, description="Activates python bindings")

    depends_on("boost@:1.66", when="@:3.0")
    depends_on(Boost.with_default_variants)
    depends_on("lapack")
    depends_on("cmake@3.5.1:", type="build")
    depends_on("python", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-scipy", when="+python", type=("build", "run"))
    depends_on("py-pybind11", when="@3.1:+python", type=("build", "run"))

    depends_on("mumps", when="~mpi external_solvers=mumps")
    depends_on("mumps+mpi", when="+mpi external_solvers=mumps")
    depends_on("netlib-scalapack", when="+mpi external_solvers=mumps")
    depends_on("petsc+double", when="~mpi external_solvers=petsc")
    depends_on("petsc+double+mpi", when="+mpi external_solvers=petsc")

    depends_on("mpi", when="+mpi")
    depends_on("scotch", when="+mpi")

    extends("python", when="+python")

    conflicts("%gcc@:5.3")
    conflicts("@:3.0 external_solvers=petsc")
    conflicts("@:3.0 +python")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DAKANTU_COHESIVE_ELEMENT:BOOL=ON",
            "-DAKANTU_DAMAGE_NON_LOCAL:BOOL=ON",
            "-DAKANTU_HEAT_TRANSFER:BOOL=ON",
            "-DAKANTU_SOLID_MECHANICS:BOOL=ON",
            "-DAKANTU_STRUCTURAL_MECHANICS:BOOL=OFF",
            f"-DAKANTU_PARALLEL:BOOL={'ON' if spec.satisfies('+mpi') else 'OFF'}",
            f"-DAKANTU_PYTHON_INTERFACE:BOOL={'ON' if spec.satisfies('+python') else 'OFF'}",
        ]

        if spec.satisfies("@:3.0"):
            args.extend(
                [
                    "-DCMAKE_CXX_FLAGS=-Wno-class-memaccess",
                    "-DAKANTU_TRACTION_AT_SPLIT_NODE_CONTACT:BOOL=OFF",
                ]
            )
        else:
            args.append("-DAKANTU_TRACTION_AT_SPLIT_NODE_CONTACT:BOOL=ON")

        solvers = []
        if spec.satisfies("external_solvers=mumps"):
            solvers.append("Mumps")
            args.append(f"-DMUMPS_DIR:PATH=${spec['mumps'].prefix}")
        if spec.satisfies("external_solvers=petsc"):
            solvers.append("PETSc")

        if len(solvers) > 0:
            args.extend(
                [
                    f"-DAKANTU_IMPLICIT_SOLVER:STRING={'+'.join(solvers)}",
                    "-DAKANTU_IMPLICIT:BOOL=ON",
                ]
            )
        else:
            args.append("-DAKANTU_IMPLICIT:BOOL=OFF")

        return args
