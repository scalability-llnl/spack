# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyflakes(PythonPackage):
    """A simple program which checks Python source files for errors."""

    homepage = "https://github.com/PyCQA/pyflakes"
    url      = "https://github.com/PyCQA/pyflakes/archive/2.1.1.tar.gz"

    version('2.2.0', sha256='4a6927b9ca7fc19817176d54b3ee2ee4202f064febdee8624ee8340303cfda7b')
    version('2.1.1', sha256='2c98f07a9dd57d9f33561f6b54a64a766cdf79a3c869bd8c07b7fe03094fb8c3')
    version('2.1.0', sha256='6cd8775b6430daad386c0de00dfbc27ce2c24468cdcc4d3da41e4aa39d8ce167')
    version('1.6.0', sha256='f9c72359e05bf8dc27eaaee8cdcae464497f2ccadae87ac6517605ba6040ec99')
    version('1.5.0', sha256='943ba426420a66b5adebdbe8007e676bba11bf4006e7964d9d9ae98478c57792')
    version('1.4.0', sha256='7b0c1fe9be9c2b8ebc13bcc7e73f6d1862426c880d467126822a3ad1f8f3be79')
    version('1.3.0', sha256='7370356f3e20b537e61dfbcaf1ce7bf60aa7147e9e3e639e6401b445acfa3228')
    version('1.2.3', sha256='4c1c30a63e5ede3cb61ebbe238d4414a039b767b99f85f0574099e314e7102a2')
    version('1.2.2', sha256='c014aa6a936ccb29eaa89ef1ed4770eec650ea6e3f2c736b667428939fda5532')
    version('1.2.1', sha256='7de610c7a1dfba2cd34910732db399050ed969b459acc773797f6ff1f742725f')
    version('1.2.0', sha256='8860de31de5ea68586c3f92f0a81ea78282145bd536d80fe5f717462c9d11c6c')
    version('1.1.0', sha256='eb660821bed20c269dbacb5630fd8e9200012b8fbec2bdf63b0a5237773ea165')
    version('1.0.0', sha256='06fe9162e0ef561ca00b32766daa2196587d2faefaea8fa28f72af202b046587')
    version('0.9.2', sha256='ef67b057b4fc4ce463a7303688d45c50a7e420e8b4b3dabcd443cb265d4081b5')
    version('0.9.1', sha256='e22d2e24cc97a03db24aa8d96cb0fc66ca110adabc321215f5feca2f1068d29a')
    version('0.9.0', sha256='b1d395d1af3922edbfdbd05ac7082d855a2613aff2cd949ff0f29e25fb51f7f3')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pyflakes requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
