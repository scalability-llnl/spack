# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleAuthHttplib2(PythonPackage):
    """Google Authentication Library: httplib2 transport."""

    homepage = "https://github.com/GoogleCloudPlatform/google-auth-library-python-httplib2"
    pypi = "google-auth-httplib2/google-auth-httplib2-0.0.3.tar.gz"

    license("Apache-2.0")

    version("0.1.0", sha256="a07c39fd632becacd3f07718dfd6021bf396978f03ad3ce4321d060015cc30ac")
    version("0.0.3", sha256="098fade613c25b4527b2c08fa42d11f3c2037dda8995d86de0745228e965d445")

    depends_on("py-setuptools", type="build")
    depends_on("py-google-auth", type=("build", "run"))
    depends_on("py-httplib2@0.15:", when="@0.1:", type=("build", "run"))
    depends_on("py-httplib2@0.9.1:", type=("build", "run"))
    depends_on("py-six", when="@0.1:", type=("build", "run"))
