# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlPipeline(Package):
    """The Azure Machine Learning SDK for Python can be used to create ML
    pipelines as well as to submit and track individual pipeline runs."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_pipeline/azureml_pipeline-1.11.0-py3-none-any.whl"

    version('1.23.0', sha256='ed0fae96771840d3ffd63d63df1b1eed2f50c3b8dbe7b672a4f1ba6e66d0a392', expand=False)
    version('1.11.0', sha256='8233c66b4120e86b9a9346608ca53bf48d5b9f0558300314034426dd0d7897d6', expand=False)
    version('1.8.0',  sha256='43ce39789d9a255f147311e40274b5f2571c7ef3b52e218f248724ccb377a02c', expand=False)

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-pipeline-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline-steps@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))

    depends_on('py-azureml-pipeline-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline-steps@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-pipeline-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline-steps@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
