# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonPtrace(PythonPackage):
    """python-ptrace is a debugger using ptrace (Linux, BSD and Darwin system
    call to trace processes) written in Python."""

    pypi = "python-ptrace/python-ptrace-0.9.8.tar.gz"

    license("GPL-2.0-only")

    version("0.9.8", sha256="1e3bc6223f626aaacde8a7979732691c11b13012e702fee9ae16c87f71633eaa")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
