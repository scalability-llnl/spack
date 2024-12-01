# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastai(PythonPackage):
    """You can use fastai without any installation by using
    Google Colab. In fact, every page of this documentation is
    also available as an interactive notebook - click "Open in
    colab" at the top of any page to open it (be sure to change
    the Colab runtime to "GPU" to have it run fast!) See the
    fast.ai documentation on Using Colab for more
    information."""

    homepage = "https://github.com/fastai/fastai/tree/master/"
    pypi = "fastai/fastai-2.5.3.tar.gz"

    license("Apache-2.0")

    version("2.5.3", sha256="0cae50617979b052f0ed7337800e6814ee346b792203cf48305709c935e8eeb7")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@36.2:", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-fastdownload@0.0.5:1", type=("build", "run"))
    depends_on("py-fastcore@1.3.22:1.3", type=("build", "run"))
    depends_on("py-torchvision@0.8.2:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-fastprogress@0.2.4:", type=("build", "run"))
    depends_on("pil@6.0.1:", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-spacy@:3", type=("build", "run"))
    depends_on("py-torch@1.7.0:1.10", type=("build", "run"))
