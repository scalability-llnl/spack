# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiDpct(IntelOneApiPackage):
    """The Intel DPC++ Compatibility Tool assists in migrating your
    existing CUDA code to SYCL code. The tool ports both CUDA
    language kernels and library API calls. Typically, 90%-95% of
    CUDA code automatically migrates to SYCL code.

    """

    maintainers("rscohn2")

    homepage = "https://www.intel.com/content/www/us/en/developer/tools/oneapi/dpc-compatibility-tool.html#gs.2p8km6"

    version(
        "2024.2.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/e3b7b68d-65dd-4d03-9119-ce3ad448657e/l_dpcpp-ct_p_2024.2.1.64_offline.sh",
        sha256="87af24e0151bcde66c568f73156532a055569b349a7dbd34178344245a43ca1f",
        expand=False,
    )
    version(
        "2024.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/6b83dabd-75cf-4371-b4cd-91160175d5ff/l_dpcpp-ct_p_2024.2.0.424_offline.sh",
        sha256="43a6c5fa646291ea4f8ee94e2e711ee42bbd6aff7901bda1694e1ea99e6852e2",
        expand=False,
    )
    version(
        "2024.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/997fe522-cedf-46da-a54d-be4f22992fa1/l_dpcpp-ct_p_2024.1.0.378_offline.sh",
        sha256="f4855ef768b9067476f0e216140c65777e301c9b32be45d9e644d54b6dc21e1b",
        expand=False,
    )
    version(
        "2024.0.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/6633bc4b-5356-471a-9aae-d5e63e7acd95/l_dpcpp-ct_p_2024.0.0.49394_offline.sh",
        sha256="5fdba92edf24084187d98f083f9a6e17ee6b33ad8a736d6c9cdd3dbd4e0eab8a",
        expand=False,
    )
    version(
        "2023.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/764119eb-2959-4b51-bb3c-3cf581c16186/l_dpcpp-ct_p_2023.2.0.49333_offline.sh",
        sha256="3b4ca40c23a5114d4c5591694e4b43960bb55329455e86d8d876c3d5a366159b",
        expand=False,
    )
    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/a9d2cc2d-9c1c-4de3-b6da-94229bbe0bca/l_dpcpp-ct_p_2023.1.0.44450_offline.sh",
        sha256="8349d013afd5828ac53d3e47e8f7b3326401d791036b3003b0398ed41c916524",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19100/l_dpcpp-ct_p_2023.0.0.25483_offline.sh",
        sha256="81f392d16a10cbdb8e9d053f18566304a78e1be624280ad43ddbc0dfd767fc7f",
        expand=False,
    )
    version(
        "2022.2.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18991/l_dpcpp-ct_p_2022.2.1.14994_offline.sh",
        sha256="ea2fbe36de70eb3c78c97133f81e0b2a2fbcfc9525e77125a183d7af446ef3e6",
        expand=False,
    )
    version(
        "2022.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18908/l_dpcpp-ct_p_2022.2.0.8701_offline.sh",
        sha256="ca79b89ba4b97accb868578a1b7ba0e38dc5e4457d45c6c2552ba33d71b52128",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18746/l_dpcpp-ct_p_2022.1.0.172_offline.sh",
        sha256="ec42f4df3f9daf1af587b14b8b6644c773a0b270e03dd22ac9e2f49131e3e40c",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "dpcpp-ct"
