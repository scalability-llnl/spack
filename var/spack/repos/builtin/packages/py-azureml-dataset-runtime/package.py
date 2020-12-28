# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzuremlDatasetRuntime(Package):
    """The purpose of this package is to coordinate dependencies within
    AzureML packages. It is not intended for public use."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml-dataset-runtime/azureml_dataset_runtime-1.11.0.post1-py3-none-any.whl"

    version('1.11.0.post1', sha256='65c20f276399a7d406c4850af7a6f149472d301931fd1da6a60bad59d43fa47b', expand=False)

    variant('fuse', default=False, description='Build with FUSE support')

    extends('python')
    depends_on('python@3.0:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-azureml-dataprep@2.0.1:2.0.999', type=('build', 'run'))
    depends_on('py-pyarrow@0.17.0:0.999', type=('build', 'run'))
    depends_on('py-fusepy@3.0.1:3.999', when='+fuse', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
