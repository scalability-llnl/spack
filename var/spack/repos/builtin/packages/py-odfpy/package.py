# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOdfpy(PythonPackage):
    """Odfpy is a library to read and write OpenDocument v. 1.2 files."""

    homepage = "https://github.com/eea/odfpy"
    pypi = "odfpy/odfpy-1.4.1.tar.gz"

    license("GPL-2.0-or-later")

    version("1.4.1", sha256="db766a6e59c5103212f3cc92ec8dd50a0f3a02790233ed0b52148b70d3c438ec")

    depends_on("py-setuptools", type="build")
    depends_on("py-defusedxml", type=("build", "run"))
