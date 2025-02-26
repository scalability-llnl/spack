# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumpyGroupies(PythonPackage):
    """This package consists of a couple of optimised tools for doing things
    that can roughly be considered "group-indexing operations". The most
    prominent tool is `aggregate`. `aggregate` takes an array of values, and
    an array giving the group number for each of those values. It then returns
    the sum (or mean, or std, or any, ...etc.) of the values in each group.
    You have probably come across this idea before, using `matlab` accumarray,
    `pandas` groupby, or generally MapReduce algorithms and histograms. There
    are different implementations of `aggregate` provided, based on plain
    `numpy`, `numba` and `weave`. Performance is a main concern, and so far we
    comfortably beat similar implementations in other packages (check the
    benchmarks)."""

    homepage = "https://github.com/ml31415/numpy-groupies"
    pypi = "numpy_groupies/numpy_groupies-0.9.20.tar.gz"

    license("BSD-2-Clause")

    version("0.11.2", sha256="2fda978c4d28d2f1633a63972f425d0a7f2f12a75505d215b41b6de712e2ec4b")
    version("0.9.20", sha256="923a382d6bc6876384b58a9c0503b05b9d36a660f329695c2d33e4f93fcbbe3d")

    depends_on("python@3.7:3.11", type=("build", "run"), when="@0.9.20")
    depends_on("python@3.9:", type=("build", "run"), when="@0.11.2:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build", when="@0.11.2:")
    depends_on("py-numpy", type=("build", "run"))
