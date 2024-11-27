# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFindlibs(PythonPackage):
    """A package to search for shared libraries on various platforms."""

    homepage = "https://github.com/ecmwf/findlibs"
    pypi = "findlibs/findlibs-0.0.2.tar.gz"

    license("Apache-2.0")

    version("0.0.2", sha256="6c7e038496f9a97783ab2cd5736bb68522d5bebd8b0eb17c976b6a4ae4032c8d")

    depends_on("py-setuptools", type="build")

    # See https://github.com/ecmwf/findlibs/pull/5
    patch(
        "https://github.com/ecmwf/findlibs/commit/66a99a99d5d0a3215ed44aeb0af57991f3f7b8af.patch?full_index=1",
        sha256="6701e0e38d377b6459c0eedca76030f7400ac0bcc9c00aaba7ddf4fee6143159",
        when="@0.0.2",
    )
