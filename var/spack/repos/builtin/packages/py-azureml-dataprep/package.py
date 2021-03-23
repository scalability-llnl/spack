# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzuremlDataprep(Package):
    """Azure ML Data Preparation SDK."""

    homepage = "http://aka.ms/data-prep-sdk"
    url      = "https://pypi.io/packages/py3/a/azureml_dataprep/azureml_dataprep-2.0.2-py3-none-any.whl"

    version('2.11.0', sha256='755c0d7cfe228705aee7adc97813fb6d7d6ecb048b66f47c1fd5897f2709c3a2', expand=False)
    version('2.10.1', sha256='a36f807112ff1e64d21265b8e7f40154c93e3bead539e2a74c9d74200fd77c86', expand=False)
    version('2.0.2', sha256='9b9e97d9ed29c0641d3ceb37745ff078143bd235c53df528f847ec0684c52f79', expand=False)
    version('1.8.2', sha256='e53f3206f0bd4af8d5e7de3a94c2c6e662902b86e94a7b9d930e36329fe5820f', expand=False)

    variant('fuse', default=False, description='Build with FUSE support')

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')

    depends_on('py-dotnetcore2@2.1.14:2.999', type=('build', 'run'))
    depends_on('py-azureml-dataprep-native@30.0.0:30.999', when='@2.10.0:', type=('build', 'run'))
    depends_on('py-azureml-dataprep-native@14.2.1:14.999', when='@:2.0.2', type=('build', 'run'))
    depends_on('py-azureml-dataprep-rslex@1.9.0:1.9.999', when='@2.11.0:', type=('build', 'run'))
    depends_on('py-azureml-dataprep-rslex@1.8.0:1.8.999', when='@2.10.1', type=('build', 'run'))
    depends_on('py-cloudpickle@1.1.0:1.999', type=('build', 'run'))
    depends_on('py-azure-identity@1.2.0:1.4.999', when='@2.10.0:', type=('build', 'run'))
    depends_on('py-azure-identity@1.2.0:1.2.999', when='@:2.0.2', type=('build', 'run'))
    depends_on('py-fusepy@3.0.1:3.999', when='+fuse', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
