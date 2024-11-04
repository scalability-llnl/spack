# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CosmoflowBenchmark(Package, CudaPackage):
    """This is a an implementation of the CosmoFlow 3D convolutional neural
    network for benchmarking. It is written in TensorFlow with the Keras API
    and uses Horovod for distributed training."""

    homepage = "https://github.com/sparticlesteve/cosmoflow-benchmark"
    git = "https://github.com/sparticlesteve/cosmoflow-benchmark.git"

    tags = ["proxy-app"]

    version("master", branch="master")

    depends_on("python@3:", type=("build", "run"))

    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-horovod", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))

    depends_on("py-tensorflow+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-tensorflow~cuda~nccl", when="~cuda", type=("build", "run"))
    depends_on("py-torch+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-torch~cuda~nccl", when="~cuda", type=("build", "run"))
    depends_on("py-horovod tensor_ops=mpi", when="~cuda", type=("build", "run"))

    def install(self, spec, prefix):
        # Mostly  about providing an environment so just copy everything
        install_tree(".", prefix)
