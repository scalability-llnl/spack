# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyTensorboardPluginWit(Package):
    """The What-If Tool makes it easy to efficiently and
       intuitively explore up to two models' performance
       on a dataset. Investigate model performances for
       a range of features in your dataset, optimization
       strategies and even manipulations to individual
       datapoint values. All this and more, in a visual way
       that requires minimal code."""

    homepage = "https://pypi.python.org/project/tensorboard-plugin-wit"
    url      = "https://github.com/PAIR-code/what-if-tool/archive/v1.7.0.tar.gz"
    git      = "https://github.com/pair-code/what-if-tool.git"

    maintainers = ['aweits']

    version('master', branch='master')
    version('1.7.0', sha256='30dcab9065b02c3f1476f4fb92b27f6feb6c00cdb281699c44d8e69c86745247')

    depends_on('bazel@0.26.1:', type='build')
    depends_on('py-setuptools@36.2.0:', type='build')
    depends_on('python@2.7:2.8,3.2:', type=('build', 'run'))
    depends_on('py-wheel', type='build')

    extends('python')

    patch('tboard_shellenv.patch')

    phases = ['setup', 'build', 'install']

    def setup_build_environment(self, env):
        tmp_path = '/tmp/spack/tb-plugin'
        mkdirp(tmp_path)
        env.set('TEST_TMPDIR', tmp_path)

    def setup(self, spec, prefix):
        builddir = join_path(self.stage.source_path, 'spack-build')
        mkdirp(builddir)
        filter_file(r'dest=.*',
                    'dest="{0}"'.format(builddir),
                    'tensorboard_plugin_wit/pip_package/build_pip_package.sh')
        filter_file(r'pip install .*',
                    '',
                    'tensorboard_plugin_wit/pip_package/build_pip_package.sh')
        filter_file(r'command \-v .*',
                    '',
                    'tensorboard_plugin_wit/pip_package/build_pip_package.sh')
        filter_file(r'virtualenv venv',
                    '',
                    'tensorboard_plugin_wit/pip_package/build_pip_package.sh')
        filter_file('unset PYTHON_HOME',
                    'export PYTHONPATH="{0}"'.format(env['PYTHONPATH']),
                    'tensorboard_plugin_wit/pip_package/build_pip_package.sh')
        filter_file('python setup.py',
                    '{0} setup.py'.format(spec['python'].command.path),
                    'tensorboard_plugin_wit/pip_package/build_pip_package.sh')

    def build(self, spec, prefix):
        tmp_path = env['TEST_TMPDIR']
        bazel('--nohome_rc',
              '--nosystem_rc',
              '--output_user_root=' + tmp_path,
              'run',
              # watch https://github.com/bazelbuild/bazel/issues/7254
              '--define=EXECUTOR=remote',
              '--verbose_failures',
              '--subcommands=pretty_print',
              'tensorboard_plugin_wit/pip_package:build_pip_package')

    def install(self, spec, prefix):
        with working_dir('spack-build/release'):
            setup_py('install', '--prefix={0}'.format(prefix),
                     '--single-version-externally-managed', '--root=/')
