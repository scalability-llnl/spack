from spack import *

class TensorflowEstimator(Package):
    """TensorFlow Estimator is a high-level TensorFlow API that greatly simplifies machine learning programming."""

    homepage = "https://github.com/tensorflow/estimator"
    url      = "https://github.com/tensorflow/estimator/archive/v1.13.0.tar.gz"

    version('2.0.0-alpha', '739923c39443ec614f5348d7ff7f1d03')
    version('1.13.0',      '50ee7a8fdd1a0abad027b63999fb464b', preferred=True)

    extends('python')

    depends_on('tensorflow@2.0.0-alpha0',  when='@2.0.0-alpha')
    depends_on('tensorflow@1.13.1',        when='@1.13.0')

    depends_on('bazel@0.19.0',             type='build')
    depends_on('py-pip',                   type='build')
    depends_on('py-funcsigs@1.0.2:',       type=('build', 'run'))

    def install(self, spec, prefix):
        tmp_path = os.path.join(env.get('SPACK_TMPDIR', '/tmp/spack'), 'tf-estimator', str(self.module.site_packages_dir)[1:])
        mkdirp(tmp_path)
        env['TEST_TMPDIR'] = tmp_path
        env['HOME'] = tmp_path

        # bazel uses system PYTHONPATH instead of spack paths
        bazel('--action_env', 'PYTHONPATH={0}'.format(env['PYTHONPATH']), '//tensorflow_estimator/tools/pip_package:build_pip_package')

        build_pip_package = Executable('bazel-bin/tensorflow_estimator/tools/pip_package/build_pip_package')
        build_pip_package(tmp_path)

        pip = Executable('pip')
        pip('install', '--prefix={0}'.format(prefix), '--find-links={0}'.format(tmp_path), 'tensorflow-estimator')
