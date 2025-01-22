# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyWebdataset(PythonPackage):
    """Python-based I/O for deep learning problems."""

    homepage = "https://github.com/webdataset/webdataset"
    pypi = "webdataset/webdataset-0.1.62.tar.gz"

    license("BSD-3-Clause")

    version("0.1.62", sha256="78b6c7810116d6875fa1ed8eb2dea29a54b86fde014cc2069f4c08fc3530ceb5")

    with default_args(type=("build", "link", "run")):
        depends_on("python@3.6:")

    # setup.py and requires.txt
    depends_on("py-braceexpand")
    depends_on("py-numpy")
