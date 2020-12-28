# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMistune(PythonPackage):
    """
    Python markdown parser
    """
    homepage = "http://mistune.readthedocs.org/en/latest/"
    url      = "https://github.com/lepture/mistune/archive/v0.7.1.tar.gz"

    version('0.8.4', sha256='a1443771ea9ed7268a0cb3cf31462604ae148938ba32070bd5c54545f8f36a5d')
    version('0.8.3', sha256='666c93fc10cb0aa924a373898a709eba4d43f4e453264a4c7396878ec8145a4a')
    version('0.8.2', sha256='997c6d723350093760ccd48b722344b3330a5f947dec264e129160b85037784e')
    version('0.8.1', sha256='77ae24a5accfd62d23f945d7e6598392194f8ca6ef1bd70ddc81e151ac3eb1fe')
    version('0.8',   sha256='f479dc2ceac7d593231e77448cb5cf7194fdbebad1d88fcdb78eacac1c042f6e')
    version('0.7.4', sha256='5030d5e3e0ec90fbdaed0f52d3c756ffb30e4ab46c3de159c97482c09569abcb')
    version('0.7.3', sha256='c4f391e61d3b5e8fbb112669a5c6960fb04b71b61d35f0f09a201809545b1676')
    version('0.7.2', sha256='a3fe17dfad99bd353485879a5c05827dd2932219da8b078212a21797f6cdbf0b')
    version('0.7.1', sha256='d6684534174caa30e0169e106a7152aee14507796a610b76be9fe9b335b18410')
    version('0.7', sha256='9b2cac8053d21dde5f2b3edb01948dac8ee5c3a85eeeeb6913c3ddf2f773c7b6')
    version('0.6', sha256='c2d976c06c099edb525b8ac3745f3d3b5c49af6189edb6de390ddf9c248913cf')
    version('0.5.1', sha256='c4ecfbb99acbb034c4f4580496502bde6b33f3dfc47873c59ee7e509c05dc822')
    version('0.5', sha256='3320b7fd80e44a1ac27658e19e67215f464c080b02c8af9fce57050d411560d2')

    depends_on('py-setuptools', type='build')
