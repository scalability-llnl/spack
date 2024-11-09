# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Nccl(MakefilePackage, CudaPackage):
    """Optimized primitives for collective multi-GPU communication."""

    homepage = "https://github.com/NVIDIA/nccl"
    url = "https://github.com/NVIDIA/nccl/archive/v2.7.3-1.tar.gz"

    maintainers("adamjstewart")
    libraries = ["libnccl.so"]

    version("2.22.3-1", sha256="45151629a9494460e73375281e8b0fe379141528879301899ece9b776faca024")
    version("2.21.5-1", sha256="1923596984d85e310b5b6c52b2c72a1b93da57218f2bc5a5c7ac3d59297a3303")
    version("2.20.3-1", sha256="19456bd63ca7d23a8319cbbdbaaf6c25949dd51161a9f8809f6b7453282983dd")
    version("2.19.3-1", sha256="1c5474553afedb88e878c772f13d6f90b9226b3f2971dfa6f873adb9443100c2")
    version("2.18.5-1", sha256="16ac98f3e926c024ce48e10ab220e19ce734adc48c423cfd55ad6f509bd1179f")
    version("2.18.3-1", sha256="6477d83c9edbb34a0ebce6d751a1b32962bc6415d75d04972b676c6894ceaef9")
    version("2.18.1-1", sha256="0e4ede5cf8df009bff5aeb3a9f194852c03299ae5664b5a425b43358e7a9eef2")
    version("2.17.1-1", sha256="1311a6fd7cd44ad6d4523ba03065ce694605843fd30a5c0f77aa3d911abe706d")
    version("2.16.2-1", sha256="7f7c738511a8876403fc574d13d48e7c250d934d755598d82e14bab12236fc64")
    version("2.15.5-1", sha256="f4ac3c74d469c9cd718f82e1477759785db9b9f8cc9d9ecc103485805b8394a3")
    version("2.14.3-1", sha256="0fffb6f91e029ea4d95efabd7bddc6eecf8bf136e4f46bf812bff7d8eee53c79")
    version("2.13.4-1", sha256="d5f5243200d4e40683c56f04435bfd6defa379cb4f2b8c07b0f191df0f66c3d9")
    version("2.12.12-1", sha256="49b4fbfeebf1f62f6ceb69e72504045d8d1b4e7609e3c2477906f3004c7e2d82")
    version("2.12.10-1", sha256="7f53ed9f1af25bf5290e774d4fbe7a8fc71bcad34ab943602d36e4d0a8d30d16")
    version("2.12.7-1", sha256="928d02e61637128f53320a89088c9c2e597fe9d25548dfaf06238bf5a87420fd")
    version("2.11.4-1", sha256="db4e9a0277a64f9a31ea9b5eea22e63f10faaed36dded4587bbc8a0d8eceed10")
    version("2.10.3-1", sha256="55de166eb7dcab9ecef2629cdb5fb0c5ebec4fae03589c469ebe5dcb5716b3c5")
    version("2.9.9-1", sha256="01629a1bdadbadb2828e26023ba7685bbc07678468cb7df63cc96460f5337e08")
    version("2.9.8-1", sha256="f6e5d9c10e6e54ee21f9707d2df684083d0cccf87bd5a4dbc795803da2bc9f5a")
    version("2.9.6-1", sha256="c4b1f5a88f03c0ac8f1dcbe27723cd75cfe051754078d83629efaaed10ce8731")
    version("2.8.4-1", sha256="a5c1b4da6e1608ee63baa87f6df424bba7a8b1cedad597a25d5b4cf8d56d0865")
    version("2.8.3-1", sha256="3ae89ddb2956fff081e406a94ff54ae5e52359f5d645ce977c7eba09b3b782e6")
    version("2.7.8-1", sha256="fa2bec307270f30fcf6280a85f24ea8801e0ce3b3027937c7325260a890b07e0")
    version("2.7.6-1", sha256="60dd9b1743c2db6c05f60959edf98a4477f218115ef910d7ec2662f2fb5cf626")
    version("2.7.5-1", sha256="26a8dec6fa0a776eb71205d618d58e26d372621719788a23b33db6fdce4426bf")
    version("2.7.3-1", sha256="dc7b8794373306e323363314c3327796e416f745e8003490fc1407a22dd7acd6")
    version("2.6.4-1", sha256="ed8c9dfd40e013003923ae006787b1a30d3cb363b47d2e4307eaa2624ebba2ba")
    version("2.5.7-1", sha256="781a6bb2278566be4abbdf22b2fa19afc7306cff4b312c82bd782979b368014e")
    version("2.5.6-2", sha256="8a30e0b4813a825592872fcbeeede22a659e2c399074dcce02960591dc81387d")
    version("2.5.6-1", sha256="38a37d98be11f43232b988719226866b407f08b9666dcaf345796bd8f354ef54")
    version("2.4.8-1", sha256="e2260da448ebbebe437f74768a346d28c74eabdb92e372a3dc6652a626318924")
    version("2.4.6-1", sha256="ea4421061a7b9c454f2e088f68bfdbbcefab80ce81cafc70ee6c7742b1439591")
    version("2.4.2-1", sha256="e3dd04b22eb541394bd818e5f78ac23a09cc549690d5d55d6fccc1a36155385a")
    version("2.3.7-1", sha256="e6eff80d9d2db13c61f8452e1400ca2f098d2dfe42857cb23413ce081c5b9e9b")
    version("2.3.5-5", sha256="bac9950b4d3980c25baa8e3e4541d2dfb4d21edf32ad3b89022d04920357142f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", default=True, description="Build with CUDA")

    depends_on("rdma-core")

    # https://github.com/NVIDIA/nccl/issues/244
    patch("so_reuseport.patch", when="@2.3.7-1:2.4.8-1")

    conflicts("~cuda", msg="NCCL requires CUDA")
    conflicts(
        "cuda_arch=none",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.(\d+\.\d+\.\d+)", lib)
        return match.group(1) if match else None

    @property
    def build_targets(self):
        cuda_arch = self.spec.variants["cuda_arch"].value
        cuda_gencode = " ".join(self.cuda_flags(cuda_arch))

        return [
            "CUDA_HOME={0}".format(self.spec["cuda"].prefix),
            "NVCC_GENCODE={0}".format(cuda_gencode),
        ]

    @property
    def install_targets(self):
        if self.version >= Version("2.3.5-5"):
            return ["PREFIX={0}".format(self.prefix), "src.install"]
        else:
            return ["PREFIX={0}".format(self.prefix), "install"]
