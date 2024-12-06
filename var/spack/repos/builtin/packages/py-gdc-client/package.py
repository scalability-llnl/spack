# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGdcClient(PythonPackage):
    """The gdc-client provides several convenience functions
    over the GDC API which provides general download/upload via HTTPS."""

    homepage = "https://github.com/NCI-GDC/gdc-client"
    url = "https://github.com/NCI-GDC/gdc-client/archive/1.4.0.tar.gz"

    license("Apache-2.0")

    version("1.4.0", sha256="3ae6664f9666c75ffbf3c883409cfa51333f61d23b7aa99010925a084b4c9582")

    depends_on("py-setuptools", type="build")
