# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygments(PythonPackage):
    """Pygments is a syntax highlighting package written in Python."""

    homepage = "http://pygments.org/"
    url      = "https://pypi.io/packages/source/P/Pygments/Pygments-2.4.2.tar.gz"

    version('2.6.1', sha256='647344a061c249a3b74e230c739f434d7ea4d8b1d5f3721bc0f3558049b38f44')
    version('2.4.2', sha256='881c4c157e45f30af185c1ffe8d549d48ac9127433f2c380c24b84572ad66297')
    version('2.3.1', sha256='5ffada19f6203563680669ee7f53b64dabbeb100eb51b61996085e99c03b284a')
    version('2.2.0', sha256='dbae1046def0efb574852fab9e90209b23f556367b5a320c0bcb871c77c3e8cc')
    version('2.1.3', sha256='88e4c8a91b2af5962bfa5ea2447ec6dd357018e86e94c7d14bd8cacbc5b55d81')
    version('2.0.1', sha256='5e039e1d40d232981ed58914b6d1ac2e453a7e83ddea22ef9f3eeadd01de45cb')
    version('2.0.2', sha256='7320919084e6dac8f4540638a46447a3bd730fca172afc17d2c03eed22cf4f51')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@:2.5')
    depends_on('python@3.5:', type=('build', 'run'), when='@2.6:')
    depends_on('py-setuptools', type=('build', 'run'))
