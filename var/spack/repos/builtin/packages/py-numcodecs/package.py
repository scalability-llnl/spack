# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumcodecs(PythonPackage):
    """Numcodecs is a Python package providing buffer compression and
    transformation codecs for use in data storage and communication
    applications.
    """

    homepage = "https://github.com/zarr-developers/numcodecs"
    pypi = "numcodecs/numcodecs-0.6.4.tar.gz"
    git = "https://github.com/zarr-developers/numcodecs.git"

    version('master', branch='master', submodules=True)
    version('0.7.3', sha256='022b12ad83eb623ec53f154859d49f6ec43b15c36052fa864eaf2d9ee786dd85')
    version('0.6.4', sha256='ef4843d5db4d074e607e9b85156835c10d006afc10e175bda62ff5412fca6e4d')

    variant('msgpack', default=False, description='Codec to encode data as msgpacked bytes.')

    depends_on('python@3.6:3.999', when='@0.7:', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@:0.6.999', type=('build', 'link', 'run'))
    depends_on('py-setuptools@18.1:', type='build')
    depends_on('py-setuptools-scm@1.5.5:', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-msgpack', type=('build', 'run'), when='+msgpack')

    patch('apple-clang-12.patch', when='%apple-clang@12:')
