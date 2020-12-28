# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyInferenceSchema(Package):
    """This package is intended to provide a uniform schema for common machine
    learning applications, as well as a set of decorators that can be used to
    aid in web based ML prediction applications."""

    homepage = "https://pypi.org/project/inference-schema/"
    url      = "https://pypi.io/packages/py3/i/inference-schema/inference_schema-1.0.2-py3-none-any.whl"

    version('1.0.2', sha256='fd379becbd12dcf9f7a1ad5c03b163d501ef1dcc4fb85204735c84b1d139f478', expand=False)

    variant('numpy', default=False, description='Enable numpy support')
    variant('pandas', default=False, description='Enable pandas support')
    variant('pyspark', default=False, description='Enable pyspark support')

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-python-dateutil@2.5.3:', type=('build', 'run'))
    depends_on('py-pytz@2017.2:', type=('build', 'run'))
    depends_on('py-wrapt@1.11.1', type=('build', 'run'))
    depends_on('py-numpy@1.13.0:', when='+numpy', type=('build', 'run'))
    depends_on('py-pandas@0.20.2:', when='+pandas', type=('build', 'run'))
    depends_on('py-pyspark@2.3.2', when='+pyspark', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
