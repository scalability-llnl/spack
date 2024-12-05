# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBidscoin(PythonPackage):
    """Converts and organises raw MRI data-sets according to the Brain Imaging
    Data Structure (BIDS)."""

    homepage = "https://github.com/Donders-Institute/bidscoin"
    pypi = "bidscoin/bidscoin-3.7.4.tar.gz"

    license("GPL-3.0-or-later")

    version("4.1.1", sha256="28730e9202d3c44d77c0bbdea9565e00adfdd23e85a6f3f121c1bfce1a7b462b")
    version("4.0.0", sha256="3b0c26f2e250e06b6f526cdbee09517e1f339da8035c0a316609b4463d75824d")
    version("3.7.4", sha256="efa32238fb7b75e533e7f5cc318ad5a703716d291985435d43f1de4f18402517")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@62.2:", when="@4.1:", type="build")
    depends_on("py-setuptools@61:", when="@4:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-argparse-manpage+setuptools", when="@4.1:", type="build")

    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pydicom@2:", type=("build", "run"))
    depends_on("py-pyqt6", when="@4.1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.15.35:", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@4.1: ^python@:3.10", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-tqdm@4.60:", when="@4:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-multiecho@0.25:", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-bids-validator", when="@4:", type=("build", "run"))
    depends_on("dcm2niix", type=("build", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", when="@:3", type="build")
    depends_on("py-pyqt5@5.12.1:", when="@:4.0", type=("build", "run"))
    depends_on("py-pydeface", when="@4.0", type=("build", "run"))
    depends_on("py-pytest", when="@4.0", type=("build", "run"))
