# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiCcl(IntelOneApiLibraryPackage):
    """The Intel oneAPI Collective Communications Library (oneCCL) enables
    developers and researchers to more quickly train newer and
    deeper models. This is done by using optimized communication
    patterns to distribute model training across multiple
    nodes. The library is designed for easy integration into deep
    learning frameworks, whether you are implementing them from
    scratch or customizing existing ones.

    """

    maintainers("rscohn2")

    # oneAPI Collective Communications Library
    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/oneccl.html"
    )

    depends_on("intel-oneapi-mpi")

    version(
        "2021.13.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/4b4cf672-c1f9-4bac-97c4-f4ae10a0a020/l_oneapi_ccl_p_2021.13.1.32_offline.sh",
        sha256="05027a00d3b97754c8ba4ec009901b95e11a88d32c1206ea464ac6ea8b5aa03b",
        expand=False,
    )
    version(
        "2021.13.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/2413acba-2216-4a35-9c74-82694a20d176/l_oneapi_ccl_p_2021.13.0.300_offline.sh",
        sha256="0cb848fb86b2eec6ed53910f961211c43bab628ada47e5b3d401bfff59942c02",
        expand=False,
    )
    version(
        "2021.12.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/cad4b3be-a272-4ed0-b67a-3871e495cb28/l_oneapi_ccl_p_2021.12.0.311_offline.sh",
        sha256="77b60a56d02c3700182370698b760cb17c66be700ca98bda1f30b39b9948e375",
        expand=False,
    )
    version(
        "2021.11.2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/7a2bbe23-9cf2-47a3-945f-fc160b9d868a/l_oneapi_ccl_p_2021.11.2.7_offline.sh",
        sha256="095be44ae21348ead46008844667a30da92a0afac305f722777c345394e50a14",
        expand=False,
    )
    version(
        "2021.11.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/07958f2f-8d95-422d-8c18-a4c7352b005c/l_oneapi_ccl_p_2021.11.1.9_offline.sh",
        sha256="35817d40f57c0d35b9bacf3935cedc1c82fc8d809513d82580561f63f31cac17",
        expand=False,
    )
    version(
        "2021.11.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/9e63eba5-2b3d-4032-ad22-21f02e35b518/l_oneapi_ccl_p_2021.11.0.49161_offline.sh",
        sha256="35fde9862d620c211064addfd3c15c4fc33bcaac6fe050163eb59a006fb9d476",
        expand=False,
    )
    version(
        "2021.10.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/3230823d-f799-4d1f-8ef3-a17f086a7719/l_oneapi_ccl_p_2021.10.0.49084_offline.sh",
        sha256="482b9a083c997df496309a40ef1293807fc0ce1c7c43ebe6be2acf568087544b",
        expand=False,
    )
    version(
        "2021.9.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/44e093fc-663b-4ae5-9c08-24a55211aca3/l_oneapi_ccl_p_2021.9.0.43543_offline.sh",
        sha256="9f8e457d97881f2aa96de1d80eff96de095dd9636892f7868db8493493fa63c4",
        expand=False,
    )
    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19135/l_oneapi_ccl_p_2021.8.0.25371_offline.sh",
        sha256="c660405fcc29bddd5bf9371b8e586c597664fb1ae59eb17cb02685cc662db82c",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19029/l_oneapi_ccl_p_2021.7.1.16948_offline.sh",
        sha256="daab05a0779db343b600253df8fea93ab0ed20bd630d89883dd651b6b540b1b2",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18891/l_oneapi_ccl_p_2021.7.0.8733_offline.sh",
        sha256="a0e64db03868081fe075afce8abf4cb94236effc6c52e5049118cfb2ef81a6c7",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18697/l_oneapi_ccl_p_2021.6.0.568.sh",
        sha256="e3c50c9cbeb350e8f28488b2e8fee54156116548db8010bb2c2443048715d3ea",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18472/l_oneapi_ccl_p_2021.5.1.494_offline.sh",
        sha256="237f45d3c43447460e36eb7d68ae3bf611aa282015e57c7fe06c2004d368a68e",
        expand=False,
    )
    version(
        "2021.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18371/l_oneapi_ccl_p_2021.5.0.478_offline.sh",
        sha256="47584ad0269fd13bcfbc2cd0bb029bdcc02b723070abcb3d5e57f9586f4e74f8",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18188/l_oneapi_ccl_p_2021.4.0.433_offline.sh",
        sha256="004031629d97ef99267d8ea962b666dc4be1560d7d32bd510f97bc81d9251ef6",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17920/l_oneapi_ccl_p_2021.3.0.343_offline.sh",
        sha256="0bb63e2077215cc161973b2e5029919c55e84aea7620ee9a848f6c2cc1245e3f",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17731/l_oneapi_ccl_p_2021.2.0.269_offline.sh",
        sha256="18b7875030243295b75471e235e91e5f7b4fc15caf18c07d941a6d47fba378d7",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17391/l_oneapi_ccl_p_2021.1.1.54_offline.sh",
        sha256="de732df57a03763a286106c8b885fd60e83d17906936a8897a384b874e773f49",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2021.11:"

    @property
    def component_dir(self):
        return "ccl"
