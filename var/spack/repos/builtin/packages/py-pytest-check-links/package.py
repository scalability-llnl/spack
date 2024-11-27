# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestCheckLinks(PythonPackage):
    """pytest plugin that checks URLs for HTML-containing files."""

    homepage = "https://github.com/jupyterlab/pytest-check-links"
    pypi = "pytest-check-links/pytest_check_links-0.3.4.tar.gz"

    license("BSD-3-Clause")

    version("0.3.4", sha256="4b3216548431bf9796557e8ee8fd8e5e77a69a4690b3b2f9bcf6fb5af16a502b")

    depends_on("py-setuptools@17.1:", type="build")
    depends_on("py-pbr@1.9:", type="build")
