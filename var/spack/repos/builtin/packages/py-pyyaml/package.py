# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyyaml(PythonPackage):
    """PyYAML is a YAML parser and emitter for Python."""

    homepage = "https://pyyaml.org/wiki/PyYAML"
    url      = "https://pypi.io/packages/source/P/PyYAML/PyYAML-5.3.1.tar.gz"
    git      = "https://github.com/yaml/pyyaml.git"

    maintainers = ['adamjstewart']

    version('5.3.1', sha256='b8eac752c5e14d3eca0e6dd9199cd627518cb5ec06add0de9d32baeee6fe645d')
    version('5.1.2', sha256='01adf0b6c6f61bd11af6e10ca52b7d4057dd0be0343eb9283c878cf3af56aee4')
    version('5.1',   sha256='436bc774ecf7c103814098159fbb84c2715d25980175292c648f2da143909f95')
    version('3.13',  sha256='3ef3092145e9b70e3ddd2c7ad59bdd0252a94dfe3949721633e41344de00a6bf')
    version('3.12',  sha256='592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab')
    version('3.11',  sha256='c36c938a872e5ff494938b33b14aaa156cb439ec67548fcab3535bb78b0846e8')

    variant('libyaml', default=True, description='Use libYAML bindings')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('libyaml', when='+libyaml')

    phases = ['build_ext', 'install']

    @property
    def import_modules(self):
        modules = ['yaml']

        if '+libyaml' in self.spec:
            modules.append('yaml.cyaml')

        return modules

    def setup_py(self, *args, **kwargs):
        # Cast from tuple to list
        args = list(args)

        if '+libyaml' in self.spec:
            args.insert(0, '--with-libyaml')
        else:
            args.insert(0, '--without-libyaml')

        super(PyPyyaml, self).setup_py(*args, **kwargs)

    def build_ext_args(self, spec, prefix):
        args = []

        if '+libyaml' in spec:
            args.extend([
                spec['libyaml'].libs.search_flags,
                spec['libyaml'].headers.include_flags,
            ])

        return args

    # Tests need to be re-added since `phases` was overridden
    run_after('install')(
        PythonPackage._run_default_install_time_test_callbacks)
    run_after('install')(PythonPackage.sanity_check_prefix)
