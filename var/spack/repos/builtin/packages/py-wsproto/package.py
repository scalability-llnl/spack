# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWsproto(PythonPackage):
    """This repository contains a pure-Python implementation of
    a WebSocket protocol stack. It's written from the ground up
    to be embeddable in whatever program you choose to use,
    ensuring that you can communicate via WebSockets, as
    defined in RFC6455, regardless of your programming
    paradigm."""

    homepage = "https://github.com/python-hyper/wsproto/"
    pypi = "wsproto/wsproto-1.0.0.tar.gz"

    license("MIT")

    version("1.0.0", sha256="868776f8456997ad0d9720f7322b746bbe9193751b5b290b7f924659377c8c38")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-h11@0.9.0:0", type=("build", "run"))
