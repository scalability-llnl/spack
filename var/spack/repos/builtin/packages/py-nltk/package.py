# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNltk(PythonPackage):
    """The Natural Language Toolkit (NLTK) is a Python package for
    natural language processing."""

    homepage = "https://www.nltk.org/"
    pypi = "nltk/nltk-3.5.zip"

    license("Apache-2.0")

    version("3.9.1", sha256="87d127bd3de4bd89a4f81265e5fa59cb1b199b27440175370f7417d2bc7ae868")
    version("3.8.1", sha256="1834da3d0682cba4f2cede2f9aad6b0fafb6461ba451db0efb6f9c39798d64d3")
    version("3.5", sha256="845365449cd8c5f9731f7cb9f8bd6fd0767553b9d53af9eb1b3abf7700936b35")

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/n/nltk/nltk-{0}.{1}"
        extension = "zip"
        if version >= Version("3.9.1"):
            extension = "tar.gz"
        return url.format(version.dotted, extension)

    maintainers("meyersbs")

    variant("data", default=False, description="Download the NLTK data")

    depends_on("python@3.8:", when="@3.9.1:", type=("build", "run"))
    depends_on("python@3.7:", when="@3.8.1:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-regex@2021.8.3:", when="@3.8.1:", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))

    resource(
        name="perluniprops",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/misc/perluniprops.zip",
        when="+data",
        sha256="57d54f591c4ed299b3cdf348eecf774ab2858f19e66955352d94ae555e2050ef",
        destination="nltk_data/misc",
        placement="perluniprops",
    )

    resource(
        name="mwa_ppdb",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/misc/mwa_ppdb.zip",
        when="+data",
        sha256="65f70300d720a280eb19899b222c94a630be5e378f01a658cc0a4bb50fa50b41",
        destination="nltk_data/misc",
        placement="mwa_ppdb",
    )

    resource(
        name="punkt",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip",
        when="+data@:3.8.1",
        sha256="51c3078994aeaf650bfc8e028be4fb42b4a0d177d41c012b6a983979653660ec",
        destination="nltk_data/tokenizers",
        placement="punkt",
    )

    resource(
        name="punkt_tab",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt_tab.zip",
        when="+data@3.8.2:",
        sha256="c2b16c23d738effbdc5789d7aa601397c13ba2819bf922fb904687f3f16657ed",
        destination="nltk_data/tokenizers",
        placement="punkt_tab",
    )

    resource(
        name="rslp",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/stemmers/rslp.zip",
        when="+data",
        sha256="f482f9666a2a76cdd4acab16b01a44b002550ebaac29906dbd5a1bbc281e4f8b",
        destination="nltk_data/stemmers",
        placement="rslp",
    )

    resource(
        name="porter_test",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/stemmers/porter_test.zip",
        when="+data",
        sha256="7760e1ae3a7a975d0b67f8afd9a0a53a29f94da73508b525d1b6e08205924669",
        destination="nltk_data/stemmers",
        placement="porter_test",
    )

    resource(
        name="snowball_data",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/stemmers/snowball_data.zip",
        when="+data",
        sha256="e8a05c19890f8651df2b958b0f6e318d4476b8a500e26ed63f89077aed0585a2",
        destination="nltk_data/stemmers",
        placement="snowball_data",
    )

    resource(
        name="maxent_ne_chunker",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/chunkers/maxent_ne_chunker.zip",
        when="+data",
        sha256="b7cdb936c551c06ef2cdc6227238c5ccc9c8c5259a11f99f4a937419d52af61b",
        destination="nltk_data/chunkers",
        placement="maxent_ne_chunker",
    )

    resource(
        name="moses_sample",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/models/moses_sample.zip",
        when="+data",
        sha256="0639dfa1d1939295d29c3d57478b1eb7767405dc916effe2cf6a90071943f7e8",
        destination="nltk_data/models",
        placement="moses_sample",
    )

    resource(
        name="bllip_wsj_no_aux",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/models/bllip_wsj_no_aux.zip",
        when="+data",
        sha256="e00339b708f23c24b5cf67ff3db5711dd4d80b21083f52787cf167bf77ac2126",
        destination="nltk_data/models",
        placement="bllip_wsj_no_aux",
    )

    resource(
        name="word2vec_sample",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/models/word2vec_sample.zip",
        when="+data",
        sha256="d29ff84a6ceca407f8578648568c55894dac34641ceb1fa02f920264fe326b43",
        destination="nltk_data/models",
        placement="word2vec_sample",
    )

    resource(
        name="wmt15_eval",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/models/wmt15_eval.zip",
        when="+data",
        sha256="56ea67e320f75be1abdee60b9d57aef1bd50324edd176e11c3c40f451043c80e",
        destination="nltk_data/models",
        placement="wmt15_eval",
    )

    resource(
        name="spanish_grammars",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/grammars/spanish_grammars.zip",
        when="+data",
        sha256="4207035d8795d37000c06391d97b068ae470a43db697d96473018f392552b742",
        destination="nltk_data/grammars",
        placement="spanish_grammars",
    )

    resource(
        name="sample_grammars",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/grammars/sample_grammars.zip",
        when="+data",
        sha256="8c3e4fecdc47ef1d262401eda08bde995cf4ed912a7934a32905263485240872",
        destination="nltk_data/grammars",
        placement="sample_grammars",
    )

    resource(
        name="large_grammars",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/grammars/large_grammars.zip",
        when="+data",
        sha256="5a81e5278757fafe6e8f19b16f6e4363783635ee332c5c238a30e190f735da59",
        destination="nltk_data/grammars",
        placement="large_grammars",
    )

    resource(
        name="book_grammars",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/grammars/book_grammars.zip",
        when="+data",
        sha256="cc63b32d680888c04b3c332218d645a9f9db8571ffe7229808391c889796ffbd",
        destination="nltk_data/grammars",
        placement="book_grammars",
    )

    resource(
        name="basque_grammars",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/grammars/basque_grammars.zip",
        when="+data",
        sha256="40ec8a0e92079f32a6900189e8551909506e727b19652f28641fcd825a374ec7",
        destination="nltk_data/grammars",
        placement="basque_grammars",
    )

    resource(
        name="maxent_treebank_pos_tagger",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/taggers/maxent_treebank_pos_tagger.zip",
        when="+data",
        sha256="6ba605d803ad5e9aeb604dc9c82573afd44e9c9ad1f228788eb05ddd88ef0b24",
        destination="nltk_data/taggers",
        placement="maxent_treebank_pos_tagger",
    )

    resource(
        name="averaged_perceptron_tagger",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/taggers/averaged_perceptron_tagger.zip",
        when="+data",
        sha256="e1f13cf2532daadfd6f3bc481a49859f0b8ea6432ccdcd83e6a49a5f19008de9",
        destination="nltk_data/taggers",
        placement="averaged_perceptron_tagger",
    )

    resource(
        name="averaged_perceptron_tagger_ru",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/taggers/averaged_perceptron_tagger_ru.zip",
        when="+data",
        sha256="82a4ec6fd815dcee0fe6e150aed8fefa0ae501eba6e62b94fafbfc089af8954b",
        destination="nltk_data/taggers",
        placement="averaged_perceptron_tagger_ru",
    )

    resource(
        name="universal_tagset",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/taggers/universal_tagset.zip",
        when="+data",
        sha256="d490e1ae8f5625dcdfdda04be15c22a2aade8c2561a36a61edcdf0c7d6aa8352",
        destination="nltk_data/taggers",
        placement="universal_tagset",
    )

    resource(
        name="vader_lexicon",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/sentiment/vader_lexicon.zip",
        when="+data",
        sha256="8adba4294eef3964d820bf655e37e61bdc3a341994356af59b74fb3b4a36ce5c",
        destination="nltk_data/sentiment",
        placement="vader_lexicon",
    )

    resource(
        name="lin_thesaurus",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/lin_thesaurus.zip",
        when="+data",
        sha256="04ebd29f0ad826700241b608f739bb8b9098c8de998f4a903535de5c3240c0a9",
        destination="nltk_data/corpora",
        placement="lin_thesaurus",
    )

    resource(
        name="movie_reviews",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/movie_reviews.zip",
        when="+data",
        sha256="a41211ae685019137410268134db6a1a14428c89b671eb83056151a878539008",
        destination="nltk_data/corpora",
        placement="movie_reviews",
    )

    resource(
        name="problem_reports",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/problem_reports.zip",
        when="+data",
        sha256="f9e691dcf5eed49827d892b1fc9eb6d73ca2cfa3d5c555fed316990ea6d15c8a",
        destination="nltk_data/corpora",
        placement="problem_reports",
    )

    resource(
        name="pros_cons",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/pros_cons.zip",
        when="+data",
        sha256="b5bca541ba5b2e614cde2213ddcca027416f6997067c90e45c173bf55c6fade8",
        destination="nltk_data/corpora",
        placement="pros_cons",
    )

    resource(
        name="masc_tagged",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/masc_tagged.zip",
        when="+data",
        sha256="678a5141cf3381bedb1839c58a330507337be07c7c71603279c0ef5337032304",
        destination="nltk_data/corpora",
        placement="masc_tagged",
    )

    resource(
        name="sentence_polarity",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/sentence_polarity.zip",
        when="+data",
        sha256="6e1ed4405b65c7eabf1d199a7f7c437091ac21da0ea7467b410a74062574566b",
        destination="nltk_data/corpora",
        placement="sentence_polarity",
    )

    resource(
        name="webtext",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/webtext.zip",
        when="+data",
        sha256="9e32dbae4879464b8f420a0dc721855bb26167b720d7695588d2ca2aeadf501a",
        destination="nltk_data/corpora",
        placement="webtext",
    )

    resource(
        name="nps_chat",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/nps_chat.zip",
        when="+data",
        sha256="a4433d5da5e62fdbede49efa572a53a0139fff1014ffbe86cb263e17cbb4a837",
        destination="nltk_data/corpora",
        placement="nps_chat",
    )

    resource(
        name="city_database",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/city_database.zip",
        when="+data",
        sha256="df142032cac15d388171d018531ba9038fd48293567901ad56b378a40e1f8dfe",
        destination="nltk_data/corpora",
        placement="city_database",
    )

    resource(
        name="europarl_raw",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/europarl_raw.zip",
        when="+data",
        sha256="ad553e177baac263840c10980e6f3e76d5d15f7f7a078bd98520b36edb69b27c",
        destination="nltk_data/corpora",
        placement="europarl_raw",
    )

    resource(
        name="biocreative_ppi",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/biocreative_ppi.zip",
        when="+data",
        sha256="d30fe4ac6e2b71a15376401de7cd5bde1252deb28d3d45920ab740281e78e74b",
        destination="nltk_data/corpora",
        placement="biocreative_ppi",
    )

    resource(
        name="verbnet3",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/verbnet3.zip",
        when="+data",
        sha256="fa0136a7699c52f0bd532dc5adc0914745aa4369a52ae1465cb11841060ec1de",
        destination="nltk_data/corpora",
        placement="verbnet3",
    )

    resource(
        name="pe08",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/pe08.zip",
        when="+data",
        sha256="3a4aa7d07cf89afbc8894b9d2f68239ad8452d4e815ad4b3f5824f13425227dd",
        destination="nltk_data/corpora",
        placement="pe08",
    )

    resource(
        name="pil",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/pil.zip",
        when="+data",
        sha256="0538ee1d94de616004fd2434cf03840dffab5507cf8b56725b6ef82b572deb76",
        destination="nltk_data/corpora",
        placement="pil",
    )

    resource(
        name="crubadan",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/crubadan.zip",
        when="+data",
        sha256="8d64c8ff52f47a44381cad0795cf7fe3f8ff7907a1f92c09aadef8e163efdbc7",
        destination="nltk_data/corpora",
        placement="crubadan",
    )

    resource(
        name="gutenberg",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gutenberg.zip",
        when="+data",
        sha256="2d3c3ab548c653944310f37f536443ec85d0a0ad855fcae217a0c9efdce2d611",
        destination="nltk_data/corpora",
        placement="gutenberg",
    )

    resource(
        name="propbank",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/propbank.zip",
        when="+data",
        sha256="320eee3cd06a15b5daac578d494ae109dc2414d9ea941bf9cc514796b6b1547a",
        destination="nltk_data/corpora",
        placement="propbank",
    )

    resource(
        name="machado",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/machado.zip",
        when="+data",
        sha256="772463b1553c1b0ff1fc0360768b31f59b488f7a52d44cc92c3e31ca289acce9",
        destination="nltk_data/corpora",
        placement="machado",
    )

    resource(
        name="state_union",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/state_union.zip",
        when="+data",
        sha256="366c1dc82b2abf896f42b2ec50ba802a0141a29f75d29ca48a7a243ce5bfbe8d",
        destination="nltk_data/corpora",
        placement="state_union",
    )

    resource(
        name="twitter_samples",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/twitter_samples.zip",
        when="+data",
        sha256="aac71c20e1e05003b7812321936c5635dfede61902aca2b94419a1124979c6dd",
        destination="nltk_data/corpora",
        placement="twitter_samples",
    )

    resource(
        name="semcor",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/semcor.zip",
        when="+data",
        sha256="126fa2e829ab63edd5b3fd9de45ef1d60d6880e01e25abc55b5ac7918a824655",
        destination="nltk_data/corpora",
        placement="semcor",
    )

    resource(
        name="wordnet31",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet31.zip",
        when="+data",
        sha256="2a9e7da7d0c17ad875e4171a4d28ae17ab6969c7d67f1cf0f59d65c66d0fdd37",
        destination="nltk_data/corpora",
        placement="wordnet31",
    )

    resource(
        name="extended_omw",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/extended_omw.zip",
        when="+data",
        sha256="c59b90f2902c351eeb0ce97a49a1b7cf73d4e2f5b05cbda0e903eb20b5ee168a",
        destination="nltk_data/corpora",
        placement="extended_omw",
    )

    resource(
        name="names",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/names.zip",
        when="+data",
        sha256="0eec7e958b34982662b8f05824ae64642dea097b08057ade65c252191c5fe7ca",
        destination="nltk_data/corpora",
        placement="names",
    )

    resource(
        name="ptb",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/ptb.zip",
        when="+data",
        sha256="f73b6a584bc7907cdd694d0661655a2e76a82ca74dc9bdae757236918d416bf7",
        destination="nltk_data/corpora",
        placement="ptb",
    )

    resource(
        name="nombank.1.0",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/nombank.1.0.zip",
        when="+data",
        sha256="eb7c4228bdaf6d528630db60f818e53dd69d4ef7a5722f7066a920c0c7d90c76",
        destination="nltk_data/corpora",
        placement="nombank.1.0",
    )

    resource(
        name="floresta",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/floresta.zip",
        when="+data",
        sha256="7675017f8b36cb85013b7a4171659fb55c427110e1e2fd4bcd92c4c771a14bfd",
        destination="nltk_data/corpora",
        placement="floresta",
    )

    resource(
        name="comtrans",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/comtrans.zip",
        when="+data",
        sha256="95a334f6bd910d2271d159bf53c5ce08516be3fa1cceb32521232c21dd2131f9",
        destination="nltk_data/corpora",
        placement="comtrans",
    )

    resource(
        name="knbc",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/knbc.zip",
        when="+data",
        sha256="88a7822a33d16418e88b2f95084396496953a1c1087bf3e233d3e1fec3f935e8",
        destination="nltk_data/corpora",
        placement="knbc",
    )

    resource(
        name="mac_morpho",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/mac_morpho.zip",
        when="+data",
        sha256="1c6138beba28b9c71edfd4b54991c5e1cf36a4d6b0ad8c66f8aa27c57b07547b",
        destination="nltk_data/corpora",
        placement="mac_morpho",
    )

    resource(
        name="swadesh",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/swadesh.zip",
        when="+data",
        sha256="0b69919501a098f25d2abad9edb84689e1ed44915ca1c65c7832d2bf9d1de3b9",
        destination="nltk_data/corpora",
        placement="swadesh",
    )

    resource(
        name="rte",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/rte.zip",
        when="+data",
        sha256="2f806ead4d53171601254747c3b7c97d758e63a6ef54e3c010a6d62885ab214a",
        destination="nltk_data/corpora",
        placement="rte",
    )

    resource(
        name="toolbox",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/toolbox.zip",
        when="+data",
        sha256="f57d06b30360c5f52cc05c29e75b083eb23981416cce718206c80da0e931592e",
        destination="nltk_data/corpora",
        placement="toolbox",
    )

    resource(
        name="jeita",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/jeita.zip",
        when="+data",
        sha256="4415bd6365628be5eeb80fe7aefe2b9161ef6cfc4d604d101feec6b59aedcbfd",
        destination="nltk_data/corpora",
        placement="jeita",
    )

    resource(
        name="product_reviews_1",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/product_reviews_1.zip",
        when="+data",
        sha256="627bfb0bb7c87586246d99b4402c3d7e4fb77ac14559d8695c283bd6850615ac",
        destination="nltk_data/corpora",
        placement="product_reviews_1",
    )

    resource(
        name="omw",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/omw.zip",
        when="+data",
        sha256="e2cd473805b480b5448ae3f2c3e824978f2528dc1a95a14fe3072777a2f12519",
        destination="nltk_data/corpora",
        placement="omw",
    )

    resource(
        name="wordnet2022",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet2022.zip",
        when="+data",
        sha256="5ccbb3382b9d147d4acac12645b3d6f375d1f5e4cd037fedadef74d069a8ee3f",
        destination="nltk_data/corpora",
        placement="wordnet2022",
    )

    resource(
        name="sentiwordnet",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/sentiwordnet.zip",
        when="+data",
        sha256="b66876a17aaeb4c7c7c8d2f5bb2cf91fde16e1b76e2421e5480fedd17ad248c1",
        destination="nltk_data/corpora",
        placement="sentiwordnet",
    )

    resource(
        name="product_reviews_2",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/product_reviews_2.zip",
        when="+data",
        sha256="272b08fe130882e5867aa7ecc69a65616099183c4ccc10374a62c271801b0bc1",
        destination="nltk_data/corpora",
        placement="product_reviews_2",
    )

    resource(
        name="abc",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/abc.zip",
        when="+data",
        sha256="129bb6001beb828049a90a59b7dd3c2f0594a47012e48fc5177dfae38e658565",
        destination="nltk_data/corpora",
        placement="abc",
    )

    resource(
        name="wordnet2021",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet2021.zip",
        when="+data",
        sha256="d7ef7d289da4dd0f33f07d9745856adc74689a53a8fa9be5dcfd3c87c5da24db",
        destination="nltk_data/corpora",
        placement="wordnet2021",
    )

    resource(
        name="udhr2",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/udhr2.zip",
        when="+data",
        sha256="0796c314b09a930c989c6f9d93d226af9af13feccd88496e196c743dd266c7f3",
        destination="nltk_data/corpora",
        placement="udhr2",
    )

    resource(
        name="senseval",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/senseval.zip",
        when="+data",
        sha256="fbcb658b562969e47a19a45e04c452d874755d157db936d815ca391ca88bfdea",
        destination="nltk_data/corpora",
        placement="senseval",
    )

    resource(
        name="words",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/words.zip",
        when="+data",
        sha256="54ed02917d6771dcc3e8141218960d020947f7f2ccfd9ac9b320979349746015",
        destination="nltk_data/corpora",
        placement="words",
    )

    resource(
        name="framenet_v15",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/framenet_v15.zip",
        when="+data",
        sha256="ea723e8575f1d7eeb0b39e7cd14a4d608f24adec4496800bfea3bdff82ffdcc8",
        destination="nltk_data/corpora",
        placement="framenet_v15",
    )

    resource(
        name="unicode_samples",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/unicode_samples.zip",
        when="+data",
        sha256="9f8e483e02aa29319648c794942ccd4b13c1029322907138b6fa662315e2d845",
        destination="nltk_data/corpora",
        placement="unicode_samples",
    )

    resource(
        name="kimmo",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/kimmo.zip",
        when="+data",
        sha256="5be9a891a08ac48914cccf8f98f3469c1e76e8d3aae16243220839e8c3fe16f4",
        destination="nltk_data/corpora",
        placement="kimmo",
    )

    resource(
        name="framenet_v17",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/framenet_v17.zip",
        when="+data",
        sha256="22f6aad6fb799ba4dbed0440714e1118442ad7d7345351de37428581284f471c",
        destination="nltk_data/corpora",
        placement="framenet_v17",
    )

    resource(
        name="chat80",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/chat80.zip",
        when="+data",
        sha256="6147451ba5bef268044e3fba446b5988da757fc2ed18d951d38d4eec864c66c0",
        destination="nltk_data/corpora",
        placement="chat80",
    )

    resource(
        name="qc",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/qc.zip",
        when="+data",
        sha256="091fb01e50883014d150acb7d5013d787136968b3f955ae01725a65e7e80f304",
        destination="nltk_data/corpora",
        placement="qc",
    )

    resource(
        name="inaugural",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/inaugural.zip",
        when="+data",
        sha256="7c5fb5793e31fbeae12bf1aa0ffda5336468f07cedb50654c6d31ca384e2046b",
        destination="nltk_data/corpora",
        placement="inaugural",
    )

    resource(
        name="wordnet",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip",
        when="+data",
        sha256="cbda5ea6eef7f36a97a43d4a75f85e07fccbb4f23657d27b4ccbc93e2646ab59",
        destination="nltk_data/corpora",
        placement="wordnet",
    )

    resource(
        name="stopwords",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip",
        when="+data",
        sha256="15c94179887425ca1bedc265608cab9f27d650211f709bb929e320990a4b01d1",
        destination="nltk_data/corpora",
        placement="stopwords",
    )

    resource(
        name="verbnet",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/verbnet.zip",
        when="+data",
        sha256="6bc3620a6dc1c50aec46a97e5ddb51e64c015b9f7d37246805c5f8acfd6d172d",
        destination="nltk_data/corpora",
        placement="verbnet",
    )

    resource(
        name="shakespeare",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/shakespeare.zip",
        when="+data",
        sha256="f1251d8c254710363254ba29c9dc0888d5cb13d5ac736ebc6fb14380f447cfc3",
        destination="nltk_data/corpora",
        placement="shakespeare",
    )

    resource(
        name="ycoe",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/ycoe.zip",
        when="+data",
        sha256="e402fa937d6a0b4603495e79f91af02c3f192977e6f15cc5ed5962b5d3673d9a",
        destination="nltk_data/corpora",
        placement="ycoe",
    )

    resource(
        name="ieer",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/ieer.zip",
        when="+data",
        sha256="1f63b08ed212c1d52545307838d183c79e02fd09cc8c5a48542f82c61c078b5d",
        destination="nltk_data/corpora",
        placement="ieer",
    )

    resource(
        name="cess_cat",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/cess_cat.zip",
        when="+data",
        sha256="c5b42b363365bfaa9a0616e448eb50da9668d2f5b6d1ff9d12b5c28ae09543cb",
        destination="nltk_data/corpora",
        placement="cess_cat",
    )

    resource(
        name="switchboard",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/switchboard.zip",
        when="+data",
        sha256="6a1a22b659e2fe616129addab0e7967335e67c7dae6a6e63be10778dd0455d06",
        destination="nltk_data/corpora",
        placement="switchboard",
    )

    resource(
        name="comparative_sentences",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/comparative_sentences.zip",
        when="+data",
        sha256="d076e1bab25c7c2a39e8850aefbb64a2188ebc5033bf21aeb656f4fab15f7f8b",
        destination="nltk_data/corpora",
        placement="comparative_sentences",
    )

    resource(
        name="subjectivity",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/subjectivity.zip",
        when="+data",
        sha256="741f3371e1a4375051b874fd82fd55857b90975473c91c19a3101cbe17fc4d8c",
        destination="nltk_data/corpora",
        placement="subjectivity",
    )

    resource(
        name="udhr",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/udhr.zip",
        when="+data",
        sha256="97e4c9dfa4a402f243d60b03d511afb04cf63f92f9ad1be9108b511448c329fa",
        destination="nltk_data/corpora",
        placement="udhr",
    )

    resource(
        name="pl196x",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/pl196x.zip",
        when="+data",
        sha256="494a7ee616e13b0f798793a9af8da8445b3b83bc4aa3c6bb239967e6ce3cbbeb",
        destination="nltk_data/corpora",
        placement="pl196x",
    )

    resource(
        name="paradigms",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/paradigms.zip",
        when="+data",
        sha256="5875c44cd547b6a8fdde48f8f798fe45bcad7cb232a93ee5fae17fed130c9870",
        destination="nltk_data/corpora",
        placement="paradigms",
    )

    resource(
        name="gazetteers",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gazetteers.zip",
        when="+data",
        sha256="3e4df6d5a03a3e4e109e488366e96e98d84f085b98d70f3dc11ecd6ce6ca48ab",
        destination="nltk_data/corpora",
        placement="gazetteers",
    )

    resource(
        name="timit",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/timit.zip",
        when="+data",
        sha256="666c6650fb054001e2e1d9aa9b1889fc46629a0081ced7049686c2a598326668",
        destination="nltk_data/corpora",
        placement="timit",
    )

    resource(
        name="treebank",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/treebank.zip",
        when="+data",
        sha256="9da92d76c3666cfb6cddeaed0f7e86b344cce0f0928a286d439e555f19c37399",
        destination="nltk_data/corpora",
        placement="treebank",
    )

    resource(
        name="sinica_treebank",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/sinica_treebank.zip",
        when="+data",
        sha256="395958a28f06d92ce1de0f0cf1bb17dc4a5cc882d27487447252ad615641e9ba",
        destination="nltk_data/corpora",
        placement="sinica_treebank",
    )

    resource(
        name="opinion_lexicon",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/opinion_lexicon.zip",
        when="+data",
        sha256="7a5da68d53016c5d1fca38f7dd81844cff73466371f90968d1ef15c85b873193",
        destination="nltk_data/corpora",
        placement="opinion_lexicon",
    )

    resource(
        name="ppattach",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/ppattach.zip",
        when="+data",
        sha256="ff27399cb353bc6a48ec7ed90f31e6f4c94f270662482b7db07ca0923adb5468",
        destination="nltk_data/corpora",
        placement="ppattach",
    )

    resource(
        name="dependency_treebank",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/dependency_treebank.zip",
        when="+data",
        sha256="0df483999f1391f32b141d6047d8ce19efd0a5a3e63ca019bfc4af8530f51fbd",
        destination="nltk_data/corpora",
        placement="dependency_treebank",
    )

    resource(
        name="reuters",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/reuters.zip",
        when="+data",
        sha256="9a59a43823f02a6e2777075c989a3dc454e4b6f68e0332ee3c0e8264075b62f5",
        destination="nltk_data/corpora",
        placement="reuters",
    )

    resource(
        name="genesis",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/genesis.zip",
        when="+data",
        sha256="0cac241f88d7999f81a45e26b1764b2d1f3b4d21654aa954e0d5349eb4784cd0",
        destination="nltk_data/corpora",
        placement="genesis",
    )

    resource(
        name="cess_esp",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/cess_esp.zip",
        when="+data",
        sha256="ae5b12898039e51911ae16d25c4822cb92adcfc034a2e12b57676d21d3c94884",
        destination="nltk_data/corpora",
        placement="cess_esp",
    )

    resource(
        name="conll2007",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/conll2007.zip",
        when="+data",
        sha256="b1e2865b31cdbc016a437c29dc3e190042ef2e237b21ba2a69082b7dc1c007ca",
        destination="nltk_data/corpora",
        placement="conll2007",
    )

    resource(
        name="nonbreaking_prefixes",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/nonbreaking_prefixes.zip",
        when="+data",
        sha256="62dd9fe11b21d201ca26cf2351595512965d5fe064f9d6ce1873c6231b46d869",
        destination="nltk_data/corpora",
        placement="nonbreaking_prefixes",
    )

    resource(
        name="dolch",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/dolch.zip",
        when="+data",
        sha256="e4a58e0f13809ac86bc819e245aeb60981ea4edcac7025509af99fa6b67305cd",
        destination="nltk_data/corpora",
        placement="dolch",
    )

    resource(
        name="smultron",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/smultron.zip",
        when="+data",
        sha256="6748fb331f7b06dd529617590277414a8d3b65291f68367d8b04615cf621702c",
        destination="nltk_data/corpora",
        placement="smultron",
    )

    resource(
        name="alpino",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/alpino.zip",
        when="+data",
        sha256="2e4551748dc81707b01d5adabb62c308ae5cb70fc526936310502431a1db96ef",
        destination="nltk_data/corpora",
        placement="alpino",
    )

    resource(
        name="wordnet_ic",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet_ic.zip",
        when="+data",
        sha256="a931b34bb9013ac3c1291f64c812fd039802995a2b1246b8f7525e82080110e3",
        destination="nltk_data/corpora",
        placement="wordnet_ic",
    )

    resource(
        name="brown",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/brown.zip",
        when="+data",
        sha256="9b275f9b3b95d7bd66ccfb7cd259f445a13bbe5d1f4107aba09fd3e8364bafa6",
        destination="nltk_data/corpora",
        placement="brown",
    )

    resource(
        name="bcp47",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/bcp47.zip",
        when="+data",
        sha256="435d986fd9de0ae540a34e0978dbbaf5d1db7576b2bc7571da71cf6a01c8dfaa",
        destination="nltk_data/corpora",
        placement="bcp47",
    )

    resource(
        name="panlex_swadesh",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/panlex_swadesh.zip",
        when="+data",
        sha256="dc028da016ba7d5f9bcc39263b0c3dc27bd56025672b18ccaec4578833fe4dff",
        destination="nltk_data/corpora",
        placement="panlex_swadesh",
    )

    resource(
        name="conll2000",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/conll2000.zip",
        when="+data",
        sha256="01e65164f268366e7caa0db92332a1955d081908c87016e2c7640c3c5279b7cd",
        destination="nltk_data/corpora",
        placement="conll2000",
    )

    resource(
        name="universal_treebanks_v20",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/universal_treebanks_v20.zip",
        when="+data",
        sha256="7132fdee74f85cb908558ffa3a6dac5c1f3762d4095a316990eb19a647421d8a",
        destination="nltk_data/corpora",
        placement="universal_treebanks_v20",
    )

    resource(
        name="brown_tei",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/brown_tei.zip",
        when="+data",
        sha256="335bec1ea6362751d5d5c46970137ebb01c80bf7d7d75558787729d275e0a687",
        destination="nltk_data/corpora",
        placement="brown_tei",
    )

    resource(
        name="cmudict",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/cmudict.zip",
        when="+data",
        sha256="d07cca47fd72ad32ea9d8ad1219f85301eeaf4568f8b6b73747506a71fb5afd6",
        destination="nltk_data/corpora",
        placement="cmudict",
    )

    resource(
        name="omw-1.4",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/omw-1.4.zip",
        when="+data",
        sha256="3b941e664852f3297b6040236626065796a2aaf7d7f9eec8779a3beaa1096c2d",
        destination="nltk_data/corpora",
        placement="omw-1.4",
    )

    resource(
        name="mte_teip5",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/mte_teip5.zip",
        when="+data",
        sha256="2847497d2f8c42c510e82e7cde37537a2a1da7d6e458d879fb22f73f4eef6059",
        destination="nltk_data/corpora",
        placement="mte_teip5",
    )

    resource(
        name="indian",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/indian.zip",
        when="+data",
        sha256="6f5aff392fc953769b6ccb994bd70e33ec6f0226e93979470255fa97abf692f9",
        destination="nltk_data/corpora",
        placement="indian",
    )

    resource(
        name="conll2002",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/conll2002.zip",
        when="+data",
        sha256="64440e49236d0d393e08e0b266284966d68e2d2a82a50cc41b8e96d98c03b5c8",
        destination="nltk_data/corpora",
        placement="conll2002",
    )

    resource(
        name="tagsets",
        url="https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/help/tagsets.zip",
        when="+data",
        sha256="e44c8ffd7e8759064573e8d4ae837dbb4b15ec68b2ca02cdf6a513dab8b12ca4",
        destination="nltk_data/help",
        placement="tagsets",
    )

    def setup_run_environment(self, env):
        if "+data" in self.spec:
            env.prepend_path("NLTK_DATA", self.prefix.nltk_data)

    @run_after("install")
    def install_data(self):
        if "+data" in self.spec:
            install_tree("nltk_data", self.prefix.nltk_data)

    # May require additional third-party software:
    # https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software
