# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kealib(CMakePackage):
    """An HDF5 Based Raster File Format.

    KEALib provides an implementation of the GDAL data model.
    The format supports raster attribute tables, image pyramids,
    meta-data and in-built statistics while also handling very
    large files and compression throughout.

    Based on the HDF5 standard, it also provides a base from which
    other formats can be derived and is a good choice for long
    term data archiving. An independent software library (libkea)
    provides complete access to the KEA image format and a GDAL
    driver allowing KEA images to be used from any GDAL supported software.

    Development work on this project has been funded by Landcare Research.
    """
    homepage = "http://www.kealib.org/"
    url      = "https://github.com/ubarsc/kealib/releases/download/kealib-1.4.12/kealib-1.4.12.tar.gz"
    git      = "https://github.com/ubarsc/kealib"

    maintainers = ['gillins']

    version('develop')
    version('1.4.12', sha256='0b100e36b3e25e57487aa197d7be47f22e1b30afb16a57fdaa5f877696ec321e')
    version('1.4.11', sha256='3d64cdec560c7a338ccb38e3a456db4e3b176ac62f945daa6e332e60fe4eca90')
    version('1.4.10', sha256='b1bd2d6834d2fe09ba456fce77f7a9452b406dbe302f7ef1aabe924e45e6bb5e')
    version('1.4.9',  sha256='1c80489f17114a229097c2e8c61d5e4c82ea63ae631c81a817fef95cfd527174')
    version('1.4.8',  sha256='0f24d8478865abcb17865c8f49c0370095726c529b8ac373ffae018ad3d40a02')
    version('1.4.7',  sha256='ec38751b3b555d3a26f0c7445f2d2cd9d7c3a3502237519a206a50cb58df56ec')

    depends_on('cmake@2.8.10:', type='build')
    depends_on('hdf5+cxx+hl')

    patch('cmake.patch', when='@1.4.7')

    @property
    def root_cmakelists_dir(self):
        if self.version >= Version('1.4.9'):
            return '.'
        else:
            return 'trunk'

    def cmake_args(self):
        spec = self.spec

        if self.version >= Version('1.4.9'):
            return [
                '-DHDF5_ROOT={0}'.format(spec['hdf5'].prefix)
            ]
        else:
            return [
                '-DHDF5_INCLUDE_DIR={0}'.format(
                    spec['hdf5'].headers.directories[0]),
                '-DHDF5_LIB_PATH={0}'.format(
                    spec['hdf5'].libs.directories[0])
            ]
