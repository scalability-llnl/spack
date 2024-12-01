# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNtplib(PythonPackage):
    """Simple interface to query NTP servers from Python."""

    homepage = "https://github.com/cf-natali/ntplib"
    git = "https://github.com/cf-natali/ntplib.git"
    pypi = "ntplib/ntplib-0.4.0.tar.gz"

    license("MIT")

    version("0.4.0", sha256="899d8fb5f8c2555213aea95efca02934c7343df6ace9d7628a5176b176906267")

    depends_on("python@2.7,3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
