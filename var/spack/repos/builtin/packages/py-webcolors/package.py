# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebcolors(PythonPackage):
    """Working with color names and values formats defined by HTML and CSS."""

    homepage = "https://pypi.org/project/webcolors/"
    pypi = "webcolors/webcolors-1.11.1.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("24.6.0", sha256="1d160d1de46b3e81e58d0a280d0c78b467dc80f47294b91b1ad8029d2cedb55b")
    version("1.13", sha256="c225b674c83fa923be93d235330ce0300373d02885cef23238813b0d5668304a")
    version("1.12", sha256="16d043d3a08fd6a1b1b7e3e9e62640d09790dce80d2bdd4792a175b35fe794a9")
    version("1.11.1", sha256="76f360636957d1c976db7466bc71dcb713bb95ac8911944dffc55c01cb516de6")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@1.12:")
    depends_on("python@3.8:", type=("build", "run"), when="@24.6:")
    depends_on("py-setuptools@61:", type=("build"))
