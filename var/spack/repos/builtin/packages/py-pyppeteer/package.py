# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-appdirs@1.4.3:1", type=("build", "run"))
    depends_on("py-importlib-metadata@1.4:", type=("build", "run"))
    depends_on("py-pyee@11", type=("build", "run"))
    depends_on("py-tqdm@4.42.1:4", type=("build", "run"))
    depends_on("py-urllib3@1.25.8:1", type=("build", "run"))
    depends_on("py-websockets@10", type=("build", "run"))
    depends_on("py-certifi@2023:", type=("build", "run"))
