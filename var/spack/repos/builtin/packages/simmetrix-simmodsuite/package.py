# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

RELEASES = [
    {
        "version": "16.0-220312",
        "components": {
            "msparalleladapt": [
                "cc6d6ecba8183f3444e55977af879b297977ff94dd7f6197028110f7e24ea60b",
                "paralleladapt",
            ],
            "msadapt": [
                "ec4a985f9b29914411d299fecfb1a994224070480be5de5f701d9968ba9da9e5",
                "base",
            ],
            "opencascade": [
                "008e7232ee3531b70143129e5a664f7db0e232bad9d11d693d725d39986a8aa4",
                "opencascade",
            ],
            "gmvoxel": [
                "4a74c54c31e9eb93f9a0c09ef3ac88f365efb19666240374aa6d1142db993a2c",
                "voxel",
            ],
            "msadv": ["d33b591147152383130cc2190f1bd7726cb9ea3590468691db3be5815802d888", "adv"],
            "pskrnl": [
                "e154c22c01ecab2e041cf5d87fcb23eab074449dae7f677f17e7863b6da70fdc",
                "parasolid",
            ],
            "gmcore": ["d9ed89d07d83f2c23eca6a27fd9000fd4c8eeefa70ac860aa28a40000a6ec93e", "base"],
            "psint": [
                "5c236e429f28a36a36cb09ec3f4778dc7b6e72447014b684792eea733bb21fd5",
                "parasolid",
            ],
            "msparallelmesh": [
                "a791f4464da54faafdc63dbcaf3d326ffc49c9ea8d53e36cc57c15607cf72db9",
                "parallelmesh",
            ],
            "mscore": ["48e367e476a03a9fa5389830a6c60824b5d620d04d87392e423a33a331ba3595", "base"],
            "fdcore": ["022de14021434d90daee8ea1200c024d98a7eb01bb9cb5a06a3b2f7ffee9c0a1", "base"],
            "gmadv": [
                "6232ec08ef5cff4269d066b035490f33c199fb545355836ef1536b1a00179b2c",
                "advmodel",
            ],
            "gmabstract": [
                "08a6c7423ed59361c5330dbe00b8914d1d55160de73002e7e552c45c8316f37a",
                "abstract",
            ],
            "discrete": [
                "f5ae00688cf202e75686955185d95952e7b581b414dd52bfef0d917e5959ab22",
                "discrete",
            ],
            "aciskrnl": [
                "c2c7b0c495d47a5662765f1b0c6f52863032e63384d85241e6313c4b773e9ed2",
                "acis",
            ],
        },
        "docs": {
            "GeomSimParasolid": [
                "3420fcc1ac67cff8f46b79553cfe478f34676b9b0cd1fa913255b48cbdfd6ad4",
                "parasolid",
            ],
            "GeomSimAcis": [
                "77b31bfb368f1e7981b3a81087e4e287c560e0a0cd08920b36dc81fea25bcdfa",
                "acis",
            ],
            "MeshSimAdvanced": [
                "abeeb0cb10cf3074295a880412e0568b653f2784b1de19f0f8ede5eec536a8bd",
                "adv",
            ],
            "GeomSim": [
                "b1e762111eb8025b966b0aca4bef3768325d9f1c1e3c72a1246b59539e444eb2",
                "base",
            ],
            "GeomSimVoxel": [
                "bc43f931670657a2cae79f9a2a02048b511fa6e405f15e583631e9f6888e7000",
                "voxel",
            ],
            "ParallelMeshSimAdapt": [
                "dd3a0fd6b889dadb45f9a894f684353fffa25bf15be60ae8e09d0c035045e192",
                "paralleladapt",
            ],
            "GeomSimAdvanced": [
                "3e971ae069baf94b38794318f97f16dc25cf50f6a81413903fbe17407cbd73b3",
                "advmodel",
            ],
            "GeomSimGranite": [
                "e438c19bb94a182068bf327988bd1ff9c1e391876cd9b7c74760b98cbfd08763",
                "granite",
            ],
            "FieldSim": [
                "5ede572cbb7539921482390e5890daa92399a5f1ee68a98d3241a7d062667d9d",
                "base",
            ],
            "MeshSimAdapt": [
                "c4be287da651c68e246034b28e141143d83fc3986fd680174a0d6de7b1cc35ab",
                "base",
            ],
            "GeomSimOpenCascade": [
                "34a8d628d07ab66159d6151276e93fdabfcc92a370f5927b66a71d3a8545652c",
                "opencascade",
            ],
            "GeomSimDiscrete": [
                "d2b11367334401ec57390a658715e91bbf3e3a0e8521fab1ad5d3f7c215b2921",
                "discrete",
            ],
            "GeomSimAbstract": [
                "601b0179b65a385a39d241a9a4e3074e4f834c817e836bea07516015c769e666",
                "abstract",
            ],
            "GeomSimDiscreteModeling": [
                "619b8254d8e3bcc94e84551e997b577dd9325131d084c3b3693ab665b7e4213b",
                "discrete",
            ],
            "ParallelMeshSim": [
                "5b74b9b5f9290111366e341c12d4777635e375523d42cb0a2b24aa1bfa8ab8c4",
                "parallelmesh",
            ],
            "MeshSim": [
                "2f1944e1853a550cc474201790555212e4b7a21d3675715de416718a789ccae2",
                "base",
            ],
        },
    },
    {
        "version": "16.0-210623",
        "components": {
            "gmadv": [
                "c40dac44695db6e97c4d4c06d1eb6eac93518c93d7860c77a69f3ea30fea3b90",
                "advmodel",
            ],
            "msparallelmesh": [
                "57d710b74887731ea0e664a154489747033af433852809181c11e8065752eaf4",
                "parallelmesh",
            ],
            "gmcore": ["5bd04f175fdf5a088140af5ca3fa03934251c097044b47fdf3ea2cd0afc28547", "base"],
            "pskrnl": [
                "87957818b20839d3835a343894c396f7c591d1f0bfd728d33ad21b1adb4e887c",
                "parasolid",
            ],
            "msadapt": [
                "5ba66819bb2c56eb1e07e6c2659afc8c971005b08ed059f8c62a185236e45dac",
                "base",
            ],
            "gmvoxel": [
                "15dfc389665086ea37b9835fecd6b46070572878308796afa960077cc2bf7e0a",
                "voxel",
            ],
            "msparalleladapt": [
                "1db2c34a398c5965a2a675006c96a3603e0124188b52159776b7c616efa48457",
                "paralleladapt",
            ],
            "mscore": ["7029871c52d6c3bb782ae2acb7360130105649cd9cf63815ae95cf4089cb786d", "base"],
            "psint": [
                "c8a3dbacafa70b13bc9fb8322699a1cfc812b2cfd3ea05cba9135623eae761d8",
                "parasolid",
            ],
            "fdcore": ["75f9bcd7cb9ab9dedb73166539c08b53bd8e91c5619d3dce605ba19c63d1ee5c", "base"],
            "msadv": ["0018e0a6b9d7724867f7379bc619269481c318ee4dfd0724511c032534ae04a1", "adv"],
            "aciskrnl": [
                "2a9b9da9b0c09857de7fef0dea0e96222bd30e297bd37bea962751dab6762500",
                "acis",
            ],
            "discrete": [
                "f17cd198f8749c763cc8e200cfd6734604e1d316a48d7d0e537a9a890d884904",
                "discrete",
            ],
            "gmabstract": [
                "068d0309d5ff9668fc0474edf7f4e20503827400e34492e2ed55b46a0c9e1858",
                "abstract",
            ],
        },
        "docs": {
            "GeomSimAdvanced": [
                "02e4566042ae4de10c4acb577142e82d15f32caa296fe1b578c62a38da707066",
                "advmodel",
            ],
            "MeshSim": [
                "cc1dc77cece7aac6ded003c872c651ad8321bc9ce931ad141b17d2de7bf513c5",
                "base",
            ],
            "GeomSimVoxel": [
                "49b8f85f59acc8c973bf46c1f999a0ae64cdf129371587879de056c0ac3500d8",
                "voxel",
            ],
            "MeshSimAdvanced": [
                "2d2689979104414d91d804ca3c34a69104e572b8f231c4e324b09e57675b61cc",
                "adv",
            ],
            "GeomSimGranite": [
                "17f18831a12b06c0e085486d94d3a4275d7ed94ad53fec689e8877217856c750",
                "granite",
            ],
            "GeomSimParasolid": [
                "492bd311cc42dadd1f76064c57d35e886b9a7da4c48576ec4d34844fcdaddb8d",
                "parasolid",
            ],
            "GeomSimAcis": [
                "341c6aeda7f9189f4e886cb75c5989cb9ece6ecba1b1c9d5273b94f74a3dd40b",
                "acis",
            ],
            "GeomSimDiscrete": [
                "e9d42da613a3acadbcdee5d8d6fc3b093f58b51d158f2a392b7da0e5f74e0388",
                "discrete",
            ],
            "MeshSimAdapt": [
                "e27510e588105bdb0ca62c2629dfd41dfca6039b7b2ff0298ef83d3a48d7dd23",
                "base",
            ],
            "GeomSimAbstract": [
                "398c1a15efcddd3b86a7b0334af6f8b529710f815f73f5655d3c7271e92b194e",
                "abstract",
            ],
            "GeomSimDiscreteModeling": [
                "f444aed59569731f65eea920322adcc224c67b715ecba85a1898cf418de58237",
                "discrete",
            ],
            "FieldSim": [
                "bac947998d4de1c4edba271645310d4784290bec30bf0cf41d00ae6ea8b27c97",
                "base",
            ],
            "GeomSim": [
                "95cb24165d47701daa8da7131ca1173d38f4dab80c1ca0d75843b464fed92097",
                "base",
            ],
            "ParallelMeshSim": [
                "fb1e3ac0ab7208d771057880c693e529e7c821772265b89125d371a1b34fa651",
                "parallelmesh",
            ],
            "ParallelMeshSimAdapt": [
                "246c5c8b30194239f41a79f2ffd205fd9ae69bcb8127d19a94f12c278a27f106",
                "paralleladapt",
            ],
        },
    },
    {
        "version": "14.0-191122",
        "components": {
            "gmadv": [
                "01cea5f7aff5e442ea544df054969740ad33e2ff4097cf02de31874d16a0c7c2",
                "advmodel",
            ],
            "msadapt": [
                "69839698f24969f97963869fd212bdcff0b5d52dd40ec3fdc710d878e43b527a",
                "base",
            ],
            "gmvoxel": [
                "bfea15e1fc5d258ed9db69132042a848ca81995e92bf265215e4b88d08a308a8",
                "voxel",
            ],
            "gmabstract": [
                "dccdcd4b71758e4110cd69b0befa7875e5c1f3871f87478410c6676da3f39092",
                "abstract",
            ],
            "fdcore": ["6981b2eb0c0143e6abc3ec29918fc3552f81018755770bf922d2491275984e1a", "base"],
            "msparallelmesh": [
                "1e1a431ec9dd85354ff42c6a2a41df7fbe3dfe5d296f40105c4d3aa372639dc3",
                "parallelmesh",
            ],
            "mscore": ["bca80fcb2c86e7b6dc0259681ccd73197ce85c47f00f1910bd6b518fa0b3a092", "base"],
            "discrete": [
                "430e5f2270864b1ab9c8dff75d2510147a0c5cde8af0828975d9e38661be3a35",
                "discrete",
            ],
            "gmimport": [
                "e83b3c43b7c695fa96ed42253a4b317a2882bcb8987fd3225c09492e353e49aa",
                "import",
            ],
            "pskrnl": [
                "31455cfce746b2339b3644f3890d4444014fb839654a9f576ec747d28ff6c1c4",
                "parasolid",
            ],
            "gmcore": ["af5d89b9ce266cac5b45f2bf96e1324e87e54c6e2f568bd5b6a85c41122d39e4", "base"],
            "aciskrnl": [
                "764e5633e6d502951788accfb8c34ed59430a4779a44d1775fd67f9aab8a654a",
                "acis",
            ],
            "msparalleladapt": [
                "8ae607112958f6b9d319736c71a6597cf99a8a59ceed733f2a939cb9cfa6dd67",
                "paralleladapt",
            ],
            "psint": [
                "f6c90b2fe87e690b2cba20f357d03c5962fed91541d6b79e01dc25cb8f01d1e0",
                "parasolid",
            ],
            "msadv": ["f18a8285d539cb07b00fde06fe970d958eceabf2a10182bcca6c8ad1c074c395", "adv"],
        },
        "docs": {
            "MeshSim": [
                "f3c475072f270ff49ac2f6639ca1cddb0642889648cbea7df1a3f1b85f7cac36",
                "base",
            ],
            "GeomSimVoxel": [
                "9f4ee5a8204fee1d899cb912e0379f8be7a826e81ca0a0d8a670a4b804ca1276",
                "voxel",
            ],
            "MeshSimAdvanced": [
                "8c8bc3709238e600e8938c7c345588f8947d89eae98a228b0d0e3d46f5f4c0d9",
                "adv",
            ],
            "GeomSimDiscreteModeling": [
                "4e8e26a88e8a5ad396a637597a52f5973d8f77abc0a5b99fa737caf37226d6cc",
                "discrete",
            ],
            "GeomSimAdvanced": [
                "5efb38317d6be7862ce34024922ca372b30691a30af820474e2e26e4c3055278",
                "advmodel",
            ],
            "GeomSimParasolid": [
                "6851bdaf6d96e7b2335fce3394825e9876800f0aba0a42644758dc1bd06f60fe",
                "parasolid",
            ],
            "GeomSimImport": [
                "d931ecfc332460c825b473c0950c7ae8ff9f845e0d1565f85bfd7698da5e6d26",
                "import",
            ],
            "ParallelMeshSim": [
                "0f0d235b25a660271e401488e412220f574b341dadb827f7b82f0e93172b5cdb",
                "parallelmesh",
            ],
            "ParallelMeshSimAdapt": [
                "7964ebbd7e8d971ea85fc5260e44f7e876da5ad474dc67d8d6fc939bfa5ba454",
                "paralleladapt",
            ],
            "GeomSimAcis": [
                "dea82efbc4e3043ecda163be792ef295057e08be17654a7783ce7ca5e786f950",
                "acis",
            ],
            "MeshSimAdapt": [
                "ee4d5595572c1fe1a0d78bd9b85c774a55e994c48170450d6c5f34b05fcf2411",
                "base",
            ],
            "FieldSim": [
                "6b09b4ab278911d3e9229fd4cd8dc92ba188f151d42d9d7b96d542aad2af1fac",
                "base",
            ],
            "GeomSim": [
                "0673823d649998367c0e427055911eae971bb6e8c76625882e7a7901f4d18c44",
                "base",
            ],
            "GeomSimDiscrete": [
                "58dfd33fc5cdd2ab24e9084377943f28d5ba68b8c017b11b71cde64c5e4f2113",
                "discrete",
            ],
            "GeomSimAbstract": [
                "16248cd2a0d133029eb4b79d61397da008e4d5b5c3eaf0161a0a44148b0bc519",
                "abstract",
            ],
        },
    },
    {
        "version": "12.0-191027",
        "components": {
            "gmadv": [
                "1a133523062974c4d9acb1d52baa3893dc891482aebaaeb79a7dc907461d5dbc",
                "advmodel",
            ],
            "fdcore": ["c3a89093f811cb489698d203dbe68ca910e6c67ea75c0a7aba73dd369508b9ec", "base"],
            "mscore": ["a2f043278d45d8729020b663c66c57960fcec33dafd3d90db55f0a9e32723bce", "base"],
            "msparallelmesh": [
                "2f6fd47d3c5c2f1ece4634985a522ac599d3cee20ad8a4623f252cc75aa32c4c",
                "parallelmesh",
            ],
            "msparalleladapt": [
                "8d288730b1300215a32f3b21624bd2e0e2d8a684fe928459757fcec7e0aeb7d3",
                "paralleladapt",
            ],
            "gmabstract": [
                "3b608f21e6c11db5bb48e49f9cd7e9d88aeec4feadebd778529a5c9d506d08c6",
                "abstract",
            ],
            "gmimport": [
                "fc1626c7b1522b90eaa3926e1253b84d28440c7df8634decdedb79b5229be800",
                "import",
            ],
            "discrete": [
                "a15ead08138f0c59c7ee46cd0d348d4f26e1b021d2580a134cf2b84a7337bcf9",
                "discrete",
            ],
            "aciskrnl": [
                "8773f00e08d237052c877e79d1a869214f59891e812d70df938b2a5e5423a96f",
                "acis",
            ],
            "msadv": ["41bdb9555ab9feb0891f0832a49fc29777d40957473f315e1c33e1c0077cba7d", "adv"],
            "psint": [
                "b040ab48833eb2a748f757e2de6929f3002aa98db459ba92bd9a88e443e5cb07",
                "parasolid",
            ],
            "gmvoxel": [
                "19fba83c9c7eac20d9613236530fbae652dc8edef35233214f0f92b81c91a877",
                "voxel",
            ],
            "msadapt": [
                "1a752adb6724c3328fffb26f1aebed007d3c2a5df725cd29aa0cf0fdfda1f39a",
                "base",
            ],
            "gmcore": ["ec95bae84b36644e6e04cf0a6b4e813a51990d0a30519176ebb8a05f681af7f2", "base"],
            "pskrnl": [
                "7b7b4952513e06c8c23aa8f7c1748f5c199d9af70ea06c4a359412237ed8ac1d",
                "parasolid",
            ],
        },
        "docs": {
            "FieldSim": [
                "5109d91fe61ccdaf0af5aa869aea9c38ec98760746ec3983d100f870cbb1cb63",
                "base",
            ],
            "ParallelMeshSim": [
                "a1e6618a77022a9580beac4c698dd4b9aa70f617a27db9ce13ab1f2388475290",
                "parallelmesh",
            ],
            "GeomSimAcis": [
                "f0319b32eb417fa9b237575d9b2dc1c061848888c36fd4da97d97cdbb3cf19c3",
                "acis",
            ],
            "GeomSimAbstract": [
                "c44023e6944522057c47925db49089031c7de9b67938ca6a987e04fadfeda9b7",
                "abstract",
            ],
            "GeomSimDiscrete": [
                "ad648752fa7d2dc1ce234a612e28ce84eb1f064a1decadf17b42e9fe56967350",
                "discrete",
            ],
            "MeshSimAdapt": [
                "dcb7d6ec74c910b41b5ae707d9fd4664fcb3a0fdb2c876caaa28a6f1cf701024",
                "base",
            ],
            "MeshSim": [
                "e5a8cb300b1e13b9f2733bf8b738872ffb37d9df15836a6ab264483c10000696",
                "base",
            ],
            "GeomSimParasolid": [
                "2bf33cc5b3879716437d45fde0a02caaa165e37d248d05b4b00708e76573a15e",
                "parasolid",
            ],
            "GeomSimImport": [
                "5309433dcdce660e062412f070719eefcc6299764e9b0169533ff343c9c9c406",
                "import",
            ],
            "ParallelMeshSimAdapt": [
                "2e8e0ceede3107b85dba9536f3bbf5e6959793073a5147548cfb01ca568c8da2",
                "paralleladapt",
            ],
            "GeomSimDiscreteModeling": [
                "ff88ec234b890315cc36539e3f73f4f977dab94160860950e7b7ee0303c9b55e",
                "discrete",
            ],
            "GeomSim": [
                "62ae33372f999d5e62a1b7b161ddd7de04c055adc85cfd258e088c95b76d5fef",
                "base",
            ],
            "GeomSimVoxel": [
                "7a624ddaebd833077511acac3efd4b4c1dab09bd9feff40aba0813182eeb262f",
                "voxel",
            ],
            "GeomSimAdvanced": [
                "f0ab801ddf3d701a4ac3f8c47900cc858a4488eb0fe2f663504ba260cd270d20",
                "advmodel",
            ],
            "MeshSimAdvanced": [
                "bb532027e4fcc311a7c376383da010aed5ee133a9122b186a4e5c7d0cf1d976b",
                "adv",
            ],
        },
    },
]


def simmetrix_makecomponenturl(name):
    """only supporting the linux libraries"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = "-" + "linux64.tgz"
    return prefix + name + suffix


def simmetrix_makedocurl(name):
    """doc zip files are not os/arch specific"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = ".zip"
    return prefix + name + suffix


def simmetrix_setkernelcmakeprefixpath(spec, path, env):
    if "+acis" in spec:
        env.append_path("CMAKE_PREFIX_PATH", join_path(path, "acisKrnl"))
        env.append_path("LD_LIBRARY_PATH", join_path(path, "acisKrnl"))
    if "+parasolid" in spec:
        env.append_path("CMAKE_PREFIX_PATH", join_path(path, "psKrnl"))
        env.append_path("LD_LIBRARY_PATH", join_path(path, "psKrnl"))


def simmetrix_resource(name, url, sha256, condition):
    # The tarballs/zips each have the same directory structure.  Because of
    # this, and the bug in spack described here:
    # https://github.com/spack/spack/pull/3553#issuecomment-391424244
    # , they cannot be expanded into the source root directory.
    # Once this is fixed the 'destination=name' argument can be removed.
    resource(name=name, url=url, sha256=sha256, destination=name, when=condition)


class SimmetrixSimmodsuite(Package):
    """Simmetrix' Simulation Modeling Suite is a set of component software
    toolkits that allow developers to easily implement geometry-based
    simulation applications.
    Each component of the Simulation Modeling Suite is designed to address
    specific capabilities:
    | MeshSim - automatic mesh generation
    | FieldSim - simulation data management
    | GeomSim - direct, untranslated access to geometry from a wide variety
    of sources
    """

    maintainers("cwsmith")
    homepage = "http://www.simmetrix.com/products/SimulationModelingSuite/main.html"
    manual_download = True

    license_required = True
    license_vars = ["SIM_LICENSE_FILE"]

    variant("base", default=True, description="enable the base components")
    variant("advmodel", default=False, description="enable advaced modeling")
    variant("abstract", default=False, description="enable abstract modeling")
    variant("voxel", default=False, description="enable voxel modeling")
    variant("discrete", default=False, description="enable discrete modeling")
    variant("acis", default=False, description="enable acis modeling")
    variant("parasolid", default=False, description="enable parasolid modeling")
    variant(
        "opencascade",
        default=False,
        when="@16.0-220312:",
        description="enable opencascade modeling",
    )
    variant("granite", default=False, description="enable granite modeling")
    variant("import", default=False, description="enable import modeling")
    variant("adv", default=False, description="enable advanced meshing")
    variant("parallelmesh", default=False, description="enable parallel meshing")
    variant("paralleladapt", default=False, description="enable parallel adaptation")

    depends_on("mpi")
    depends_on("libtirpc", type="link")

    oslib = "x64_rhel8_gcc83"

    for release in RELEASES:
        # define the version using the mscore tarball
        sim_version = release["version"]
        main_pkg_name = "mscore"
        url = simmetrix_makecomponenturl(main_pkg_name)
        sha256 = release["components"][main_pkg_name][0]
        version(sim_version, sha256=sha256, url=url)
        # define resources for the other tarballs
        for _name, atts in release["components"].items():
            # skip the tarball used for the version(...) call
            if _name == "mscore":
                continue
            sha256 = atts[0]
            feature = atts[1]
            url = simmetrix_makecomponenturl(_name)
            condition = "@{0}+{1}".format(sim_version, feature)
            simmetrix_resource(_name, url, sha256, condition)
        # define resources for the document zip files
        for _name, atts in release["docs"].items():
            sha256 = atts[0]
            feature = atts[1]
            url = simmetrix_makedocurl(_name)
            condition = "@{0}+{1}".format(sim_version, feature)
            simmetrix_resource(_name, url, sha256, condition)

    def setup_dependent_build_environment(self, env, dependent_spec):
        archlib = join_path(self.prefix.lib, self.oslib)
        env.append_path("CMAKE_PREFIX_PATH", archlib)
        simmetrix_setkernelcmakeprefixpath(self.spec, archlib, env)

    def setup_run_environment(self, env):
        archlib = join_path(self.prefix.lib, self.oslib)
        env.append_path("CMAKE_PREFIX_PATH", archlib)
        simmetrix_setkernelcmakeprefixpath(self.spec, archlib, env)

    def install(self, spec, prefix):
        if not spec.satisfies("platform=linux"):
            raise InstallError("Only the linux platform is supported")
        source_path = self.stage.source_path
        for release in RELEASES:
            simversion = release["version"]
            if simversion != spec.version.string:
                continue
            for name, atts in release["components"].items():
                feature = atts[1]
                if "+" + feature in spec:
                    if name == "mscore":
                        install_tree(join_path(source_path, "lib"), prefix.lib)
                        install_tree(join_path(source_path, "include"), prefix.include)
                    else:
                        path = join_path(source_path, name, self.version.string)
                        install_tree(path, prefix)
            for name, atts in release["docs"].items():
                feature = atts[1]
                if "+" + feature in spec:
                    path = join_path(source_path, name, self.version.string)
                    install_tree(path, prefix)

        workdir = prefix.code.PartitionWrapper
        if "+parallelmesh" in spec:
            with working_dir(workdir):
                mpi_id = spec["mpi"].name + spec["mpi"].version.string
                # build the wrapper lib
                make(
                    "-f",
                    "Makefile.custom",
                    "CC=%s" % spec["mpi"].mpicc,
                    "CXX=%s" % spec["mpi"].mpicxx,
                    "PARALLEL=%s" % mpi_id,
                    "PQUAL=-%s" % mpi_id,
                    "OPTFLAGS=-O2 -DNDEBUG " + self.compiler.cc_pic_flag,
                )
                libname = "libSimPartitionWrapper-" + mpi_id + ".a"
                wrapperlibpath = join_path(workdir, "lib", libname)
                install(wrapperlibpath, join_path(prefix.lib, self.oslib))
