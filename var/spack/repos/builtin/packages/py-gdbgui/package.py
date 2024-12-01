# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGdbgui(PythonPackage):
    """gdbgui is a modern, free, browser-based frontend to gdb"""

    homepage = "https://gdbgui.com"
    pypi = "gdbgui/gdbgui-0.11.2.1.tar.gz"

    license("GPL-3.0-or-later")

    version("0.13.2.0", sha256="80e347a08b8cc630ab9f68482a1ed92c844fbfde46dc21fd39f3e6ef14b72e54")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-flask@0.12.2:0", type=("build", "run"))
    depends_on("py-flask-compress@1.4.0:1", type=("build", "run"))
    depends_on("py-flask-socketio@2.9.3:2", type=("build", "run"))
    depends_on("py-gevent@1.2.2:1", type=("build", "run"))
    depends_on("py-pygdbmi@0.9.0.0:0", type=("build", "run"))
    depends_on("py-pygments@2.2.0:2", type=("build", "run"))
    depends_on("gdb", type="run")
