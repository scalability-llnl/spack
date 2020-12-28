# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpyder(PythonPackage):
    """Scientific PYthon Development EnviRonment"""

    homepage = "https://github.com/spyder-ide/spyder"
    url      = "https://pypi.io/packages/source/s/spyder/spyder-3.1.3.tar.gz"

    version('3.1.3', sha256='4978872cc5a006803bc8742d0a8fb43c49aef9524f0a9fcb8bd6dfcfdc2d2d6a')

    depends_on('python@2.7.0:2.8.0,3.3.0:', type=('build', 'run'))
    depends_on('py-rope@0.9.4:',      type=('build', 'run'), when='^python@:3')
    # depends_on('py-rope_py3k',    type=('build', 'run'), when='^python@3:')
    depends_on('py-jedi@0.9.0',       type=('build', 'run'))
    # otherwise collision with py-flake8
    depends_on('py-pyflakes@1.2.3',   type=('build', 'run'))
    depends_on('py-pygments@2.0:',    type=('build', 'run'))
    depends_on('py-qtconsole@4.2.0:', type=('build', 'run'))
    depends_on('py-nbconvert',        type=('build', 'run'))
    depends_on('py-sphinx',           type=('build', 'run'))
    # The pycodestyle dependency is split in two, because internally it
    # changes its name from pep8 to pycodestyle, and spyder does not cope
    # with this change until @3.2.0
    # https://github.com/PyCQA/pycodestyle/issues/466
    # https://github.com/spyder-ide/spyder/blob/master/CHANGELOG.md#version-32-2017-07-24
    depends_on('py-pycodestyle@:1.7.1', when='@:3.1.99', type=('build', 'run'))
    depends_on('py-pycodestyle@2.1.0:', when='@3.2.0:',  type=('build', 'run'))
    depends_on('py-pylint',           type=('build', 'run'))
    depends_on('py-psutil',           type=('build', 'run'))
    depends_on('py-qtawesome@0.4.1:', type=('build', 'run'))
    depends_on('py-qtpy@1.1.0:',      type=('build', 'run'))
    # technically this is a transitive dependency in order for py-pyqt4
    # to pick up webkit, but this is the easier solution (see #9207)
    depends_on('qt+webkit',           type=('build', 'run'))
    depends_on('py-pickleshare',      type=('build', 'run'))
    depends_on('py-pyzmq',              type=('build', 'run'))
    depends_on('py-chardet@2.0.0:',   type=('build', 'run'))
    depends_on('py-numpydoc',         type=('build', 'run'))
