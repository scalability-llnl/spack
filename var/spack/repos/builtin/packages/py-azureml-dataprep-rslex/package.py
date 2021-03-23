# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import archspec

from spack import *


class PyAzuremlDataprepRslex(Package):
    """Azure Machine Learning Data Prep RsLex is a Rust implementation of Data Prep's
    capabilities to load, transform, and write data for machine learning workflows."""

    homepage = "http://aka.ms/data-prep-sdk"

    if sys.platform == 'darwin':
        version('1.9.0-py3.9', sha256='9bdaa31d129dac19ee20d5a3aad1726397e90d8d741b4f6de4554040800fefe8', expand=False,
                url='https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp39-cp39-macosx_10_9_x86_64.whl')
        version('1.9.0-py3.8', sha256='9b2e741ac1c53d3f7e6061d264feccf157d97e404c772933a176e6021014484e', expand=False, preferred=True,
                url='https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp38-cp38-macosx_10_9_x86_64.whl')
        version('1.9.0-py3.7', sha256='9993b369fb9d94d885611859ee957582304c1d8953fc8b48567b786bbfd8062b', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp37-cp37m-macosx_10_9_x86_64.whl')
        version('1.9.0-py3.6', sha256='80d518774591deb2c8f1457708c10c9ba348407d7aa49e0710358f46846fcbef', expand=False,
                url='https://pypi.io/packages/cp36/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp36-cp36m-macosx_10_9_x86_64.whl')
        version('1.9.0-py3.5', sha256='91a5c09796e60570620efb7d66f05647557ec6d39aab8b22c0e13926c402ca5b', expand=False,
                url='https://pypi.io/packages/cp35/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp35-cp35m-macosx_10_9_x86_64.whl')

        version('1.8.0-py3.9', sha256='677c25a7e23ec7f91d25aa596f382f7f3b6d60fbc3258bead2b2a6aa42f3a16d', expand=False,
                url='https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp39-cp39-macosx_10_9_x86_64.whl')
        version('1.8.0-py3.8', sha256='d7f2dec06296544b1707f5b01c6a4eaad744b4abfe9e8e89830b561c84d95a7a', expand=False,
                url='https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp38-cp38-macosx_10_9_x86_64.whl')
        version('1.8.0-py3.7', sha256='8e9feb3187f11fb86f525bc88bf6a6171d7e7d6e2860411a5b82d1f3ecaa8ae8', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp37-cp37m-macosx_10_9_x86_64.whl')
        version('1.8.0-py3.6', sha256='f5f7c9af1f1ecfbfee0e5822db180de05c6f5aeed34f6d0b3fd26e210f476d3e', expand=False,
                url='https://pypi.io/packages/cp36/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp36-cp36m-macosx_10_9_x86_64.whl')
        version('1.8.0-py3.5', sha256='1c610a25a3e09d4ebb95c42baaa57b5c0c66e31522a6bff52dda0df2d6ac7f4d', expand=False,
                url='https://pypi.io/packages/cp35/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp35-cp35m-macosx_10_9_x86_64.whl')
    elif sys.platform.startswith('linux'):
        version('1.9.0-py3.9', sha256='79d52bb427e3ca781a645c4f11f7a8e5e2c8f61e61bfc162b4062d8e47bcf3d6', expand=False,
                url='https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp39-cp39-manylinux1_x86_64.whl')
        version('1.9.0-py3.8', sha256='a52461103b45867dd919bab593bb6f2426c9b5f5a435081e82a3c57c54c3add6', expand=False, preferred=True,
                url='https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp38-cp38-manylinux1_x86_64.whl')
        version('1.9.0-py3.7', sha256='d7b6e15401b88cec2915b0bd6298ae7f54584d01ee14e4a24ffb950b7578bceb', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp37-cp37m-manylinux1_x86_64.whl')
        version('1.9.0-py3.6', sha256='2723bf56f2d11e5ee00c6619f2365bd594e85ba116ffc912a2433c52913d0890', expand=False,
                url='https://pypi.io/packages/cp36/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp36-cp36m-manylinux1_x86_64.whl')
        version('1.9.0-py3.5', sha256='d5c6d363da2b3ace1baa9ad3e645ad8a19fdacf0b95dd1f8b6ab19c4371cc10f', expand=False,
                url='https://pypi.io/packages/cp35/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.9.0-cp35-cp35m-manylinux1_x86_64.whl')

        version('1.8.0-py3.9', sha256='e251a077669703ca117b157b225fbc20832169f913476cf79c01a5c6f8ff7a50', expand=False,
                url='https://pypi.io/packages/cp39/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp39-cp39-manylinux1_x86_64.whl')
        version('1.8.0-py3.8', sha256='2ebfa164f0933a5cec383cd27ba10d33861a73237ef481ada5a9a822bb55514a', expand=False,
                url='https://pypi.io/packages/cp38/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp38-cp38-manylinux1_x86_64.whl')
        version('1.8.0-py3.7', sha256='0588c6e503635aa6d4c64f7bbb3a3be52679f24ac89e2c8d4e96fd991d7006a2', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp37-cp37m-manylinux1_x86_64.whl')
        version('1.8.0-py3.6', sha256='195507ba55aa5ac7c5d37d05b8ac25813add0da5cc9bd4a04f2cb5da984cb287', expand=False,
                url='https://pypi.io/packages/cp36/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp36-cp36m-manylinux1_x86_64.whl')
        version('1.8.0-py3.5', sha256='9dfbd1065030dee3aa45b6796c087acffb06cfcbe97cc877e255e21e320362be', expand=False,
                url='https://pypi.io/packages/cp35/a/azureml_dataprep_rslex/azureml_dataprep_rslex-1.8.0-cp35-cp35m-manylinux1_x86_64.whl')

    extends('python')
    depends_on('py-pip', type='build')

    depends_on('python@3.9.0:3.9.999', when='@1.9.0-py3.9,1.8.0-py3.9', type=('build', 'run'))
    depends_on('python@3.8.0:3.8.999', when='@1.9.0-py3.8,1.8.0-py3.8', type=('build', 'run'))
    depends_on('python@3.7.0:3.7.999', when='@1.9.0-py3.7,1.8.0-py3.7', type=('build', 'run'))
    depends_on('python@3.6.0:3.6.999', when='@1.9.0-py3.6,1.8.0-py3.6', type=('build', 'run'))
    depends_on('python@3.5.0:3.5.999', when='@1.9.0-py3.5,1.8.0-py3.5', type=('build', 'run'))

    for t in set([str(x.family) for x in archspec.cpu.TARGETS.values()
                 if str(x.family) != 'x86_64']):
        conflicts('target={0}:'.format(t), msg='py-azureml-dataprep-rslex is available x86_64 only')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
