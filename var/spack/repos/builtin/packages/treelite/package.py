# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Treelite(CMakePackage, PythonPackage):
    """Treelite is a model compiler for efficient deployment of
    decision tree ensembles."""

    homepage = "https://github.com/dmlc/treelite"
    url      = "https://github.com/dmlc/treelite/archive/0.93.tar.gz"

    version('0.93',    sha256='7d347372f7fdc069904afe93e69ed0bf696ba42d271fe2f8bf6835d2ab2f45d5')

    variant('protobuf', default=False, description='Build with protobuf')
    variant('python', default=True, description='Build with python support')

    depends_on('protobuf', when='+protobuf')
    depends_on('python@3.6:', when='+python', type=('build', 'run'))
    depends_on('py-setuptools', when='+python', type='build')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-scipy', when='+python', type=('build', 'run'))

    build_directory = 'build'
    phases = ['cmake', 'build', 'python_build', 'install', 'python_install']

    def cmake_args(self):
        args = []

        if '+protobuf' in self.spec:
            args.append('-DENABLE_PROTOBUF:BOOL=ON')
            args.append('-DProtobuf_LIBRARY={0}'.format(
                self.spec['protobuf'].prefix))
        else:
            args.append('-DENABLE_PROTOBUF:BOOL=OFF')

        return args

    def python_build(self, spec, prefix):
        if '+python' in spec:
            self._build_directory = 'python'
            PythonPackage.build_ext(self, spec, prefix)
        else:
            print('python deselected')

    def python_install(self, spec, prefix):
        if '+python' in spec:
            PythonPackage.install(self, spec, prefix)
        else:
            print('python deselected')

    def setup_py(self, *args, **kwargs):
        setup = self.setup_file()

        with working_dir(os.path.join(self.stage.source_path, 'python')):
            self.python('-s', setup, '--no-user-cfg', *args, **kwargs)
