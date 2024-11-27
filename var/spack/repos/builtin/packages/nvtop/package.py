# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvtop(CMakePackage, CudaPackage):
    """Nvtop stands for Neat Videocard TOP, a (h)top like task monitor
    for AMD and NVIDIA GPUS. It can handle multiple GPUs and print
    information about them in a htop familiar way"""

    homepage = "https://github.com/Syllo/nvtop"
    url = "https://github.com/Syllo/nvtop/archive/refs/tags/3.0.1.zip"

    maintainers("marcost2")

    license("GPL-3.0-or-later")

    version("3.0.1", sha256="3cb6df2390e29792ed90de54c9332ec25e9d960abddcbb92d8544d658da2b5b3")
    version("3.0.0", sha256="711f1a1ef51ed3f7b1d61c858c4ac1fabb244595cf7b2403f80efcabe81d889e")
    version("2.0.4", sha256="5dc96057597343c66ebe46ae1a5415749ffbfafde99358eea6b533d6fee232e8")
    version("2.0.3", sha256="d5fb13bf0bfe2d18fbb6e073020c346e4778c1183293d9ceee1468d900fc297e")
    version("2.0.2", sha256="9a85c083e45be0a2d3e2135ce8df5a97340388fa7c72f086571826d501fec1de")
    version("2.0.1", sha256="ef18ce85d632eb1c22d3a3653976b2c088260039702df39fd0181f7cd3ae277d")
    version("2.0.0", sha256="1651f34274c334a682f280dcb2f28d9642d44c7b22afe8c431cab91345b50f31")
    version("1.2.2", sha256="543cbfdae3241fab1ea022402734c12e69d5988583193adaab69fdfae6e14c84")
    version("1.2.1", sha256="197992cdd0e2e151fce91a7ba56f717e4d85b317c396001e8dbd84dc2ba363cd")

    variant(
        "support",
        values=("nvidia", "amd", "intel"),
        default="nvidia,amd,intel",
        multi=True,
        description="Which GPU vendors to build support for",
    )

    depends_on("ncurses")
    depends_on("libdrm", when="support=amd")

    def cmake_args(self):
        return [
            self.define("NVIDIA_SUPPORT", self.spec.satisfies("support=nvidia")),
            self.define("AMDGPU_SUPPORT", self.spec.satisfies("support=amd")),
            self.define("INTEL_SUPPORT", self.spec.satisfies("support=intel")),
        ]
