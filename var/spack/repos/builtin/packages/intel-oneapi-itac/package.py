# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiItac(IntelOneApiPackage):
    """The Intel Trace Analyzer and Collector profiles and analyzes MPI applications to help
    focus your optimization efforts.

    Find temporal dependencies and bottlenecks in your code.
    Check the correctness of your application.
    Locate potential programming errors, buffer overlaps, and deadlocks.
    Visualize and understand parallel application behavior.
    Evaluate profiling statistics and load balancing.
    Analyze performance of subroutines or code blocks.
    Learn about communication patterns, parameters, and performance data.
    Identify communication hot spots.
    Decrease time to solution and increase application efficiency.

    """

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/trace-analyzer.html"

    maintainers("rscohn2")

    version(
        "2022.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/d75145c0-e3e2-4806-a2f8-8e46972ea2cb/l_itac_oneapi_p_2022.4.0.16_offline.sh",
        sha256="746a51d91be17e5916ec74d6b3691bf58c2820cc9a2920f104e6e96383505bbe",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/644eec67-83d9-4bdd-be0d-d90587ec72ed/l_itac_oneapi_p_2022.1.0.158_offline.sh",
        sha256="2a1f4be6b349d1629006ee72087b361a5f3e714bddd1ef932045d0c03c0b20e8",
        expand=False,
    )
    version(
        "2022.0.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/e83526f5-7e0f-4708-9e0d-47f1e65f29aa/l_itac_oneapi_p_2022.0.0.49690_offline.sh",
        sha256="6ab2888afcfc981273aed3df316463fbaf511faf83ee091ca79016459b03b79e",
        expand=False,
    )
    version(
        "2021.10.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/226adf12-b7f6-407e-95a9-8e9ab76d7631/l_itac_oneapi_p_2021.10.0.14_offline.sh",
        sha256="cfff2ee19c793b64074b5490a16acbe8c9767f41d391d7c71c0004fdcec501c7",
        expand=False,
    )
    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19129/l_itac_oneapi_p_2021.8.0.25341_offline.sh",
        sha256="9e943e07cbe7bcb2c6ec181cea5a2fd2241555bed695050f5069467fe7140c37",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19024/l_itac_oneapi_p_2021.7.1.15324_offline.sh",
        sha256="fb26689efdb7369e211b5cf05f3e30d491a2787f24fef174b23241b997cc442f",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18886/l_itac_oneapi_p_2021.7.0.8707_offline.sh",
        sha256="719faeccfb1478f28110b72b1558187590a6f44cce067158f407ab335a7395bd",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18694/l_itac_oneapi_p_2021.6.0.434_offline.sh",
        sha256="1ecc2735da960041b051e377cadb9f6ab2f44e8aa44d0f642529a56a3cbba436",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2022:"

    @property
    def component_dir(self):
        return "itac"
