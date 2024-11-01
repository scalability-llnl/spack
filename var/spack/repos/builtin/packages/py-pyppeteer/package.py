# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyppeteer(PythonPackage):
    """Headless chrome/chromium automation library
    (unofficial port of puppeteer)."""

    homepage = "https://github.com/pyppeteer/pyppeteer"
    pypi = "pyppeteer/pyppeteer-2.0.0.tar.gz"

    license("MIT")

    version("2.0.0", sha256="4af63473ff36a746a53347b2336a49efda669bcd781e400bc1799b81838358d9")

    depends_on("py-poetry-core", type="build")
