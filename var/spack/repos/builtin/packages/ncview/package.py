# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ncview(AutotoolsPackage):
    """Simple viewer for NetCDF files."""
    homepage = "http://meteora.ucsd.edu/~pierce/ncview_home_page.html"
    url      = "ftp://cirrus.ucsd.edu/pub/ncview/ncview-2.1.7.tar.gz"

    version('2.1.8', sha256='e8badc507b9b774801288d1c2d59eb79ab31b004df4858d0674ed0d87dfc91be')
    version('2.1.7', sha256='a14c2dddac0fc78dad9e4e7e35e2119562589738f4ded55ff6e0eca04d682c82')

    depends_on('netcdf-c')
    depends_on('udunits')
    depends_on('libpng')
    depends_on('libxaw')

    def configure_args(self):
        spec = self.spec

        config_args = []

        if spec.satisfies('^netcdf-c+mpi'):
            config_args.append('CC={0}'.format(spec['mpi'].mpicc))

        return config_args
