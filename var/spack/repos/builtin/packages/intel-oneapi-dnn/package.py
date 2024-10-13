# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiDnn(IntelOneApiLibraryPackage):
    """The Intel oneAPI Deep Neural Network Library (oneDNN) helps
    developers improve productivity and enhance the performance of
    their deep learning frameworks. It supports key data type
    formats, including 16 and 32-bit floating point, bfloat16, and
    8-bit integers and implements rich operators, including
    convolution, matrix multiplication, pooling, batch
    normalization, activation functions, recurrent neural network
    (RNN) cells, and long short-term memory (LSTM) cells.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onednn.html"
    )

    version(
        "2024.2.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/7c850be0-b17d-4b7f-898d-3bc5fc36aa8d/l_onednn_p_2024.2.1.76_offline.sh",
        sha256="86f143568529465d6e8b87763e645774f40ac3c38d7713088a597a3f941978bb",
        expand=False,
    )
    version(
        "2024.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/6f830f51-56cd-4ea6-ade7-0f066c9b1939/l_onednn_p_2024.2.0.571_offline.sh",
        sha256="9bc74f8e48758c0ce7dda4c9f8f961a26f48c25e5ad5335c6e7ecbd7ece38c97",
        expand=False,
    )
    version(
        "2024.1.1",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/5f6d82fa-2580-4bb1-83bb-cce7a52d1d34/l_onednn_p_2024.1.1.16_offline.sh",
        sha256="a67a387bc0d30a5ca1bd0ed3d551ed13df7dba7939b208fd0c81a24425e6e90a",
        expand=False,
    )
    version(
        "2024.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/759e8b2a-cbff-4b4f-ad88-08deb7730e73/l_onednn_p_2024.1.0.571_offline.sh",
        sha256="580cb133e08b522945172a396dec9c83dd6e951602c4f36a6c346b25ab2e48c5",
        expand=False,
    )
    version(
        "2024.0.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/dc309221-d210-4f3a-9406-d897df8deab8/l_onednn_p_2024.0.0.49548_offline.sh",
        sha256="17fbd5cc5d08de33625cf2879c0cceec53c91bbcd0b863e8f29d27885bac88c9",
        expand=False,
    )
    version(
        "2023.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/2d218b97-0175-4f8c-8dba-b528cec24d55/l_onednn_p_2023.2.0.49517_offline.sh",
        sha256="96bb92b1b072e1886151b2fc0e48f27a2dc378cd92bd3f428f5166b83ae41798",
        expand=False,
    )
    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/df0fd85e-f52a-437a-8d49-be12b560607c/l_onednn_p_2023.1.0.46343_offline.sh",
        sha256="0dfe16e7e81d0bf21b304e22f0cf9cb02cd4c10febddbcefea75bab2231a46d2",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19137/l_onednn_p_2023.0.0.25399_offline.sh",
        sha256="f974901132bf55ba11ce782747ba9443f38d67827bce3994775eeb86ed018869",
        expand=False,
    )
    version(
        "2022.2.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19035/l_onednn_p_2022.2.1.16994_offline.sh",
        sha256="2102964a36a5b58b529385706e6829456ee5225111c33dfce6326fff5175aace",
        expand=False,
    )
    version(
        "2022.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18933/l_onednn_p_2022.2.0.8750_offline.sh",
        sha256="920833cd1f05f2fdafb942c96946c3925eb734d4458d52f22f2cc755133cb9e0",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18725/l_onednn_p_2022.1.0.132_offline.sh",
        sha256="0b9a7efe8dd0f0b5132b353a8ee99226f75bae4bab188a453817263a0684cc93",
        expand=False,
    )
    version(
        "2022.0.2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18476/l_onednn_p_2022.0.2.43_offline.sh",
        sha256="a2a953542b4f632b51a2527d84bd76c3140a41c8085420da4237e2877c27c280",
        expand=False,
    )
    version(
        "2022.0.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18441/l_onednn_p_2022.0.1.26_offline.sh",
        sha256="8339806300d83d2629952e6e2f2758b52f517c072a20b7b7fc5642cf1e2a5410",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18221/l_onednn_p_2021.4.0.467_offline.sh",
        sha256="30cc601467f6a94b3d7e14f4639faf0b12fdf6d98df148b07acdb4dfdfb971db",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17923/l_onednn_p_2021.3.0.344_offline.sh",
        sha256="1521f6cbffcf9ce0c7b5dfcf1a2546a4a0c8d8abc99f3011709039aaa9e0859a",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17751/l_onednn_p_2021.2.0.228_offline.sh",
        sha256="62121a3355298211a124ff4e71c42fc172bf1061019be6c6120830a1a502aa88",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17385/l_onednn_p_2021.1.1.55_offline.sh",
        sha256="24002c57bb8931a74057a471a5859d275516c331fd8420bee4cae90989e77dc3",
        expand=False,
    )

    depends_on("tbb")

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "dnnl"

    def __target(self):
        if self.v2_layout:
            return self.component_prefix
        else:
            return self.component_prefix.cpu_dpcpp_gpu_dpcpp

    @property
    def headers(self):
        # This should match the directories added to CPATH by
        # env/vars.sh for the component
        if self.v2_layout:
            dirs = [self.component_prefix.include]
        else:
            dirs = [self.component_prefix.cpu_dpcpp_gpu_dpcpp.include]

        return self.header_directories(dirs)

    @property
    def libs(self):
        # libmkldnn was removed before 2024, but not sure when
        return find_libraries(["libdnnl", "libmkldnn"], self.__target().lib)
