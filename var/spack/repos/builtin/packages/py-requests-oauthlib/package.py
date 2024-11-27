# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsOauthlib(PythonPackage):
    """This project provides first-class OAuth library support for Requests."""

    homepage = "https://github.com/requests/requests-oauthlib"
    pypi = "requests-oauthlib/requests-oauthlib-1.2.0.tar.gz"

    license("ISC")

    version("1.3.1", sha256="75beac4a47881eeb94d5ea5d6ad31ef88856affe2332b9aafb52c6452ccf0d7a")
    version("1.3.0", sha256="b4261601a71fd721a8bd6d7aa1cc1d6a8a93b4a9f5e96626f8e4d91e8beeaa6a")
    version("1.2.0", sha256="bd6533330e8748e94bf0b214775fed487d309b8b8fe823dc45641ebcd9a32f57")
    version("0.3.3", sha256="37557b4de3eef50d2a4c65dc9382148b8331f04b1c637c414b3355feb0f007e9")

    depends_on("py-setuptools", type="build")
    depends_on("py-oauthlib@3.0.0:", type=("build", "run"))
    depends_on("py-requests@2.0.0:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
