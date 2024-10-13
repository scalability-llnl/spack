# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiAdvisor(IntelOneApiLibraryPackageWithSdk):
    """Intel Advisor is a design and analysis tool for developing
    performant code. The tool supports C, C++, Fortran, SYCL, OpenMP,
    OpenCL code, and Python. It helps with the following: Performant
    CPU Code: Design your application for efficient threading,
    vectorization, and memory use. Efficient GPU Offload: Identify
    parts of the code that can be profitably offloaded. Optimize the
    code for compute and memory.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/advisor.html"
    )

    version(
        "2024.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/e36c14f6-6142-44ff-b498-d4ff169cc8b0/l_oneapi_advisor_p_2024.3.0.43_offline.sh",
        sha256="6d230a0d11b972c4c677e041a6077216de79037376f5776b3b291113e25335be",
        expand=False,
    )
    version(
        "2024.2.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/65f69c5c-b41f-4688-8a41-ece8f2bbbb5a/l_oneapi_advisor_p_2024.2.1.44_offline.sh",
        sha256="2ef23dac756dc41bd7021297d3f3248968d7a0e29372e6b19b8752eb8d2e6a61",
        expand=False,
    )
    version(
        "2024.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/a4c8046c-6abf-4f53-a33c-4a587cd80fc1/l_oneapi_advisor_p_2024.2.0.683_offline.sh",
        sha256="8a6a8ced2456ea7c538aad01b4e6e0bd41244bcb438f76d4b87af5f63f94a733",
        expand=False,
    )
    version(
        "2024.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/414cea14-4f3c-45f0-b854-44fb6cf9f34b/l_oneapi_advisor_p_2024.1.0.500_offline.sh",
        sha256="1c327777a34a7e70e5840b9555ebf44615bf0295fcf3c673576d36a9a8979090",
        expand=False,
    )
    version(
        "2024.0.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/2d6b30ed-c7ea-4ad1-b138-91614f8242e8/l_oneapi_advisor_p_2024.0.1.17_offline.sh",
        sha256="3b34ff2b13737c7e0b7b97ee9544cf0718feab80f2a8e7728e4149e66d09a14a",
        expand=False,
    )
    version(
        "2024.0.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/88c5bdaa-7a2d-491f-9871-7170fadc3d52/l_oneapi_advisor_p_2024.0.0.49522_offline.sh",
        sha256="0ef3cf39c2fbb39371ac2470dad7d0d8cc0a2709c4f78dcab58d115b446c81c4",
        expand=False,
    )
    version(
        "2023.2.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/0b0e8bf2-30e4-4a26-b1ef-e369b0181b35/l_oneapi_advisor_p_2023.2.0.49489_offline.sh",
        sha256="48ab7fa2b828a273d467c8f07efd64d6cf2fcdcfe0ff567bd1d1be7a5d5d8539",
        expand=False,
    )
    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/a1ef7661-8921-4f19-ba40-2901231439f4/l_oneapi_advisor_p_2023.1.0.43480_offline.sh",
        sha256="64788f6f4cbe23a2123dcd01d91de9154dcb2b83390bb18da6e0f2928575855e",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19094/l_oneapi_advisor_p_2023.0.0.25338_offline.sh",
        sha256="5d8ef163f70ee3dc42b13642f321d974f49915d55914ba1ca9177ed29b100b9d",
        expand=False,
    )
    version(
        "2022.3.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18985/l_oneapi_advisor_p_2022.3.1.15323_offline.sh",
        sha256="f05b58c2f13972b3ac979e4796bcc12a234b1e077400b5d00fc5df46cd228899",
        expand=False,
    )
    version(
        "2022.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18872/l_oneapi_advisor_p_2022.3.0.8704_offline.sh",
        sha256="ae1e542e6030b04f70f3b9831b5e92def97ce4692c974da44e7e9d802f25dfa7",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18730/l_oneapi_advisor_p_2022.1.0.171_offline.sh",
        sha256="b627dbfefa779b44e7ab40dfa37614e56caa6e245feaed402d51826e6a7cb73b",
        expand=False,
    )
    version(
        "2022.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18369/l_oneapi_advisor_p_2022.0.0.92_offline.sh",
        sha256="f1c4317c2222c56fb2e292513f7eec7ec27eb1049d3600cb975bc08ed1477993",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18220/l_oneapi_advisor_p_2021.4.0.389_offline.sh",
        sha256="dd948f7312629d9975e12a57664f736b8e011de948771b4c05ad444438532be8",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "advisor"
