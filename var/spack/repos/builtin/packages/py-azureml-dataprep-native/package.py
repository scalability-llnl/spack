# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys


class PyAzuremlDataprepNative(Package):
    """Python Package for AzureML DataPrep specific native extensions."""

    homepage = "http://aka.ms/data-prep-sdk"

    if sys.platform == 'darwin':
        version('30.0.0-py3.9', sha256='eaf3fcd9f965e87b03fe89d7c6fe6abce53483a79afc963e4981061f4c250e85', expand=False,
                url='https://pypi.io/packages/cp39/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp39-cp39-macosx_10_9_x86_64.whl')
        version('30.0.0-py3.8', sha256='6772b638f9d03a041b17ce4343061f5d543019200904b9d361b2b2629c3595a7', expand=False, preferred=True,
                url='https://pypi.io/packages/cp38/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp38-cp38-macosx_10_9_x86_64.whl')
        version('30.0.0-py3.7', sha256='1fb47c48edf795aaa1b3e589a4d580fc61d639c0bb26519271736c72155d008e', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp37-cp37m-macosx_10_9_x86_64.whl')
        version('30.0.0-py3.6', sha256='bd81f0ac0df442b4e09bd2ee76ccff1279437b73e08324d9038c13a5e4708598', expand=False,
                url='https://pypi.io/packages/cp36/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp36-cp36m-macosx_10_9_x86_64.whl')
        version('30.0.0-py3.5', sha256='2d1702a2dd9b851ccba9d4624a240f5657f3f34a89977f01ee99f9ccaab905a9', expand=False,
                url='https://pypi.io/packages/cp35/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp35-cp35m-macosx_10_9_x86_64.whl')

        version('14.2.1-py3.7', sha256='0711ea6465a555d4ed052b7ecf3ed580d711ca7499a12be4c9736d5555ab2786', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_native/azureml_dataprep_native-14.2.1-cp37-cp37m-macosx_10_9_x86_64.whl')
    elif sys.platform.startswith('linux'):
        version('30.0.0-py3.9', sha256='b8673136948f682c84d047feacbfee436df053cba4f386f31c4c3a245a4e3646', expand=False,
                url='https://pypi.io/packages/cp39/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp39-cp39-manylinux1_x86_64.whl')
        version('30.0.0-py3.8', sha256='d07cf20f22b14c98576e135bbad9bb8aaa3108941d2beaadf050b4238bc93a18', expand=False, preferred=True,
                url='https://pypi.io/packages/cp38/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp38-cp38-manylinux1_x86_64.whl')
        version('30.0.0-py3.7', sha256='897063c21d7b1b8cb070f8992e78291c402559434e9d4a5bb85b595a5c676fe6', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp37-cp37m-manylinux1_x86_64.whl')
        version('30.0.0-py3.6', sha256='d2560d3f20cd3b8ad2d2159b1048b83dd330cf8c44aa8becedd6dcaf72876062', expand=False,
                url='https://pypi.io/packages/cp36/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp36-cp36m-manylinux1_x86_64.whl')
        version('30.0.0-py3.5', sha256='15b55d903d5688b5a9a290e388db62c8f3d042bc1796db44723f4455b7b18d07', expand=False,
                url='https://pypi.io/packages/cp35/a/azureml_dataprep_native/azureml_dataprep_native-30.0.0-cp35-cp35m-manylinux1_x86_64.whl')

        version('14.2.1-py3.7', sha256='0817ec5c378a9bcd1af8edda511ca9d02bdc7087e6f8802c459c9b8f3fde4ade', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_native/azureml_dataprep_native-14.2.1-cp37-cp37m-manylinux1_x86_64.whl')

    extends('python')
    depends_on('py-pip', type='build')

    depends_on('python@3.9.0:3.9.999', when='@30.0.0-py3.9', type=('build', 'run'))
    depends_on('python@3.8.0:3.8.999', when='@30.0.0-py3.8', type=('build', 'run'))
    depends_on('python@3.7.0:3.7.999', when='@30.0.0-py3.7', type=('build', 'run'))
    depends_on('python@3.6.0:3.6.999', when='@30.0.0-py3.6', type=('build', 'run'))
    depends_on('python@3.5.0:3.5.999', when='@30.0.0-py3.5', type=('build', 'run'))

    depends_on('python@3.7.0:3.7.999', when='@14.2.1-py3.7', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
