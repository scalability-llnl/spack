# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMypy(PythonPackage):
    """Optional static typing for Python."""

    homepage = "https://www.mypy-lang.org/"
    pypi = "mypy/mypy-0.740.tar.gz"
    git = "https://github.com/python/mypy.git"

    maintainers("adamjstewart")

    license("MIT AND PSF-2.0", checked_by="tgamblin")

    version("1.11.2", sha256="7f9993ad3e0ffdc95c2a14b66dee63729f021968bff8ad911867579c65d13a79")
    version("1.11.1", sha256="f404a0b069709f18bbdb702eb3dcfe51910602995de00bd39cea3050b5772d08")
    version("1.10.1", sha256="1f8f492d7db9e3593ef42d4f115f04e556130f2819ad33ab84551403e97dd4c0")
    version("1.9.0", sha256="3cc5da0127e6a478cddd906068496a97a7618a21ce9b54bde5bf7e539c7af974")
    version("1.8.0", sha256="6ff8b244d7085a0b425b56d327b480c3b29cafbd2eff27316a004f9a7391ae07")
    version("1.7.1", sha256="fcb6d9afb1b6208b4c712af0dafdc650f518836065df0d4fb1d800f5d6773db2")
    version("1.7.0", sha256="1e280b5697202efa698372d2f39e9a6713a0395a756b1c6bd48995f8d72690dc")
    version("1.6.1", sha256="4d01c00d09a0be62a4ca3f933e315455bde83f37f892ba4b08ce92f3cf44bcc1")
    version("1.6.0", sha256="4f3d27537abde1be6d5f2c96c29a454da333a2a271ae7d5bc7110e6d4b7beb3f")
    version("1.5.1", sha256="b031b9601f1060bf1281feab89697324726ba0c0bae9d7cd7ab4b690940f0b92")
    version("1.5.0", sha256="f3460f34b3839b9bc84ee3ed65076eb827cd99ed13ed08d723f9083cada4a212")
    version("1.4.1", sha256="9bbcd9ab8ea1f2e1c8031c21445b511442cc45c89951e49bbf852cbb70755b1b")
    version("1.4.0", sha256="de1e7e68148a213036276d1f5303b3836ad9a774188961eb2684eddff593b042")
    version("1.3.0", sha256="e1f4d16e296f5135624b34e8fb741eb0eadedca90862405b1f1fde2040b9bd11")
    version("1.2.0", sha256="f70a40410d774ae23fcb4afbbeca652905a04de7948eaf0b1789c8d1426b72d1")
    version("1.1.1", sha256="ae9ceae0f5b9059f33dbc62dea087e942c0ccab4b7a003719cb70f9b8abfa32f")
    version("1.0.1", sha256="28cea5a6392bb43d266782983b5a4216c25544cd7d80be681a155ddcdafd152d")
    version("1.0.0", sha256="f34495079c8d9da05b183f9f7daec2878280c2ad7cc81da686ef0b484cea2ecf")
    version("0.991", sha256="3c0165ba8f354a6d9881809ef29f1a9318a236a6d81c690094c5df32107bde06")
    version("0.990", sha256="72382cb609142dba3f04140d016c94b4092bc7b4d98ca718740dc989e5271b8d")
    version("0.982", sha256="85f7a343542dc8b1ed0a888cdd34dca56462654ef23aa673907305b260b3d746")
    version("0.981", sha256="ad77c13037d3402fbeffda07d51e3f228ba078d1c7096a73759c9419ea031bf4")
    version("0.971", sha256="40b0f21484238269ae6a57200c807d80debc6459d444c0489a102d7c6a75fa56")
    version("0.961", sha256="f730d56cb924d371c26b8eaddeea3cc07d78ff51c521c6d04899ac6904b75492")
    version("0.960", sha256="d4fccf04c1acf750babd74252e0f2db6bd2ac3aa8fe960797d9f3ef41cf2bfd4")
    version("0.950", sha256="1b333cfbca1762ff15808a0ef4f71b5d3eed8528b23ea1c3fb50543c867d68de")
    version("0.942", sha256="17e44649fec92e9f82102b48a3bf7b4a5510ad0cd22fa21a104826b5db4903e2")
    version("0.941", sha256="cbcc691d8b507d54cb2b8521f0a2a3d4daa477f62fe77f0abba41e5febb377b7")
    version("0.940", sha256="71bec3d2782d0b1fecef7b1c436253544d81c1c0e9ca58190aed9befd8f081c5")
    version("0.931", sha256="0038b21890867793581e4cb0d810829f5fd4441aa75796b53033af3aa30430ce")
    version("0.930", sha256="51426262ae4714cc7dd5439814676e0992b55bcc0f6514eccb4cf8e0678962c2")
    version("0.921", sha256="eca089d7053dff45d6dcd5bf67f1cabc311591e85d378917d97363e7c13da088")
    version("0.920", sha256="a55438627f5f546192f13255a994d6d1cf2659df48adcf966132b4379fd9c86b")
    version("0.910", sha256="704098302473cb31a218f1775a873b376b30b4c18229421e9e9dc8916fd16150")
    version("0.900", sha256="65c78570329c54fb40f956f7645e2359af5da9d8c54baa44f461cdc7f4984108")
    version("0.800", sha256="e0202e37756ed09daf4b0ba64ad2c245d357659e014c3f51d8cd0681ba66940a")
    version("0.790", sha256="2b21ba45ad9ef2e2eb88ce4aeadd0112d0f5026418324176fd494a6824b74975")
    version("0.740", sha256="48c8bc99380575deb39f5d3400ebb6a8a1cb5cc669bbba4d3bb30f904e0a0e7d")
    version("0.670", sha256="e80fd6af34614a0e898a57f14296d0dacb584648f0339c2e000ddbf0f4cc2f8d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # pyproject.toml
    depends_on("py-setuptools@40.6.2:", when="@0.790:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel@0.30:", when="@0.790:", type="build")
    depends_on("py-types-psutil", when="@0.981:", type="build")
    depends_on("py-types-setuptools", when="@0.981:", type="build")

    # setup.py
    depends_on("python@3.8:", when="@1.5:", type=("build", "run"))
    depends_on("python@3.7:", when="@0.981:", type=("build", "run"))
    depends_on("py-typing-extensions@4.6:", when="@1.11:", type=("build", "run"))
    depends_on("py-typing-extensions@4.1:", when="@1.5:", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="@0.930:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@0.700:", type=("build", "run"))
    depends_on("py-mypy-extensions@1:", when="@1.1:", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.3:", when="@0.930:1.0", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.3:0.4", when="@0.700:0.929", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.0:0.4", when="@:0.699", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@0.950: ^python@:3.10", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@0.930:0.949", type=("build", "run"))
    depends_on("py-tomli@1.1:2", when="@0.920:0.929", type=("build", "run"))

    # Historical dependencies
    depends_on("py-types-typed-ast@1.5.8.5:1.5", when="@1.2:1.4", type="build")
    depends_on("py-types-typed-ast@1.5.8:1.5", when="@0.981:1.1", type="build")
    depends_on("py-toml", when="@0.900:0.910", type=("build", "run"))
    depends_on("py-typed-ast@1.4.0:1", when="@0.920:1.4 ^python@:3.7", type=("build", "run"))
    depends_on("py-typed-ast@1.4.0:1.4", when="@0.900:0.910 ^python@:3.7", type=("build", "run"))
    depends_on("py-typed-ast@1.4.0:1.4", when="@0.700:0.899", type=("build", "run"))
    depends_on("py-typed-ast@1.3.1:1.3", when="@:0.699", type=("build", "run"))

    # https://github.com/python/mypy/issues/13627
    conflicts("^python@3.10.7:", when="@:0.971")
