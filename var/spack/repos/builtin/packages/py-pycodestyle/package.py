# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycodestyle(PythonPackage):
    """pycodestyle is a tool to check your Python code against some of the
    style conventions in PEP 8. Note: formerly called pep8."""

    homepage = "https://github.com/PyCQA/pycodestyle"
    pypi = "pycodestyle/pycodestyle-2.8.0.tar.gz"

    license("MIT")

    version("2.11.0", sha256="259bcc17857d8a8b3b4a2327324b79e5f020a13c16074670f9c8c8f872ea76d0")
    version("2.10.0", sha256="347187bdb476329d98f695c213d7295a846d1152ff4fe9bacb8a9590b8ee7053")
    version("2.9.1", sha256="2c9607871d58c76354b697b42f5d57e1ada7d261c261efac224b664affdc5785")
    version("2.9.0", sha256="beaba44501f89d785be791c9462553f06958a221d166c64e1f107320f839acc2")
    version("2.8.0", sha256="eddd5847ef438ea1c7870ca7eb78a9d47ce0cdb4851a5523949f2601d0cbbe7f")
    version("2.7.0", sha256="c389c1d06bf7904078ca03399a4816f974a1d590090fecea0c63ec26ebaf1cef")
    version("2.6.0", sha256="c58a7d2815e0e8d7972bf1803331fb0152f867bd89adf8a01dfd55085434192e")
    version("2.5.0", sha256="a603453c07e8d8e15a43cf062aa7174741b74b4a27b110f9ad03d74d519173b5")
    version("2.3.1", sha256="682256a5b318149ca0d2a9185d365d8864a768a28db66a84a2ea946bcc426766")
    version("2.3.0", sha256="a5910db118cf7e66ff92fb281a203c19ca2b5134620dd2538a794e636253863b")
    version("2.2.0", sha256="df81dc3293e0123e2e8d1f2aaf819600e4ae287d8b3af8b72181af50257e5d9a")
    version("2.1.0", sha256="5b540e4f19b4938c082cfd13f5d778d1ad2308b337abbc687ab9335233f5f3e2")
    version("2.0.0", sha256="37f0420b14630b0eaaf452978f3a6ea4816d787c3e6dcbba6fb255030adae2e7")

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pycodestyle requires py-setuptools during runtime as well.
    depends_on("py-setuptools", type=("build", "run"))
