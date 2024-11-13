# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitLearnExtra(PythonPackage):
    """A set of useful tools compatible with scikit-learn

    scikit-learn-extra is a Python module for machine learning that extends
    scikit-learn. It includes algorithms that are useful but do not satisfy the
    scikit-learn inclusion criteria, for instance due to their novelty or lower
    citation number."""

    homepage = "https://github.com/scikit-learn-contrib/scikit-learn-extra"
    pypi = "scikit-learn-extra/scikit-learn-extra-0.2.0.tar.gz"

    license("BSD-3-Clause")

    version("0.2.0", sha256="3b1bb5fedde47920eb4b3fa0a0c18f80cc7359d9d0496720178788c6153b8019")

    depends_on("cxx", type="build")  # generated

    # For upperbound see https://github.com/scikit-learn-contrib/scikit-learn-extra/issues/164
    depends_on("python@3.6:3.10", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.28.5:", type="build")
    depends_on("py-numpy@1.13.3:", type=("build", "run"))
    depends_on("py-scipy@0.19.1:", type=("build", "run"))
    # For upperbound see https://github.com/scikit-learn-contrib/scikit-learn-extra/issues/171
    depends_on("py-scikit-learn@0.23:1.2", type=("build", "run"))
