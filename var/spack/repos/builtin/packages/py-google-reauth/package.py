# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleReauth(PythonPackage):
    """Google Reauth Library."""

    homepage = "https://github.com/Google/google-reauth-python"
    pypi = "google-reauth/google-reauth-0.1.1.tar.gz"

    license("Apache-2.0")

    version("0.1.1", sha256="f9f6852a55c2c5453d581cd01f3d1278e86147c03d008409800390a834235892")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyu2f", type=("build", "run"))
