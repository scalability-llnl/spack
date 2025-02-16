# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetis(PythonPackage):
    """Wrapper for the METIS library for partitioning graphs (and other stuff)."""

    homepage = "https://github.com/kw/metis-python"
    pypi = "metis/metis-0.2a5.tar.gz"

    maintainers("Chrismarsh")

    license("MIT", checked_by="Chrismarsh")

    version("0.2a5", sha256="c98f4aa129141554bea8d9e62daea5fea8351439f723e8e27fe593c2b7c53903")

    depends_on("py-setuptools", type="build")
    depends_on("metis", type=("build", "run"))
