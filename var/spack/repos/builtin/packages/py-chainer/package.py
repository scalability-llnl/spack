# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import json


class PyChainer(PythonPackage):
    """
    Chainer is a Python-based deep learning framework aiming at flexibility.

    It provides automatic differentiation APIs based on the define-by-run
    approach (a.k.a. dynamic computational graphs) as well as object-oriented
    high-level APIs to build and train neural networks.
    It also supports CUDA/cuDNN using CuPy for high performance training
    and inference.
    """

    homepage = "https://chainer.org/"
    url      = "https://github.com/chainer/chainer/archive/v7.2.0.tar.gz"

    maintainers = ['adamjstewart']

    version('7.2.0', sha256='6e2fba648cc5b8a5421e494385b76fe5ec154f1028a1c5908557f5d16c04f0b3')
    version('6.7.0', sha256='87cb3378a35e7c5c695028ec91d58dc062356bc91412384ea939d71374610389')

    variant("mn", default=False, description="run with ChainerMN")

    depends_on('python@3.5.1:', when='@7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-typing-extensions', type=('build', 'run'))
    depends_on('py-typing-extensions@:3.6.6', when='@:6', type=('build', 'run'))
    depends_on('py-filelock', type=('build', 'run'))
    depends_on('py-protobuf@3:', type=('build', 'run'))
    depends_on('py-typing@:3.6.6', when='@:6', type=('build', 'run'))

    # Dependencies only required for test of ChainerMN
    depends_on('py-matplotlib', type=('build', 'run'), when='+mn')
    depends_on('py-mpi4py', type=('build', 'run'), when='+mn')
    depends_on("mpi", type=("build", "run"), when='+mn')

    @run_after('install')
    def cache_test_sources(self):
        if '+mn' in self.spec:
            self.cache_extra_test_sources("examples")

    def test(self):
        if "+mn" in self.spec:
            # Run test of ChainerMN
            test_dir = self.test_suite.current_test_data_dir

            mnist_dir = join_path(
                self.install_test_root, "examples", "chainermn", "mnist"
            )
            mnist_file = join_path(mnist_dir, "train_mnist.py")
            mpi_name = self.spec["mpi"].prefix.bin.mpirun
            python_exe = self.spec["python"].command.path
            opts = [
                "-n",
                "4",
                python_exe,
                mnist_file,
                "-o",
                test_dir,
            ]
            env["OMP_NUM_THREADS"] = "4"

            self.run_test(
                mpi_name,
                options=opts,
                work_dir=test_dir,
            )

            # check results
            json_open = open(join_path(test_dir, 'log'), 'r')
            json_load = json.load(json_open)
            v = dict([(d.get('epoch'), d.get('main/accuracy')) for d in json_load])
            if 1 not in v or 20 not in v:
                raise RuntimeError('Cannot find epoch 1 or epoch 20')
            if abs(1.0 - v[1]) < abs(1.0 - v[20]):
                raise RuntimeError('ChainerMN Test Failed !')
