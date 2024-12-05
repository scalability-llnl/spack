# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPython3Openid(PythonPackage):
    """OpenID support for modern servers and consumers."""

    homepage = "https://github.com/necaris/python3-openid"
    pypi = "python3-openid/python3-openid-3.2.0.tar.gz"

    license("Apache-2.0")

    version("3.2.0", sha256="33fbf6928f401e0b790151ed2b5290b02545e8775f982485205a066f874aaeaf")

    depends_on("py-setuptools", type="build")
