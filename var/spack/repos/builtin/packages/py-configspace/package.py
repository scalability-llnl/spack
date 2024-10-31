# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigspace(PythonPackage):
    """Creation and manipulation of parameter configuration spaces for
    automated algorithm configuration and hyperparameter tuning."""

    maintainers("Kerilk", "mdorier")

    homepage = "https://automl.github.io/ConfigSpace/master/"
    pypi = "configspace/configspace-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("main", git="https://github.com/automl/ConfigSpace.git", branch="main")
    version("1.1.4", sha256="afd625a9bcf4c01efa06114ce9dcc718cf9cba68910b602849b1c59654415762")
    version("1.1.3", sha256="8b77e77bd1c286a57e35da87552e33052f6793ddbcc696a9fc62425f60739ac2")
    version("1.1.2", sha256="8cd77438f976ce65ce2d056fbd659d12ca1425fe230b737942261879b7c542f0")
    version("1.1.1", sha256="450e5dccb52ffc56ec5ade131eaa95207412e1fa44883d611e024fc185a54bf0")
    version("1.1.0", sha256="84f20d2b78365a33820558749975667e9bb81d8fb283fcf2ef5bae6052745481")
    version("1.0.1", sha256="ffaf2c02db1df47589d5501178827e945d3f953f2812e7e44a9c3029ea13a543")
    version("1.0.0", sha256="cc55ac8a550c86bee7853417f1eda22d46185fb911b5875754619735966e2736")
    version("0.7.1", sha256="57b5b8e28ed6ee14ecf6206fdca43ca698ef63bc1531f081d482b26acf4edf1a")
    version("0.6.1", sha256="b0a9487c7997481a041feee46f2c8fc9fb9787e1ff553250838d62624dfb0d5a")
    version("0.6.0", sha256="9b6c95d8839fcab220372673214b3129b45dcd8b1179829eb2c65746cacb72a9")
    version("0.5.0", sha256="c8b61fe119829c29c47fc8719bb5f5740ae3034c793040f7bff67dbc9eb9c754")
    version("0.4.21", sha256="09c5ee343f2850865609cc91f2ab27da0a6182f7f196354f9550f6da578ea827")
    version("0.4.20", sha256="2e4ca06f5a6a61e5322a73dd7545468c79f2a3e8385cab92fdada317af41d9e9")

    depends_on("c", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython@:0.29.36", type="build", when="@:0.9.9")
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-scipy", when="@0.4.21:")
    depends_on("py-typing-extensions", when="@0.6.0:")
    depends_on("py-more-itertools", when="@0.6.1:")

    def url_for_version(self, version):
        new_url = (
            "https://files.pythonhosted.org/packages/source/c/configspace/configspace-{0}.tar.gz"
        )
        old_url = (
            "https://files.pythonhosted.org/packages/source/C/ConfigSpace/ConfigSpace-{0}.tar.gz"
        )
        if version >= Version("1.0.0"):
            return new_url.format(version)
        else:
            return old_url.format(version)
