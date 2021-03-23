# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlPipelineCore(Package):
    """Core functionality to enable azureml-pipeline feature."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_pipeline_core/azureml_pipeline_core-1.11.0-py3-none-any.whl"

    version('1.23.0', sha256='347e3e41559879611d53eeff5c05dd133db6fa537edcf2b9f70d91aad461df02', expand=False)
    version('1.11.0', sha256='98012195e3bba12bf42ac69179549038b3563b39e3dadab4f1d06407a00ad8b3', expand=False)
    version('1.8.0',  sha256='24e1c57a57e75f9d74ea6f45fa4e93c1ee3114c8ed9029d538f9cc8e4f8945b2', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-azureml-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))

    depends_on('py-azureml-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
