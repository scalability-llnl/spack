# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyValidators(PythonPackage):
    """Python Data Validation for Humans."""

    homepage = "https://github.com/kvesteri/validators"
    pypi = "validators/validators-0.20.0.tar.gz"

    license("MIT")

    version("0.34.0", sha256="647fe407b45af9a74d245b943b18e6a816acf4926974278f6dd617778e1e781f")
    version("0.20.0", sha256="24148ce4e64100a2d5e267233e23e7afeb55316b47d30faae7eb6e7292bc226a")

    depends_on("py-setuptools", type="build")
    depends_on("py-decorator@3.4:", type=("build", "run"), when="@:0.20.7")
