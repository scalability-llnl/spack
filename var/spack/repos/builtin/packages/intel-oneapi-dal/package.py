# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiDal(IntelOneApiLibraryPackage):
    """Intel oneAPI Data Analytics Library (oneDAL) is a library that
    helps speed up big data analysis by providing highly optimized
    algorithmic building blocks for all stages of data analytics
    (preprocessing, transformation, analysis, modeling, validation,
    and decision making) in batch, online, and distributed
    processing modes of computation. The library optimizes data
    ingestion along with algorithmic computation to increase
    throughput and scalability.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onedal.html"
    )

    version(
        "2024.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/ed2c397a-9a78-4466-9179-b39b7da07e83/l_daal_oneapi_p_2024.7.0.14_offline.sh",
        sha256="aa7b072fe019ce253a111b38055f3949222d7be5231b4df2780a7ded16cd9097",
        expand=False,
    )
    version(
        "2024.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/1edf7074-80f8-4b97-aad3-5023b41b7ecd/l_daal_oneapi_p_2024.6.0.418_offline.sh",
        sha256="2e5966348df4dd70b2887512dca12ecc671de831a30ca21a23a28822c4d24f9f",
        expand=False,
    )
    version(
        "2024.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/6ca2d1a8-b7c7-4a70-9c38-2b437dacae1a/l_daal_oneapi_p_2024.5.0.284_offline.sh",
        sha256="65d437f8841fd4872e35708f3c989bc00022fe041e750e8c35dee010bd87db9d",
        expand=False,
    )
    version(
        "2024.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/3cee4c6c-b7d1-42ce-8bbb-d829a700952f/l_daal_oneapi_p_2024.2.0.280_offline.sh",
        sha256="921dbbf200096166d58ab5b8baeb93a8c85ad8a98cc43e178ae0c2f29af02212",
        expand=False,
    )
    version(
        "2024.0.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/37364086-b3cd-4a54-8736-7893732c1a86/l_daal_oneapi_p_2024.0.0.49569_offline.sh",
        sha256="45e71c7cbf38b04a34c47e36e2d86a48847f2f0485bafbc3445077a9ba3fa73c",
        expand=False,
    )
    version(
        "2023.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/fa218373-4b06-451f-8f4c-66b7d14b8e8b/l_daal_oneapi_p_2023.2.0.49574_offline.sh",
        sha256="643c6b5a9d06bc82b610257645cde116dc0473935a3b969850fa72c6cb952eaf",
        expand=False,
    )
    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/c209d29f-3d06-45fb-8f04-7b2f47b93a7c/l_daal_oneapi_p_2023.1.0.46349_offline.sh",
        sha256="5ed5c021a2d3c0e65702d0ae3e18010a85af18bdfbc534e783797d3b23c56801",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19122/l_daal_oneapi_p_2023.0.0.25395_offline.sh",
        sha256="83d0ca7501c882bf7e1f250e7310dafa6b6fd404858298ce9cde7546654d43bc",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19032/l_daal_oneapi_p_2021.7.1.16996_offline.sh",
        sha256="2328927480b0ba5d380028f981717b63ee323f8a1616a491a160a0a0b239e285",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18895/l_daal_oneapi_p_2021.7.0.8746_offline.sh",
        sha256="c18e68df120c2b1db17877cfcbb1b5c93a47b2f4756a3444c663d0f03be4eee3",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18698/l_daal_oneapi_p_2021.6.0.915_offline.sh",
        sha256="bc9a430f372a5f9603c19ec25207c83ffd9d59fe517599c734d465e32afc9790",
        expand=False,
    )
    version(
        "2021.5.3",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18480/l_daal_oneapi_p_2021.5.3.832_offline.sh",
        sha256="6d3503cf7be2908bbb7bd18e67b8f2e96ad9aec53d4813c9be620adaa2db390f",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18432/l_daal_oneapi_p_2021.5.1.803_offline.sh",
        sha256="bba7bee3caef14fbb54ad40615222e5da429496455edf7375f11fd84a72c87ba",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18218/l_daal_oneapi_p_2021.4.0.729_offline.sh",
        sha256="61da9d2a40c75edadff65d052fd84ef3db1da5d94f86ad3956979e6988549dda",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17905/l_daal_oneapi_p_2021.3.0.557_offline.sh",
        sha256="4c2e77a3a2fa5f8a09b7d68760dfca6c07f3949010836cd6da34075463467995",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17747/l_daal_oneapi_p_2021.2.0.358_offline.sh",
        sha256="cbf4e64dbd21c10179f2d1d7e8b8b0f12eeffe6921602df33276cd0ebd1f8e34",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17443/l_daal_oneapi_p_2021.1.1.79_offline.sh",
        sha256="6e0e24bba462e80f0fba5a46e95cf0cca6cf17948a7753f8e396ddedd637544e",
        expand=False,
    )

    depends_on("tbb")

    provides("daal")
    provides("onedal")

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "dal"

    @property
    def headers(self):
        # This should match the directories added to CPATH by
        # env/vars.sh for the component
        if self.v2_layout:
            dirs = [self.component_prefix.include, self.component_prefix.include.dal]
        else:
            dirs = [self.component_prefix.include]

        return self.header_directories(dirs)
