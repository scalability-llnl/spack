# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningApiAccess(PythonPackage):
    """Lightning Frontend Showing how a given API can be accessed."""

    homepage = "https://github.com/Lightning-AI/LAI-API-Access-UI-Component"

    # sdist not available on PyPI or GitHub
    url = "https://files.pythonhosted.org/packages/py3/l/lightning-api-access/lightning_api_access-0.0.5-py3-none-any.whl"
    list_url = "https://pypi.org/simple/lightning-api-access/"

    version("0.0.5", sha256="08657fee636377534332df92e0bee893d46cb877f9642cba09ce560aed95fd40")
