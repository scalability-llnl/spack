# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PyPybind11(CMakePackage):
    """pybind11 -- Seamless operability between C++11 and Python.

    pybind11 is a lightweight header-only library that exposes C++ types in
    Python and vice versa, mainly to create Python bindings of existing C++
    code. Its goals and syntax are similar to the excellent Boost.Python
    library by David Abrahams: to minimize boilerplate code in traditional
    extension modules by inferring type information using compile-time
    introspection."""

    homepage = "https://pybind11.readthedocs.io"
    url      = "https://github.com/pybind/pybind11/archive/v2.6.2.tar.gz"
    git      = "https://github.com/pybind/pybind11.git"

    maintainers = ['ax3l']

    version('master', branch='master')
    version('2.6.2', sha256='8ff2fff22df038f5cd02cea8af56622bc67f5b64534f1b83b9f133b8366acff2')
    version('2.6.1', sha256='cdbe326d357f18b83d10322ba202d69f11b2f49e2d87ade0dc2be0c5c34f8e2a')
    version('2.5.0', sha256='97504db65640570f32d3fdf701c25a340c8643037c3b69aec469c10c93dc8504', preferred=True)
    version('2.4.3', sha256='1eed57bc6863190e35637290f97a20c81cfe4d9090ac0a24f3bbf08f265eb71d')
    version('2.3.0', sha256='0f34838f2c8024a6765168227ba587b3687729ebf03dc912f88ff75c7aa9cfe8')
    version('2.2.4', sha256='b69e83658513215b8d1443544d0549b7d231b9f201f6fc787a2b2218b408181e')
    version('2.2.3', sha256='3a3b7b651afab1c5ba557f4c37d785a522b8030dfc765da26adc2ecd1de940ea')
    version('2.2.2', sha256='b639a2b2cbf1c467849660801c4665ffc1a4d0a9e153ae1996ed6f21c492064e')
    version('2.2.1', sha256='f8bd1509578b2a1e7407d52e6ee8afe64268909a1bbda620ca407318598927e7')
    version('2.2.0', sha256='1b0fda17c650c493f5862902e90f426df6751da8c0b58c05983ab009951ed769')
    version('2.1.1', sha256='f2c6874f1ea5b4ad4ffffe352413f7d2cd1a49f9050940805c2a082348621540')
    version('2.1.0', sha256='2860f2b8d0c9f65f0698289a161385f59d099b7ead1bf64e8993c486f2b93ee0')

    depends_on('py-setuptools', type='build')

    extends('python')

    # compiler support
    conflicts('%gcc@:4.7')
    conflicts('%clang@:3.2')
    conflicts('%intel@:16')

    def cmake_args(self):
        args = []
        args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s'
                    % self.spec['python'].command.path)
        args += [
            '-DPYBIND11_TEST:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF')
        ]
        return args

    def setup_build_environment(self, env):
        env.set('PYBIND11_USE_CMAKE', 1)

    # https://github.com/pybind/pybind11/pull/1995
    @when('@:2.4.99')
    def patch(self):
        """ see https://github.com/spack/spack/issues/13559 """
        filter_file('import sys',
                    'import sys; return "{0}"'.format(self.prefix.include),
                    'pybind11/__init__.py',
                    string=True)

    def install(self, spec, prefix):
        super(PyPybind11, self).install(spec, prefix)
        setup_py('install', '--single-version-externally-managed', '--root=/',
                 '--prefix={0}'.format(prefix))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('spack-test', create=True):
            # test include helper points to right location
            python = self.spec['python'].command
            py_inc = python(
                '-c',
                'import pybind11 as py; ' +
                self.spec['python'].package.print_string('py.get_include()'),
                output=str).strip()
            for inc in [py_inc, self.prefix.include]:
                inc_file = join_path(inc, 'pybind11', 'pybind11.h')
                assert os.path.isfile(inc_file)
