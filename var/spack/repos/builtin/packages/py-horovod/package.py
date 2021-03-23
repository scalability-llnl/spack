# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyHorovod(PythonPackage, CudaPackage):
    """Horovod is a distributed deep learning training framework for
    TensorFlow, Keras, PyTorch, and Apache MXNet."""

    homepage = "https://github.com/horovod"
    git      = "https://github.com/horovod/horovod.git"

    maintainers = ['adamjstewart', 'aweits', 'tgaddair']

    version('master', branch='master', submodules=True)
    version('0.21.3', tag='v0.21.3', submodules=True)
    version('0.21.2', tag='v0.21.2', submodules=True)
    version('0.21.1', tag='v0.21.1', submodules=True)
    version('0.21.0', tag='v0.21.0', submodules=True)
    version('0.20.3', tag='v0.20.3', submodules=True)
    version('0.20.2', tag='v0.20.2', submodules=True)
    version('0.20.1', tag='v0.20.1', submodules=True)
    version('0.20.0', tag='v0.20.0', submodules=True)
    version('0.19.5', tag='v0.19.5', submodules=True)
    version('0.19.4', tag='v0.19.4', submodules=True)
    version('0.19.3', tag='v0.19.3', submodules=True)
    version('0.19.2', tag='v0.19.2', submodules=True)
    version('0.19.1', tag='v0.19.1', submodules=True)
    version('0.19.0', tag='v0.19.0', submodules=True)
    version('0.18.2', tag='v0.18.2', submodules=True)
    version('0.18.1', tag='v0.18.1', submodules=True)
    version('0.18.0', tag='v0.18.0', submodules=True)
    version('0.17.1', tag='v0.17.1', submodules=True)
    version('0.17.0', tag='v0.17.0', submodules=True)
    version('0.16.4', tag='v0.16.4', submodules=True)
    version('0.16.3', tag='v0.16.3', submodules=True)
    version('0.16.2', tag='v0.16.2', submodules=True)

    # https://github.com/horovod/horovod/blob/master/docs/install.rst
    variant('frameworks', default='pytorch',
            description='Deep learning frameworks to build support for',
            values=('tensorflow', 'pytorch', 'mxnet', 'keras', 'spark', 'ray'),
            multi=True)
    variant('controllers', default='mpi',
            description='Controllers to coordinate work between processes',
            values=('mpi', 'gloo'), multi=True)
    variant('tensor_ops', default='nccl',
            description='Framework to use for GPU/CPU operations',
            values=('nccl', 'mpi', 'gloo', 'ccl'), multi=False)
    variant('cuda', default=True, description='Build with CUDA')
    variant('rocm', default=False, description='Build with ROCm')

    # Required dependencies
    depends_on('python@3.6:',    type=('build', 'run'), when='@0.20:')
    depends_on('py-setuptools',  type='build')
    depends_on('py-cloudpickle', type=('build', 'run'))
    depends_on('py-psutil',      type=('build', 'run'))
    depends_on('py-pyyaml',      type=('build', 'run'))
    depends_on('py-six',         type=('build', 'run'), when='@:0.19')
    depends_on('py-dataclasses', type=('build', 'run'), when='@0.20: ^python@:3.6')

    # Framework dependencies
    depends_on('py-tensorflow@1.1.0:',  type=('build', 'link', 'run'), when='frameworks=tensorflow')
    depends_on('py-tensorflow@1.15:',   type=('build', 'link', 'run'), when='frameworks=tensorflow @0.20:')
    depends_on('py-torch@0.4.0:',       type=('build', 'link', 'run'), when='frameworks=pytorch')
    depends_on('py-torch@1.2:',         type=('build', 'link', 'run'), when='frameworks=pytorch @0.20:')
    depends_on('py-torchvision',        type=('build', 'run'),         when='frameworks=pytorch @:0.19.1')
    depends_on('py-cffi@1.4.0:',        type=('build', 'run'),         when='frameworks=pytorch')
    depends_on('mxnet@1.4.1:+python',   type=('build', 'link', 'run'), when='frameworks=mxnet')
    depends_on('py-keras@2.0.8,2.1.2:', type=('build', 'run'),         when='frameworks=keras')
    depends_on('py-h5py@:2.999',        type=('build', 'run'),         when='frameworks=spark')
    depends_on('py-numpy',              type=('build', 'run'),         when='frameworks=spark')
    depends_on('py-petastorm@0.8.2',    type=('build', 'run'),         when='frameworks=spark @:0.19.1')
    depends_on('py-petastorm@0.9.0:',   type=('build', 'run'),         when='frameworks=spark @0.19.2:0.21.0')
    depends_on('py-petastorm@0.9.8:',   type=('build', 'run'),         when='frameworks=spark @0.21.1:')
    depends_on('py-pyarrow@0.15.0:',    type=('build', 'run'),         when='frameworks=spark')
    depends_on('py-pyspark@2.3.2:',     type=('build', 'run'),         when='frameworks=spark ^python@:3.7')
    depends_on('py-pyspark@3.0.0:',     type=('build', 'run'),         when='frameworks=spark ^python@3.8:')
    depends_on('py-ray',                type=('build', 'run'),         when='frameworks=ray')

    # Build dependencies
    depends_on('cmake@2.8.12:', type='build', when='@0.20:')
    depends_on('pkgconfig', type='build')

    # Controller dependencies
    depends_on('mpi', when='controllers=mpi')
    # There does not appear to be a way to use an external Gloo installation
    depends_on('cmake', type='build', when='controllers=gloo')
    depends_on('libuv@1.26:', when='controllers=gloo platform=darwin')

    # Tensor Operations dependencies
    depends_on('nccl@2:', when='tensor_ops=nccl')
    depends_on('mpi', when='tensor_ops=mpi')
    # There does not appear to be a way to use an external Gloo installation
    depends_on('cmake', type='build', when='tensor_ops=gloo')

    conflicts('cuda_arch=none', when='+cuda',
              msg='Must specify CUDA compute capabilities of your GPU, see '
              'https://developer.nvidia.com/cuda-gpus')
    conflicts('tensor_ops=nccl', when='~cuda~rocm', msg='NCCL requires either CUDA or ROCm support')
    conflicts('frameworks=ray', when='@:0.19', msg='Ray integration was added in 0.20.X')
    conflicts('controllers=gloo', when='@:0.20.0 platform=darwin', msg='Gloo cannot be compiled on MacOS')

    # https://github.com/horovod/horovod/pull/1835
    patch('fma.patch', when='@0.19.0:0.19.1')

    @property
    def import_modules(self):
        modules = [
            'horovod', 'horovod.runner', 'horovod.runner.util',
            'horovod.runner.elastic', 'horovod.runner.driver',
            'horovod.runner.common', 'horovod.runner.common.util',
            'horovod.runner.common.service', 'horovod.runner.http',
            'horovod.runner.task', 'horovod.common'
        ]

        if 'frameworks=tensorflow' in self.spec:
            modules.append('horovod.tensorflow')

        if 'frameworks=pytorch' in self.spec:
            modules.extend([
                'horovod.torch', 'horovod.torch.mpi_lib',
                'horovod.torch.elastic', 'horovod.torch.mpi_lib_impl'
            ])

        if 'frameworks=mxnet' in self.spec:
            modules.append('horovod.mxnet')

        if 'frameworks=keras' in self.spec:
            modules.extend(['horovod.keras', 'horovod._keras'])

        if 'frameworks=spark' in self.spec:
            modules.extend([
                'horovod.spark', 'horovod.spark.driver',
                'horovod.spark.common', 'horovod.spark.task'
            ])

        if 'frameworks=ray' in self.spec:
            modules.append('horovod.ray')

        if 'frameworks=tensorflow,keras' in self.spec:
            modules.append('horovod.tensorflow.keras')

        if 'frameworks=spark,pytorch' in self.spec:
            modules.append('horovod.spark.torch')

        if 'frameworks=spark,keras' in self.spec:
            modules.append('horovod.spark.keras')

        return modules

    def setup_build_environment(self, env):
        # https://github.com/horovod/horovod/blob/master/docs/install.rst#environment-variables

        # Build system
        env.set('PKG_CONFIG_EXECUTABLE',
                self.spec['pkgconfig'].prefix.bin.join('pkg-config'))
        if '^cmake' in self.spec:
            env.set('HOROVOD_CMAKE', self.spec['cmake'].command.path)
        env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))

        # Frameworks
        if 'frameworks=tensorflow' in self.spec:
            env.set('HOROVOD_WITH_TENSORFLOW', 1)
        else:
            env.set('HOROVOD_WITHOUT_TENSORFLOW', 1)
        if 'frameworks=pytorch' in self.spec:
            env.set('HOROVOD_WITH_PYTORCH', 1)
        else:
            env.set('HOROVOD_WITHOUT_PYTORCH', 1)
        if 'frameworks=mxnet' in self.spec:
            env.set('HOROVOD_WITH_MXNET', 1)
        else:
            env.set('HOROVOD_WITHOUT_MXNET', 1)

        # Controllers
        if 'controllers=mpi' in self.spec:
            env.set('HOROVOD_WITH_MPI', 1)
        else:
            env.set('HOROVOD_WITHOUT_MPI', 1)
        if 'controllers=gloo' in self.spec:
            env.set('HOROVOD_WITH_GLOO', 1)
        else:
            env.set('HOROVOD_WITHOUT_GLOO', 1)

        # Tensor Operations
        if 'tensor_ops=nccl' in self.spec:
            env.set('HOROVOD_GPU_ALLREDUCE', 'NCCL')
            env.set('HOROVOD_GPU_ALLGATHER', 'NCCL')
            env.set('HOROVOD_GPU_BROADCAST', 'NCCL')

            env.set('HOROVOD_NCCL_HOME', self.spec['nccl'].prefix)
            env.set('HOROVOD_NCCL_INCLUDE',
                    self.spec['nccl'].headers.directories[0])
            env.set('HOROVOD_NCCL_LIB', self.spec['nccl'].libs.directories[0])

            if '+cuda' in self.spec:
                env.set('HOROVOD_GPU', 'CUDA')

                env.set('HOROVOD_CUDA_HOME', self.spec['cuda'].prefix)
                cuda_cc_list = ','.join(self.spec.variants['cuda_arch'].value)
                env.set('HOROVOD_BUILD_CUDA_CC_LIST', cuda_cc_list)
                env.set('HOROVOD_CUDA_INCLUDE',
                        self.spec['cuda'].headers.directories[0])
                env.set('HOROVOD_CUDA_LIB',
                        self.spec['cuda'].libs.directories[0])
            elif '+rocm' in self.spec:
                env.set('HOROVOD_GPU', 'ROCM')
                # env.set('HOROVOD_ROCM_HOME', self.spec['rocm'].prefix)
        else:
            env.set('HOROVOD_CPU_OPERATIONS',
                    self.spec.variants['tensor_ops'].value.upper())

    def test(self):
        super(PyHorovod, self).test()
        run_test(self.prefix.bin.horovodrun, '--check-build')
