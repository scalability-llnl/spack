# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeras(PythonPackage):
    """Deep Learning library for Python. Convnets, recurrent neural networks,
    and more. Runs on Theano or TensorFlow."""

    homepage = "http://keras.io"
    url      = "https://pypi.io/packages/source/K/Keras/Keras-1.2.2.tar.gz"

    version('2.2.4', sha256='90b610a3dbbf6d257b20a079eba3fdf2eed2158f64066a7c6f7227023fd60bc9')
    version('2.2.3', sha256='694aee60a6f8e0d3d6d3e4967e063b4623e3ca90032f023fd6d16bb5f81d18de')
    version('2.2.2', sha256='468d98da104ec5c3dbb10c2ef6bb345ab154f6ca2d722d4c250ef4d6105de17a')
    version('2.2.1', sha256='0d3cb14260a3fa2f4a5c4c9efa72226ffac3b4c50135ba6edaf2b3d1d23b11ee')
    version('2.2.0', sha256='5b8499d157af217f1a5ee33589e774127ebc3e266c833c22cb5afbb0ed1734bf')
    version('2.1.6', sha256='c14af1081242c25617ade7eb62121d58d01f16e1e744bae9fc4f1f95a417716e')
    version('2.1.5', sha256='907ad29add1fff27342a9f4fe3e60003d450d3af41a38f22f629c7736fc8399d')
    version('2.1.4', sha256='7ee1fcc79072ac904a4f008d715bcb78c60250ae3cd41d99e268c60ade8d0d3a')
    version('2.1.3', sha256='7ca3a381523bad40a6922e88951a316664cb088fd01cea07e5ec8ada3327e3c7')
    version('2.1.2', sha256='3ee56fc129d9d00b1916046e50056047836f97ada59df029e5661fb34442d5e8')
    version('2.1.1', sha256='f0ca2458c60d9711edf4291230b31795307ad3781cb6232ff4792b53c8f55123')
    version('2.1.0', sha256='67a0d66c20fff99312fc280e34c8f6dc3dbb027d4a33c13c79bec3c1173f6909')
    version('2.0.9', sha256='6b8572cf1b4a22fd0120b7c23382ba4fa04a6f0397e02af1249be9a7309d1767')
    version('2.0.8', sha256='899dc6aaed366f20100b9f80cf1093ea5b43eecc74afd1dc63a4e48dfa776ab9')
    version('2.0.7', sha256='a6c72ee2b94be1ffefe7e77b69582b9827211f0c356b2189459711844d3634c0')
    version('2.0.6', sha256='0519480abe4ad18b2c2d1bc580eab75edd82c95083d341a1157952f4b00019bb')
    version('2.0.5', sha256='cbce24758530e070fe1b403d6d21391cbea78c037b70bf6afc1ca9f1f8269eff')
    version('2.0.4', sha256='1cbe62af6821963321b275d5598fd94e63c11feaa1d4deaa79c9eb9ee0e1d68a')
    version('2.0.3', sha256='398dbd4a95e9d3ab2b2941d3e0c19362d397a2a6c3a667ab89d3d6aad30997f4')
    version('1.2.2', sha256='d2b18c4336eb9c4f0d03469870257efa7980a9b036c9d46dcf4d49e7f4487e2d')
    version('1.2.1', sha256='6adce75b2050608e6683c3046ef938bfdc5bfcd4c6b6c522df5e50d18e0ac7c6')
    version('1.2.0', sha256='33d5297cd0c280640dc5c075466995c05911bc1da35c83ae57b2a48188b605e2')
    version('1.1.2', sha256='cfde0a424961ead4982a7ebefd77d8ca382810b5a69b566fa64c57d8f340eeb4')
    version('1.1.1', sha256='be1b67f62e5119f6f24a239a865dc47e6d9aa93b97b506ba34cab7353dbc23b6')
    version('1.1.0', sha256='36d83b027ba9d2c9da8e1eefc28f600ca93dc03423e033b633cbac9061af8a5d')

    depends_on('py-keras-applications', type='run', when='@2.2:')
    depends_on('py-keras-preprocessing', type='run', when='@2.2:')
    depends_on('py-setuptools', type='build')
    depends_on('py-theano', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
