# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastjet(AutotoolsPackage):
    """
    A high energy physics software package for jet finding in pp
    and e+e- collisions.
    """

    homepage = "http://fastjet.fr/"
    # The server that hosts fastjet.fr rejects range request
    # which causes spack to fail during fetching. Until this is fixed, use
    # a mirror instead of the upstream url
    # url  = "http://fastjet.fr/repo/fastjet-3.4.0.tar.gz"
    url = "https://lcgpackages.web.cern.ch/tarFiles/sources/fastjet-3.3.4.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan", "vvolkl")

    license("GPL-2.0-only")

    version("3.4.2", sha256="b3d33155b55ce43f420cd6d99b525acf7bdc2593a7bb7ea898a9ddb3d8ca38e3")
    version("3.4.1", sha256="05608c6ff213f06dd9de723813d6b4dccd51e661ac13098f74bfc9eeaf1cb5aa")
    version("3.4.0", sha256="ee07c8747c8ead86d88de4a9e4e8d1e9e7d7614973f5631ba8297f7a02478b91")
    version("3.3.4", sha256="432b51401e1335697c9248519ce3737809808fc1f6d1644bfae948716dddfc03")
    version("3.3.3", sha256="30b0a0282ce5aeac9e45862314f5966f0be941ce118a83ee4805d39b827d732b")
    version("3.3.2", sha256="3f59af13bfc54182c6bb0b0a6a8541b409c6fda5d105f17e03c4cce8db9963c2")
    version("3.3.1", sha256="76bfed9b87e5efdb93bcd0f7779e27427fbe38e05fe908c2a2e80a9ca0876c53")
    version("3.3.0", sha256="e9da5b9840cbbec6d05c9223f73c97af1d955c166826638e0255706a6b2da70f")
    version("3.2.2", sha256="3a70cb6ba64071db49a7eecad821679e1a0dadd84e8abca83e518802b3d876e5")
    version("3.2.1", sha256="c858b6c4f348c3676afa173251bb16d987674e64679a84306510e3963f858d5b")
    version("3.2.0", sha256="96a927f1a336ad93cff30f07e2dc137a4de8ff7d74d5cd43eb455f42cf5275e3")
    version("3.1.3", sha256="9809c2a0c89aec30890397d01eda56621e036589b66d7b3cd196cf087c65e40d")
    version("3.1.2", sha256="dcc834e53da821cbac459c00249d5d18aee6ac866f37551d6a0c60690d3c170b")
    version("3.1.1", sha256="38303789390726803bd3e7b3a245933273e86342d080b82754df44f5168634eb")
    version("3.1.0", sha256="f8dc701dfdb124f009b7614010b911e8cc552655c2a966a7f2608a6caa062263")
    version("3.0.6", sha256="9718f1d014afe4433bc0612a67a050d720c486fcfa7ad9c9b96bf087b0f3da0b")
    version("3.0.5", sha256="0781a5528a0374b3189190abc8e8a2bdfbeaab7ed64e8c74ec0389a86bbabff9")
    version("3.0.4", sha256="8161ea18087cea97de37bd9df2a49895ca1ef72732f5766af7c62738b21ed2c9")
    version("3.0.3", sha256="6a3e5869cf43b325c7222a925e195b2bd624db922958a926cb4211c00882a50d")
    version("3.0.2", sha256="6035a3295253bcd6dd68408985dbedc4a7c5aec13ed1dfa5fdb3cb9229dc6d31")
    version("3.0.1", sha256="4f17c235e73a6fcbc8ee39c15a00f166b701e732033e623625f55fe93220a4ed")
    version("3.0.0", sha256="f63252e3e9d27553c65642ff35d82913b804dfd569d2446c01166882dbf2577f")
    version("2.4.5", sha256="a175849393a3a251b8f92ea9f747b74236dfc83d2786ef5dd92b39c57316a727")
    version("2.4.4", sha256="4d97a8494e9aae7e5738e97d224f5aafb44ae8c5d5021f836d5c8c20fc5030fc")
    version("2.4.3", sha256="0560622140f9f2dfd9e316bfba6a7582c4aac68fbe06f333bd442363f54a3e40")
    version("2.4.2", sha256="504714b8d4895b41c6399347a873bbcf515037d9f5cf3cd5413c9d7aac67f16f")
    version("2.4.1", sha256="764de6c3b9ff3e6d1f48022eb0d536054e7321e73c9f71f7eb1e93f90b6e8ad0")
    version("2.4.0", sha256="96af9b21076be779e686c83a921d4598d93329eb69f9789fe619e27cbad6034a")
    version("2.3.4", sha256="8bd1d9c12866cc768974e9c05c95e00c2fec3c65854ee91b7fb11709db9c5c12")
    version("2.3.3", sha256="c7eadb8ddd956815f3387ed611faae746c05b69b7550de8ae802a00342b159b0")
    version("2.3.2", sha256="ba8b17fcc8edae16faa74608e8da53e87a8c574aa21a28c985ea0dfedcb95210")
    version("2.3.1", sha256="16c32b420e1aa7d0b6fecddd980ea0f2b7e3c2c66585e06f0eb3142677ab6ccf")
    version("2.3.0", sha256="e452fe4a9716627bcdb726cfb0917f46a7ac31f6006330a6ccc1abc43d9c2d53")
    # older version use .tar instead of .tar.gz extension, to be added

    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="plugins=all")
    depends_on("fortran", type="build", when="plugins=pxcone")

    variant("shared", default=True, description="Builds a shared version of the library")
    variant("auto-ptr", default=False, description="Use auto_ptr")
    variant(
        "thread-safety",
        default="limited",
        values=("none", "limited", "full"),
        multi=False,
        when="@3.4.0:",
        description="Enables thread safety",
    )
    variant("atlas", default=False, description="Patch to make random generator thread_local")

    variant(
        "cxxstd",
        default="11",
        values=("11", "17", "20", "23"),
        multi=False,
        description="Use the specified C++ standard when building",
    )

    available_plugins = (
        conditional("atlascone", when="@2.4.0:"),
        conditional("cdfcones", when="@2.1.0:"),
        conditional("cmsiterativecone", when="@2.4.0:"),
        conditional("d0runicone", when="@3.0.0:"),
        conditional("d0runiicone", when="@2.4.0:"),
        conditional("eecambridge", when="@2.4.0:"),
        conditional("gridjet", when="@3.0.0:"),
        conditional("jade", when="@2.4.0:"),
        conditional("nesteddefs", when="@2.4.0:"),
        conditional("pxcone", when="@2.1.0:"),
        conditional("siscone", when="@2.1.0:"),
        conditional("trackjet", when="@2.4.0:"),
    )
    variant(
        "plugins",
        values=disjoint_sets(("all",), ("cxx",), available_plugins)
        .prohibit_empty_set()
        .with_default("all"),
        description="List of plugins to enable, or 'cxx' or 'all'",
    )

    patch("atlas.patch", when="@:3.3 +atlas", level=0)
    patch(
        "https://gitlab.cern.ch/sft/lcgcmake/-/raw/23c82f269b8e5df0190e20b7fbe06db16b24d667/externals/patches/fastjet-3.4.1.patch",
        sha256="1c7eed1d825f2013116778366a2d27b850c46a2848389174f78829fa24cd1c45",
        when="@3.4:3.4.1 +atlas",
        level=0,
    )

    def configure_args(self):
        extra_args = []
        plugins = self.spec.variants["plugins"].value
        if "all" in plugins:
            extra_args += ["--enable-allplugins"]
        elif "cxx" in plugins:
            extra_args += ["--enable-allcxxplugins"]
        else:
            for plugin in self.available_plugins:
                # conditional returns an iterable _ConditionalVariantValues
                for v in plugin:
                    # this version does not support this plugin
                    if not self.spec.satisfies(v.when):
                        continue
                    enabled = v.value in plugins
                    extra_args += [f"--{'enable' if enabled else 'disable'}-{v.value}"]
        extra_args += self.enable_or_disable("shared")
        extra_args += self.enable_or_disable("auto-ptr")
        if self.spec.variants["thread-safety"].value == "limited":
            extra_args += ["--enable-limited-thread-safety"]
        if self.spec.variants["thread-safety"].value == "full":
            extra_args += ["--enable-thread-safety"]

        return extra_args

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            flags.append(f"-std=c++{self.spec.variants['cxxstd'].value}")
        return (None, flags, None)
