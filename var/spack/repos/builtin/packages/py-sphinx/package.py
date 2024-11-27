# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinx(PythonPackage):
    """Sphinx Documentation Generator."""

    homepage = "https://www.sphinx-doc.org/en/master/"
    pypi = "Sphinx/sphinx-7.1.0.tar.gz"

    maintainers("adamjstewart")

    license("BSD-2-Clause")

    version("8.1.0", sha256="109454425dbf4c78ecfdd481e56f078376d077edbda29804dba05c5161c8de06")
    version("8.0.2", sha256="0cce1ddcc4fd3532cf1dd283bc7d886758362c5c1de6598696579ce96d8ffa5b")
    version("8.0.1", sha256="7f762c18cfc1d4493e42f4a06a204c1ca55806c53f80a059e208e88d0668d661")
    version("8.0.0", sha256="22551dc8fda6038a422bf1de59d91b31837b66afe45a3f30b2d8cc5aa9337343")

    version("7.4.7", sha256="242f92a7ea7e6c5b406fdc2615413890ba9f699114a9c09192d7dfead2ee9cfe")
    version("7.4.6", sha256="116918d455c493fff3178edea12b4fe1c1e4894680fd81e7b7431ea21d47ca52")
    version("7.4.5", sha256="a4abe5385bf856df094c1e6cadf24a2351b12057be3670b99a12c05a01d209f5")
    version("7.4.4", sha256="43c911f997a4530b6cffd4ff8d5516591f6c60d178591f4406f0dd02282e3f64")
    version("7.4.3", sha256="bd846bcb09fd2b6e94ce3e1ad50f4618bccf03cc7c17d0f3fa87393c0bd9178b")
    version("7.4.2", sha256="946f1a6fa317b02f76deee78392ba712badc01cccd231b5995d933ae3365a151")
    version("7.4.1", sha256="09539a16d74d1850b123cdd0752b9d24f3adc025ff887d611d1010348cd3648c")
    version("7.4.0", sha256="8385520a28dc129ebf8b5fccfa1beb71215fd4455c6d10fa418e08c3c7a2ff9c")
    version("7.3.7", sha256="a4a7db75ed37531c05002d56ed6948d4c42f473a36f46e1382b0bd76ca9627bc")
    version("7.3.6", sha256="fc9f3d13fed5c9a0e677d368090e209899ce5d0081eb552b657e2923e57517f0")
    version("7.3.5", sha256="30d03bbaa53b77d38863fd6b95cc4edb4a84a1512787b3b0c12fb3b4fb25d9e9")
    version("7.3.4", sha256="614826a7cf76f0a4525875c3ed55e2c3618f906897cb7ad53511c5fedcbb35aa")
    version("7.3.3", sha256="1918ba7a7c52f88b5a41ab7e8c55828235994968cfaeb5d10532711e1264087f")
    version("7.3.2", sha256="404a4610689936c2259711e9927174489bac500baa398f31f9ab641e42981e9d")
    version("7.3.1", sha256="9d9e436f536620e13cea3becf107cd5b2fe65922c9fc24d1945543b6657f3468")
    version("7.3.0", sha256="7ad02a0677d43cbaab3f9477355a412e449472d3f4693e2df3842e7ccb7ae7c8")
    version("7.2.6", sha256="9a5160e1ea90688d5963ba09a2dcd8bdd526620edbb65c328728f1b2228d5ab5")
    version("7.2.5", sha256="1a9290001b75c497fd087e92b0334f1bbfa1a1ae7fddc084990c4b7bd1130b88")
    version("7.2.4", sha256="1aeec862bf1edff4374012ac38082e0d1daa066c9e327841a846401164797988")
    version("7.2.3", sha256="ece68bb4d77b7dc090573825db45a6f9183e74098d1c21573485de250b1d1e3f")
    version("7.2.2", sha256="1c0abe6d4de7a6b2c2b109a2e18387bf27b240742e1b34ea42ac3ed2ac99978c")
    version("7.2.1", sha256="dad5e865dcdeb1486f70d8963cc9140561836bb243c311868cf11eb0f741497a")
    version("7.2.0", sha256="da9a84f7456885622bb30ebac42467168396ac2e494182c60dd864aa27405ba3")
    version("7.1.2", sha256="780f4d32f1d7d1126576e0e5ecc19dc32ab76cd24e950228dcf7b1f6d3d9e22f")
    version("7.1.1", sha256="59b8e391f0768a96cd233e8300fe7f0a8dc2f64f83dc2a54336a9a84f428ff4e")
    version("7.1.0", sha256="8f336d0221c3beb23006b3164ed1d46db9cebcce9cb41cdb9c5ecd4bcc509be0")
    version("7.0.1", sha256="61e025f788c5977d9412587e733733a289e2b9fdc2fef8868ddfbfc4ccfe881d")
    version("7.0.0", sha256="283c44aa28922bb4223777b44ac0d59af50a279ac7690dfe945bb2b9575dc41b")

    version("6.2.1", sha256="6d56a34697bb749ffa0152feafc4b19836c755d90a7c59b72bc7dfd371b9cc6b")
    version("6.2.0", sha256="9ef22c2941bc3d0ff080d25a797f7521fc317e857395c712ddde97a19d5bb440")
    version("6.1.3", sha256="0dac3b698538ffef41716cf97ba26c1c7788dba73ce6f150c1ff5b4720786dd2")
    version("6.1.2", sha256="19678b91c1f4e2025cfe3bfcbf473ffa3b086651bbdd43d6816e16e4cc58a8b4")
    version("6.1.1", sha256="6a8e43b5030b9870d7402fb56f5efeebb83b76d65bf1c567a89b555340e127b2")
    version("6.1.0", sha256="b0fd0a1993733492572bbd429b5ec081e17c082b5b5168ffae50524c3a90fd3c")
    version("6.0.1", sha256="6217d768c3c865769c1561ea31c2f27d3bea413c9b0e1fd4722811ea148a4a46")
    version("6.0.0", sha256="58c140ecd9aa0abbc8ff6da48a266648eac9e5bfc8e49576efd2979bf46f5961")

    version("5.3.0", sha256="51026de0a9ff9fc13c05d74913ad66047e104f56a129ff73e174eb5c3ee794b5")
    version("5.2.3", sha256="5b10cb1022dac8c035f75767799c39217a05fc0fe2d6fe5597560d38e44f0363")
    version("5.2.2", sha256="7225c104dc06169eb73b061582c4bc84a9594042acae6c1582564de274b7df2f")
    version("5.2.1", sha256="c009bb2e9ac5db487bcf53f015504005a330ff7c631bb6ab2604e0d65bae8b54")
    version("5.2.0", sha256="1790c2098937dcfa7871c9d102c24eccd4a8b883b67c5c1e26892fb52d102542")
    version("5.1.1", sha256="ba3224a4e206e1fbdecf98a4fae4992ef9b24b85ebf7b584bb340156eaf08d89")
    version("5.1.0", sha256="7893d10d9d852c16673f9b1b7e9eda1606b420b7810270294d6e4b44c0accacc")
    version("5.0.2", sha256="b18e978ea7565720f26019c702cd85c84376e948370f1cd43d60265010e1c7b0")
    version("5.0.1", sha256="f4da1187785a5bc7312cc271b0e867a93946c319d106363e102936a3d9857306")
    version("5.0.0", sha256="464d9c1bd5613bcebe76b46658763f3f3dbb184da7406e632a84596d3cd8ee90")

    version("4.5.0", sha256="7bf8ca9637a4ee15af412d1a1d9689fec70523a68ca9bb9127c2f3eeb344e2e6")
    version("4.4.0", sha256="6caad9786055cb1fa22b4a365c1775816b876f91966481765d7d50e9f0dd35cc")
    version("4.3.2", sha256="0a8836751a68306b3fe97ecbe44db786f8479c3bf4b80e3a7f5c838657b4698c")
    version("4.3.1", sha256="32a5b3e9a1b176cc25ed048557d4d3d01af635e6b76c5bc7a43b0a34447fbd45")
    version("4.3.0", sha256="6d051ab6e0d06cba786c4656b0fe67ba259fe058410f49e95bee6e49c4052cbf")
    version("4.2.0", sha256="94078db9184491e15bce0a56d9186e0aec95f16ac20b12d00e06d4e36f1058a6")
    version("4.1.2", sha256="3092d929cd807926d846018f2ace47ba2f3b671b309c7a89cd3306e80c826b13")
    version("4.1.1", sha256="23c846a1841af998cb736218539bb86d16f5eb95f5760b1966abcd2d584e62b8")
    version("4.1.0", sha256="4219f14258ca5612a0c85ed9b7222d54da69724d7e9dd92d1819ad1bf65e1ad2")
    version("4.0.3", sha256="dff357e6a208eb7edb2002714733ac21a9fe597e73609ff417ab8cf0c6b4fbb8")
    version("4.0.2", sha256="b5c2ae4120bf00c799ba9b3699bc895816d272d120080fbc967292f29b52b48c")
    version("4.0.1", sha256="cf5104777571b2b7f06fa88ee08fade24563f4a0594cf4bd17d31c47b8740b4c")
    version("4.0.0", sha256="b246ebd74f5fb966d7e90086bbda5ed74ee4d30b4c3cbefddc1fb5210aa317c7")

    version("3.5.4", sha256="19010b7b9fa0dc7756a6e105b2aacd3a80f798af3c25c273be64d7beeb482cb1")
    version("3.4.1", sha256="e450cb205ff8924611085183bf1353da26802ae73d9251a8fcdf220a8f8712ef")
    version("3.2.0", sha256="cf2d5bc3c6c930ab0a1fbef3ad8a82994b1bf4ae923f8098a05c7e5516f07177")
    version("3.0.0", sha256="6a099e6faffdc3ceba99ca8c2d09982d43022245e409249375edf111caf79ed3")

    version("2.4.4", sha256="b4c750d546ab6d7e05bdff6ac24db8ae3e8b8253a3569b754e445110a0a12b66")
    version("2.2.0", sha256="0d586b0f8c2fc3cc6559c5e8fd6124628110514fda0e5d7c82e682d749d2e845")

    version("1.8.5", sha256="c7658aab75c920288a8cf6f09f244c6cfdae30d82d803ac1634d9f223a80ca08")
    version("1.8.4", sha256="c1c00fc4f6e8b101a0d037065043460dffc2d507257f2f11acaed71fd2b0c83c")
    version("1.8.2", sha256="120732cbddb1b2364471c3d9f8bfd4b0c5b550862f99a65736c77f970b142aea")
    version("1.7.4", sha256="e9b1a75a3eae05dded19c80eb17325be675e0698975baae976df603b6ed1eb10")
    version("1.6.3", sha256="af8bdb8c714552b77d01d4536e3d6d2879d6cb9d25423d29163d5788e27046e6")
    version("1.6.1", sha256="7581d82c3f206f0ac380edeeba890a2e2d2be011e5abe94684ceb0df4b6acc3f")
    version("1.5.5", sha256="4064ea6c56feeb268838cb8fbbee507d0c3d5d92fa63a7df935a916b52c9e2f5")
    version("1.4.5", sha256="c5df65d97a58365cbf4ea10212186a9a45d89c61ed2c071de6090cdf9ddb4028")
    version("1.3.1", sha256="1a6e5130c2b42d2de301693c299f78cc4bd3501e78b610c08e45efc70e2b5114")

    depends_on("py-flit-core@3.7:", when="@5.2:", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@8:")
        depends_on("python@3.9:", when="@7.2:")
        depends_on("python@3.8:", when="@6:")
        depends_on("py-sphinxcontrib-applehelp@1.0.7:", when="@8.1:")
        depends_on("py-sphinxcontrib-applehelp", when="@2:")
        depends_on("py-sphinxcontrib-devhelp@1.0.6:", when="@8.1:")
        depends_on("py-sphinxcontrib-devhelp", when="@2:")
        depends_on("py-sphinxcontrib-htmlhelp@2.0.6:", when="@8.1:")
        depends_on("py-sphinxcontrib-htmlhelp@2:", when="@4.1.1:")
        depends_on("py-sphinxcontrib-htmlhelp", when="@2:")
        depends_on("py-sphinxcontrib-jsmath@1.0.1:", when="@8.1:")
        depends_on("py-sphinxcontrib-jsmath", when="@2:")
        depends_on("py-sphinxcontrib-qthelp@1.0.6:", when="@8.1:")
        depends_on("py-sphinxcontrib-qthelp", when="@2:")
        depends_on("py-sphinxcontrib-serializinghtml@1.1.9:", when="@7.2.3:")
        depends_on("py-sphinxcontrib-serializinghtml@1.1.5:", when="@4.1.1:")
        depends_on("py-sphinxcontrib-serializinghtml", when="@2:")
        depends_on("py-jinja2@3.1:", when="@7.4:")
        depends_on("py-jinja2@3:", when="@5.2:")
        depends_on("py-jinja2@2.3:2", when="@:4.0.1")
        depends_on("py-jinja2@2.3:")
        depends_on("py-pygments@2.17:", when="@7.4:")
        depends_on("py-pygments@2.14:", when="@7.2:")
        depends_on("py-pygments@2.13:", when="@6.0.1:")
        depends_on("py-pygments@2.12:", when="@5.2:")
        depends_on("py-pygments@2:")
        depends_on("py-docutils@0.20:0.21", when="@7.4:")
        depends_on("py-docutils@0.18.1:0.21", when="@7.3")
        depends_on("py-docutils@0.18.1:0.20", when="@7.0.1:7.2")
        depends_on("py-docutils@0.18.1:0.19", when="@6.2:7.0.0")
        depends_on("py-docutils@0.18:0.19", when="@6.0:6.1")
        depends_on("py-docutils@0.14:0.19", when="@5.1:5")
        depends_on("py-docutils@0.14:0.18", when="@5.0")
        depends_on("py-docutils@0.14:0.17", when="@4")
        depends_on("py-docutils@0.12:0.16", when="@:3")
        depends_on("py-snowballstemmer@2.2:", when="@7.4:")
        depends_on("py-snowballstemmer@2:", when="@5.2:")
        depends_on("py-snowballstemmer@1.1:")
        depends_on("py-babel@2.13:", when="@7.4:")
        depends_on("py-babel@2.9:", when="@5.2:")
        depends_on("py-babel@1.3:")
        depends_on("py-alabaster@0.7.14:", when="@8:")
        depends_on("py-alabaster@0.7.14:0.7", when="@7.3:7.4")
        depends_on("py-alabaster@0.7", when="@:7.2")
        depends_on("py-imagesize@1.3:", when="@5.2:")
        depends_on("py-imagesize", when="@1.4:")
        depends_on("py-requests@2.30:", when="@7.4:")
        depends_on("py-requests@2.25:", when="@6:")
        depends_on("py-requests@2.5:", when="@2:")
        depends_on("py-requests@2.4:", when="@1.5.2:")
        depends_on("py-packaging@23:", when="@7.4:")
        depends_on("py-packaging@21:", when="@5.2:")
        depends_on("py-packaging", when="@1.7:")
        depends_on("py-tomli@2:", when="@7.3.1: ^python@:3.10")
        depends_on("py-colorama@0.4.6:", when="@7.4: platform=windows")
        depends_on("py-colorama@0.4.5:", when="@5.2: platform=windows")
        depends_on("py-colorama@0.3.5:", when="platform=windows")

    # Historical dependencies
    depends_on("py-setuptools", when="@4.4:5.1", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-importlib-metadata@6:", when="@7.4: ^python@:3.9")
        depends_on("py-importlib-metadata@4.8:", when="@5.2: ^python@:3.9")
        depends_on("py-importlib-metadata@4.4:", when="@4.4: ^python@:3.9")
        depends_on("py-setuptools", when="@:4.3")
        depends_on("py-sphinxcontrib-websupport", when="@1.6:1")
        depends_on("py-six@1.5:", when="@:1")
        depends_on("py-sphinx-rtd-theme@0.1:", when="@:1.3")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/S/Sphinx/{}-{}.tar.gz"
        if version >= Version("7.1"):
            name = "sphinx"
        else:
            name = "Sphinx"
        return url.format(name, version)
