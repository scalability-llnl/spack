# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlTelemetry(Package):
    """Machine learning (ML) telemetry package is used to collect telemetry
    data."""

    homepage = "https://docs.microsoft.com/en-us/azure/machine-learning/service/"
    url      = "https://pypi.io/packages/py3/a/azureml_telemetry/azureml_telemetry-1.11.0-py3-none-any.whl"

    version('1.23.0', sha256='68f9aac77e468db80e60f75d0843536082e2884ab251b6d3054dd623bd9c9e0d', expand=False)
    version('1.11.0', sha256='0d46c4a7bb8c0b188f1503504a6029384bc2237d82a131e7d1e9e89c3491b1fc', expand=False)
    version('1.8.0',  sha256='de657efe9773bea0de76c432cbab34501ac28606fe1b380d6883562ebda3d804', expand=False)

    extends('python')
    depends_on('python@3.5:3.999', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-applicationinsights', type=('build', 'run'))

    depends_on('py-azureml-core@1.23.0:1.23.999', when='@1.23.0', type=('build', 'run'))

    depends_on('py-azureml-core@1.11.0:1.11.999', when='@1.11.0', type=('build', 'run'))

    depends_on('py-azureml-core@1.8.0:1.8.999', when='@1.8.0', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
