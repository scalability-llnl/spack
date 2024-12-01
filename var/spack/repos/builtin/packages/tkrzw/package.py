# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tkrzw(AutotoolsPackage):
    """Tkrzw is a C++ library implementing database managers with various algorithms."""

    homepage = "https://dbmx.net/tkrzw/"
    url = "https://dbmx.net/tkrzw/pkg/tkrzw-0.9.22.tar.gz"
    git = "https://github.com/estraier/tkrzw.git"

    license("Apache-2.0")

    version("master", branch="master")
    version("1.0.29", sha256="abaabd6fc89a19ed8a202ac3711bc3b0763d928bc3a8eeeea73a3679f7e7f790")
    version("0.9.44", sha256="088ac619fbf7fc22c110674b3f8fe8d8573a1d7088e5616b268fd9f68ba25650")
    version("0.9.43", sha256="60f7b579edb4f911ecaf35ff6c07f53b3d566424d8bf179b1991ade5071f0bbc")
    version("0.9.42", sha256="135fb404d5a1b0bcee717f8e648a6f5ff140ec30069fecfde3b380f611356535")
    version("0.9.41", sha256="76e68fb9a7c34eb927224a4a2b755ba4040e7066a42cf930c4f7bc2656c11d83")
    version("0.9.40", sha256="3da034215aabeb371f7553a3e54d2b20ec63d3aa391cef3cef36ba40da7f4bb4")
    version("0.9.39", sha256="a64eea9b05305877c936fb3b231f8924264319ee187545771c56fd08f67af6a8")
    version("0.9.38", sha256="8036a40e2f4d13312ce33ed6bef0121525f1e7acf96900a5540ef3c633cfcf64")
    version("0.9.37", sha256="cf1f1cd5d5e8826f44560ede56b135d396236d843fcf485f2c9feb5ca27e373b")
    version("0.9.36", sha256="370e41b0b10c8b50f8dbe686a2fcb4efad53cfe26dd72739bc8f72ec3f480829")
    version("0.9.35", sha256="5a1703a895f51948a3648ddbe7944dc28593c6746e93eadcd52bf0acd9ad5490")
    version("0.9.34", sha256="0e236e5381400855f678154b794e9e7c33db7677f40e5241dd39e56fcfa640a7")
    version("0.9.33", sha256="ea78e1a0042af8fa447184752e0ee0476a6074ffb77c880337b38d580b734abb")
    version("0.9.32", sha256="be70ad680e5807406e1962133c97da5fdda7ed62df0b2e8d2446bd1daf728f03")
    version("0.9.31", sha256="624f8c03282cd06f46fa4270eb4717680f4779a2b4338c1bbe8b2ea8fb2b48cb")
    version("0.9.30", sha256="fea33337f0115f600afaedf872a828a4f516f4d86e6f6db7a648b03682b2499f")
    version("0.9.29", sha256="120e5d471cd60f9f6c1b7eb25391dd055c4be12b8332124032b0489ad13c6989")
    version("0.9.28", sha256="b2d363c7fa12a44d8f8d38cf97fbeb1bc068b2fcc1de7b628b2c20a22256fce3")
    version("0.9.27", sha256="69d8e7cc998c7f33d6208df721bd5449f2bbf15b1af79186a17864ea36c522f0")
    version("0.9.26", sha256="ee33d48b6aa071db37e4297b478bf5731d9a1289e83ca6c61afaafea78e13387")
    version("0.9.25", sha256="6e2ba961d6963d1d0c572a3a3493dee655202007b133efc25f10b85dfc5f182d")
    version("0.9.24", sha256="23ee06d5d1e359d7c40c834850751a55e5b19c34a4c086e90df1c7bfac7bd4ea")
    version("0.9.23", sha256="43ba9e79b19fe782adf9abfaef7aa40811379ec98c3682313913d07cc9eb29c6")
    version("0.9.22", sha256="f892dcabc87d53086a7c1db129d05dda9c1e6b341d94d438daa8bf6a9e55407c")
    version("0.9.21", sha256="47211285fe41b5697d67eb4c22e850109acb4c657ebbaaf7eb815d3aac5bcc99")
    version("0.9.20", sha256="6750c8539a0c874c2ae673f852b47373f3d688365bd0ef97abb857b02a84095f")
    version("0.9.19", sha256="77c456368c0a0e241a87075bfe6f24a945fd603be5b5c63f6ae8af6f3aa87b3a")
    version("0.9.18", sha256="f1b4151aa932b413380290ab63117ff824006aef6812a6f854a5112969de52c8")
    version("0.9.17", sha256="aa2d40babf275a0b97d81706defaaa5c974724b3c8ffa028b9b46367fe151522")
    version("0.9.16", sha256="2380b3de12ffea78d59249fb3ac3a2b16a4422b3a3282d0afcf450286dc3622d")
    version("0.9.15", sha256="1e0e858c625804ae77c9386d5ded42c62211a356406d9264a4a37473d2f958cd")
    version("0.9.14", sha256="57671a539bb9c0a223e8117c83053aa43fa9050e9231ebef7c6411f65cdaeaa6")
    version("0.9.13", sha256="a6806fd30443cc2bed4539437bd8858b14a38fc81825fe4c49e754b7c133c866")
    version("0.9.12", sha256="6d45a28015012763e55e959a71e6a0a31f808f4f2867784c750f96e16aa50c8b")
    version("0.9.11", sha256="1d93a6966f9ab1f15568ee3d53ac54809f4b73230d0062b4ad65ebb6578f302e")
    version("0.9.10", sha256="6956a33d1ccfca1c290851dc74c625dd6a3c8dc246264c8d686ad89d58f58b25")
    version("0.9.9", sha256="e16cd6b10ce4d97a59958a205ffce7b0db09f49f1b18c437a869fa0ae1279b81")
    version("0.9.8", sha256="5ee485c12060963b49963242545eb28524f8917e27db02def220d35edbba4fa5")
    version("0.9.7", sha256="90e0244b5b67d6142cbe3186564e39676d06024203c34a492b73b17561067a95")
    version("0.9.6", sha256="6194d9fb4c9cb565e05d1fdd0569bd25ba26a987f037aeee226d35145a54d0c2")
    version("0.9.5", sha256="02da0da3f43cc4932851b1b00174acd0835becfda966d5a9f874dc2205e1fb52")
    version("0.9.4", sha256="727a52fc706ee28ef45a0fd6bce8c08911365dd016ccdb4cce7ad3a595b7c0ed")
    version("0.9.3", sha256="945b978402425de6f4cb156544ddf34d928b28100ff93d931816eec3b51be9aa")
    version("0.9.2", sha256="9040af148ab3f35c6f1d4c83f2eba8b68625dbd760f2c0537a9981dbc9bbc661")
    version("0.9.1", sha256="1062502f93d4a9b387372d89265a9ede1704c6bcadd9aac23f5fc8383e26045a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "compression",
        values=any_combination_of("zlib", "lz4", "lzma", "zstd"),
        description="List of supported compression backends",
    )

    depends_on("zlib-api", when="compression=zlib")
    depends_on("lz4", when="compression=lz4")
    depends_on("xz", when="compression=lzma")  # lzma.h is in the xz package, not in lzma
    depends_on("zstd", when="compression=zstd")

    conflicts("compression=zlib", when="@:0.9.29")
    conflicts("compression=lz4", when="@:0.9.29")
    conflicts("compression=lzma", when="@:0.9.29")
    conflicts("compression=zstd", when="@:0.9.29")
    conflicts("%gcc@:7.2.0")  # need C++17 standard

    def configure_args(self):
        spec = self.spec
        args = []
        if "compression=zlib" in spec:
            args.append("--enable-zlib")
        if "compression=lz4" in spec:
            args.append("--enable-lz4")
        if "compression=lzma" in spec:
            args.append("--enable-lzma")
        if "compression=zstd" in spec:
            args.append("--enable-zstd")
        return args
