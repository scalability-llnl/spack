# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class EcpDataVisSdk(BundlePackage):
    """ECP Data & Vis SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"

    tags = ['ecp']
    maintainers = ['chuckatkins']

    version('1.0')

    ############################################################
    # Variants
    ############################################################

    # I/O
    variant('adios2', default=True, description="Enable ADIOS2")
    variant('darshan', default=True, description="Enable Darshan")
    variant('faodel', default=False, description="Enable FAODEL")
    variant('hdf5', default=True, description="Enable HDF5")
    variant('pnetcdf', default=True, description="Enable PNetCDF")
    variant('unifyfs', default=True, description="Enable UnifyFS")
    variant('veloc', default=True, description="Enable VeloC")

    # Vis
    variant('ascent', default=False, description="Enable Ascent")
    variant('paraview', default=False, description="Enable ParaView")
    variant('sz', default=True, description="Enable SZ")
    variant('vtkm', default=False, description="Enable VTK-m")
    variant('zfp', default=True, description="Enable ZFP")

    # Outstanding concretization issues
    # variant('cinema', default=True, description="Enable Cinema")

    # Outstanding build issues
    # variant('catalyst', default=False, description="Enable Catalyst")
    # variant('visit', default=False, description="Enable VisIt")

    ############################################################
    # This is a messy workaround until the clingo concretizer can be required.
    # The intent is to map package variants to dependency variants:
    #   Package variants a, and b, mapping to dependency variants A and B
    #   produce the following set of dependencies:
    #     depends_on('foo+A+B', when='+a+b')
    #     depends_on('foo+A~B', when='+a~b')
    #     depends_on('foo~A+B', when='~a+b')
    #     depends_on('foo~A~B', when='~a~b')
    #   The clingo concretizer will allow that to be expressed much simpler by
    #   only considering defaults once everything else is resolved:
    #     depends_on('foo')
    #     depends_on('foo+A', when='+a')
    #     depends_on('foo+B', when='+b')
    ############################################################

    # Helper function to generate dependencies on the Cartesian product of
    # variants.  If a dictionary is passed then it provides a mapping of
    # package variant name to dependency variant name.  Otherwise assume they
    # are the same variant name in both the package and dependency
    def variants2deps(dep_spec, pkg_spec, variants):
        if not type(variants) is dict:
            variants = dict([(v, v) for v in variants])
        n = len(variants)
        for i in range(0, pow(2, n)):
            state = ['+' if d == '1' else '~' for d in format(i, '0' + str(n) + 'b')]
            [pkg_vars, dep_vars] = [''.join(v) for v in zip(
                *[(s + pv, s + dv) for s, (pv, dv) in zip(state, variants.items())])]
            dependency = ' '.join((dep_spec, dep_vars))
            predicate = ' '.join((pkg_spec, pkg_vars))
            depends_on(dependency, when=predicate)

    ############################################################
    # Dependencies
    ############################################################
    variants2deps('adios2+shared+mpi+fortran+python+blosc+sst+ssc+dataman',
                  '+adios2', ['hdf5', 'sz', 'zfp'])

    depends_on('darshan-runtime+mpi', when='+darshan')
    depends_on('darshan-util', when='+darshan')

    variants2deps('faodel+shared+mpi network=libfabric', '+faodel', ['hdf5'])

    depends_on('hdf5 +shared+mpi', when='+hdf5')
    # +fortran breaks the concretizer... Needs new concretizer
    # depends_on('hdf5 +shared+mpi+fortran', when='+hdf5')

    depends_on('parallel-netcdf+shared+fortran', when='+pnetcdf')

    variants2deps('unifyfs+fortran', '+unifyfs', ['hdf5'])

    depends_on('veloc', when='+veloc')

    depends_on('ascent+shared+mpi+fortran+openmp+python+vtkh+dray', when='+ascent')
    depends_on('catalyst', when='+catalyst')

    depends_on('py-cinema-lib', when='+cinema')
    depends_on('py-cinemasci', when='+cinema')

    variants2deps('paraview+shared+mpi+python3+kits', '+paraview', ['hdf5'])
    # +adios2 is not yet enabled in the paraview package
    # depends_on('paraview+adios2', when='+paraview +adios2')

    depends_on('visit', when='+visit')

    depends_on('vtk-m+shared+mpi+openmp+rendering', when='+vtkm')

    # +python is currently broken in sz
    # variants2deps('sz+shared+fortran+python+random_access', '+sz', ['hdf5'])
    variants2deps('sz+shared+fortran+random_access', '+sz', ['hdf5'])

    depends_on('zfp', when='+zfp')
