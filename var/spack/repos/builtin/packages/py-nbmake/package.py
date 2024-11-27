# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbmake(PythonPackage):
    """Pytest plugin for testing notebooks."""

    homepage = "https://github.com/treebeardtech/nbmake"
    pypi = "nbmake/nbmake-0.5.tar.gz"

    license("Apache-2.0")

    version("1.4.3", sha256="9afc46ba05cc22f5a78047a758dca32386c95eaaa41501b25ce108cf733d9622")
    version("1.4.1", sha256="7f602ba5195e80e4f2527944bb06d3b4df0d1520e73ba66126b51132b1f646ea")
    version("1.4", sha256="2d3b97b83a8a378d5d828ad7b5412e509b82ed883662af16533236c909cfa20a")
    version("1.3.5", sha256="95d4716928171120fae562e69440989a636e2af8616c829573e9574f5bea30db")
    version("1.3.4", sha256="70464b131b25dc91bd80bc79806673bd9e694b0d353a42402b7359c10c890350")
    version("1.3.3", sha256="0982e1e2c26b2fda7bac10f35b242c2b9b9b2574456975da158da05b0092888f")
    version("1.3.2", sha256="763ee648962a8706808ad3e780e314e6a79b168cf2edbb3b026987ee7bbf57be")
    version("1.3.1", sha256="e77f98e7d21e618bef1ba1c30904ce48657f934ebe359502c85a229184fbdfc8")
    version("1.3.0", sha256="49d5c59aefe45eaf8e2d8feff86c8e6de5547d823667305562364385e60d7206")
    version("1.2.1", sha256="63227b0ffe6045b7285ac7fce168ef050e6b0afe9bb02557a5f391311e2584b8")
    version("1.2", sha256="9aa299ad026047cb4d2191f10f1b5c9e1155f194b162f0d708c94acfea03d19c")
    version("1.1", sha256="d59158797cecb7d7b248a061854fbd7fa0bdd9ff2c19b0d0bae8ee2ca90ffd13")
    version("1.0", sha256="3ee5893b84507a7bc6af0e3eabb27edc926953527c790a4975e8f75af5a29ee5")
    version("0.10", sha256="1b0ee9e125b2d170a54ca2da3d8b45392e0ae663165469bd77f62290448ab96d")
    version("0.9", sha256="f2d8542be4763310c264be7caa12b36932ea40b3019dc66632ebda2a71589768")
    version("0.8", sha256="76bb053cffe9104fb873b6208b47ce1e71c9408849c5b1073090e6f6fb3a7ce7")
    version("0.7", sha256="b03adba337dad79bec3c9a5cb52d0d52859c793c74656795018ad37a32570d41")
    version("0.6", sha256="20dcec145507eec664d61ab36fa248797de6348e7013c9547028077bc46acde2")
    version("0.5", sha256="da9bf1bbc377c9d1d697f99952834017c39b4983e7e482a038dec705955a8ae9")

    depends_on("py-setuptools", type="build")
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-pytest@6.1.0:", when="@1.2.1:", type=("build", "run"))
    depends_on("py-pytest@6.1.0:6", when="@0.10:1.2.0", type=("build", "run"))
    depends_on("py-pytest@6.1.2:6", when="@:0.9", type=("build", "run"))
    depends_on("python@3.7.0:3", when="@1.3:", type=("build", "run"))
    depends_on("python@3.6.1:3", when="@:1.2", type=("build", "run"))
    depends_on("py-nbclient@0.6.6:0.6", when="@1.3.1:", type=("build", "run"))
    depends_on("py-nbclient@0.5.13:0.5", when="@1.3.0", type=("build", "run"))
    depends_on("py-nbclient@0.5.5:0.5", when="@1.2", type=("build", "run"))
    depends_on("py-nbclient@0.3:0", when="@:1.1", type=("build", "run"))
    depends_on("py-nbformat@5.0.8:5", type=("build", "run"))
    depends_on("py-pygments@2.7.3:2", type=("build", "run"))
    depends_on("py-ipykernel@5.4.0:", when="@0.7:", type=("build", "run"))
    depends_on("py-ipykernel@5.4.0:5", when="@0.5", type=("build", "run"))

    # Historical dependencies
    depends_on("py-pydantic@1.7.2:1", when="@:1.4.1", type=("build", "run"))
