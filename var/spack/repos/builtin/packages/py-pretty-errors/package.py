# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPrettyErrors(PythonPackage):
    """Prettifies Python exception output to make it legible."""

    homepage = "https://github.com/onelivesleft/PrettyErrors/"
    pypi = "pretty-errors/pretty_errors-1.2.25.tar.gz"

    license("MIT")

    version("1.2.25", sha256="a16ba5c752c87c263bf92f8b4b58624e3b1e29271a9391f564f12b86e93c6755")

    depends_on("py-setuptools", type="build")
    depends_on("py-colorama", type=("build", "run"))
