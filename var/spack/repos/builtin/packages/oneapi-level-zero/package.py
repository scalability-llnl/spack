# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OneapiLevelZero(CMakePackage):
    """oneAPI Level Zero Loader.

    Applications that need low-level control of a oneAPI level zero
    device link against the loader. The loader depends on a separately
    installed level zero driver. See
    https://dgpu-docs.intel.com/technologies/level-zero.html for
    information on how to install the driver.
    """

    homepage = "https://dgpu-docs.intel.com/technologies/level-zero.html"
    url = "https://github.com/oneapi-src/level-zero/archive/refs/tags/v1.7.15.tar.gz"

    maintainers("rscohn2")

    license("MIT")

    version("1.17.2", sha256="f1b7414f468779a6c422d38bd06b2e5a59d861c9b1af826472724078b49b2277")
    version("1.17.0", sha256="edf820eab84a5f746fee730604f0381c8811f7942302c0835226715e5ae93a25")
    version("1.16.15", sha256="dba50f512c7da81c8d2c487f04c0fcf0ffff79a41f88a90658c96680e7c97be6")
    version("1.16.14", sha256="afd1dfc4db6869a3e252bf15a2a6e1d59b4e511671ebc3e29becd4ac4dc4f03e")
    version("1.16.11", sha256="885bc356d1ecb74e4d3406ece91503d998dd0b4ab484864c38fd41dac588afbb")
    version("1.16.9", sha256="1d348370ba47a7047ae58805a7a33f219d78c8cbb1dd32a0b6c140be66f71d11")
    version("1.16.1", sha256="f341dd6355d8da6ee9c29031642b8e8e4259f91c13c72d318c81663af048817e")
    version("1.16.0", sha256="e5bf9caddeabf58b73252ada5390a78772001d91ec853ee12636811aeb66db41")
    version("1.15.13", sha256="fadda7306dc05c279a9dfc0c60749846351ce5ac7186692201220acb02c59787")
    version("1.15.8", sha256="80663dbd4d01d9519185c6e568f2e836bfea7484363f4da8cf5cf77c3bf58602")
    version("1.15.7", sha256="3f82c83218cc047dc98a3b0767b874964d757b808d9954a2e8949edfcdddbf81")
    version("1.15.1", sha256="aa96edb85a7953041baf8e7d0b0a0e10fa85673e52f5d0466bc2fc802beb9522")
    version("1.15.0", sha256="0472f919435e72d93ef00239694c9380692f923fa1d3bf7e7ba79270cf78291c")
    version("1.14.0", sha256="44b9cfa039625e4d9b273bebda26597a91d34c039ea22311530777ea386cfe6c")
    version("1.13.5", sha256="bb0f37c40b1b2c1eb2c379928314539cac778d3accfc5de66d9f909a2f69fd32")
    version("1.13.1", sha256="9c41640edd3738528911405ffe31c3caa9f9a747c43f6a7375a7b2e77eca3192")
    version("1.13.0", sha256="8966e16f5152d14fed3b2d526d1a75eb99b8ef870499d8375c5d327345d09e48")
    version("1.12.0", sha256="96e6f7ce0179833316f70582ebe4889619349cd4fb1a76efd49a71d8e8ac2e93")
    version("1.11.0", sha256="eee9805bdf0973aff5858a32a8c3ac98e0337b64648d96bb8adeaecc0bdda5bd")
    version("1.10.0", sha256="2811e4128ff6114020d0a147c2769b9b2e782e68ad49827685c33b9e716bf6ab")
    version("1.9.9", sha256="3d1784e790bbaae5f160b920c07e7dc2941640d9c631aaa668ccfd57aafc7b56")
    version("1.9.4", sha256="7f91ed993be1e643c752cf95a319a0fc64113d91ec481fbb8a2f478f433d3380")
    version("1.8.12", sha256="9c5d3dd912882abe8e2e3ba72f8c27e2a2d86759ac48f6318a0df091204985eb")
    version("1.8.8", sha256="3553ae8fa0d2d69c4210a8f3428bd6612bd8bb8a627faf52c3658a01851e66d2")
    version("1.8.5", sha256="b6e9663bbcc53c148d32376998298bec6f7c434ef2218c61fa708963e3a09394")
    version("1.8.1", sha256="de9582ca075dbd207113d432c4d70a2daaf9d6904672c707e340d43cf4e114a5")
    version("1.8.0", sha256="d4089820ed6338ce1616746498bff9383cd9485568190b7977d7c5bf0bf8297b")
    version("1.7.15", sha256="c39bb05a8e5898aa6c444e1704105b93d3f1888b9c333f8e7e73825ffbfb2617")
    version("1.7.9", sha256="b430a7f833a689c899b32172a31c3bca1d16adcad8ff866f240a3a8968433de7")
    version("1.7.4", sha256="23a3f393f6e8f7ed694e0d3248d1ac1b92f2b6964cdb4d747abc23328050513b")
    version("1.6.2", sha256="ef124adc7a011b672e661fbe38873d7db6546c068a4a03610fdc5118b6b6cbf7")
    version("1.5.4", sha256="0332215bd00f49e3cc75cf0cfb0111b5e8b7f41046f0b85e29725f00c26bf750")
    version("1.5", sha256="f93523b412522713bb28d54e2326cac0c342a0cd2662f524c17a65887cf868e8")
    version("1.4.1", sha256="2878fa29cbf5cea677a00f6dde6eb42d147c98c8d2a99fefece284d85cd1476b")
    version("1.3.7", sha256="e84c7f36316257eb46f74b41aef5c37fb593a8821497e45dfeda81aceba0abbc")
    version("1.3.6", sha256="c2b3bd6e4ee3cc874bdcc32bc8705bd217ffc46b194c77e27b23b8391c0c9704")
    version("1.2.3", sha256="69689429fcdaef74fa8395785aca65f5652e410bd6c56f47b2b64692c098892b")

    depends_on("cxx", type="build")  # generated
