# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtQuick3d(QtPackage):
    """A new module and API for defining 3D content in Qt Quick."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    license("BSD-3-Clause")

    version("6.7.3", sha256="3e68f3a9a330e7b9a92ddf5b8d7a0874a107ea77636c788f598de65e327eb4a0")
    version("6.7.2", sha256="67021658cb10bfa6d969c4219d599ab2f4775d08fb4ae56da17fbec305088b55")
    version("6.7.1", sha256="c889b70305da7595df87c3bd062474787b722ab216bc2e6226e33fae3ec3459d")
    version("6.7.0", sha256="3adb7cc458c21a4642e7138cc0ca12934cd7075633d06c46c689f65718c8ba73")
    version("6.6.3", sha256="6990aac1434722cdf54fa6b3ebbae6d2af4d4dc89d6d33a2146c83c49be59ecb")
    version("6.6.2", sha256="b99184a1ef912219374b2bb9a9b1899c1c55694736bc3185e2306db16c66b4ab")
    version("6.6.1", sha256="57abc6e178d2b28cfac544c71cb20f362409267be5422ca3fbaa46a1bbfd5515")
    version("6.6.0", sha256="2cda12649cfb6c23261c48e626714ca7eb01fa4b20e0bed02031f9c488c820ad")
    version("6.5.3", sha256="5df7494824c44fc73c03348b218166db5c4d8d42bd7d221f15e58c962cf657e5")
    version("6.5.2", sha256="7b40e578fc1ee2a5f5c413873fdb0552bb97829b70296ba3c6844da062608a7e")
    version("6.5.1", sha256="2b4f65f6c616302b38656f287e9acdf5a9f0e220ef79eaa2e80946780898fa51")
    version("6.5.0", sha256="eaf41f06450b2be50f16b39ec06c06d10dd337b7516aba1d95695b326fd9ef40")
    version("6.4.3", sha256="609f37efb97c9ef893630b5d29f1ad98a51a47700e260c604931285ac8521479")
    version("6.4.2", sha256="940145615fe3c4c8fb346c5bfc10f94fc7a4005c8c187886e0f3088ea0ce0778")
    version("6.4.1", sha256="67daeed69b9e7b3da516c6205e737fdba30a267978c1fb9d34723a6dc5588585")
    version("6.4.0", sha256="37987536da151b7c2cddabfde734759ebe6173708d32cb85aa008e151751270e")
    version("6.3.2", sha256="a3ec81393f1cd45eb18ee3d47582998679eef141b856bdd2baa2d41f019a0eea")
    version("6.3.1", sha256="79f0813ff776dc2aa07a8513ecd9d550dd8d449dc8fcd834fb0c9b22ea4a1893")
    version("6.3.0", sha256="413dec87828155ea0c0424e6b40c777bf0710f1ffaf98969c5d8b19ad3992823")
    version("6.2.4", sha256="7292ed4373a92913c6811f2faa5191f0426f84bd93a3f6eb7d54b62626b56db5")
    version("6.2.3", sha256="35d06edbdd83b7d781b70e0bada18911fa9b774b6403589d5b21813a73584d80")

    depends_on("cxx", type="build")  # generated

    depends_on("qt-base +network", when="@6.3.0:")

    depends_on("assimp@5.0.1:")
    depends_on("embree", when="@6.4:")

    vendor_deps_to_remove = ["assimp", "embree"]

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-declarative@" + v, when="@" + v)
        depends_on("qt-quicktimeline@" + v, when="@" + v)

    def cmake_args(self):
        args = super().cmake_args() + [
            self.define("FEATURE_quick3d_assimp", True),
            self.define("FEATURE_system_assimp", True),
        ]
        return args
