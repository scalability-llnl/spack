# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Package automatically generated using 'pip2spack' converter


class PyPyro4(PythonPackage):
    """
    distributed object middleware for Python (RPC)
    """

    homepage = "http://pyro4.readthedocs.io"
    pypi = "Pyro4/Pyro4-4.81.tar.gz"
    maintainers("liuyangzhuan")

    license("MIT")

    version("4.81", sha256="e130da06478b813173b959f7013d134865e07fbf58cc5f1a2598f99479cdac5f")
    version("4.80", sha256="46847ca703de3f483fbd0b2d22622f36eff03e6ef7ec7704d4ecaa3964cb2220")
    version("4.79", sha256="b1eb34c9a1e63f731ca480f3e2c48169341a25a7504397badbaaab07e0f3241e")
    version("4.78", sha256="b69200747c4c69bfa6fa8b917806b0a9ee7939daaf67ab9bb5ccac7e5179feee")
    version("4.77", sha256="2bfe12a22f396474b0e57c898c7e2c561a8f850bf2055d8cf0f7119f0c7a523f")
    version("4.76", sha256="ac1fda8d3fd9b5ff2cb8e7e400f95a1b1ae28c5df1aa82d1833a5a898e476334")
    version("4.75", sha256="3897c0254046d4cb412a4d1a8f2f9c2c1c1ae643a24db07d0abdb51acdb8d7b5")
    version("4.74", sha256="89ed7b12c162e5124f322f992f9506c44f5e1a379926cf01ee73ef810d3bf75f")
    version("4.73", sha256="536b07a097d0619e7ab1effa3747fda177a24168d17a07a93ca9ac30977608f7")
    version("4.72", sha256="2766b53db49f70b0d047fa6871aeb47484ba7e50cf53cfa37d26f87742c0b6a8")
    version("4.71", sha256="78b686b584c180061fe3cfc3adcad4da46b3a7f42be1f9f0d7491cd006541cf3")
    version("4.70", sha256="614dc4a7a79a861ee15215a6e60081950b2790b7b5cc91555ebeec75d8444aa5")
    version("4.63", sha256="67d2b34156619ba37e92100af95aade8129dd2b7327eb05821d43887451f7d7b")
    version("4.62", sha256="e301edfb2bc47768b7222a68cae8de8be796d1d9f61cdbd1af9039985ed5009c")
    version("4.61", sha256="c465cb2ea2a90b887988d4249de8c0566bdfb16101fdc570e07e598a92e94d1e")
    version("4.60", sha256="52fa5fe8173d234f57b6ca3214df3f34e88356c94081685db6249bff8f0b4f7f")
    version("4.59", sha256="6a39dadbd2a83b6fd5ab7f5402f8a4befd467b5c0404b8610a8797f748b72a38")
    version("4.58", sha256="2c6d133bcec6039a681475bc878ec98c598ccd33105c1994c7b5217932ee2c0c")
    version("4.57", sha256="fb3bf07951c2942b5f955770d50c0152565f0da79a2c1a359cfe2062fe0a82b2")
    version("4.56", sha256="a80c27e1debbd8d8725ee4a8f0d30cf831dde5e80b04bfa9c912932c4c13d6aa")
    version("4.55", sha256="49a7a142542d87dde1cecc8d3ee048ec9481ba861d61234d219fadd06e6ced96")
    version("4.54", sha256="aede879916c0f6e84e560b38af421c24cb5089b66c8f632aa5ac48b20ecde93a")
    version("4.53", sha256="c6ca6461472a74a7608a2247413b66e951889351fcf8e9eed5d7232ae844b702")
    version("4.52", sha256="449f4bdf8dcbaca90e6436eb40c4e860b0de47346e2c7735d0584496d28451e5")
    version("4.51", sha256="d6508b8c70d612356a8ddbe486890b03d840c37b5f7cd8e9366bc4c0dd44d3e6")
    version("4.50", sha256="cb199540c2ceae9d67d5f2b20dc002d93f909d5072c3da4381c119d7a4b6d1cf")
    version("4.49", sha256="6ae7fb0ce9ae5ca6f1d32487d8606219e7296ae7d22e650e7f9db63399608b76")
    version("4.48", sha256="3115def913cf6035000047bb270efefb55a25449a17ed392afde6fd531c82fd2")
    version("4.47", sha256="9354b722f9f5965ade5839241c8d7ff06ec2fac678a2c9e197a63966da241c89")
    version("4.46", sha256="165ed717275217448d786f9c15777eca889f5344d54eef9482996dfee01b668b")
    version("4.45", sha256="e32d3f32e52d84e3456c0d389a115b5430a8bb14dd01336c627355a2f34dba78")
    version("4.43", sha256="b6f924fa74f21d14c851450e157711914a402bfc2f3a880c1b2c275fd4cda6d6")
    version("4.42", sha256="03951643015a1537ad82fbf99fba6e208007447404aab1a020dce7216120d32a")
    version("4.41", sha256="3af4749140e9d4032632277ac19e7fd4761856d2df0f0643c574d1e7174a9703")
    version("4.40", sha256="00423d3710f60b2da146075a59e17bfa837f556ed2c8acafe05bc209dcaac3e9")
    version("4.39", sha256="39c6ca7f86b0f0bebfeada687a5a8b99f66470a52b0f815195ae63c683266f24")
    version("4.38", sha256="837fb552f54e46e54a13fa03c321073ba8373715346c4bc7e522b2c82a2c75c9")
    version("4.37", sha256="2c4c9e7c3dbace3c75524324b6a686381be37bebab89b5001c0670418cec89c7")
    version("4.36", sha256="fcbfbe22b044440fab3d6cbee11d18532b63accefe9cc30b2c41994cdeb08829")
    version("4.35", sha256="97ef658b96fa10bac3e01097b1e2b6630fea2b307081ec6f2ac00f85e6020178")
    version("4.34", sha256="36886e660290aa5afd06f735f587717f7f366b3535b7b0d3082b4e99ded9dc37")
    version("4.33", sha256="9c01202190b7cdebe629e13abb70f050f421139f8115d1626321f442a9f54df8")
    version("4.32", sha256="736eb96801881a61b9da72dced2d49574067443545892355af94411392526902")
    version("4.31", sha256="0fd9342a216299ff24761e641714c7bd3e42c364f277eb3600d40085f4ace6c3")
    version("4.30", sha256="1b38a52dd89cc6aee145d23bd74f586c73268938c6f346b20583ee0242d7d170")
    version("4.29", sha256="3a17eaea8055962ff35bb9117f0860243d7977c34cbfcafc76e8e26309e339cf")
    version("4.28", sha256="a094cb12e4e328e8b3b06bb313212f1826208c107fa6b48cf02f0ccdc32b562b")
    version("4.27", sha256="ee32544fb04e7f4a2d223b442b306bd67cc900b7e9b5917f0b33d1979e6db34f")
    version("4.26", sha256="213145815f00b6855b1ba71c20e78fd1d3c41595fae270308483cdba8d3fcec6")
    version("4.25", sha256="ac2b0123badcb76c63eb716fcd95e0ee4021d345b5db05fda19253c59e39b384")
    version("4.24", sha256="24d2ceaabbd886981d0df56f8f7e5f7f1a9db173778baa4965605f6880c90eb8")
    version("4.23", sha256="57d6feee20a565f9de3302376a2531cfda50755088442102963b16e6f70b2e3b")
    version("4.22", sha256="d8f611f384edbd240006d8c0f56135e74199ab88e9416cfc78cf5472f1ff337d")
    version("4.21", sha256="96bc4bdccab27d935a44f1d9a8df94986d4b3361f5ff9382e86300ed5b9fdfa2")
    version("4.20", sha256="72d3fb6dc653e6ae36bd47f2667fbff3c587c72f8bfb3f0dcb1763ee86c906f8")
    version("4.18", sha256="52d7f6e10c44475052ac8b6828ed6f8b728a1c5d7e674b441eb0e930029ea4cd")
    version("4.17", sha256="1d0cecdd3340dca695d6f833830e7a59f937d4bedbcff53109abe66e5a65d22c")
    version("4.16", sha256="6a996700b877d268b48f91f91e356d2a4b20cb12207c05943d04504f6a0de0c7")
    version("4.15", sha256="7b9dc43d6be79e4e542b8520715cb3ab7f9095afccc93bce9cacc271c665bf7d")
    version("4.14", sha256="90c4f84ae9932d66825c61af9cd67b0b2877b477c967812a5d6953d67f3b003d")
    version("4.13", sha256="afbc6964e593e7efed3fa5c91af45c4491cfdb994e7fdbe285cbb3719162cb90")
    version("4.12", sha256="69f1beeafbe8f27bdac18e29ce97dd63cc1bdf847ff221ed0a6f0042047fa237")
    version("4.11", sha256="d84ccfe85b14b3cb086f98d70dbf05671d6cb8498bd6f20f0041d6010dd320da")
    version("4.10", sha256="de74e5e020a8a26cd357f5917afb48f7e14e161ca58574a1c653441bdbe9711c")

    depends_on("py-setuptools", type="build")
    depends_on("py-serpent@1.27:", type=("build", "run"))
