##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyMdanalysis(PythonPackage):
    """MDAnalysis is a Python toolkit to analyze molecular dynamics
    trajectories generated by a wide range of popular simulation
    packages including DL_Poly, CHARMM, Amber, NAMD, LAMMPS, and
    Gromacs. (See the lists of supported trajectory formats and
    topology formats.)"""

    homepage = "http://www.mdanalysis.org"
    url      = "https://pypi.io/packages/source/M/MDAnalysis/MDAnalysis-0.15.0.tar.gz"

    version('0.15.0', '19e5a8e6c2bfe85f6209d1d7a36e4f20')

    variant('analysis', default=True, 
            description='Enable analysis packages: matplotlib, scipy, seaborn')
    variant('amber', default=False,
            description='Support AMBER netcdf format.')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.16:', type='build')
    depends_on('py-numpy@1.5.0:', type=('build', 'run'))
    depends_on('py-six@1.4.0:', type=('build', 'run'))
    depends_on('py-biopython@1.59:', type=('build', 'run'))
    depends_on('py-networkx@1.0:', type=('build', 'run'))
    depends_on('py-griddataformats@0.3.2:', type=('build', 'run'))

    depends_on('py-matplotlib', when='+analysis', type=('build', 'run'))
    depends_on('py-scipy', when='+analysis', type=('build', 'run'))
    depends_on('py-seaborn', when='+analysis', type=('build', 'run'))

    depends_on('py-netcdf4@1.0:', when='+amber', type=('build', 'run'))
    depends_on('hdf5', when='+amber', type=('run'))
