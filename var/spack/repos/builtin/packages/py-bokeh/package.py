# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBokeh(PythonPackage):
    """Statistical and novel interactive HTML plots for Python"""

    homepage = "http://github.com/bokeh/bokeh"
    pypi = "bokeh/bokeh-0.12.2.tar.gz"

    version('1.3.4', sha256='e2d97bed5b199a10686486001fed5c854e4c04ebe28859923f27c52b93904754')
    version('0.12.2', sha256='0a840f6267b6d342e1bd720deee30b693989538c49644142521d247c0f2e6939')

    depends_on('py-setuptools', type='build', when="@1.3.4:")
    depends_on('python@2.6:',             type=('build', 'run'), when='@0.12.2')
    depends_on('python@2.7:',             type=('build', 'run'), when='@1.3.4:')
    depends_on('py-requests@1.2.3:',      type=('build', 'run'), when='@0.12.2')
    depends_on('pil@4.0:',                type=('build', 'run'), when='@1.3.4:')
    depends_on('py-packaging@16.8:',      type=('build', 'run'), when='@1.3.4:')
    depends_on('py-six@1.5.2:',           type=('build', 'run'))
    depends_on('py-pyyaml@3.10:',         type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'))
    depends_on('py-jinja2@2.7:',          type=('build', 'run'))
    depends_on('py-numpy@1.7.1:',         type=('build', 'run'))
    depends_on('py-tornado@4.3:',         type=('build', 'run'))
    depends_on('py-futures@3.0.3:',       type=('build', 'run'), when='^python@2.7:2.8')
