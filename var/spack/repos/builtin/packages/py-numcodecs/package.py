# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumcodecs(PythonPackage):
    """Numcodecs is a Python package providing buffer compression and
    transformation codecs for use in data storage and communication
    applications.
    """

    homepage = "https://github.com/zarr-developers/numcodecs"
    url      = "https://pypi.io/packages/source/n/numcodecs/numcodecs-0.6.4.tar.gz"

    version('0.6.4', sha256='ef4843d5db4d074e607e9b85156835c10d006afc10e175bda62ff5412fca6e4d')

    variant('msgpack', default=False, description='Codec to encode data as msgpacked bytes.')

    depends_on('py-setuptools@18.0:',       type='build')
    depends_on('py-setuptools-scm@1.5.4:',  type=('build', 'run'))
    depends_on('py-numpy@1.7:',             type=('build', 'run'))
    depends_on('py-msgpack', type=('build', 'run'), when='+msgpack')
