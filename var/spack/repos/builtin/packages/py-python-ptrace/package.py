# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonPtrace(PythonPackage):
    """python-ptrace is a debugger using ptrace (Linux, BSD and Darwin system
    call to trace processes) written in Python."""

    pypi = "python-ptrace/python-ptrace-0.9.8.tar.gz"

    license("GPL-2.0-only")

    version("0.9.9", sha256="56bbfef44eaf3a77be48138cca5767cdf471e8278fe1499f9b72f151907f25cf")
    version("0.9.8", sha256="1e3bc6223f626aaacde8a7979732691c11b13012e702fee9ae16c87f71633eaa")

    depends_on("c", type="build")

    depends_on("py-setuptools", type="build")

    # uses imp
    depends_on("python@:3.11", when="@:0.9.8")
