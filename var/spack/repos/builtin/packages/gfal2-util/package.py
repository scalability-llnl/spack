# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gfal2Util(PythonPackage):
    """CLI for gfal2."""

    homepage = "https://dmc-docs.web.cern.ch/dmc-docs/gfal2-util.html"
    url = "https://github.com/cern-fts/gfal2-util/archive/refs/tags/v1.9.0.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("1.9.0", sha256="9a5194b7ac80381c0787ec7c2405cc3e060fc03bb99e80bbeb388ec3675cb13d")

    depends_on("py-setuptools", type="build")
