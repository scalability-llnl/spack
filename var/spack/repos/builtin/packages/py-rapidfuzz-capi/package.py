# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRapidfuzzCapi(PythonPackage):
    """
    C-API of RapidFuzz, which can be used to extend RapidFuzz from separate packages.
    """

    homepage = "https://github.com/maxbachmann/rapidfuzz_capi"
    pypi = "rapidfuzz_capi/rapidfuzz_capi-1.0.5.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("1.0.5", sha256="b3af179874b28364ba1b7850e37d0d353de9cf5b844e3569c023b74da3a9c68e")

    depends_on("py-setuptools", type="build")
