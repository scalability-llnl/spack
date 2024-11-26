# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIpython(PythonPackage):
    """IPython provides a rich toolkit to help you make the most out of using
    Python interactively."""

    homepage = "https://ipython.readthedocs.org/"
    pypi = "ipython/ipython-7.18.1.tar.gz"
    git = "https://github.com/ipython/ipython"

    # "IPython.kernel" was deprecated for py-ipython@:7 and fails to import, leave
    # out of "import_modules" to ensure that import tests pass.
    # for py-ipython@8: "IPython.kernel" was removed
    skip_modules = ["IPython.kernel"]

    license("BSD-3-Clause")

    version("8.28.0", sha256="0d0d15ca1e01faeb868ef56bc7ee5a0de5bd66885735682e8a322ae289a13d1a")
    version("8.27.0", sha256="0b99a2dc9f15fd68692e898e5568725c6d49c527d36a9fb5960ffbdeaa82ff7e")
    version("8.26.0", sha256="1cec0fbba8404af13facebe83d04436a7434c7400e59f47acf467c64abd0956c")
    version("8.25.0", sha256="c6ed726a140b6e725b911528f80439c534fac915246af3efc39440a6b0f9d716")
    version("8.24.0", sha256="010db3f8a728a578bb641fdd06c063b9fb8e96a9464c63aec6310fbcb5e80501")
    version("8.23.0", sha256="7468edaf4f6de3e1b912e57f66c241e6fd3c7099f2ec2136e239e142e800274d")
    version("8.22.2", sha256="2dcaad9049f9056f1fef63514f176c7d41f930daa78d05b82a176202818f2c14")
    version("8.21.0", sha256="48fbc236fbe0e138b88773fa0437751f14c3645fb483f1d4c5dee58b37e5ce73")
    version("8.20.0", sha256="2f21bd3fc1d51550c89ee3944ae04bbc7bc79e129ea0937da6e6c68bfdbf117a")
    version("8.19.0", sha256="ac4da4ecf0042fb4e0ce57c60430c2db3c719fa8bdf92f8631d6bd8a5785d1f0")
    version("8.18.1", sha256="ca6f079bb33457c66e233e4580ebfc4128855b4cf6370dddd73842a9563e8a27")
    version("8.17.2", sha256="126bb57e1895594bb0d91ea3090bbd39384f6fe87c3d57fd558d0670f50339bb")
    version("8.16.1", sha256="ad52f58fca8f9f848e256c629eff888efc0528c12fe0f8ec14f33205f23ef938")
    version("8.15.0", sha256="2baeb5be6949eeebf532150f81746f8333e2ccce02de1c7eedde3f23ed5e9f1e")
    version("8.14.0", sha256="1d197b907b6ba441b692c48cf2a3a2de280dc0ac91a3405b39349a50272ca0a1")
    version("8.11.0", sha256="735cede4099dbc903ee540307b9171fbfef4aa75cfcacc5a273b2cda2f02be04")
    version("8.5.0", sha256="097bdf5cd87576fd066179c9f7f208004f7a6864ee1b20f37d346c0bcb099f84")
    version("8.0.1", sha256="ab564d4521ea8ceaac26c3a2c6e5ddbca15c8848fd5a5cc325f960da88d42974")
    version("7.31.1", sha256="b5548ec5329a4bcf054a5deed5099b0f9622eb9ea51aaa7104d215fece201d8c")
    version("7.28.0", sha256="2097be5c814d1b974aea57673176a924c4c8c9583890e7a5f082f547b9975b11")
    version("7.27.0", sha256="58b55ebfdfa260dad10d509702dc2857cb25ad82609506b070cf2d7b7df5af13")
    version("7.26.0", sha256="0cff04bb042800129348701f7bd68a430a844e8fb193979c08f6c99f28bb735e")
    version("7.21.0", sha256="04323f72d5b85b606330b6d7e2dc8d2683ad46c3905e955aa96ecc7a99388e70")
    version("7.18.1", sha256="a331e78086001931de9424940699691ad49dfb457cea31f5471eae7b78222d5e")
    version("7.5.0", sha256="e840810029224b56cd0d9e7719dc3b39cf84d577f8ac686547c8ba7a06eeab26")
    version("7.3.0", sha256="06de667a9e406924f97781bda22d5d76bfb39762b678762d86a466e63f65dc39")
    version("5.8.0", sha256="4bac649857611baaaf76bc82c173aa542f7486446c335fe1a6c05d0d491c8906")
    version("5.1.0", sha256="7ef4694e1345913182126b219aaa4a0047e191af414256da6772cf249571b961")

    depends_on("python@3.9:", when="@8.13.1:", type=("build", "run"))
    depends_on("python@3.8: +sqlite3", when="@8:", type=("build", "run"))
    depends_on("py-setuptools@61.2:", when="@8.22:", type="build")
    depends_on("py-setuptools@51:", when="@8:", type="build")
    depends_on("py-setuptools@18.5:", when="@:7", type="run")
    depends_on("py-setuptools", type="build")

    depends_on("py-colorama", when="platform=windows", type=("build", "run"))
    depends_on("py-decorator", type=("build", "run"))
    depends_on("py-exceptiongroup", when="@8.15: ^python@:3.10", type=("build", "run"))
    depends_on("py-jedi@0.16:", when="@7.18,7.20:", type=("build", "run"))
    depends_on("py-jedi@0.10:", when="@7.5:7.17,7.19", type=("build", "run"))
    depends_on("py-matplotlib-inline", when="@7.23:", type=("build", "run"))
    depends_on("py-pexpect@4.4:", when="@7.18: platform=linux", type=("build", "run"))
    depends_on("py-pexpect@4.4:", when="@7.18: platform=darwin", type=("build", "run"))
    depends_on("py-pexpect", when="platform=linux", type=("build", "run"))
    depends_on("py-pexpect", when="platform=darwin", type=("build", "run"))
    depends_on("py-prompt-toolkit@3.0.41:3.0", when="@8.18.1:", type=("build", "run"))
    depends_on("py-prompt-toolkit@3.0.30:3.0.36,3.0.38:3.0", when="@8.11:", type=("build", "run"))
    depends_on("py-prompt-toolkit@3.0.2:3.0", when="@8.5:", type=("build", "run"))
    depends_on("py-prompt-toolkit@2.0.0:2,3.0.2:3.0", when="@7.26:", type=("build", "run"))
    depends_on("py-prompt-toolkit@3.0.2:3.0", when="@7.18:7.25", type=("build", "run"))
    depends_on("py-prompt-toolkit@2.0.0:2.0", when="@7.5.0", type=("build", "run"))
    depends_on("py-prompt-toolkit@2.0.0:2", when="@7.0.0:7.5.0", type=("build", "run"))
    depends_on("py-prompt-toolkit@1.0.4:1", when="@:7.0.0", type=("build", "run"))
    depends_on("py-prompt-toolkit@1.0.3:1", when="@:7.0.0", type=("build", "run"))
    depends_on("py-pygments@2.4:", when="@8.1:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-stack-data", when="@8:", type=("build", "run"))
    depends_on("py-traitlets@5.13:", when="@8.22.1:", type=("build", "run"))
    depends_on("py-traitlets@5:", when="@8:", type=("build", "run"))
    depends_on("py-traitlets@4.2:", type=("build", "run"))
    depends_on("py-traitlets", type=("build", "run"))
    depends_on("py-typing-extensions@4.6:", when="@8.24: ^python@:3.11", type=("build", "run"))
    depends_on("py-typing-extensions", when="@8.23: ^python@:3.11", type=("build", "run"))
    depends_on("py-typing-extensions", when="@8.12: ^python@:3.9", type=("build", "run"))

    # Historical dependencies
    depends_on("py-appnope", when="@:8.17 platform=darwin", type=("build", "run"))
    depends_on("py-backcall", when="@7.3.0:8.16", type=("build", "run"))
    depends_on("py-black", when="@8.0", type=("build", "run"))
    depends_on("py-pickleshare", when="@:8.16", type=("build", "run"))
    depends_on("py-simplegeneric@0.8:", when="@:7.0.0", type=("build", "run"))
