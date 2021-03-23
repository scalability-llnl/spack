# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlTrainAutomlClient(Package):
    """The azureml-train-automl-client package contains functionality for
    automatically finding the best machine learning model and its parameters,
    given training and test data."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_train_automl_client/azureml_train_automl_client-1.11.0-py3-none-any.whl"

    version('1.23.0', sha256='ac5f1ce9b04b4e61e2e28e0fa8d2d8e47937a546f624d1cd3aa6bc4f9110ecbe', expand=False)
    version('1.11.0', sha256='3184df60a46917e92140a299aecb54591b19df490a3f4f571ff1f92c5e70a715', expand=False)
    version('1.8.0',  sha256='562300095db6c4dea7b052e255c53dd95c4c3d0589a828b545497fe1ca7e9677', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-automl-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-dataset-runtime@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))

    depends_on('py-azureml-automl-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-dataset-runtime@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-dataprep@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-automl-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-telemetry@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
