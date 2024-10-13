# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiIppcp(IntelOneApiLibraryPackage):
    """Intel Integrated Performance Primitives (Intel IPP) is an extensive
    library of ready-to-use, domain-specific functions that are
    highly optimized for diverse Intel architectures. These
    functions take advantage of Single Instruction, Multiple Data
    (SIMD) instructions and improve the performance of
    computation-intensive applications, including signal
    processing, data compression, video processing, and
    cryptography. The intel-oneapi-ippcp package contains support
    for cryptography and everything else can be found in the
    intel-oneapi-ipp package.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/ipp.html"
    )

    version(
        "2021.12.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/8d82c537-2756-4000-a6cf-d7fedbfb9499/l_ippcp_oneapi_p_2021.12.1.14_offline.sh",
        sha256="d83dc57a2471579297dd3a303b93c50c6be37c0f7aaac80d0fc34dda90e4750a",
        expand=False,
    )
    version(
        "2021.12.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/16cce450-2d08-474f-a783-da6061bd8de9/l_ippcp_oneapi_p_2021.12.0.472_offline.sh",
        sha256="4a27c6209481b7f4b52f75660c243f0fc9884c18bda34fe8bf8493b9cfb00daa",
        expand=False,
    )
    version(
        "2021.11.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/a28fefdf-f67e-43a9-8e42-fcccd9da1fff/l_ippcp_oneapi_p_2021.11.0.37_offline.sh",
        sha256="58c2cee4bacb6a706173e0e59153f96d6686b35b7f124638a7b66c08674226ee",
        expand=False,
    )
    version(
        "2021.9.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/6792a758-2d69-4ff3-ad24-233fb3bf56e4/l_ippcp_oneapi_p_2021.9.0.533_offline.sh",
        sha256="5eca6fd18d9117f8cb7c599cee418b9cc3d7d5d5404f1350d47289095b6a1254",
        expand=False,
    )
    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/f488397a-bd8f-449f-9127-04de8426aa35/l_ippcp_oneapi_p_2021.8.0.49493_offline.sh",
        sha256="ac380d98dc9a12007f11537a1a57a848d4ccb251c4773608b088cf677e72c6d8",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/3697d9d0-907f-40d4-a2a7-7d83c45b72cb/l_ippcp_oneapi_p_2021.7.0.43492_offline.sh",
        sha256="2efc961a2beab091ce8f9b1b06792d85ea00778e36c773b0d8efcffb3dec7b49",
        expand=False,
    )
    version(
        "2021.6.3",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19108/l_ippcp_oneapi_p_2021.6.3.25343_offline.sh",
        sha256="82e7f577a73af8c168a28029019f85136617ac762438e77d21647a70dec74baf",
        expand=False,
    )
    version(
        "2021.6.2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18999/l_ippcp_oneapi_p_2021.6.2.15006_offline.sh",
        sha256="3c285c12da98a4d16e9a5ba237c8c51780475af54b1d1162185480ac891f16ee",
        expand=False,
    )
    version(
        "2021.6.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18923/l_ippcp_oneapi_p_2021.6.1.8714_offline.sh",
        sha256="a83c2e74f78ea00aae877259df38baab31e78bc04c0a387a1de36fff712eb225",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18709/l_ippcp_oneapi_p_2021.6.0.536_offline.sh",
        sha256="dac90862b408a6418f3782a5c4bf940939b1307ff4841ecfc6a29322976a2d43",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18470/l_ippcp_oneapi_p_2021.5.1.462_offline.sh",
        sha256="7ec058abbc1cdfd240320228d6426c65e5a855fd3a27e11fbd1ad2523f64812a",
        expand=False,
    )
    version(
        "2021.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18364/l_ippcp_oneapi_p_2021.5.0.445_offline.sh",
        sha256="e71aee288cc970b9c9fe21f7d5c300dbc2a4ea0687c7028f200d6b87e6c895a1",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18187/l_ippcp_oneapi_p_2021.4.0.401_offline.sh",
        sha256="2ca2320f733ee75b4a27865185a1b0730879fe2c47596e570b1bd50d0b8ac608",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17886/l_ippcp_oneapi_p_2021.3.0.315_offline.sh",
        sha256="0214d132d8e64b02e9cc63182e2099fb9caebf8c240fb1629ae898c2e1f72fb9",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17684/l_ippcp_oneapi_p_2021.2.0.231_offline.sh",
        sha256="64cd5924b42f924b6a8128a8bf8e686f5dc52b98f586ffac6c2e2f1585e3aba9",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17415/l_ippcp_oneapi_p_2021.1.1.54_offline.sh",
        sha256="c0967afae22c7a223ec42542bcc702121064cd3d8f680eff36169c94f964a936",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2021.9:"

    @property
    def component_dir(self):
        return "ippcp"
