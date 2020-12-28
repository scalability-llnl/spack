# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHpcbench(PythonPackage):
    """Define and run your benchmarks"""

    homepage = "https://github.com/BlueBrain/hpcbench"

    url      = "https://pypi.io/packages/source/h/hpcbench/hpcbench-0.8.tar.gz"
    git      = "https://github.com/BlueBrain/hpcbench.git"

    version('master', branch='master')
    version('0.8', sha256='120f5b1e6ff05a944b34a910f3099b4b0f50e96c60cf550b8fc6c42f64194697')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.6', type='build')
    depends_on('py-cached-property@1.3.1:', type=('build', 'run'))
    depends_on('py-clustershell@1.8:', type=('build', 'run'))
    depends_on('py-cookiecutter@1.6.0', type=('build', 'run'))
    depends_on('py-docopt@0.6.2', type=('build', 'run'))
    depends_on('py-elasticsearch@6:6.999', type=('build', 'run'))
    depends_on('py-jinja2@2.10', type=('build', 'run'))
    depends_on('py-mock@2.0.0', type=('build', 'run'))
    depends_on('py-numpy@1.13.3', type=('build', 'run'))
    depends_on('py-pyyaml@3.12:', type=('build', 'run'))
    depends_on('py-python-magic@0.4.15', type=('build', 'run'))
    depends_on('py-six@1.11', type=('build', 'run'))
