# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ceed(BundlePackage):
    """Ceed is a collection of benchmarks, miniapps, software libraries and
       APIs for efficient high-order finite element and spectral element
       discretizations for exascale applications developed in the Department of
       Energy (DOE) and partially supported by the Exascale Computing Project
       (ECP). This is a Spack bundle package that installs the CEED software
       components."""

    homepage = "https://ceed.exascaleproject.org"

    maintainers = ['jedbrown', 'v-dobrev', 'tzanio']

    version('3.0.0')
    version('2.0.0')
    version('1.0.0')

    variant('cuda', default=False,
            description='Enable CUDA support')
    variant('mfem', default=True, description='Build MFEM, Laghos and Remhos')
    variant('nek', default=True,
            description='Build Nek5000, GSLIB, Nekbone, and NekCEM')
    variant('occa', default=True,
            description='Enable OCCA support')
    variant('petsc', default=True,
            description='Build PETSc and HPGMG')
    variant('pumi', default=True,
            description='Build PUMI')
    variant('quickbuild', default=True,
            description='Speed-up the build by disabling variants in packages')
    # TODO: Add 'int64' variant?

    # LibCEED
    # ceed-3.0
    depends_on('libceed@0.6~cuda', when='@3.0.0~cuda')
    depends_on('libceed@0.6+cuda+magma', when='@3.0.0+cuda')
    depends_on('libceed@0.6+occa', when='@3.0.0+occa')
    depends_on('libceed@0.6~occa', when='@3.0.0~occa')
    # ceed-2.0
    depends_on('libceed@0.4~cuda', when='@2.0.0~cuda')
    depends_on('libceed@0.4+cuda', when='@2.0.0+cuda')
    depends_on('libceed@0.4+occa', when='@2.0.0+occa')
    depends_on('libceed@0.4~occa', when='@2.0.0~occa')
    # ceed-1.0
    depends_on('libceed@0.2~cuda', when='@1.0.0~cuda')
    depends_on('libceed@0.2+cuda', when='@1.0.0+cuda')
    depends_on('libceed@0.2+occa', when='@1.0.0+occa')
    depends_on('libceed@0.2~occa', when='@1.0.0~occa')

    # OCCA
    # ceed-3.0
    depends_on('occa@1.0.9~cuda', when='@3.0.0+occa~cuda')
    depends_on('occa@1.0.9+cuda', when='@3.0.0+occa+cuda')
    # ceed-2.0
    depends_on('occa@1.0.8~cuda', when='@2.0.0+occa~cuda')
    depends_on('occa@1.0.8+cuda', when='@2.0.0+occa+cuda')
    # ceed-1.0
    depends_on('occa@1.0.0-alpha.5~cuda', when='@1.0.0+occa~cuda')
    depends_on('occa@1.0.0-alpha.5+cuda', when='@1.0.0+occa+cuda')

    # Nek5000, GSLIB, Nekbone, and NekCEM
    # ceed-3.0
    depends_on('nek5000@19.0', when='@3.0.0+nek')
    depends_on('nektools@19.0%gcc', when='@3.0.0+nek')
    depends_on('gslib@1.0.6', when='@3.0.0+nek')
    depends_on('nekbone@17.0', when='@3.0.0+nek')
    depends_on('nekcem@c8db04b', when='@3.0.0+nek')
    # ceed-2.0
    depends_on('nek5000@17.0', when='@2.0.0+nek')
    depends_on('nektools@17.0%gcc', when='@2.0.0+nek')
    depends_on('gslib@1.0.2', when='@2.0.0+nek')
    depends_on('nekbone@17.0', when='@2.0.0+nek')
    depends_on('nekcem@7332619', when='@2.0.0+nek')
    # ceed-1.0
    depends_on('nek5000@17.0', when='@1.0.0+nek')
    depends_on('nektools@17.0%gcc', when='@1.0.0+nek')
    depends_on('gslib@1.0.2', when='@1.0.0+nek')
    depends_on('nekbone@17.0', when='@1.0.0+nek')
    depends_on('nekcem@0b8bedd', when='@1.0.0+nek')

    # PETSc
    # ceed-3.0
    depends_on('petsc+cuda', when='@3.0.0+petsc+cuda')
    # For a +quickbuild we disable hdf5, and superlu-dist in PETSc.
    depends_on('petsc@3.13.0:3.13.99~hdf5~superlu-dist',
               when='@3.0.0+petsc+quickbuild')
    depends_on('petsc@3.13.0:3.13.99+mpi+double~int64', when='@3.0.0+petsc~mfem')
    # Coax concretizer to use version of hypre required by transitive
    # dependencies (mfem, petsc)
    depends_on('hypre@:2.18.2', when='@3.0.0+mfem')
    # The mfem petsc examples need the petsc variants +hypre, +suite-sparse,
    # and +mumps:
    depends_on('petsc@3.13.0:3.13.99+mpi+hypre+suite-sparse+mumps+double~int64',
               when='@3.0.0+petsc+mfem')
    # ceed-2.0
    # For a +quickbuild we disable hdf5, and superlu-dist in PETSc.
    # Ideally, these can be turned into recommendations to Spack for
    # concretizing the PETSc spec, if Spack ever supports recommendations.
    depends_on('petsc@3.11.1~hdf5~superlu-dist',
               when='@2.0.0+petsc+quickbuild')
    depends_on('petsc@3.11.1+mpi+double~int64', when='@2.0.0+petsc~mfem')
    # The mfem petsc examples need the petsc variants +hypre, +suite-sparse,
    # and +mumps:
    depends_on('petsc@3.11.1+mpi+hypre+suite-sparse+mumps+double~int64',
               when='@2.0.0+petsc+mfem')
    depends_on('hpgmg@0.4+fe', when='@2.0.0+petsc')
    # ceed-1.0
    # For a +quickbuild we disable hdf5, and superlu-dist in PETSc.
    # Ideally, these can be turned into recommendations to Spack for
    # concretizing the PETSc spec, if Spack ever supports recommendations.
    depends_on('petsc@3.8.3~hdf5~superlu-dist',
               when='@1.0.0+petsc+quickbuild')
    depends_on('petsc@3.8.3+mpi+double~int64', when='@1.0.0+petsc~mfem')
    # The mfem petsc examples need the petsc variants +hypre, +suite-sparse,
    # and +mumps:
    depends_on('petsc@3.8.3+mpi+hypre+suite-sparse+mumps+double~int64',
               when='@1.0.0+petsc+mfem')
    depends_on('hpgmg@a0a5510df23b+fe', when='@1.0.0+petsc')

    # MAGMA
    # ceed-3.0
    depends_on('magma@2.5.3', when='@3.0.0+cuda')
    # ceed-2.0
    depends_on('magma@2.5.0', when='@2.0.0+cuda')
    # ceed-1.0
    depends_on('magma@2.3.0', when='@1.0.0+cuda')

    # PUMI
    # ceed-3.0
    depends_on('pumi@2.2.2', when='@3.0.0+pumi')
    # ceed-2.0
    depends_on('pumi@2.2.0', when='@2.0.0+pumi')
    # ceed-1.0
    depends_on('pumi@2.1.0', when='@1.0.0+pumi')

    # MFEM, Laghos, Remhos
    # ceed-3.0
    depends_on('mfem@4.1.0+mpi+examples+miniapps', when='@3.0.0+mfem~petsc')
    depends_on('mfem@4.1.0+mpi+petsc+examples+miniapps',
               when='@3.0.0+mfem+petsc')
    depends_on('mfem@4.1.0+pumi', when='@3.0.0+mfem+pumi')
    depends_on('mfem@4.1.0+gslib', when='@3.0.0+mfem+nek')
    depends_on('mfem@4.1.0+libceed', when='@3.0.0+mfem')
    depends_on('mfem@4.1.0+cuda', when='@3.0.0+mfem+cuda')
    depends_on('mfem@4.1.0+occa', when='@3.0.0+mfem+occa')
    depends_on('laghos@3.0', when='@3.0.0+mfem')
    depends_on('remhos@1.0', when='@3.0.0+mfem')

    # If using gcc version <= 4.8 build suite-sparse version <= 5.1.0
    depends_on('suite-sparse@:5.1.0', when='@3.0.0%gcc@:4.8+mfem+petsc')

    # ceed-2.0
    depends_on('mfem@3.4.0+mpi+examples+miniapps', when='@2.0.0+mfem~petsc')
    depends_on('mfem@3.4.0+mpi+petsc+examples+miniapps',
               when='@2.0.0+mfem+petsc')
    depends_on('mfem@3.4.0+pumi', when='@2.0.0+mfem+pumi')
    depends_on('laghos@2.0', when='@2.0.0+mfem')
    # Help the spack concretizer find a suitable version of hypre:
    depends_on('hypre~internal-superlu', when='@2.0.0+mfem')
    depends_on('hypre~internal-superlu~superlu-dist',
               when='@2.0.0+mfem+quickbuild')

    # If using gcc version <= 4.8 build suite-sparse version <= 5.1.0
    depends_on('suite-sparse@:5.1.0', when='@2.0.0%gcc@:4.8+mfem+petsc')

    # ceed-1.0
    depends_on('mfem@3.3.2+mpi+examples+miniapps', when='@1.0.0+mfem~petsc')
    depends_on('mfem@3.3.2+mpi+petsc+examples+miniapps',
               when='@1.0.0+mfem+petsc')
    depends_on('laghos@1.0', when='@1.0.0+mfem')
    # The next line seems to be necessary because the concretizer somehow
    # decides that mfem requires 'hypre+internal-superlu' even though the mfem
    # package lists simply 'hypre' as dependency. This is only an issue because
    # petsc explicitly requires 'hypre~internal-superlu' which for the
    # concretizer is a conflict.
    depends_on('hypre~internal-superlu', when='@1.0.0+mfem')

    # If using gcc version <= 4.8 build suite-sparse version <= 5.1.0
    depends_on('suite-sparse@:5.1.0', when='@1.0.0%gcc@:4.8+mfem+petsc')
