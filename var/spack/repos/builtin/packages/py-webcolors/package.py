# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebcolors(PythonPackage):
    """Working with color names and values formats defined by HTML and CSS."""

    homepage = "https://pypi.org/project/webcolors/"
    pypi = "webcolors/webcolors-1.11.1.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("24.11.1", sha256="ecb3d768f32202af770477b8b65f318fa4f566c22948673a977b00d589dd80f6")
    version("24.8.0", sha256="08b07af286a01bcd30d583a7acadf629583d1f79bfef27dd2c2c5c263817277d")
    version("24.6.0", sha256="1d160d1de46b3e81e58d0a280d0c78b467dc80f47294b91b1ad8029d2cedb55b")
    version("1.13", sha256="c225b674c83fa923be93d235330ce0300373d02885cef23238813b0d5668304a")
    version("1.12", sha256="16d043d3a08fd6a1b1b7e3e9e62640d09790dce80d2bdd4792a175b35fe794a9")
    version("1.11.1", sha256="76f360636957d1c976db7466bc71dcb713bb95ac8911944dffc55c01cb516de6")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@1.12:")
    depends_on("python@3.8:", type=("build", "run"), when="@24.6:")
    depends_on("python@3.9:", type=("build", "run"), when="@24.11:")
    depends_on("py-setuptools@61:", type=("build"), when="@:24.10")
    depends_on("py-pdm-backend", type=("build"), when="@24.11:")
