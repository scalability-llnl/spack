# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Hdfview(Package):
    """HDFView is a visual tool written in Java for browsing
    and editing HDF (HDF5 and HDF4) files."""

    homepage = "https://www.hdfgroup.org/downloads/hdfview/"
    url      = "https://s3.amazonaws.com/hdf-wordpress-1/wp-content/uploads/manual/HDFView/hdfview-3.0.tar.gz"

    version('3.1.1', sha256='1cfd127ebb4c3b0ab1cfe54649a410fc7a1c2d73f45564697d3729f4aa6b0ba3',
            url='https://support.hdfgroup.org/ftp/HDF5/releases/HDF-JAVA/hdfview-3.1.1/src/hdfview-3.1.1.tar.gz')
    version('3.0', sha256='e2a16d3842d8947f3d4f154ee9f48a106c7f445914a9e626a53976d678a0e934')

    # unknown flag: --ignore-missing-deps
    patch('fix_build.patch', when='@3.1.1')

    depends_on('ant', type='build')
    depends_on('hdf5 +java')
    depends_on('hdf +java -external-xdr +shared')

    def install(self, spec, prefix):
        env['HDF5LIBS'] = spec['hdf5'].prefix
        env['HDFLIBS'] = spec['hdf'].prefix

        ant = which('ant')
        ant('-Dbuild.debug=false', 'deploy')

        dir_version = os.listdir('build/HDF_Group/HDFView/')[0]
        path = 'build/HDF_Group/HDFView/{0}/'.format(dir_version)
        hdfview = '{0}/{1}'.format(path, 'hdfview.sh')

        filter_file(
            r'\$dir',
            prefix,
            hdfview
        )

        mkdirp(prefix.bin)
        install(hdfview, prefix.bin.hdfview)
        chmod = which('chmod')
        chmod('+x', self.prefix.bin.hdfview)
        install_tree(path, prefix)
