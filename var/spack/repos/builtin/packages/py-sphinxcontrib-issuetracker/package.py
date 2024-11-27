# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribIssuetracker(PythonPackage):
    """Sphinx integration with different issuetrackers."""

    homepage = "https://sphinxcontrib-issuetracker.readthedocs.org/"
    pypi = "sphinxcontrib-issuetracker/sphinxcontrib-issuetracker-0.11.tar.gz"

    license("BSD-2-Clause")

    version("0.11", sha256="843753d8b5e989116378ab45ecccb368fb78dc56eaa1554ed25e4fbf22745f4e")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@1.1:", type=("build", "run"))
    depends_on("py-requests@1.1:", type=("build", "run"))
