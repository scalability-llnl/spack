# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtTools(QtPackage):
    """Qt Tools contains tools like Qt Designer."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    license("BSD-3-Clause")

    version("6.7.2", sha256="3ae2db630606edf94cc368691ee1da9c0bae7a06ff46c544c459cece8b60b62a")

    variant(
        "designer",
        default=False,
        description="Qt Widgets Designer for designing and building GUIs with Qt Widgets.",
    )

    depends_on("qt-base +network")
    depends_on("qt-base +widgets", when="+designer")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)

    def cmake_args(self):
        spec = self.spec

        args = super().cmake_args() + []

        def define(cmake_var, value):
            args.append(self.define(cmake_var, value))

        if spec.satisfies("+designer"):
            define("FEATURE_designer", True)

        return args

    def setup_run_environment(self, env):
        env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)
