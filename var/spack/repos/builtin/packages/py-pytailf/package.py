# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytailf(PythonPackage):
    """Simple python tail -f wrapper"""

    homepage = "https://bitbucket.org/angry_elf/pytailf/src/default/"
    pypi = "pytailf/pytailf-1.1.tar.bz2"

    version("1.1", sha256="d97135ef28ac4a51dfd98887131ce2bffd5d0d6ba757793a4b79740dfb067ace")

    depends_on("py-setuptools", type="build")
