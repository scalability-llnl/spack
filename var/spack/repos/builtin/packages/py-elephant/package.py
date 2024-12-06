# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyElephant(PythonPackage):
    """Elephant is a package for analysis of electrophysiology data in Python"""

    homepage = "http://neuralensemble.org/elephant/"
    pypi = "elephant/elephant-0.11.0.tar.gz"
    git = "https://github.com/NeuralEnsemble/elephant.git"

    # list of GitHub accounts to notify when the package is updated.
    maintainers("Moritz-Alexander-Kern")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("0.14.0", sha256="02ce3b2a8d08dc19828f95384551339ea0946bc405c1db9aace54135417c2b0f")
    version("0.13.0", sha256="2c6463cf9ace41631f2af196c5b80b468bf1c4b264d3a6b1ea0fb587d9e7dd67")
    version("0.12.0", sha256="81f8d668f92d8688344bb7a9c5abaa8438d824560c935a411e6e36ddf7dc7c72")
    version("0.11.2", sha256="f8759fff0bbb136ae4ffc8d1eacadeea8ba56610d705c3bf207de87ada3ba240")
    version("0.11.1", sha256="d604a202583440fdf9d95d42cef50a410bd74fcaaa1a925b139435f27ab012ef")
    version("0.11.0", sha256="7b547964dbd196361edc922db2c5a7c0c886ef1effcca6c6dc7adb06f966a3be")
    version("0.10.0", sha256="7e69a113475e4db01b3563328953c037d37f1597d9f2edf0d51fb65e9aebf096")
    version("0.9.0", sha256="3e3d4a8e45d708f48bdcadcc4933c66f757d1ede6a1e172af0c07331b64ca180")
    version("0.8.0", sha256="f7c2649d5b7cfdbaa4442457c75f86af01cc8e7ce2c63f5b3d4687bb94e10af2")
    version("0.7.0", sha256="76785fe10c40042504928fde2fc57182230bbe39cf0fb0dcaffaba76219b046a")
    version("0.6.4", sha256="b8c5f2c00ad3249e1fe428d0b8a1dbcaee4a69464481f5f8fd55d2f7f22c45a3")
    version("0.4.1", sha256="86b21a44cbacdc09a6ba6f51738dcd5b42ecd553d73acb29f71a0be7c82eac81")
    version("0.3.0", sha256="747251ccfb5820bdead6391411b5faf205b4ddf3ababaefe865f50b16540cfef")

    depends_on("cxx", type="build")  # generated

    variant("docs", default=False, description="Install documentation dependencies")
    variant(
        "extras", default=False, description="Build with extras for GPFA, ASSET", when="@0.6.4:"
    )

    depends_on("py-setuptools", type="build")

    depends_on("python@3.8:", type=("build", "run"), when="@0.12.0:")

    depends_on("py-neo@0.10.0:", type=("build", "run"), when="@0.11.0:")
    depends_on("py-neo@0.9.0", type=("build", "run"), when="@0.9.0:0.10.0")
    depends_on("py-neo@0.8.0", type=("build", "run"), when="@0.6.4:0.8.0")
    depends_on("py-neo@0.3.4:", type=("build", "run"), when="@0.3.0:0.4.1")
    depends_on("py-numpy@1.19.5:", type=("build", "run"), when="@0.12.0:")
    depends_on("py-numpy@1.18.1:1.23.5", type=("build", "run"), when="@0.6.4:0.11.2")
    depends_on("py-numpy@1.8.2:", type=("build", "run"), when="@0.3.0:0.4.1")
    depends_on("py-quantities@0.14.1:", type=("build", "run"), when="@0.14.0:")
    depends_on("py-quantities@0.12.1:0.13.0,0.14.1:", type=("build", "run"), when="@0.6.4:0.13.0")
    depends_on("py-quantities@0.10.1:0.13.0,0.14.1:", type=("build", "run"), when="@0.3.0:0.4.1")
    depends_on("py-scipy@1.5.4:", type=("build", "run"), when="@0.6.4:")
    depends_on("py-scipy@0.14.0:", type=("build", "run"), when="@0.3.0:0.4.1")
    depends_on("py-six@1.10.0:", type=("build", "run"), when="@0.6.4:")
    depends_on("py-tqdm", type=("build", "run"), when="@0.6.4:")

    depends_on("py-pandas@0.18.0:", type=("build", "run"), when="+extras")
    depends_on("py-scikit-learn@0.23.2:", type=("build", "run"), when="+extras")
    depends_on("py-statsmodels@0.12.1:", type=("build", "run"), when="+extras")
    depends_on("py-jinja2@2.11.2:", type=("build", "run"), when="+extras")

    depends_on("py-numpydoc@1.1.0:", type=("build", "run"), when="@0.9.0:+docs")
    depends_on("py-numpydoc@0.5:", type=("build", "run"), when="@0.3.0:0.8.0+docs")
    depends_on("py-jupyter@1.0.0:", type=("build", "run"), when="@0.7.0:+docs")
    depends_on("py-sphinx@3.3.0:", type=("build", "run"), when="@0.9.0:+docs")
    depends_on("py-sphinx@2.4.3:", type=("build", "run"), when="@0.7.0:0.8.0+docs")
    depends_on("py-sphinx@1.2.2:", type=("build", "run"), when="@0.3.0:0.6.0+docs")
    depends_on("py-nbsphinx@0.8.0:", type=("build", "run"), when="@0.9.0:+docs")
    depends_on("py-nbsphinx@0.5.0:", type=("build", "run"), when="@0.7.0:0.8.0+docs")
    depends_on("py-sphinxcontrib-bibtex@1.0.1:", type=("build", "run"), when="@0.7.0:+docs")
    depends_on("py-sphinx-tabs@1.3.0:", type=("build", "run"), when="@0.9.0:+docs")
    depends_on("py-sphinx-tabs@1.1.13:", type=("build", "run"), when="@0.7.0:0.8.0+docs")
    depends_on("py-matplotlib@3.3.2:", type=("build", "run"), when="@0.9.0:+docs")
    depends_on("py-matplotlib@3.1.0:", type=("build", "run"), when="@0.8.0+docs")
