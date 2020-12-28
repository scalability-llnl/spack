# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EcpVizSdk(BundlePackage):
    """ECP Viz & Analysis SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"
    git      = "https://github.com/chuckatkins/ecp-data-viz-sdk.git"

    maintainers = ['chuckatkins']

    version('1.0', branch='master')

    variant('ascent', default=False, description="Enable Ascent")
    # variant('catalyst', default=False, description="Enable Catalyst")
    variant('paraview', default=False, description="Enable ParaView")
    variant('sz', default=False, description="Enable SZ")
    variant('vtkm', default=False, description="Enable VTK-m")
    variant('zfp', default=False, description="Enable ZFP")

    # Outstanding build issues
    # variant('visit', default=False, description="Enable VisIt")

    # Missing spack package
    # variant('cinema', default=False, description="Enable Cinema")
    # variant('rover', default=False, description="Enable ROVER")

    depends_on('ascent+shared+mpi+fortran+openmp+python+vtkh+dray', when='+ascent')
    depends_on('catalyst', when='+catalyst')
    depends_on('paraview+shared+mpi+python3+hdf5+kits', when='+paraview')
    depends_on('visit', when='+visit')
    depends_on('vtk-m+shared+mpi+openmp+rendering', when='+vtkm')
    depends_on('sz+shared+fortran+hdf5+python+random_access', when='+sz')
    depends_on('zfp', when='+zfp')
