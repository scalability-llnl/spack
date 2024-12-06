# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJedi(PythonPackage):
    """An autocompletion tool for Python that can be used for text editors."""

    homepage = "https://github.com/davidhalter/jedi"
    pypi = "jedi/jedi-0.9.0.tar.gz"

    license("MIT")

    version("0.18.2", sha256="bae794c30d07f6d910d32a7048af09b5a39ed740918da923c6b780790ebac612")
    version("0.18.1", sha256="74137626a64a99c8eb6ae5832d99b3bdd7d29a3850fe2aa80a4126b2a7d949ab")
    version("0.18.0", sha256="92550a404bad8afed881a137ec9a461fed49eca661414be45059329614ed0707")
    version("0.17.2", sha256="86ed7d9b750603e4ba582ea8edc678657fb4007894a12bcf6f4bb97892f31d20")
    version("0.17.1", sha256="807d5d4f96711a2bcfdd5dfa3b1ae6d09aa53832b182090b222b5efb81f52f63")
    version("0.15.1", sha256="ba859c74fa3c966a22f2aeebe1b74ee27e2a462f56d3f5f7ca4a59af61bfe42e")
    version("0.15.0", sha256="9f16cb00b2aee940df2efc1d7d7c848281fd16391536a3d4561f5aea49db1ee6")
    version("0.14.1", sha256="53c850f1a7d3cfcd306cc513e2450a54bdf5cacd7604b74e42dd1f0758eaaf36")
    version("0.14.0", sha256="49ccb782651bb6f7009810d17a3316f8867dde31654c750506970742e18b553d")
    version("0.13.3", sha256="2bb0603e3506f708e792c7f4ad8fc2a7a9d9c2d292a358fbbd58da531695595b")
    version("0.13.2", sha256="571702b5bd167911fe9036e5039ba67f820d6502832285cde8c881ab2b2149fd")
    version("0.13.1", sha256="b7493f73a2febe0dc33d51c99b474547f7f6c0b2c8fb2b21f453eef204c12148")
    version("0.13.0", sha256="e4db7a2e08980e48c6aec6588483629c81fdcf9b6d9e6a372b40ed7fec91f310")
    version("0.12.1", sha256="b409ed0f6913a701ed474a614a3bb46e6953639033e31f769ca7581da5bd1ec1")
    version("0.12.0", sha256="1972f694c6bc66a2fac8718299e2ab73011d653a6d8059790c3476d2353b99ad")
    version("0.10.2", sha256="7abb618cac6470ebbd142e59c23daec5e6e063bfcecc8a43a037d2ab57276f4e")
    version("0.10.1", sha256="2420daf6fd00e80caf1bc22903598b5bf5560c900113dcc120eaefc7b4d50e06")
    # unfortunately pypi.io only offers a .whl for 0.10.0
    version(
        "0.10.0",
        sha256="d6a7344df9c80562c3f62199278004ccc7c5889be9f1a6aa5abde117ec085123",
        url="https://github.com/davidhalter/jedi/archive/v0.10.0.tar.gz",
    )
    version("0.9.0", sha256="3b4c19fba31bdead9ab7350fb9fa7c914c59b0a807dcdd5c00a05feb85491d31")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-parso@0.8", when="@0.18.0:", type=("build", "run"))
    depends_on("py-parso@0.7", when="@0.17", type=("build", "run"))
    depends_on("py-parso@0.5.2:", when="@0.15.2:0.16", type=("build", "run"))
    depends_on("py-parso@0.5.0:", when="@0.14.1:0.15.1", type=("build", "run"))
    depends_on("py-parso@0.3.0:", when="@0.12.1:0.14.0", type=("build", "run"))
    depends_on("py-parso@0.2.0:", when="@0.12.0", type=("build", "run"))
