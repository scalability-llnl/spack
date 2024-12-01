# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRsatoolbox(PythonPackage):
    """Representational Similarity Analysis (RSA) in Python."""

    homepage = "https://github.com/rsagroup/rsatoolbox"
    pypi = "rsatoolbox/rsatoolbox-0.0.3.tar.gz"
    git = "https://github.com/rsagroup/rsatoolbox.git"

    license("MIT")

    version("main", branch="main")
    version("0.2.0", sha256="ecdcb50387c4b6330077ec2a3a221696078071319b8a0c32ed8128cd38da6863")
    version("0.1.5", sha256="439839fb20e2efa0c7c975ad305df8995a509ed3426ad0384ebfff20663fd58b")
    version("0.1.2", sha256="2d091cbaa33373bf9da4df5ca8d127f0e427431a3db726076090ab2d54fe1213")
    version("0.1.0", sha256="245f909d31909ba896b765fa51ea019510dd690c6bb8d04b178a9c76ec36dce9")
    version("0.0.5", sha256="7ede9309755a6173c26f08fd36fa436a11993c7ae0fa9fce05f38be7af0dc6eb")
    version("0.0.4", sha256="84153fa4c686c95f3e83f2cb668b97b82b53dc2a565856db80aa5f8c96d09359")
    version("0.0.3", sha256="9bf6e16d9feadc081f9daaaaab7ef38fc1cd64dd8ef0ccd9f74adb5fe6166649")

    depends_on("python@3.8:", type=("build", "run"), when="@0.1.5:")
    depends_on("python@:3.10", type=("build", "run"), when="@:0.1.2")

    depends_on("py-setuptools@68:", type="build", when="@0.1.5:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm+toml@8.0:", type="build", when="@0.1.5:")
    depends_on("py-setuptools-scm+toml@7.0", type="build", when="@0.0.5:0.1.4")
    depends_on("py-cython@3", type="build", when="@0.0.5:")
    depends_on("py-twine@4.0.1:", type="build", when="@0.1.5:")
    depends_on("py-twine@4.0.1:4.0", type="build", when="@0.0.5:0.1.4")

    depends_on("py-numpy@1.21.2:", type=("build", "run"))
    depends_on("py-scipy@1.10.1:", type=("build", "run"), when="@0.2:")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-pandas", when="@0.0.4:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-importlib-resources@5.12:", type=("build", "run"), when="^python@:3.8")
    depends_on("py-networkx@3:", type=("build", "run"), when="@0.2:")

    conflicts("^py-matplotlib@3.9.1")

    # old dependcies
    depends_on("py-coverage", type=("build", "run"), when="@:0.1.1")
    depends_on("py-petname@2.2", type=("build", "run"), when="@0.0.4")

    @when("@:0.0.3")
    def patch(self):
        # tests are looking for a not existing requirements.txt file
        with working_dir("tests"):
            open("requirements.txt", "a").close()
