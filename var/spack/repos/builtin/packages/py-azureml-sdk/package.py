# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlSdk(Package):
    """Microsoft Azure Machine Learning Python SDK."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_sdk/azureml_sdk-1.11.0-py3-none-any.whl"

    maintainers = ['adamjstewart']

    version('1.23.0', sha256='b9520f426831acb99fafa1ecd154b6bfd4f73fbf71e918d819f9db4a75438ab9', expand=False)
    version('1.11.0', sha256='d8c9d24ea90457214d798b0d922489863dad518adde3638e08ef62de28fb183a', expand=False)
    version('1.8.0',  sha256='61107db1403ce2c1a12064eb0fa31a1d075debbf32dd17cb93b7639b615b7839', expand=False)

    extends('python')
    # https://github.com/Azure/MachineLearningNotebooks/issues/1285
    depends_on('python@3.5:3.8.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-dataset-runtime@1.23.0:1.23.999 +fuse', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-train@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-train-automl-client@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))

    depends_on('py-azureml-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-dataset-runtime@1.11.0:1.11.999 +fuse', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-train@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-train-automl-client@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-train@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-train-automl-client@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-dataprep@1.8.0:1.8.999 +fuse', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
