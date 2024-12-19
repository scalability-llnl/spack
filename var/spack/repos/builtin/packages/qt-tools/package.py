# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtTools(QtPackage):
    """Qt Tools contains tools like Qt Designer."""

    url = QtPackage.get_url(__qualname__)
    git = QtPackage.get_git(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    maintainers("wdconinc")

    license("BSD-3-Clause")

    # src/assistant/qlitehtml is a submodule that is not in the git archive
    version("6.8.1", commit="b0d66c51cbda17b213bed73d379f0900c77f457c", submodules=True)
    version("6.8.0", commit="3dd2b6ad0dd1a0480628b4cc74cb7b89a89e4a61", submodules=True)
    version("6.7.3", commit="ec4747e62a837a0262212a5f4fb03734660c7360", submodules=True)
    version("6.7.2", commit="46ffaed90df8c14d67b4b16fdf5e0b87ab227c88", submodules=True)

    variant(
        "assistant",
        default=False,
        description="Qt Assistant for viewing on-line documentation in Qt help file format.",
    )
    variant(
        "designer",
        default=False,
        description="Qt Widgets Designer for designing and building GUIs with Qt Widgets.",
    )

    depends_on("llvm +clang")

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

        if spec.satisfies("+assistant"):
            define("FEATURE_assistant", True)

        if spec.satisfies("+designer"):
            define("FEATURE_designer", True)

        return args
