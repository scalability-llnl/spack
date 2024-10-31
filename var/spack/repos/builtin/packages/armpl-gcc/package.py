# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

_os_map_before_23 = {
    "ubuntu18.04": "Ubuntu-18.04",
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-20.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rocky8": "RHEL-8",
    "amzn2": "RHEL-7",
    "amzn2023": "RHEL-7",
}

_os_map_before_24 = {
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-22.04",
    "debian12": "Ubuntu-22.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rhel9": "RHEL-9",
    "rocky8": "RHEL-8",
    "rocky9": "RHEL-9",
    "amzn2": "AmazonLinux-2",
    "amzn2023": "AmazonLinux-2023",
}

_os_pkg_map = {
    "ubuntu20.04": "deb",
    "ubuntu22.04": "deb",
    "debian12": "deb",
    "sles15": "rpm",
    "centos7": "rpm",
    "centos8": "rpm",
    "rhel7": "rpm",
    "rhel8": "rpm",
    "rhel9": "rpm",
    "rocky8": "rpm",
    "rocky9": "rpm",
    "amzn2": "rpm",
    "amzn2023": "rpm",
}

_versions = {
    "24.04": {
        "deb": ("a323074cd08af82f4d79988cc66088b18e47dea4b93323b1b8a0f994f769f2f0"),
        "macOS": ("228bf3a2c25dbd45c2f89c78f455ee3c7dfb25e121c20d2765138b5174e688dc"),
        "rpm": ("d3917523034cf5a35e4f31f9a8bf4e53e7cc97892e89739d5757cb65ce40dc2e"),
    },
    "23.10_gcc-12.2": {
        "RHEL-7": ("e5e2c69ad281a676f2a06c835fbf31d4f9fdf46aa3f3f7c8aafff46985f64902"),
        "RHEL-8": ("cc0f3572ead93d1e31797b7a39a40cff3414878df9bd24a452bf4877dc35ca4c"),
        "RHEL-9": ("18c75f57333031e454921cc3f4f22fd567e5a701424ff9ac219bbfe9955a8a96"),
        "SLES-15": ("e1e891eceaffedecf7351e2c499ef2b49a36c9af29174b366ff470d0a568c18f"),
        "Ubuntu-20.04": ("976424875c52c2062fc76cbc5d527ee82413cdc0432d7c59f423295a3b0cc612"),
        "Ubuntu-22.04": ("6dd778edf55e13e8b766d75c340f0259f6cb507a93966d76d188b8b3943c769b"),
        "AmazonLinux-2": ("423ac3df262b5fcca6cea480503b693306c970dd8e8e05c753ece92446ac7fee"),
        "AmazonLinux-2023": ("acadf3b6cde866cb41f7363b290a646a492769aaa5819d4c0d60df89913342a9"),
    },
    "23.10_gcc-11.3": {
        "RHEL-7": ("b2afbdc056ae01fb5c71935448b19300ef368962a94ae76b8811f1d328c723c2"),
        "RHEL-8": ("79b83a8a2c46b949896b3964c761cbd0b66c37826996afb62c466af5fb420bc2"),
        "RHEL-9": ("7a84f561bcf941bb25123b3ef730b4c02616bc51215933870677163e78af38e3"),
        "SLES-15": ("9243c405d092d3eabff112ccabc300e96f13c3d2c5c319df04d7093bb6f535a2"),
        "Ubuntu-20.04": ("a16df088ef9303040d92b017b233c6e4c6f0300d09c2ad0a66c0318831bf009c"),
        "Ubuntu-22.04": ("fabda66dc6388fa8c094443fa53deece5590db66caaa6a1e39e99e64d5bb0709"),
        "AmazonLinux-2": ("db5d039fa1d07695a71b8733584d878bb778d41bc0ecc3e19059b75cffdcf8cd"),
        "AmazonLinux-2023": ("977fd465702f086a69e3f7fc28f2bcb6c79a7af381dc7d865345115b26f4631f"),
    },
    "23.10_gcc-10.4": {
        "RHEL-7": ("3c8bad3af82a76ca1a45705afd47028cc26c7093377a554e692e1cd6f61cb304"),
        "RHEL-8": ("381afae0e3e94aa91029f571de0e51c2342e50b4f855db7a9b9ca66e16e26276"),
        "SLES-15": ("226e9519407331b4ad5ded8699cd15f1d9b845843304bbf21f47009a399fe2a0"),
        "Ubuntu-20.04": ("45de59f795ad9026a838ab611b03b1644169a034ce59d6cca2c7940850fa17ad"),
        "AmazonLinux-2": ("637b51da12548dc66da9132328fe2ea39ba0736af66fb30332ca8eeb540e3373"),
    },
    "23.10_gcc-9.3": {
        "RHEL-7": ("6fc2e3319b83ea2b1bf8d98ec43f614b937bb5f23d15aefe9e9171c882d24a60"),
        "RHEL-8": ("1a05548a7051d1df42280fdcfcffeaf89d519aa7978bffd29171da60fdbccecf"),
        "SLES-15": ("389ddd34e1299e4d942864f63f236158a81ce4190f59af512a1bea3221153bfe"),
        "Ubuntu-20.04": ("a1a221859b5f0962df3a0c6ce31669827bff0bfffb185b80429620f14b40f4f4"),
        "AmazonLinux-2": ("2eef9b28e95e75f0040eb61c9e1b406ec4d0b81cce3e95a652029aa0898733a0"),
    },
    "23.10_gcc-8.2": {
        "RHEL-7": ("d6596721e74e7bdc8d9ce7b8b2a4c5ab2bd430f3ca69b9ec84f587f1aa181083"),
        "RHEL-8": ("004aed52003e19a6c14df303456318e486ad783eb543b79285c7953a23722a4a"),
        "SLES-15": ("12c638c0cc5bdc220699499ec6bb160a7b889f105901f4354bd2748a77d25c8e"),
        "AmazonLinux-2": ("d039134236cda298cd0920c3c5b017eeef83fcab82949221dc7deb081026252f"),
    },
    "23.10_gcc-7.5": {
        "RHEL-7": ("1a0ca860c168987d174923dfc7800e10521303914793162a8bae2b2cd3f68203"),
        "AmazonLinux-2": ("58b201a6bbe7ee10563d8d42b32a77c4b15c57b4e81abb35d24b8c3fc9cff4d9"),
    },
    "23.10_flang-new_clang_17": {
        "macOS": ("baf09cd6d1d1b7c780b8b31cfe1dd709596b182dc714127fbc9f23007ff9e23a")
    },
    "23.06_flang-new_clang_16": {
        "macOS": ("232f5e89e0f1f4777480c64a790e477dfd2f423d3cf5704a116a2736f36250ea")
    },
    "23.04.1_gcc-12.2": {
        "RHEL-7": ("789cc093cb7e0d9294aff0fdf94b74987435a09cdff4c1b7118a03350548d03c"),
        "RHEL-8": ("1b668baec6d3df2d48c5aedc70baa6a9b638983b94bf2cd58d378859a1da49f0"),
        "RHEL-9": ("8a4d7aec2fe109aedcb9e8fdec566dc1ba3adcb3ba79e5c08b78b9717578db1c"),
        "SLES-15": ("9c8aa114907d3ac9311301b991d732d535422e73516e0f337395637ce6a14c4a"),
        "Ubuntu-20.04": ("c0a67afb6989b2bdb172052ff7d20a9e3197356714df06c862edd3ac71ef62f0"),
        "Ubuntu-22.04": ("02e59d834c341164f5acf633555024bf614726aed8a85c1b0b46d024ce7840e2"),
        "AmazonLinux-2": ("1cbb9a3d777353b42bfb5af327419c231640e7744ab46ab3a13e97802b1ce227"),
        "AmazonLinux-2023": ("ee9b0b6ee0d881280e473390007020504a147b75bf6076d245832f101b01653e"),
    },
    "23.04.1_gcc-11.3": {
        "RHEL-7": ("522e0269ca03d6251c10ee3aa8d94ceec4618887f47847defb535849434439a5"),
        "RHEL-8": ("00f6fee4ba4bbff5be6d5ad34137973ab89505fc61a23d8e0c302b8860c70484"),
        "RHEL-9": ("2402165267b25d07fd64b6d444b3120354dfd27594b11a1f082e85e76465e712"),
        "SLES-15": ("a928539efe5af760fc86a009e3d87c9648e4d4e91490c13bc136a837591549c3"),
        "Ubuntu-20.04": ("5754d8a6040bb6d0b1df326c9ab61901a72e5cc6d2d4195e52ca9271e55fb9f6"),
        "Ubuntu-22.04": ("8af5aca7512a604b051a7808701a5c0285e92d88232138612d8caf973b7b1252"),
        "AmazonLinux-2": ("8c710cb7bb21694130b915cc2650cfb85fb00cfca7e5fca9bbdec5c59a09c007"),
        "AmazonLinux-2023": ("8b9c69a72c5b1ed5814e28ddd122ab09dbe5dd3585e4c395242ed590eea6ea79"),
    },
    "23.04.1_gcc-10.2": {
        "RHEL-7": ("40d62517bd978516c308b2e57ab88772699fd8bb579d98bbc10ea397c0bab431"),
        "RHEL-8": ("76554ea1f3d143f1236afea67e33eea74660f57718ef57c12986843da75e03d3"),
        "SLES-15": ("63a6acb00300a9e85cfafd2141515ecb28dac82c1f441778d74e8add038724e2"),
        "Ubuntu-20.04": ("7b6bcb8d1b9ca8be2d29e7620862fa961d965f479fa04873616ac8cc9bb399fc"),
        "AmazonLinux-2": ("c6410ce2c109ae72568186bb7e162fcf4a9b05ea89da36d17db695b7df34f506"),
    },
    "23.04.1_gcc-9.3": {
        "RHEL-7": ("782bbc27c77c230426086c226a78b8951501066d631947438e65ca51d33f24c3"),
        "RHEL-8": ("8d3be6381b3e5032c5068a1d2e3d0e69c308a93496f85af42d43a579f9f7d9a3"),
        "SLES-15": ("abe2245674a66ec93cff3c93dac7ae04a99c6c7e43e2733de214ec188e0d6cae"),
        "Ubuntu-20.04": ("a7d385b901f2d1c07f243c816030ad19543e00667615dea1969ce16d29759271"),
        "AmazonLinux-2": ("7113b6e2c795933ce8d18d468889168732d3a52a0df4a48ef4bf4497e891083a"),
    },
    "23.04.1_gcc-8.2": {
        "RHEL-7": ("4e077813121c1cbd8abd1afe5348cafcce5b70f96affa725c7c2d8671e2d5eed"),
        "RHEL-8": ("772aaab9304191e3a398cba2dec21ec22fd0abadcaf44d44f32114968bd3b59d"),
        "SLES-15": ("33766ac351fb4628c6b39f16d6bdb310ad09d88b6a6f43740349405c960d4d21"),
        "AmazonLinux-2": ("c215ed8de77b5144a60b6552f79ef2b59ccbfac5350f083ef135305ddf643a4e"),
    },
    "23.04.1_gcc-7.5": {
        "RHEL-7": ("7b2239b2ce5315e1be14dbd8fe15aff2d3b07968d64b5c80c8ab57140b6a17a8"),
        "AmazonLinux-2": ("a2e0f176df627c50f851924ac57994f582f63b0f3d42ad0b65c915ea04dc0467"),
    },
    "22.1_gcc-11.2": {
        "RHEL-7": ("9ce7858525109cca8f4e1d533113b6410d55f10cc4db16c4742562da87a32f2b"),
        "RHEL-8": ("24f9f4496e41c2314d4ace25b6e3d63127bd586ff7bdd8a732471cbc65a8023e"),
        "SLES-15": ("5b2a88148157c2a6ac5fd5698e9cb5b8717fb5f7afeab156de253f53cef5ab71"),
        "Ubuntu-18.04": ("44315990a2bf9cca1f48cd873f97b4282c371b6894c96e58d890ba1ca9ed5b2a"),
        "Ubuntu-20.04": ("00c051e0176ac4354d6cf181d38ef5a6d41f5b1f4db0109f3abc5d877d8e0a1f"),
    },
    "22.1_gcc-10.2": {
        "RHEL-7": ("ca8bf196757b4755f817d97e289305893fbe9a195b6892c90f8414f438f42d83"),
        "RHEL-8": ("8a1b65b1086b7b9e0ccd7080f9ed1d411f98a775b61c1e05c000e584877a1e66"),
        "SLES-15": ("7d703d7a2954283f11b742e0bc8fee886135d5bc87fe3e700c05b8277de495c3"),
        "Ubuntu-18.04": ("fde39a1bad9d904f2b18445252245f30f31848fd4470b58b3124f92c4c641710"),
        "Ubuntu-20.04": ("f0dfde5e9f8ca29bb49ea4596cb56ca50c8fda51758a38281e191fb36def812a"),
    },
    "22.1_gcc-9.3": {
        "RHEL-7": ("76c8ab3687d421153f91cacd33047b65b3650b21e2094d34341a91e94c766425"),
        "RHEL-8": ("eebeedddab04a393f4afc499d8681dc531b6bba0312a583afde445efb29ab849"),
        "SLES-15": ("e33cc89582a98866aa5e1cf6573a0bbe71b98c1585bbe665173deeb561d9afc5"),
        "Ubuntu-18.04": ("453e524cb66c2525443ab09283baef1521c1389d9d967b24fa94539ceaa62088"),
        "Ubuntu-20.04": ("521b106652fd50dc23fa056f208b788a1e3e6f4dd6e162b8cd5d835d755cb3af"),
    },
    "22.1_gcc-8.2": {
        "RHEL-7": ("9a6caa9767367c16a5abc2a3c145f0fccd47052cd5e2b9e3fbf511009a85746c"),
        "RHEL-8": ("90009f854ab597ab3f4d6745d90460e01bbbe922bf4bdfd30a3e58e62352f6be"),
        "SLES-15": ("0b7a5a5631798cba794810983e6180dd57cb40d5e82a806fdbc8a00f50f01bd6"),
        "Ubuntu-18.04": ("7dddedcaf7ce56b10da4a8d21d253f5c6eec928d238233049462b4ce5fece1ae"),
    },
    "22.1_gcc-7.5": {
        "RHEL-7": ("33c66ed1aa78eec4a8bd9d9c77882e9275232f742dc7808789272dbded0032e0"),
        "Ubuntu-18.04": ("523b926595565af96cf8c4109517c30e248bb2336bdf55f626be4e7356c97b98"),
    },
    "22.0.2_gcc-11.2": {
        "RHEL-7": ("c8191f3a65762955714f020caf2a89e37ff7f9cb2326dc180c746acd8a018acd"),
        "RHEL-8": ("d69432a3148c9d2745c70859a0143285537e06920ecfdb4669ff364a9d24972c"),
        "SLES-15": ("dab5efa8cad15cc78212a085e7ed9125725fb51924cb79bd556229cde3c4f1a3"),
        "Ubuntu-18.04": ("38a9a2f8bf5101dd7a8b66b3eec7647730434b8ee5e4c5efd17a172e2ea1357e"),
        "Ubuntu-20.04": ("b7322d0e824615cd6fe784bfd4eeed359f11aa4eeb01a52cb61863844d79791f"),
    },
    "22.0.2_gcc-10.2": {
        "RHEL-7": ("1b728f7551db8b3d6a710151f24872d6ba8c97a7572581680161441268b9e500"),
        "RHEL-8": ("d0e2101db55f25a3ee5723c14c4209d5b082c6b737bad6121ae692e829b50038"),
        "SLES-15": ("4de686744937345bc7eeac06db2086535e0230813b87d6b4013f1336a54324a3"),
        "Ubuntu-18.04": ("ca08d6942352f4cdec634b5e8c3bfe46a05f04f19d957e6af56c25a433682e66"),
        "Ubuntu-20.04": ("25c5288c285fc08160a104dd2c36d2adab7f72b42b99771f93b0dfcb2b3e3230"),
    },
    "22.0.2_gcc-9.3": {
        "RHEL-7": ("2c2bc000d9819cae7785880b3bab00556fcc5eda3fb48356300048df28876e09"),
        "RHEL-8": ("1e992d603af0d1f80f05fffb0d57e3f66a5457fb82c56e38d5aec380f66b7bd9"),
        "SLES-15": ("e30b6d989b97f2065f981ce6061a00377455c84018c4639865c774994bab0c71"),
        "Ubuntu-18.04": ("fa0fa8367aa18169e045d9ba40f339629f14fdd6e7087b946b9bea9588213d5f"),
        "Ubuntu-20.04": ("7d3f6661304ecc7111e8b67b745d6d7fc15306e04e87dac4561e6040ac5f68b0"),
    },
    "22.0.2_gcc-8.2": {
        "RHEL-7": ("5a8cdbdfceb53252358842e505cfdc35c50af06d8d17d073bab41efdb78a38b5"),
        "RHEL-8": ("564f3e2fcdadc831d010aed0a938a419321a9ba8c18978bdad08f53924bd3986"),
        "SLES-15": ("c4d43e1ba84e2f09b6223ac148be3f7b4c7f83a4af77255dd1cb7ad0034c713a"),
        "Ubuntu-18.04": ("98c752dc997a3abe4ac4db16fd684bdd8aa8d4482bccf93948a593d523e477e0"),
    },
    "22.0.2_gcc-7.5": {
        "RHEL-7": ("adc76d9b1375330dd424dd85cd1aefa7bceaa3b25a353157d493d98850c0d8fa"),
        "Ubuntu-18.04": ("331846312e579e954dac54f69b1ffcda96ab51984050659f2314269e55b58b9e"),
    },
    "22.0.1_gcc-11.2": {
        "RHEL-7": ("32529fdc70c39084eafe746db6baa487815bb49dae1588ccf2f7bd7929c10f7c"),
        "RHEL-8": ("1abd0b1c47cae65ee74510cf6e25946c66f9f4244e4674d5e9f73c442901482c"),
        "SLES-15": ("631261d7b29e85e99d208bdd397bdb5fcb0b53fd834b4b5a9cf963789e29f96e"),
        "Ubuntu-18.04": ("2ec210ff3c33d94a7cbe0cd7ea92add0b954ab1b1dc438dffa1d5f516e80e3ec"),
        "Ubuntu-20.04": ("13e9b98afc01c5444799c7f2ef84716f8a7be11df93b71fe9cfdc7fc6162f6d5"),
    },
    "22.0.1_gcc-10.2": {
        "RHEL-7": ("d2d91f43872e072ccec0cfab61eccf531daf6f02997e29fef3d738178c023d7a"),
        "RHEL-8": ("d642f55937410d2d402589f09e985c05b577d1227063b8247dc5733199e124a4"),
        "SLES-15": ("6746de2db361a65edac2ff8dcd4fc84a314fd919df3758c9bad7027dcfadfea2"),
        "Ubuntu-18.04": ("f3a7a7cb1768046ef742110fa311c65504074f1a381d295d583848221e267bd9"),
        "Ubuntu-20.04": ("5da7450196d94b0aea613cf8e7c4083ae3eb2e905d049db3b300059a9fbf169b"),
    },
    "22.0.1_gcc-9.3": {
        "RHEL-7": ("8df55f83ccebf9c1de5291c701d7cbeb051ce194ffe2d1f1148b2a6be0d7ea1c"),
        "RHEL-8": ("b0e26004c40db3138939b7bddc4bbe54ec7de4e548b5dc697cce5c85a8acbb27"),
        "SLES-15": ("963278d35485ec28a8b17a89efcfe0f82d84edc4ff8af838d56648917ec7b547"),
        "Ubuntu-18.04": ("3c7d2f7d102954440539d5b541dd1f669d2ccb3daaa14de1f04d6790368d6794"),
        "Ubuntu-20.04": ("8e78bef6517f42efd878579aee2cae4e439e3cd5c8a28e3f3fa83254f7189a2f"),
    },
    "22.0.1_gcc-8.2": {
        "RHEL-7": ("1e682e319c3b07236acc3870bf291a1d0cba884112b447dad7e356fdc42bd06a"),
        "RHEL-8": ("1fad5a0de02cda0a23a7864cca653a04ceb4244e362073d2959ce7db4144bb20"),
        "SLES-15": ("fa6111264c3fbe29ec084e7322c794640a1b3c40b2f0e01f7637f3f0d87d03e2"),
        "Ubuntu-18.04": ("3d092ecd98620b31e813ad726244ff40fdcb012aa055b6695dff51bc1578039d"),
    },
    "22.0.1_gcc-7.5": {
        "RHEL-7": ("e23702a9fecfc64aa6bd56439a602f0c25b0febce059cb6c0192b575758c6f1a"),
        "Ubuntu-18.04": ("bf4e6327eedec656b696f98735aa988a75b0c60185f3c22af6b7e608abbdb305"),
    },
}


def get_os_or_pkg_manager(ver):
    platform = spack.platforms.host()
    if platform.name == "darwin":
        return "macOS"
    if ver.startswith("22."):
        return _os_map_before_23.get(platform.default_os, "")
    elif ver.startswith("23."):
        return _os_map_before_24.get(platform.default_os, "RHEL-7")
    else:
        return _os_pkg_map.get(platform.default_os, "rpm")


def get_package_url_before_24(base_url, version):
    armpl_version = version.split("_")[0]
    armpl_version_dashed = armpl_version.replace(".", "-")
    compiler_version = version.split("_", 1)[1]
    os = get_os_or_pkg_manager(armpl_version)
    if os == "macOS":
        if armpl_version.startswith("23.06"):
            return (
                f"{base_url}/{armpl_version_dashed}/"
                + f"armpl_{armpl_version}_{compiler_version}.dmg"
            )
        else:
            filename = f"arm-performance-libraries_{armpl_version}_macOS.dmg"
            return f"{base_url}/{armpl_version_dashed}/macos/{filename}"
    filename = f"arm-performance-libraries_{armpl_version}_{os}_{compiler_version}.tar"
    os_short = ""
    if armpl_version.startswith("22.0."):
        os_short = os.replace("-", "")
    else:
        os_short = os.split(".")[0].lower()
        if "amazonlinux" in os_short:
            os_short = os_short.replace("amazonlinux", "al")
    return f"{base_url}/{armpl_version_dashed}/{os_short}/{filename}"


def get_package_url_from_24(base, version):
    pkg_system = get_os_or_pkg_manager(version)
    os = "macOS" if pkg_system == "macOS" else "linux"

    extension = "tgz" if pkg_system == "macOS" else "tar"

    full_name_library = f"arm-performance-libraries_{version}_{pkg_system}"

    if pkg_system != "macOS":
        full_name_library = f"{full_name_library}_gcc"
    file_name = f"{full_name_library}.{extension}"

    vn = version.replace(".", "-")
    url_parts = f"{base}/{vn}/{os}/{file_name}"
    return url_parts


def get_package_url(version):
    base_url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries"
    if version[:2] >= "24":
        return get_package_url_from_24(base_url, version)
    else:
        return get_package_url_before_24(base_url, version)


def get_armpl_prefix(spec):
    armpl_dir = [
        d
        for d in os.listdir(spec.prefix)
        if os.path.isdir(os.path.join(spec.prefix, d)) and d.startswith("armpl_")
    ][0]
    return os.path.join(spec.prefix, armpl_dir)


def get_armpl_suffix(spec):
    suffix = ""
    if spec.satisfies("@24:"):
        suffix += "_ilp64" if spec.satisfies("+ilp64") else "_lp64"
    else:
        suffix += "_ilp64" if spec.satisfies("+ilp64") else ""
    suffix += "_mp" if spec.satisfies("threads=openmp") else ""
    return suffix


class ArmplGcc(Package):
    """Arm Performance Libraries provides optimized standard core math libraries for
    high-performance computing applications on Arm processors."""

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-performance-libraries/24-04/linux/arm-performance-libraries_24.04_deb_gcc.tar"

    maintainers("paolotricerri")

    for ver, packages in _versions.items():
        key = get_os_or_pkg_manager(ver)
        sha256sum = packages.get(key)
        url = get_package_url(ver)
        if sha256sum:
            extension = os.path.splitext(url)[1]
            # Don't attempt to expand .dmg files
            expand = extension != ".dmg"
            version(ver, sha256=sha256sum, url=url, extension=extension, expand=expand)

    conflicts("target=x86:", msg="Only available on Aarch64")
    conflicts("target=ppc64:", msg="Only available on Aarch64")
    conflicts("target=ppc64le:", msg="Only available on Aarch64")

    conflicts("%gcc@:11", when="@23.10_gcc-12.2")
    conflicts("%gcc@:10", when="@23.10_gcc-11.3")
    conflicts("%gcc@:9", when="@23.10_gcc-10.4")
    conflicts("%gcc@:8", when="@23.10_gcc-9.3")
    conflicts("%gcc@:7", when="@23.10_gcc-8.2")
    conflicts("%gcc@:6", when="@23.10_gcc-7.5")

    conflicts("%gcc@:11", when="@23.04.1_gcc-12.2")
    conflicts("%gcc@:10", when="@23.04.1_gcc-11.3")
    conflicts("%gcc@:9", when="@23.04.1_gcc-10.2")
    conflicts("%gcc@:8", when="@23.04.1_gcc-9.3")
    conflicts("%gcc@:7", when="@23.04.1_gcc-8.2")
    conflicts("%gcc@:6", when="@23.04.1_gcc-7.5")

    conflicts("%gcc@:10", when="@22.1_gcc-11.2")
    conflicts("%gcc@:9", when="@22.1_gcc-10.2")
    conflicts("%gcc@:8", when="@22.1_gcc-9.3")
    conflicts("%gcc@:7", when="@22.1_gcc-8.2")
    conflicts("%gcc@:6", when="@22.1_gcc-7.5")

    conflicts("%gcc@:10", when="@22.0.2_gcc-11.2")
    conflicts("%gcc@:9", when="@22.0.2_gcc-10.2")
    conflicts("%gcc@:8", when="@22.0.2_gcc-9.3")
    conflicts("%gcc@:7", when="@22.0.2_gcc-8.2")
    conflicts("%gcc@:6", when="@22.0.2_gcc-7.5")

    conflicts("%gcc@:10", when="@22.0.1_gcc-11.2")
    conflicts("%gcc@:9", when="@22.0.1_gcc-10.2")
    conflicts("%gcc@:8", when="@22.0.1_gcc-9.3")
    conflicts("%gcc@:7", when="@22.0.1_gcc-8.2")
    conflicts("%gcc@:6", when="@22.0.1_gcc-7.5")

    conflicts("%msvc", msg="Not compatible with MSVC compiler.")

    variant("ilp64", default=False, description="use ilp64 specific Armpl library")
    variant("shared", default=True, description="enable shared libs")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    provides("blas")
    provides("lapack")
    provides("fftw-api@3")

    # Run the installer with the desired install directory
    def install(self, spec, prefix):
        if spec.platform == "darwin":
            hdiutil = which("hdiutil")
            # Mount image
            mountpoint = os.path.join(self.stage.path, "mount")
            if spec.satisfies("@:23"):
                dmg_file = self.stage.archive_file
            else:
                # The archive file only extracts to one .dmg file
                dmg_file = os.path.join(
                    self.stage.source_path, os.listdir(self.stage.source_path)[0]
                )
            hdiutil("attach", "-mountpoint", mountpoint, dmg_file)
            try:
                # Run installer
                exe_name = [f for f in os.listdir(mountpoint) if f.endswith(".sh")][0]
                installer = Executable(os.path.join(mountpoint, exe_name))
                installer("-y", f"--install_dir={prefix}")
            finally:
                # Unmount image
                hdiutil("detach", mountpoint)
            return
        if self.compiler.name != "gcc":
            raise spack.error.SpackError(("Only compatible with GCC.\n"))

        with when("@:22"):
            armpl_version = spec.version.up_to(3).string.split("_")[0]
        with when("@23:"):
            armpl_version = spec.version.string.split("_")[0]

        exe = Executable(
            f"./arm-performance-libraries_{armpl_version}_"
            + f"{get_os_or_pkg_manager(armpl_version)}.sh"
        )
        exe("--accept", "--force", "--install-to", prefix)

    @property
    def lib_suffix(self):
        return get_armpl_suffix(self.spec)

    @property
    def blas_libs(self):
        armpl_prefix = get_armpl_prefix(self.spec)

        libname = "libarmpl" + self.lib_suffix

        # Get ArmPL Lib
        armpl_libs = find_libraries(
            [libname, "libamath", "libastring"],
            root=armpl_prefix,
            shared=self.spec.satisfies("+shared"),
            recursive=True,
        )

        armpl_libs += find_system_libraries(["libm"])

        return armpl_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def fftw_libs(self):
        return self.blas_libs

    @property
    def libs(self):
        return self.blas_libs

    @property
    def headers(self):
        armpl_dir = get_armpl_prefix(self.spec)

        if self.spec.satisfies("@24:"):
            suffix = "include"
        else:
            suffix = "include" + self.lib_suffix

        incdir = join_path(armpl_dir, suffix)

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    def setup_run_environment(self, env):
        armpl_dir = get_armpl_prefix(self.spec)
        if self.spec.platform == "darwin":
            env.prepend_path("DYLD_LIBRARY_PATH", join_path(armpl_dir, "lib"))
        else:
            env.prepend_path("LD_LIBRARY_PATH", join_path(armpl_dir, "lib"))

    @run_after("install")
    def check_install(self):
        armpl_dir = get_armpl_prefix(self.spec)
        suffix = get_armpl_suffix(self.spec)
        armpl_example_dir = join_path(armpl_dir, f"examples{suffix}")

        # run example makefile
        if self.spec.platform == "darwin":
            # Fortran examples on MacOS requires flang-new which is
            # not commonly installed, so only run the C examples.
            make("-C", armpl_example_dir, "ARMPL_DIR=" + armpl_dir, "c_examples")
        else:
            make("-C", armpl_example_dir, "ARMPL_DIR=" + armpl_dir)
        # clean up
        make("-C", armpl_example_dir, "ARMPL_DIR=" + armpl_dir, "clean")

    @run_after("install")
    def make_pkgconfig_files(self):
        if self.spec.satisfies("@:22"):
            # ArmPL pkgconfig files do not have .pc extension and are thus not found by pkg-config
            armpl_dir = get_armpl_prefix(self.spec)
            for f in find(join_path(armpl_dir, "pkgconfig"), "*"):
                symlink(f, f + ".pc")

    def setup_dependent_build_environment(self, env, dependent_spec):
        armpl_dir = get_armpl_prefix(self.spec)
        if self.spec.satisfies("@:22"):
            # pkgconfig directory is not in standard ("lib", "lib64", "share") location
            env.append_path("PKG_CONFIG_PATH", join_path(armpl_dir, "pkgconfig"))
        else:
            env.append_path("PKG_CONFIG_PATH", join_path(armpl_dir, "lib/pkgconfig"))
