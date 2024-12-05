# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelParallelStudio(IntelPackage):
    """This is an earlier version of Intel parallel software development
    tools and has now been replaced by the Intel oneAPI Toolkits.

    """

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    maintainers("rscohn2")

    depends_on("patchelf", type="build")

    # As of 2016, the product comes in three "editions" that vary by scope.
    #
    # In Spack, select the edition via the version number in the spec, e.g.:
    #   intel-parallel-studio@cluster.2018

    # NB: When updating the version numbers here, please also update them
    # in the 'intel' package.

    # Cluster Edition (top tier; all components included)
    version(
        "cluster.2020.4",
        sha256="f36e49da97b6ce24d2d464d73d7ff49d71cff20e1698c20e607919819602a9f5",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/17113/parallel_studio_xe_2020_update4_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2020.2",
        sha256="4795c44374e8988b91da20ac8f13022d7d773461def4a26ca210a8694f69f133",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16744/parallel_studio_xe_2020_update2_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2020.1",
        sha256="fd11d8de72b2bd60474f8bce7b463e4cbb2255969b9eaf24f689575aa2a2abab",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16526/parallel_studio_xe_2020_update1_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2020.0",
        sha256="573b1d20707d68ce85b70934cfad15b5ad9cc14124a261c17ddd7717ba842c64",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16225/parallel_studio_xe_2020_cluster_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "cluster.2019.5",
        sha256="c03421de616bd4e640ed25ce4103ec9c5c85768a940a5cb5bd1e97b45be33904",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15809/parallel_studio_xe_2019_update5_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2019.4",
        sha256="32aee12de3b5ca14caf7578313c06b205795c67620f4a9606ea45696ee3b3d9e",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15533/parallel_studio_xe_2019_update4_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2019.3",
        sha256="b5b022366d6d1a98dbb63b60221c62bc951c9819653ad6f5142192e89f78cf63",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15268/parallel_studio_xe_2019_update3_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2019.2",
        sha256="8c526bdd95d1da454e5cada00f7a2353089b86d0c9df2088ca7f842fe3ff4cae",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15088/parallel_studio_xe_2019_update2_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2019.1",
        sha256="3a1eb39f15615f7a2688426b9835e5e841e0c030f21dcfc899fe23e09bd2c645",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/14850/parallel_studio_xe_2019_update1_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2019.0",
        sha256="1096dd4139bdd4b3abbda69a17d1e229a606759f793f5b0ba0d39623928ee4a1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13589/parallel_studio_xe_2019_cluster_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "cluster.2018.4",
        sha256="210a5904a860e11b861720e68416f91fd47a459e4500976853291fa8b0478566",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13717/parallel_studio_xe_2018_update4_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2018.3",
        sha256="23c64b88cea5056eaeef7b4ae0f4c6a86485c97f5e41d6c8419cb00aa4929287",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12998/parallel_studio_xe_2018_update3_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2018.2",
        sha256="550bc4758f7dd70e75830d329947532ad8b7cbb85225b8ec6db7e78a3f1d6d84",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12717/parallel_studio_xe_2018_update2_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2018.1",
        sha256="f7a94e83248d2641eb7ae2c1abf681067203a5b4372619e039861b468744774c",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12374/parallel_studio_xe_2018_update1_cluster_edition.tgz",
        deprecated=True,
    )
    version(
        "cluster.2018.0",
        sha256="526e5e71c420dc9b557b0bae2a81abb33eedb9b6a28ac94996ccbcf71cf53774",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12058/parallel_studio_xe_2018_cluster_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "cluster.2017.7",
        sha256="133c3aa99841a4fe48149938a90f971467452a82f033be10cd9464ba810f6360",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12856/parallel_studio_xe_2017_update7.tgz",
        deprecated=True,
    )
    version(
        "cluster.2017.6",
        sha256="d771b00d3658934c424f294170125dc58ae9b03639aa898a2f115d7a7482dd3a",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12534/parallel_studio_xe_2017_update6.tgz",
        deprecated=True,
    )
    version(
        "cluster.2017.5",
        sha256="36e496d1d1d7d7168cc3ba8f5bca9b52022339f30b62a87ed064b77a5cbccc09",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12138/parallel_studio_xe_2017_update5.tgz",
        deprecated=True,
    )
    version(
        "cluster.2017.4",
        sha256="27d34625adfc635d767c136b5417a372f322fabe6701b651d858a8fe06d07f2d",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11537/parallel_studio_xe_2017_update4.tgz",
        deprecated=True,
    )
    version(
        "cluster.2017.3",
        sha256="856950c0493de3e8b4150e18f8821675c1cf75c2eea5ff0804f59eb301414bbe",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11460/parallel_studio_xe_2017_update3.tgz",
        deprecated=True,
    )
    version(
        "cluster.2017.2",
        sha256="83a655f0c2969409758488d70d6719fb5ea81a84b6da3feb641ce67bb240bc8a",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11298/parallel_studio_xe_2017_update2.tgz",
        deprecated=True,
    )
    version(
        "cluster.2017.1",
        sha256="c808be744c98f7471c61258144859e8e8fc92771934281a16135803e941fd9b0",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/10973/parallel_studio_xe_2017_update1.tgz",
        deprecated=True,
    )
    version(
        "cluster.2017.0",
        sha256="f380a56a25cf17941eb691a640035e79f92516346500e0df80fbdd46c5c1b301",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9651/parallel_studio_xe_2017.tgz",
        deprecated=True,
    )
    #
    version(
        "cluster.2016.4",
        sha256="ea43c150ed6f9967bc781fe4253169a0447c69bac4fe2c563016a1ad2875ae23",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9781/parallel_studio_xe_2016_update4.tgz",
        deprecated=True,
    )
    version(
        "cluster.2016.3",
        sha256="aa7c6f1a6603fae07c2b01409c12de0811aa5947eaa71dfb1fe9898076c2773e",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9061/parallel_studio_xe_2016_update3.tgz",
        deprecated=True,
    )
    version(
        "cluster.2016.2",
        sha256="280bf39c75d7f52f206759ca4d8b6334ab92d5970957b90f5aa286bb0aa8d65e",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8676/parallel_studio_xe_2016_update2.tgz",
        deprecated=True,
    )
    version(
        "cluster.2016.1",
        sha256="f5a3ab9fb581e19bf1bd966f7d40a11905e002a2bfae1c4a2140544288ca3e48",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8365/parallel_studio_xe_2016_update1.tgz",
        deprecated=True,
    )
    version(
        "cluster.2016.0",
        sha256="fd4c32352fd78fc919601bedac5658ad5ac48efbc5700d9a8d42ed7d53bd8bb7",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/7997/parallel_studio_xe_2016.tgz",
        deprecated=True,
    )
    #
    version(
        "cluster.2015.6",
        sha256="e604ed2bb45d227b151dd2898f3edd93526d58d1db1cb9d6b6f614907864f392",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8469/parallel_studio_xe_2015_update6.tgz",
        deprecated=True,
    )
    version(
        "cluster.2015.1",
        sha256="84fdf48d1de20e1d580ba5d419a5bc1c55d217a4f5dc1807190ecffe0229a62b",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/4992/parallel_studio_xe_2015_update1.tgz",
        deprecated=True,
    )

    # Professional Edition (middle tier; excluded: MPI/TAC/Cluster Checker)
    #
    # NB: Pre-2018 download packages for Professional are the same as for
    # Cluster; differences manifest only in the tokens present in the license
    # file delivered as part of the purchase.
    version(
        "professional.2020.4",
        sha256="f9679a40c63575191385837f4f1bdafbcfd3736f09ac51d0761248b9ca9cc9e6",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/17114/parallel_studio_xe_2020_update4_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2020.2",
        sha256="96f9bca551a43e09d9648e8cba357739a759423adb671d1aa5973b7a930370c5",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16756/parallel_studio_xe_2020_update2_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2020.1",
        sha256="5b547be92ecf50cb338b3038a565f5609135b27aa98a8b7964879eb2331eb29a",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16527/parallel_studio_xe_2020_update1_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2020.0",
        sha256="e88cad18d28da50ed9cb87b12adccf13efd91bf94731dc33290481306c6f15ac",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16226/parallel_studio_xe_2020_professional_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "professional.2019.5",
        sha256="0ec638330214539361f8632e20759f385a5a78013dcc980ee93743d86d354452",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15810/parallel_studio_xe_2019_update5_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2019.4",
        sha256="9b2818ea5739ade100841e99ce79ef7f4049a2513beb2ce20fc94706f1ba0231",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15534/parallel_studio_xe_2019_update4_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2019.3",
        sha256="92a8879106d0bdf1ecf4670cd97fbcdc67d78b13bdf484f2c516a533aa7a27f9",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15269/parallel_studio_xe_2019_update3_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2019.2",
        sha256="cdb629d74612d135ca197f1f64e6a081e31df68cda92346a29e1223bb06e64ea",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15089/parallel_studio_xe_2019_update2_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2019.1",
        sha256="bc83ef5a728903359ae11a2b90ad7dae4ae61194afb28bb5bb419f6a6aea225d",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/14825/parallel_studio_xe_2019_update1_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2019.0",
        sha256="94b9714e353e5c4f58d38cb236e2f8911cbef31c4b42a148d60c988e926411e2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13578/parallel_studio_xe_2019_professional_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "professional.2018.4",
        sha256="54ab4320da849108602096fa7a34aa21751068467e0d1584aa8f16352b77d323",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13718/parallel_studio_xe_2018_update4_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2018.3",
        sha256="3d8e72ccad31f243e43b72a925ad4a6908e2955682433898640ab783decf9960",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12999/parallel_studio_xe_2018_update3_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2018.2",
        sha256="fc577b29fb2c687441d4faea14a6fb6da529fc78fcb778cbface59f40e128e02",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12718/parallel_studio_xe_2018_update2_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2018.1",
        sha256="dd3e118069d87eebb614336732323b48172c8c8a653cde673a8ef02f7358e94d",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12375/parallel_studio_xe_2018_update1_professional_edition.tgz",
        deprecated=True,
    )
    version(
        "professional.2018.0",
        sha256="72308ffa088391ea65726a79d7a73738206fbb1d8ed8563e3d06eab3120fb1a0",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12062/parallel_studio_xe_2018_professional_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "professional.2017.7",
        sha256="133c3aa99841a4fe48149938a90f971467452a82f033be10cd9464ba810f6360",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12856/parallel_studio_xe_2017_update7.tgz",
        deprecated=True,
    )
    version(
        "professional.2017.6",
        sha256="d771b00d3658934c424f294170125dc58ae9b03639aa898a2f115d7a7482dd3a",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12534/parallel_studio_xe_2017_update6.tgz",
        deprecated=True,
    )
    version(
        "professional.2017.5",
        sha256="36e496d1d1d7d7168cc3ba8f5bca9b52022339f30b62a87ed064b77a5cbccc09",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12138/parallel_studio_xe_2017_update5.tgz",
        deprecated=True,
    )
    version(
        "professional.2017.4",
        sha256="27d34625adfc635d767c136b5417a372f322fabe6701b651d858a8fe06d07f2d",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11537/parallel_studio_xe_2017_update4.tgz",
        deprecated=True,
    )
    version(
        "professional.2017.3",
        sha256="856950c0493de3e8b4150e18f8821675c1cf75c2eea5ff0804f59eb301414bbe",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11460/parallel_studio_xe_2017_update3.tgz",
        deprecated=True,
    )
    version(
        "professional.2017.2",
        sha256="83a655f0c2969409758488d70d6719fb5ea81a84b6da3feb641ce67bb240bc8a",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11298/parallel_studio_xe_2017_update2.tgz",
        deprecated=True,
    )
    version(
        "professional.2017.1",
        sha256="c808be744c98f7471c61258144859e8e8fc92771934281a16135803e941fd9b0",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/10973/parallel_studio_xe_2017_update1.tgz",
        deprecated=True,
    )
    version(
        "professional.2017.0",
        sha256="f380a56a25cf17941eb691a640035e79f92516346500e0df80fbdd46c5c1b301",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9651/parallel_studio_xe_2017.tgz",
        deprecated=True,
    )
    #
    version(
        "professional.2016.4",
        sha256="ea43c150ed6f9967bc781fe4253169a0447c69bac4fe2c563016a1ad2875ae23",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9781/parallel_studio_xe_2016_update4.tgz",
        deprecated=True,
    )
    version(
        "professional.2016.3",
        sha256="aa7c6f1a6603fae07c2b01409c12de0811aa5947eaa71dfb1fe9898076c2773e",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9061/parallel_studio_xe_2016_update3.tgz",
        deprecated=True,
    )
    version(
        "professional.2016.2",
        sha256="280bf39c75d7f52f206759ca4d8b6334ab92d5970957b90f5aa286bb0aa8d65e",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8676/parallel_studio_xe_2016_update2.tgz",
        deprecated=True,
    )
    version(
        "professional.2016.1",
        sha256="f5a3ab9fb581e19bf1bd966f7d40a11905e002a2bfae1c4a2140544288ca3e48",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8365/parallel_studio_xe_2016_update1.tgz",
        deprecated=True,
    )
    version(
        "professional.2016.0",
        sha256="fd4c32352fd78fc919601bedac5658ad5ac48efbc5700d9a8d42ed7d53bd8bb7",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/7997/parallel_studio_xe_2016.tgz",
        deprecated=True,
    )
    #
    version(
        "professional.2015.6",
        sha256="e604ed2bb45d227b151dd2898f3edd93526d58d1db1cb9d6b6f614907864f392",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8469/parallel_studio_xe_2015_update6.tgz",
        deprecated=True,
    )
    version(
        "professional.2015.1",
        sha256="84fdf48d1de20e1d580ba5d419a5bc1c55d217a4f5dc1807190ecffe0229a62b",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/4992/parallel_studio_xe_2015_update1.tgz",
        deprecated=True,
    )

    # Composer Edition (basic tier; excluded: MPI/..., Advisor/Inspector/Vtune)
    version(
        "composer.2020.4",
        sha256="ac1efeff608a8c3a416e6dfe20364061e8abf62d35fbaacdffe3fc9676fc1aa3",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16759/parallel_studio_xe_2020_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2020.2",
        sha256="42af16e9a91226978bb401d9f17b628bc279aa8cb104d4a38ba0808234a79bdd",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16759/parallel_studio_xe_2020_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2020.1",
        sha256="26c7e7da87b8a83adfd408b2a354d872be97736abed837364c1bf10f4469b01e",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16530/parallel_studio_xe_2020_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2020.0",
        sha256="9168045466139b8e280f50f0606b9930ffc720bbc60bc76f5576829ac15757ae",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/16229/parallel_studio_xe_2020_composer_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "composer.2019.5",
        sha256="e8c8e4b9b46826a02c49325c370c79f896858611bf33ddb7fb204614838ad56c",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15813/parallel_studio_xe_2019_update5_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2019.4",
        sha256="1915993445323e1e78d6de73702a88fa3df2036109cde03d74ee38fef9f1abf2",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15537/parallel_studio_xe_2019_update4_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2019.3",
        sha256="15373ac6df2a84e6dd9fa0eac8b5f07ab00cdbb67f494161fd0d4df7a71aff8e",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15272/parallel_studio_xe_2019_update3_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2019.2",
        sha256="1e0f400be1f458592a8c2e7d55c1b2a4506f68f22bacbf1175af947809a4cd87",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/15092/parallel_studio_xe_2019_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2019.1",
        sha256="db000cb2ebf411f6e91719db68a0c68b8d3f7d38ad7f2049ea5b2f1b5f006c25",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/14832/parallel_studio_xe_2019_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2019.0",
        sha256="e1a29463038b063e01f694e2817c0fcf1a8e824e24f15a26ce85f20afa3f963a",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13581/parallel_studio_xe_2019_composer_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "composer.2018.4",
        sha256="94aca8f091dff9535b02f022a37aef150b36925c8ef069335621496f8e4db267",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13722/parallel_studio_xe_2018_update4_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2018.3",
        sha256="f21f7759709a3d3e3390a8325fa89ac79b1fce8890c292e73b2ba3ec576ebd2b",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/13002/parallel_studio_xe_2018_update3_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2018.2",
        sha256="02d2a9fb10d9810f85dd77700215c4348d2e4475e814e4f086eb1442462667ff",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12722/parallel_studio_xe_2018_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2018.1",
        sha256="db9aa417da185a03a63330c9d76ee8e88496ae6b771584d19003a29eedc7cab5",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12381/parallel_studio_xe_2018_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2018.0",
        sha256="ecad64360fdaff2548a0ea250a396faf680077c5a83c3c3ce2c55f4f4270b904",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12067/parallel_studio_xe_2018_composer_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "composer.2017.7",
        sha256="661e33b68e47bf335694d2255f5883955234e9085c8349783a5794eed2a937ad",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12860/parallel_studio_xe_2017_update7_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2017.6",
        sha256="771f50746fe130ea472394c42e25d2c7edae049ad809d2050945ef637becf65f",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12538/parallel_studio_xe_2017_update6_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2017.5",
        sha256="ede4ea9351fcf263103588ae0f130b4c2a79395529cdb698b0d6e866c4871f78",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/12144/parallel_studio_xe_2017_update5_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2017.4",
        sha256="4304766f80206a27709be61641c16782fccf2b3fcf7285782cce921ddc9b10ff",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2017.3",
        sha256="3648578d7bba993ebb1da37c173979bfcfb47f26e7f4e17f257e78dea8fd96ab",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2017.2",
        sha256="abd26ab2a703e73ab93326984837818601c391782a6bce52da8b2a246798ad40",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2017.1",
        sha256="bc592abee829ba6e00a4f60961b486b80c15987ff1579d6560186407c84add6f",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz",
        deprecated=True,
    )
    version(
        "composer.2017.0",
        sha256="d218db66a5bb57569bea00821ac95d4647eda7422bf8a178d1586b0fb314935a",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9656/parallel_studio_xe_2017_composer_edition.tgz",
        deprecated=True,
    )
    #
    version(
        "composer.2016.4",
        sha256="17606c52cab6f5114223a2425923c8dd69f1858f5a3bdf280e0edea49ebd430d",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz",
        deprecated=True,
    )
    version(
        "composer.2016.3",
        sha256="fcec90ba97533e4705077e0701813b5a3bcc197b010b03e96f83191a35c26acf",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz",
        deprecated=True,
    )
    version(
        "composer.2016.2",
        sha256="6309ef8be1abba7737d3c1e17af64ca2620672b2da57afe2c3c643235f65b4c7",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz",
        deprecated=True,
    )
    #
    # Pre-2016, the only product was "Composer XE"; dir structure is different.
    version(
        "composer.2015.6",
        sha256="b1e09833469ca76a2834cd0a5bb5fea11ec9986da85abf4c6eed42cd96ec24cb",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/8432/l_compxe_2015.6.233.tgz",
        deprecated=True,
    )
    version(
        "composer.2015.1",
        sha256="8a438fe20103e27bfda132955616d0c886aa6cfdd86dcd9764af5d937a8799d9",
        url="http://registrationcenter-download.intel.com/akdlm/IRC_NAS/tec/4933/l_compxe_2015.1.133.tgz",
        deprecated=True,
    )

    # Generic Variants
    variant("rpath", default=True, description="Add rpath to .cfg files")
    variant(
        "newdtags", default=False, description="Allow use of --enable-new-dtags in MPI wrappers"
    )
    variant("shared", default=True, description="Builds shared library")
    variant("ilp64", default=False, description="64 bit integers")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    auto_dispatch_options = IntelPackage.auto_dispatch_options
    variant(
        "auto_dispatch",
        values=any_combination_of(*auto_dispatch_options),
        description="Enable generation of multiple auto-dispatch code paths",
    )

    # Components available in all editions
    variant("daal", default=True, description="Install the Intel DAAL libraries")
    variant(
        "gdb", default=False, description="Install the Intel Debugger for Heterogeneous Compute"
    )
    variant("ipp", default=True, description="Install the Intel IPP libraries")
    variant("mkl", default=True, description="Install the Intel MKL library")
    variant("mpi", default=True, description="Install the Intel MPI library")
    variant("tbb", default=True, description="Install the Intel TBB libraries")

    # Components only available in the Professional and Cluster Editions
    variant("advisor", default=False, description="Install the Intel Advisor")
    variant("clck", default=False, description="Install the Intel Cluster Checker")
    variant("inspector", default=False, description="Install the Intel Inspector")
    variant("itac", default=False, description="Install the Intel Trace Analyzer and Collector")
    variant("vtune", default=False, description="Install the Intel VTune Amplifier XE")

    provides("daal", when="+daal")
    provides("ipp", when="+ipp")

    provides("mkl", when="+mkl")
    provides("blas", "lapack", when="+mkl")
    provides("scalapack", when="+mkl")

    provides("fftw-api@3", when="+mkl@professional.2017:")
    provides("fftw-api@3", when="+mkl@cluster.2017:")
    provides("fftw-api@3", when="+mkl@composer.2017:")

    provides("mpi", when="+mpi")
    provides("tbb", when="+tbb")

    conflicts("target=ppc64:", msg="intel-parallel-studio is only available for x86_64")
    conflicts("target=ppc64le:", msg="intel-parallel-studio is only available for x86_64")
    conflicts("target=aarch64:", msg="intel-parallel-studio is only available for x86_64")

    # For TBB, static linkage is not and has never been supported by Intel:
    # https://www.threadingbuildingblocks.org/faq/there-version-tbb-provides-statically-linked-libraries
    conflicts("+tbb", when="~shared")

    conflicts("+advisor", when="@composer.0:composer")
    conflicts("+clck", when="@composer.0:composer")
    conflicts("+inspector", when="@composer.0:composer")
    conflicts("+itac", when="@composer.0:composer")
    conflicts("+mpi", when="@composer.0:composer")
    conflicts("+vtune", when="@composer.0:composer")

    conflicts("+clck", when="@professional.0:professional")
    conflicts("+itac", when="@professional.0:professional")
    conflicts("+mpi", when="@professional.0:professional")

    # The following components are not available before 2016
    conflicts("+daal", when="@professional.0:professional.2015.7")
    conflicts("+daal", when="@cluster.0:cluster.2015.7")
    conflicts("+daal", when="@composer.0:composer.2015.7")

    # MacOS does not support some of the auto dispatch settings
    conflicts("auto_dispatch=SSE2", "platform=darwin", msg="SSE2 is not supported on MacOS")
    conflicts(
        "auto_dispatch=SSE3",
        "platform=darwin target=x86_64:",
        msg="SSE3 is not supported on MacOS x86_64",
    )

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Handle in callback, conveying client's compilers in additional arg.
        # CAUTION - DUP code in:
        #   ../intel-mpi/package.py
        #   ../intel-parallel-studio/package.py
        dependent_module = dependent_spec.package.module
        self._setup_dependent_env_callback(
            env,
            dependent_spec,
            compilers_of_client={
                "CC": dependent_module.spack_cc,
                "CXX": dependent_module.spack_cxx,
                "F77": dependent_module.spack_f77,
                "F90": dependent_module.spack_fc,
                "FC": dependent_module.spack_fc,
            },
        )

    def setup_run_environment(self, env):
        super().setup_run_environment(env)

        for name, value in self.mpi_compiler_wrappers.items():
            env.set(name, value)
