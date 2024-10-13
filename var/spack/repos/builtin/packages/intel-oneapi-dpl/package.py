# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiDpl(IntelOneApiLibraryPackage):
    """The Intel oneAPI DPC++ Library (oneDPL) is a companion to the Intel
    oneAPI DPC++/C++ Compiler and provides an alternative for C++
    developers who create heterogeneous applications and
    solutions. Its APIs are based on familiar standards-C++ STL,
    Parallel STL (PSTL), Boost.Compute, and SYCL*-to maximize
    productivity and performance across CPUs, GPUs, and FPGAs.

    """

    maintainers("rscohn2")

    homepage = "https://github.com/oneapi-src/oneDPL"

    version(
        "2022.6.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/fe007d71-c49f-4cdd-8a95-5c8e29c5b19c/l_oneDPL_p_2022.6.1.15_offline.sh",
        sha256="44eb3d12321e4fbf0bf8f78f47831ce4d5825cc041037ff919dca79db3354c7d",
        expand=False,
    )
    version(
        "2022.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/65565430-3eb6-49ad-ae51-e35314cc6f08/l_oneDPL_p_2022.6.0.560_offline.sh",
        sha256="540c79d2cea77c009fd7d49d65323418aded1235afd30d91192257a2f14a366f",
        expand=False,
    )
    version(
        "2022.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/d0be9e37-532e-4fde-9ac2-32c3ec5a2029/l_oneDPL_p_2022.5.0.219_offline.sh",
        sha256="41a96db8adc2de60f2e8dc8b01a6f93f39dad568a46ab1699f3b4200d0acf834",
        expand=False,
    )
    version(
        "2022.3.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/be027095-148a-4433-aff4-c6e8582da3ca/l_oneDPL_p_2022.3.0.49386_offline.sh",
        sha256="1e40c6562bc41fa5a46c80c09222bf12d36d8e82f749476d0a7e97503d4659df",
        expand=False,
    )
    version(
        "2022.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/44f88a97-7526-48f0-8515-9bf1356eb7bb/l_oneDPL_p_2022.2.0.49287_offline.sh",
        sha256="5f75e5c4e924b833a5b5d7a8cb812469d524a3ca4bda68c8ac850484dc0afd23",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/64075e93-4134-4d18-8941-827b71b7d8b9/l_oneDPL_p_2022.1.0.43490_offline.sh",
        sha256="a4e2f5ab9c3c88f7ad66817261f0ba19a8f534209999d6ceeeb083387f6eefd5",
        expand=False,
    )
    version(
        "2022.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19133/l_oneDPL_p_2022.0.0.25335_offline.sh",
        sha256="61fcdfe854393f90c43c01bff81bf917c1784bc1c128afdb0c8be2795455d3d2",
        expand=False,
    )
    version(
        "2021.7.2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19046/l_oneDPL_p_2021.7.2.15007_offline.sh",
        sha256="84d60a6b1978ff45d2c416f18ca7df542eaa8c0b18dc3abf4bb0824a91b4fc44",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18846/l_oneDPL_p_2021.7.1.8713_offline.sh",
        sha256="275c935427e3ad0eb995034b05ff2ffd13c55ee58069c3702aa383f68a1e5485",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18752/l_oneDPL_p_2021.7.0.631_offline.sh",
        sha256="1e2d735d5eccfe8058e18f96d733eda8de5b7a07d613447b7d483fd3f9cec600",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18372/l_oneDPL_p_2021.6.0.501_offline.sh",
        sha256="0225f133a6c38b36d08635986870284a958e5286c55ca4b56a4058bd736f8f4f",
        expand=False,
    )
    version(
        "2021.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18189/l_oneDPL_p_2021.5.0.445_offline.sh",
        sha256="7d4adf300a18f779c3ab517070c61dba10e3952287d5aef37c38f739e9041a68",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17889/l_oneDPL_p_2021.4.0.337_offline.sh",
        sha256="540ef0d308c4b0f13ea10168a90edd42a56dc0883024f6f1a678b94c10b5c170",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2022.3:"

    @property
    def component_dir(self):
        return "dpl"

    @property
    def headers(self):
        # This should match the directories added to CPATH by
        # env/vars.sh for the component
        if self.v2_layout:
            dirs = [self.component_prefix.include]
        else:
            dirs = [self.component_prefix.linux.include]

        return self.header_directories(dirs)
