# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylint(PythonPackage):
    """python code static checker"""

    pypi = "pylint/pylint-1.6.5.tar.gz"

    import_modules = [
        "pylint",
        "pylint.lint",
        "pylint.extensions",
        "pylint.config",
        "pylint.checkers",
        "pylint.checkers.refactoring",
        "pylint.message",
        "pylint.utils",
        "pylint.pyreverse",
        "pylint.reporters",
        "pylint.reporters.ureports",
    ]

    license("GPL-2.0-or-later")

    version("2.16.2", sha256="13b2c805a404a9bf57d002cd5f054ca4d40b0b87542bdaba5e05321ae8262c84")
    version("2.15.0", sha256="4f3f7e869646b0bd63b3dfb79f3c0f28fc3d2d923ea220d52620fd625aed92b0")
    version("2.14.4", sha256="47705453aa9dce520e123a7d51843d5f0032cbfa06870f89f00927aa1f735a4a")
    version("2.13.5", sha256="dab221658368c7a05242e673c275c488670144123f4bd262b2777249c1c0de9b")
    version("2.11.1", sha256="2c9843fff1a88ca0ad98a256806c82c5a8f86086e7ccbdb93297d86c3f90c436")
    version("2.8.2", sha256="586d8fa9b1891f4b725f587ef267abe2a1bad89d6b184520c7f07a253dd6e217")

    depends_on("python@3.6:", when="@2.8.2:", type=("build", "run"))
    depends_on("python@3.6.2:", when="@2.13.5:", type=("build", "run"))
    depends_on("python@3.7.2:", when="@2.14.0:", type=("build", "run"))
    depends_on("py-setuptools-scm", when="@2.8.2", type="build")
    depends_on("py-setuptools@17.1:", type="build")
    depends_on("py-setuptools@62.6:62", when="@2.15.0:", type="build")
    depends_on("py-wheel@0.37.1:0.37", when="@2.15.0:", type="build")
    depends_on("py-dill@0.2:", when="@2.13.5:2.15", type=("build", "run"))
    depends_on("py-dill@0.2:", when="@2.16:  ^python@:3.10", type=("build", "run"))
    depends_on("py-dill@0.3.6:", when="@2.16.0: ^python@3.11:", type=("build", "run"))
    depends_on("py-platformdirs@2.2.0:", when="@2.11.1:", type=("build", "run"))
    depends_on("py-astroid", type=("build", "run"))
    # note there is no working version of astroid for this
    depends_on("py-astroid@1.5.1:", when="@1.7:", type=("build", "run"))
    depends_on("py-astroid@2.0:", when="@2.2.0:", type=("build", "run"))
    depends_on("py-astroid@2.2.0:2", when="@2.3.0:2.7", type=("build", "run"))
    depends_on("py-astroid@2.5.6:2.6", when="@2.8.0:2.10", type=("build", "run"))
    depends_on("py-astroid@2.8.0:2.8", when="@2.11.1", type=("build", "run"))
    depends_on("py-astroid@2.11.2:2.11", when="@2.13.5:2.13", type=("build", "run"))
    depends_on("py-astroid@2.11.6:2.11", when="@2.14.2:2.14", type=("build", "run"))
    depends_on("py-astroid@2.12.4:2.13", when="@2.15", type=("build", "run"))
    depends_on("py-astroid@2.14.2:2.15", when="@2.16:", type=("build", "run"))
    depends_on("py-isort@4.2.5:", type=("build", "run"))
    depends_on("py-isort@4.2.5:4", when="@2.3.1:2.5", type=("build", "run"))
    depends_on("py-isort@4.2.5:5", when="@2.6:", type=("build", "run"))
    depends_on("py-mccabe", type=("build", "run"))
    depends_on("py-mccabe@0.6.0:0.6", when="@2.3.1:2.11", type=("build", "run"))
    depends_on("py-mccabe@0.6.0:0.7", when="@2.13:", type=("build", "run"))
    depends_on("py-tomli@1.1.0:", when="@2.13.5: ^python@:3.10", type=("build", "run"))
    depends_on("py-tomlkit@0.10.1:", when="@2.14.0:", type=("build", "run"))
    depends_on("py-colorama@0.4.5:", when="platform=windows", type=("build", "run"))
    depends_on("py-typing-extensions@3.10.0:", when="@2.11.1: ^python@:3.9", type=("build", "run"))
    depends_on("py-six", when="@1:2.3.1", type=("build", "run"))
    depends_on("py-toml@0.7.1:", when="@2.8.2:2.12.2", type=("build", "run"))
