# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySeriate(PythonPackage):
    """This is a Python implementation of Seriation
    algorithm. Seriation is an approach for ordering elements in a set
    so that the sum of the sequential pairwise distances is
    minimal. We state this task as a Travelling Salesman Problem (TSP)
    and leverage the powerful Google's or-tools to do
    heavy-lifting. Since TSP is NP-hard, it is not possible to
    calculate the precise solution for a big number of
    elements. However, the or-tools' heuristics work very well in
    practice, and they are used in e.g. Google Maps."""

    homepage = "https://github.com/src-d/seriate"
    url = "https://github.com/src-d/seriate/archive/1.1.2.tar.gz"

    license("Apache-2.0")

    version("1.1.2", sha256="5e031e865398fbe24aebdbb4a2e0015447aec50478830850f29d38660fd266e3")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.0:", type=("build", "run"))
    depends_on("py-packaging@16.0:", type=("build", "run"))
    depends_on("py-or-tools", type=("build", "run"))
