# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rocminfo(CMakePackage):
    """Radeon Open Compute (ROCm) Runtime rocminfo tool"""

    homepage = "https://github.com/ROCm/rocminfo"
    git = "https://github.com/ROCm/rocminfo.git"
    url = "https://github.com/ROCm/rocminfo/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")

    version("master", branch="master")
    version("6.2.1", sha256="ae6e08962535e76a81ed872cbd6bf6860c46fa6e4e4bc8f7849c8781359798d8")
    version("6.2.0", sha256="4d9a9051bda3355f8d2050e981435cd02528a04264a7f61162d685e7e1629f73")
    version("6.1.2", sha256="882ebe3db60b6290a81a98e0bac9b8923fbf83966f1706fd24484700b8213bcc")
    version("6.1.1", sha256="ef5e33ad3d0bae462d01e1528ffa9c83c587ccbf7ef5947e096e550480d83819")
    version("6.1.0", sha256="973352210fdc65932f0125e2db68729383727eaf4ebb7f52c88a948c14bbbb73")
    version("6.0.2", sha256="e616d364a48de18eaee661bdce999d095086905f49777663ca99312f40a63da1")
    version("6.0.0", sha256="bc29f1798644b6dea73895353dffada9db7366d0058274e587ebd3291a4d3844")
    version("5.7.1", sha256="642dc2ec4254b3c30c43064e6690861486db820b25f4906ec78bdb47e68dcd0b")
    version("5.7.0", sha256="a5a3c19513bf26f17f163a03ba5288c5c761619ef55f0cb9e15472771748b93e")
    version("5.6.1", sha256="780b186ac7410a503eca1060f4bbc35db1b7b4d1d714d15c7534cd26d8af7b54")
    version("5.6.0", sha256="87d98a736e4f7510d1475d35717842068d826096a0af7c15a395bcf9d36d7fa0")
    version("5.5.1", sha256="bcab27bb3595d5a4c981e2416458d169e85c27e603c22e743d9240473bfbe98a")
    version("5.5.0", sha256="b6107d362b70e20a10911741eb44247139b4eb43489f7fa648daff880b6de37f")
    with default_args(deprecated=True):
        version("5.4.3", sha256="72159eed31f8deee0df9228b9e306a18fe9efdd4d6c0eead871cad4617874170")
        version("5.4.0", sha256="79123b92992cce75ae679caf9a6bf57b16d24e96e54b36eb002511f3800e29c6")
        version("5.3.3", sha256="77e6adc81da6c1d153517e1d28db774205531a2ec188e6518f998328ef7897c6")
        version("5.3.0", sha256="c279da1d946771d120611b64974fde751534e787a394ceb6b8e0b743c143d782")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3:", type="build")

    for ver in [
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
        "master",
    ]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")

    for ver in [
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    def cmake_args(self):
        return [self.define("ROCM_DIR", self.spec["hsa-rocr-dev"].prefix)]
