# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiTbb(IntelOneApiLibraryPackage):
    """Intel oneAPI Threading Building Blocks (oneTBB) is a flexible
    performance library that simplifies the work of adding
    parallelism to complex applications across accelerated
    architectures, even if you are not a threading expert.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onetbb.html"
    )

    version(
        "2021.13.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/b9aad7b8-0a4c-4f95-a100-e0e2921d5777/l_tbb_oneapi_p_2021.13.1.15_offline.sh",
        sha256="cae21300e5e4e3bbb392b24db54246a103c1634296529617292be62e7b8505a4",
        expand=False,
    )
    version(
        "2021.13.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/d6b5327e-f2fd-4c90-966a-d7a0e1376686/l_tbb_oneapi_p_2021.13.0.629_offline.sh",
        sha256="f16586e5d8c479d05662359c95c6720445e95a21443f3979c9321d154947ca99",
        expand=False,
    )
    version(
        "2021.12.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/b31f6b79-10aa-4119-a437-48fe2775633b/l_tbb_oneapi_p_2021.12.0.499_offline.sh",
        sha256="13e981cb4d9d3f72058cc136f8cdedf6ba9af225ae317f91b59e2050b0d49e43",
        expand=False,
    )
    version(
        "2021.11.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/af3ad519-4c87-4534-87cb-5c7bda12754e/l_tbb_oneapi_p_2021.11.0.49527_offline.sh",
        sha256="dd878ee979d7b6da4eb973adfebf814d9d7eed86b875d31e3662d100b2fa0956",
        expand=False,
    )
    version(
        "2021.10.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/c95cd995-586b-4688-b7e8-2d4485a1b5bf/l_tbb_oneapi_p_2021.10.0.49543_offline.sh",
        sha256="a10d319e67b6904d6199f8294e970124a064d9948cf7e2b5ebab94499aadc6ca",
        expand=False,
    )
    version(
        "2021.9.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/7dcd261b-12fa-418a-b61b-b3dd4d597466/l_tbb_oneapi_p_2021.9.0.43484_offline.sh",
        sha256="77f7a256e0035d2d7b911a4b8b398f293991c7c8705ef6c94d48f4cfd760018d",
        expand=False,
    )
    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19143/l_tbb_oneapi_p_2021.8.0.25334_offline.sh",
        sha256="41074fcf6a33e41f9e8007609100e40c27f4e36b709b964835eff823e655486b",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19041/l_tbb_oneapi_p_2021.7.1.15005_offline.sh",
        sha256="f13a8e740d69347b5985c1be496a3259a86d64ec94933b3d26100dbc2f059fd4",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18901/l_tbb_oneapi_p_2021.7.0.8712_offline.sh",
        sha256="879bd2004b8e93bc12c53c43eab44cd843433e3da7a976baa8bf07a1069a87c5",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18728/l_tbb_oneapi_p_2021.6.0.835_offline.sh",
        sha256="e9ede40a3d7745de6d711d43818f820c8486ab544a45610a71118fbca20698e5",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18473/l_tbb_oneapi_p_2021.5.1.738_offline.sh",
        sha256="c154749f1f370e4cde11a0a7c80452d479e2dfa53ff2b1b97003d9c0d99c91e3",
        expand=False,
    )
    version(
        "2021.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18380/l_tbb_oneapi_p_2021.5.0.707_offline.sh",
        sha256="6ff7890a74a43ae02e0fa2d9c5533fce70a49dff8e73278b546a0995367fec5e",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18194/l_tbb_oneapi_p_2021.4.0.643_offline.sh",
        sha256="33332012ff8ffe7987b1a20bea794d76f7d8050ccff04fa6e1990974c336ee24",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17952/l_tbb_oneapi_p_2021.3.0.511_offline.sh",
        sha256="b83f5e018e3d262e42e9c96881845bbc09c3f036c265e65023422ca8e8637633",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17759/l_tbb_oneapi_p_2021.2.0.357_offline.sh",
        sha256="c1c3623c5bef547b30eac009e7a444611bf714c758d7472c114e9be9d5700eba",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17378/l_tbb_oneapi_p_2021.1.1.119_offline.sh",
        sha256="535290e3910a9d906a730b24af212afa231523cf13a668d480bade5f2a01b53b",
        expand=False,
    )

    provides("tbb")

    @property
    def component_dir(self):
        return "tbb"

    @property
    def v2_layout_versions(self):
        return "@2021.11:"

    @run_after("install")
    def fixup_prefix(self):
        # The motivation was to provide a more standard layout so tbb
        # would be more likely to work as a virtual dependence. I am
        # not sure if this mechanism is useful and it became a problem
        # for mpi so disabling for v2_layout.
        if self.v2_layout:
            return
        self.symlink_dir(self.component_prefix.include, self.prefix.include)
        self.symlink_dir(self.component_prefix.lib, self.prefix.lib)
