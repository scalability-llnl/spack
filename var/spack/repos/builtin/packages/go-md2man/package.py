# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GoMd2man(GoPackage):
    """go-md2man converts markdown into roff (man pages)"""

    homepage = "https://github.com/cpuguy83/go-md2man"
    url = "https://github.com/cpuguy83/go-md2man/archive/v1.0.10.tar.gz"

    license("MIT")

    version("2.0.4", sha256="b0a4c7c077ede56967deef6ab7e7696c0f46124b0b3360fd05564ec5a536f11f")
    version("2.0.3", sha256="7ca3a04bb4ab83387538235decc42a535097a05d2fb9f2266d0c47b33119501f")
    version("2.0.2", sha256="2f52e37101ea2734b02f2b54a53c74305b95b3a9a27792fdac962b5354aa3e4a")
    version("1.0.10", sha256="76aa56849123b99b95fcea2b15502fd886dead9a5c35be7f78bdc2bad6be8d99")
