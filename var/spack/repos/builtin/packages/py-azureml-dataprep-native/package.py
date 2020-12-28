# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyAzuremlDataprepNative(Package):
    """Python Package for AzureML DataPrep specific native extensions."""

    homepage = "http://aka.ms/data-prep-sdk"

    if sys.platform == 'darwin':
        version('14.2.1', sha256='0711ea6465a555d4ed052b7ecf3ed580d711ca7499a12be4c9736d5555ab2786', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_native/azureml_dataprep_native-14.2.1-cp37-cp37m-macosx_10_9_x86_64.whl')
    elif sys.platform.startswith('linux'):
        version('14.2.1', sha256='0817ec5c378a9bcd1af8edda511ca9d02bdc7087e6f8802c459c9b8f3fde4ade', expand=False,
                url='https://pypi.io/packages/cp37/a/azureml_dataprep_native/azureml_dataprep_native-14.2.1-cp37-cp37m-manylinux1_x86_64.whl')

    extends('python')
    depends_on('python@3.7.0:3.7.999', type=('build', 'run'))
    depends_on('py-pip', type='build')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
