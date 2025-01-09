# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Qscintilla(QMakePackage):
    """
    QScintilla is a port to Qt of Neil Hodgson's Scintilla C++ editor control.
    """

    homepage = "https://www.riverbankcomputing.com/software/qscintilla/intro"
    url = "https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.12.0/QScintilla_src-2.12.0.tar.gz"

    license("GPL-3.0-only")

    version("2.14.1", sha256="dfe13c6acc9d85dfcba76ccc8061e71a223957a6c02f3c343b30a9d43a4cdd4d")
    version("2.14.0", sha256="449353928340300804c47b3785c3e62096f918a723d5eed8a5439764e6507f4c")
    version("2.13.4", sha256="890c261f31e116f426b0ea03a136d44fc89551ebfd126d7b0bdf8a7197879986")
    version("2.13.3", sha256="711d28e37c8fccaa8229e8e39a5b3b2d97f3fffc63da10b71c71b84fa3649398")
    version("2.12.0", sha256="2116181cce3076aa4897e36182532d0e6768081fb0cf6dcdd5be720519ab1434")

    depends_on("cxx", type="build")  # generated

    variant("designer", default=False, description="Enable pluging for Qt-Designer")
    variant("python", default=False, description="Build python bindings")

    depends_on("qmake")
    with when("+python"):
        depends_on("qt+opengl", when="^[virtuals=qmake] qt")
        depends_on("qt-base +opengl", when="^[virtuals=qmake] qt-base")

    depends_on("py-pyqt6", type=("build", "run"), when="+python ^qt-base")
    depends_on("py-pyqt-builder", type="build", when="+python")
    depends_on("py-pyqt5", type=("build", "run"), when="+python ^qt@5")
    depends_on("python", type=("build", "run"), when="+python")
    # adter install inquires py-sip variant : so we need to have it
    depends_on("py-sip", type="build", when="~python")

    extends("python", when="+python")

    # https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.12.0/ChangeLog
    conflicts("^qt@4", when="@2.12:")

    build_directory = "src"  # was Qt4Qt5 before 2.12.0

    def qmake_args(self):
        # below, DEFINES ... gets rid of ...regex...errors during build
        # although, there shouldn't be such errors since we use '-std=c++11'
        args = ["CONFIG+=-std=c++11", "DEFINES+=NO_CXX11_REGEX=1"]
        # by default, the package tries to build with accessibility support, and fails
        # possibly there's a bug somewhere that needs to be fixed
        if "^qt-base" in self.spec:
            args.append("DEFINES+=QT_NO_ACCESSIBILITY")
        return args

    # When INSTALL_ROOT is unset, qscintilla is installed under qt_prefix
    # giving 'Nothing Installed Error'
    def setup_build_environment(self, env):
        env.set("INSTALL_ROOT", self.prefix)

    def setup_run_environment(self, env):
        env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)

    # Fix install prefix
    @run_after("qmake")
    def fix_install_path(self):
        makefile = FileFilter(join_path(self.build_directory, "Makefile"))
        makefile.filter(
            "$(INSTALL_ROOT)" + self.spec["qmake"].prefix, "$(INSTALL_ROOT)", string=True
        )

    @run_after("install", when="+designer")
    def make_designer(self):
        # Make designer plugin
        with working_dir(os.path.join(self.stage.source_path, "designer")):
            # TODO: qmake fails with qt6
            qmake("designer.pro", "INCLUDEPATH+=../src")
            make()
            makefile = FileFilter("Makefile")
            makefile.filter(
                "$(INSTALL_ROOT)" + self.spec["qmake"].prefix, "$(INSTALL_ROOT)", string=True
            )
            make("install")

    @run_after("install", when="+python")
    def make_qsci_python(self):
        if "^py-pyqt5" in self.spec:
            qtx = "qt5"
            py_pyqtx = "py-pyqt5"
            pyqtx = "PyQt5"
            ftoml = "pyproject-qt5.toml"
        elif "^py-pyqt6" in self.spec:
            qtx = "qt6"
            py_pyqtx = "py-pyqt6"
            pyqtx = "PyQt6"
            ftoml = "pyproject-qt6.toml"

        with working_dir(join_path(self.stage.source_path, "Python")):
            copy(ftoml, "pyproject.toml")
            sip_inc_dir = join_path(
                self.spec[py_pyqtx].package.module.python_platlib, pyqtx, "bindings"
            )

            with open("pyproject.toml", "a") as tomlfile:
                # https://pyqt-builder.readthedocs.io/en/latest/pyproject_toml.html
                tomlfile.write(f'\n[tool.sip.project]\nsip-include-dirs = ["{sip_inc_dir}"]\n')
                # add widgets and printsupport to Qsci.pro
                # also add link statement to fix "undefined symbol _Z...Qsciprinter...
                link_qscilibs = "LIBS += -L" + self.prefix.lib + " -lqscintilla2_" + qtx
                tomlfile.write(
                    f'\n[tool.sip.builder]\nqmake-settings = \
                    ["QT += widgets", "QT += printsupport", "{link_qscilibs}"]\n'
                )

            mkdirp(os.path.join(self.prefix.share.sip, pyqtx))

            sip_build = Executable(self.spec["py-sip"].prefix.bin.join("sip-build"))
            sip_build(
                "--target-dir=" + python_platlib,
                "--qsci-include-dir=" + self.spec.prefix.include,
                "--qsci-library-dir=" + self.spec.prefix.lib,
                "--api-dir=" + self.prefix.share.qsci,
                "--verbose",
            )

            makefile = FileFilter(join_path("build", "Qsci", "Makefile"))
            makefile.filter("$(INSTALL_ROOT)", "", string=True)
            make("install", "-C", join_path("build", "Qsci"))

            makefile = FileFilter(join_path("build", "Makefile"))
            makefile.filter("$(INSTALL_ROOT)", "", string=True)
            make("install", "-C", "build/")

    def test_python_import(self):
        """check Qsci import"""
        if self.spec.satisfies("~python"):
            raise SkipTest("Package must be installed with +python")

        python = self.spec["python"].command
        if "^py-pyqt5" in self.spec:
            python("-c", "import PyQt5.Qsci")
        if "^py-pyqt6" in self.spec:
            python("-c", "import PyQt6.Qsci")
