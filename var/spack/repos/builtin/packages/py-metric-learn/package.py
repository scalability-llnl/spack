# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetricLearn(PythonPackage):
    """metric-learn contains efficient Python implementations of several
    popular supervised and weakly-supervised metric learning algorithms. As
    part of scikit-learn-contrib, the API of metric-learn is compatible with
    scikit-learn, the leading library for machine learning in Python. This
    allows to use all the scikit-learn routines (for pipelining, model
    selection, etc) with metric learning algorithms through a unified
    interface."""

    homepage = "https://github.com/scikit-learn-contrib/metric-learn"
    pypi = "metric-learn/metric-learn-0.7.0.tar.gz"

    version("0.7.0", sha256="2b35246a1098d74163b16cc7779e0abfcbf9036050f4caa258e4fee55eb299cc")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.11.0:", type=("build", "run"))
    depends_on("py-scipy@0.17.0:", type=("build", "run"))
    depends_on("py-scikit-learn@0.21.3:", type=("build", "run"))
