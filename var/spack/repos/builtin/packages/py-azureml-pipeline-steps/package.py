# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlPipelineSteps(Package):
    """Represents a unit of computation in azureml-pipeline."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_pipeline_steps/azureml_pipeline_steps-1.11.0-py3-none-any.whl"

    version('1.23.0', sha256='72154c2f75624a1e7500b8e2239ae1354eeedf66d2cabb11e213b7eb80aedddb', expand=False)
    version('1.11.0', sha256='674317d9c74ec4cb05e443f50de1732e14dc4519cbe2743a44f8db0bc5e71214', expand=False)
    version('1.8.0',  sha256='3310674207ed457a26fb978e7168e400306c695f7f854f354dee9d5c7c81304c', expand=False)

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-train-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-train-automl-client@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))

    depends_on('py-azureml-train-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-train-automl-client@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-train-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-train-automl-client@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))
    depends_on('py-azureml-pipeline-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
