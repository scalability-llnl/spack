# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAzuremlAutomlCore(Package):
    """The azureml-automl-core package is a package containing functionality
    used by the azureml-train-automl package."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_automl_core/azureml_automl_core-1.11.0-py3-none-any.whl"

    version('1.11.0', sha256='da1b9cef9aabbfaee69a19d5e15f5a911eefbd126546738343a78c032860b5a5', expand=False)
    version('1.8.0',  sha256='58ce54b01570996cda860c0c80693b8db19324785a356573f105afeaa31cae6c', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-dataset-runtime@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-dataprep@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
