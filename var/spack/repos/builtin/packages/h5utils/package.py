# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5utils(AutotoolsPackage):
    """h5utils is a set of utilities for visualization and conversion of
    scientific data in the free, portable HDF5 format."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/H5utils"
    url      = "http://ab-initio.mit.edu/h5utils/h5utils-1.12.1.tar.gz"
    list_url = "http://ab-initio.mit.edu/h5utils/old/"

    version('1.12.1', sha256='7290290ca5d5d4451d757a70c86baaa70d23a28edb09c951b6b77c22b924a38d')

    variant('png',    default=True,  description='Enable PNG support')
    variant('vis5d',  default=False, description='Enable Vis5d support')
    variant('octave', default=False, description='Enable GNU Octave support')
    variant('hdf4',   default=False, description='Enable HDF4 support')
    variant('math',   default=False, description='Build h5math')

    # Required dependencies
    depends_on('hdf5')

    # Optional dependencies
    depends_on('libpng',      when='+png')
    # depends_on('vis5d',       when='+vis5d')  # TODO: Add a vis5d package
    depends_on('octave',      when='+octave')
    depends_on('hdf',         when='+hdf4')
    depends_on('libmatheval', when='+math')

    def configure_args(self):
        spec = self.spec
        args = []

        if '+vis5d' in spec:
            args.append('--with-v5d={0}'.format(spec['vis5d'].prefix))
        else:
            args.append('--without-v5d')

        if '+octave' in spec:
            args.append('--with-octave')
        else:
            args.append('--without-octave')

        if '+hdf' in spec:
            args.append('--with-hdf4')
        else:
            args.append('--without-hdf4')

        return args
