# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmBandwidthTest(CMakePackage):
    """Test to measure PciE bandwidth on ROCm platforms"""

    homepage = "https://github.com/ROCm/rocm_bandwidth_test"
    git = "https://github.com/ROCm/rocm_bandwidth_test.git"
    url = "https://github.com/ROCm/rocm_bandwidth_test/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    version("master", branch="master")
    version("6.2.1", sha256="042cfe3adc0f0ad0b8620e361b2846eb57c7b54837ed7a8c3a773e6fdc4e1af4")
    version("6.2.0", sha256="ca4caa4470c7ad0f1a4963072c1a25b0fd243844a72b26c83fcbca1e82091a41")
    version("6.1.2", sha256="4259d53350d6731613d36c03593750547f84f084569f8017783947486b8189da")
    version("6.1.1", sha256="01da756228f2bfb5e25ddb74b75a5939693b1b4f4559f37cfc85729e36a98450")
    version("6.1.0", sha256="b06522efbd1a55247412c8f535321058e2463eab4abd25505c37e8c67941ae26")
    version("6.0.2", sha256="af95fe84729701184aeb14917cee0d8d77ab1858ddcced01eb7380401e2134ae")
    version("6.0.0", sha256="9023401bd6a896059545b8e6263c6730afd89d7d45c0f5866261c300415532a6")
    version("5.7.1", sha256="7426ef1e317b8293e4d6389673cfa8c63efb3f7d061e2f50a6f0b1b706e2a2a7")
    version("5.7.0", sha256="fa95c28488ab4bb6d920b9f3c316554ca340f44c87ec2efb4cf8fa488e63ddd9")
    version("5.6.1", sha256="849af715d08dfd89e7aa5e4453b624151db1cafaa567ab5fa36a77948b90bf0d")
    version("5.6.0", sha256="ae2f7263a21a3a650068f43e3112b2b765eea80a5af2297572f850c77f83c85e")
    version("5.5.1", sha256="768b3da49fe7d4bb4e6536a8ee15be9f5e865d961e813ed4a407f32402685e1f")
    version("5.5.0", sha256="1070ce14d45f34c2c6b2fb003184f3ae735ccfd640e9df1c228988b2a5a82949")
    with default_args(deprecated=True):
        version("5.4.3", sha256="a2f5a75bf47db1e39a4626a9f5cd2d120bcafe56b1baf2455d794f7a4734993e")
        version("5.4.0", sha256="47a1ef92e565d5ce7a167cc1ebe3d4198cc04d598b259426245b8c11eb795677")
        version("5.3.3", sha256="2bc079297e639d45d57c8017f6f47bc44d4ed34613ec76c80574bb703d79b498")
        version("5.3.0", sha256="a97365c04d79663db7c85027c63a12d56356abc0a351697f49c2d82bf9ef8999")

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
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")

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

    build_targets = ["package"]
