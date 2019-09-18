# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mstk(CMakePackage):
    """MSTK is a mesh framework that allows users to represent,
    manipulate and query unstructured 3D arbitrary topology meshes
    in a general manner without the need to code their own data
    structures. MSTK is a flexible framework in that it allows a
    variety of underlying representations for the mesh while
    maintaining a common interface. It allows users to choose from
    different mesh representations either at initialization (implemented)
    or during the program execution (not yet implemented) so that the
    optimal data structures are used for the particular algorithm.
    The interaction of users and applications with MSTK is through a
    functional interface that acts as though the mesh always contains
    vertices, edges, faces and regions and maintains connectivity between
    all these entities."""

    homepage = "https://github.com/MeshToolkit/MSTK"
    git      = "https://github.com/MeshToolkit/MSTK"

    version("develop", branch='master', submodules=False, preferred=True)

    variant('parallel', default='none', description='Enable Parallel Support',
            values=(
                'none',
                'metis',
                'zoltan', 'zoltan_parmetis', 'zoltan_ptscotch'),
            multi=False)
    variant('exodusii', default=False,
            description='Enable ExodusII')
    variant('tests', default=True, description="Enable testing")

    depends_on("cmake@3.8:")

    # Parallel variant 
    depends_on("mpi", when='parallel=metis')
    depends_on("mpi", when='parallel=zoltan')
    depends_on("mpi", when='parallel=zoltan_parmetis')

    depends_on("metis", when='parallel="metis"')
    depends_on("zoltan -fortran", when='parallel="zoltan"')
    depends_on("zoltan -fortran +parmetis", when='parallel="zoltan_parmetis"')
    depends_on("zoltan -fortran", when='parallel="zoltan_ptscotch"')
    depends_on("scotch +mpi", when='parallel="zoltan_ptscotch"')

    # Exodusii variant
    # The default exodusii build with mpi support
    # It includes netcdf which includes hdf5
    depends_on("exodusii", when='+exodusii')

    def cmake_args(self):
        options = ['-DCMAKE_C_FLAGS=-std=c99']
        options.append('-DCMAKE_BUILD_TYPE=Release')
        options.append('-DMSTK_USE_MARKERS=ON')

        # Parallel variant 
        if self.spec.variants['parallel'].value != "none":
            # Use mpi for compilation
            options.append('-DCMAKE_CXX_COMPILER=mpicxx')
            options.append('-DCMAKE_C_COMPILER=mpicc')
            options.append('-DCMAKE_FORTRAN_COMPILER=mpifort')
            options.append('-DENABLE_PARALLEL=ON')
        if self.spec.variants['parallel'].value == "metis":
            options.append('-DENABLE_METIS=ON')
        elif self.spec.variants['parallel'].value == "zoltan":
            options.append('-DENABLE_ZOLTAN=ON')
        elif self.spec.variants['parallel'].value == "zoltan_parmetis":
            options.append('-DENABLE_ZOLTAN=ON')
            options.append('-DZOLTAN_NEEDS_ParMETIS=ON')
        elif self.spec.variants['parallel'].value == "zoltan_ptscotch":
            options.append('-DENABLE_ZOLTAN=ON')
            options.append('-DZOLTAN_NEEDS_PTScotch=ON')

        # ExodusII variant
        if self.spec.variants['exodusii'].value == True:
            options.append('-DENABLE_ExodusII=ON')

        return options
