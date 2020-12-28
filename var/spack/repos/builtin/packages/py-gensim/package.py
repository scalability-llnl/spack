# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGensim(PythonPackage):
    """Gensim is a Python library for topic modelling, document indexing and
    similarity retrieval with large corpora. Target audience is the natural
    language processing (NLP) and information retrieval (IR) community."""

    homepage = "https://radimrehurek.com/gensim"
    url      = "https://pypi.io/packages/source/g/gensim/gensim-3.8.1.tar.gz"

    maintainers = ['adamjstewart']

    version('3.8.3', sha256='786adb0571f75114e9c5f7a31dd2e6eb39a9791f22c8757621545e2ded3ea367')
    version('3.8.1', sha256='33277fc0a8d7b0c7ce70fcc74bb82ad39f944c009b334856c6e86bf552b1dfdc')
    version('3.8.0', sha256='ec5de7ff2bfa8692fa96a846bb5aae52f267fc322fbbe303c1f042d258af5766')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-numpy@1.11.3:1.16.1', when='^python@:2.999', type=('build', 'run'))
    depends_on('py-numpy@1.11.3:',       when='^python@3:',     type=('build', 'run'))

    depends_on('py-scipy@0.18.1:1.2.3', when='^python@:2.999', type=('build', 'run'))
    depends_on('py-scipy@0.18.1:',      when='^python@3:',     type=('build', 'run'))

    depends_on('py-six@1.5.0:', type=('build', 'run'))

    depends_on('py-smart-open@1.7.0:1.10.9999', when='@3.8.0^python@:2.999',  type=('build', 'run'))
    depends_on('py-smart-open@1.7.0:',          when='@3.8.0^python@3:',      type=('build', 'run'))
    depends_on('py-smart-open@1.8.1:1.10.9999', when='@3.8.1:^python@:2.999', type=('build', 'run'))
    depends_on('py-smart-open@1.8.1:',          when='@3.8.1:^python@3:',     type=('build', 'run'))
