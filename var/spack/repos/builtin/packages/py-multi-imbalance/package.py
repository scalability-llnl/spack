# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiImbalance(PythonPackage):
    """Multi-class imbalance is a common problem occurring in real-world
    supervised classifications tasks. While there has already been some
    research on the specialized methods aiming to tackle that challenging
    problem, most of them still lack coherent Python implementation that is
    simple, intuitive and easy to use. multi-imbalance is a python package
    tackling the problem of multi-class imbalanced datasets in machine
    learnin"""

    homepage = "https://github.com/damianhorna/multi-imbalance"
    pypi = "multi-imbalance/multi-imbalance-0.0.14.tar.gz"

    version("0.0.14", sha256="5b9e1ba5e012e0343c588fa5a4b9d69ca99464d2126f1392bac3fca24370498f")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.17.0:", type=("build", "run"))
    depends_on("py-scikit-learn@0.22:", type=("build", "run"))
    depends_on("py-pandas@0.25.1:", type=("build", "run"))
    depends_on("py-pytest@5.1.2:", type=("build", "run"))
    depends_on("py-imbalanced-learn@0.6.1:", type=("build", "run"))
    depends_on("py-coverage@5.1:", type=("build", "run"))
    depends_on("py-pytest-cov@2.8.1:", type=("build", "run"))
    depends_on("py-ipython@7.13.0:", type=("build", "run"))
    depends_on("py-seaborn@0.10.1:", type=("build", "run"))
    depends_on("py-matplotlib@3.2.1:", type=("build", "run"))
