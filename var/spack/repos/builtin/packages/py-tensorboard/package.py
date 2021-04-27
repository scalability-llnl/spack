# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import tempfile

from spack.pkgkit import *


class PyTensorboard(Package):
    """TensorBoard is a suite of web applications for
    inspecting and understanding your TensorFlow runs and
    graphs."""

    homepage = "https://github.com/tensorflow/tensorboard"
    url      = "https://github.com/tensorflow/tensorboard/archive/2.2.0.tar.gz"

    maintainers = ['aweits']

    version('2.4.1', sha256='736dc204aa292d221f5871077e60994a9a9ea8e33b841f0d754d510fe6cc7635')
    version('2.4.0', sha256='28a30794c1c797357b2086477394b59afa0b18ca48592ca3c0627f7f10536373')
    version('2.3.0', sha256='947a58702c2841eb4559637dbf8639633f79de9a0f422be9737f3563a1725440')
    version('2.2.0', sha256='d0dfbf0e4b3b5ebbc3fafa6d281d4b9aa5478eac6bac3330652ab6674278ab77')

    depends_on('python@2.7:2.8,3.2:', type=('build', 'run'))
    depends_on('bazel@2.1.0:', type='build', when='@2.2.0:')
    depends_on('py-setuptools@41.0.0:', type=('build', 'run'))
    depends_on('py-absl-py@0.4:', type=('build', 'run'))
    depends_on('py-markdown@2.6.8:', type=('build', 'run'))
    depends_on('py-requests@2.21.0:2.999', type=('build', 'run'))
    depends_on('py-futures@3.1.1:', type=('build', 'run'), when='^python@:2')
    depends_on('py-grpcio@1.24.3:', type=('build', 'run'), when='@2.3:')
    depends_on('py-grpcio@1.23.3:', type=('build', 'run'), when='@2.2')
    depends_on('py-google-auth@1.6.3:1.99.99', type=('build', 'run'))
    depends_on('py-numpy@1.12.0:', type=('build', 'run'))
    depends_on('py-protobuf@3.6.0:', type=('build', 'run'))
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-werkzeug@0.11.15:', type=('build', 'run'))
    depends_on('py-wheel', type=('build', 'run'))
    depends_on('py-wheel@0.26:', type=('build', 'run'), when='@0.6: ^python@3:')
    depends_on('py-google-auth-oauthlib@0.4.1:0.4.999', type=('build', 'run'))
    depends_on('py-tensorboard-plugin-wit@1.6.0:', type=('build', 'run'), when='@2.2.0:')

    extends('python')

    patch('tboard_shellenv.patch')

    phases = ['configure', 'build', 'install']

    def patch(self):
        filter_file('build --define=angular_ivy_enabled=True',
                    'build --define=angular_ivy_enabled=True\n'
                    'build --distinct_host_configuration=false\n'
                    'build --action_env=PYTHONPATH="{0}"\n'.format(
                        env['PYTHONPATH']),
                    '.bazelrc')

    def setup_build_environment(self, env):
        self.tmp_path = tempfile.mkdtemp(dir='/tmp', prefix='spack')
        env.set('TEST_TMPDIR', self.tmp_path)

    def configure(self, spec, prefix):
        builddir = join_path(self.stage.source_path, 'spack-build')
        mkdirp(builddir)
        filter_file(r'workdir=.*',
                    'workdir="{0}"'.format(builddir),
                    'tensorboard/pip_package/build_pip_package.sh')
        filter_file(r'pip install .*',
                    '',
                    'tensorboard/pip_package/build_pip_package.sh')
        filter_file(r'command \-v .*',
                    '',
                    'tensorboard/pip_package/build_pip_package.sh')
        filter_file(r'virtualenv .*',
                    '',
                    'tensorboard/pip_package/build_pip_package.sh')
        filter_file('trap cleanup EXIT',
                    '',
                    'tensorboard/pip_package/build_pip_package.sh')
        filter_file('unset PYTHON_HOME',
                    'export PYTHONPATH="{0}"'.format(env['PYTHONPATH']),
                    'tensorboard/pip_package/build_pip_package.sh')
        filter_file('python setup.py',
                    '{0} setup.py'.format(spec['python'].command.path),
                    'tensorboard/pip_package/build_pip_package.sh')
        if self.spec.satisfies('@2.4.0:'):
            filter_file('"@npm//@polymer/polymer",',
                        '"@npm//@polymer/polymer",\n'
                        '"@npm//@types/d3",',
                        'tensorboard/plugins/projector/vz_projector/BUILD')

    def build(self, spec, prefix):
        bazel('--nohome_rc',
              '--nosystem_rc',
              '--output_user_root=' + self.tmp_path,
              'build',
              # watch https://github.com/bazelbuild/bazel/issues/7254
              '--define=EXECUTOR=remote',
              '--verbose_failures',
              '--spawn_strategy=local',
              '--subcommands=pretty_print',
              '//tensorboard/pip_package')

    def install(self, spec, prefix):
        with working_dir('spack-build'):
            setup_py('install', '--prefix={0}'.format(prefix),
                     '--single-version-externally-managed', '--root=/')
        remove_linked_tree(self.tmp_path)
