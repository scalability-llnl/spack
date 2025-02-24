# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVirtualenvwrapper(PythonPackage):
    """virtualenvwrapper is a set of extensions to Ian Bicking's
    virtualenv tool. The extensions include wrappers for creating and
    deleting virtual environments and otherwise managing your development
    workflow, making it easier to work on more than one project at a time
    without introducing conflicts in their dependencies."""

    homepage = "https://github.com/python-virtualenvwrapper/virtualenvwrapper"
    pypi = "virtualenvwrapper/virtualenvwrapper-4.8.2.tar.gz"

    license("MIT")

    version("6.1.1", sha256="112e7ea34a9a3ce90aaea54182f0d3afef4d1a913eeb75e98a263b4978cd73c6")
    version("6.1.0", sha256="d467beac5a44be00fb5cd1bcf332398c3dab5fb3bd3af7815ea86b4d6bb3d3a4")
    version("6.0.0", sha256="4cdaca4a01bb11c3343b01439cf2d76ebe97bb28c4b9a653a9b1f1f7585cd097")
    version("4.8.4", sha256="51a1a934e7ed0ff221bdd91bf9d3b604d875afbb3aa2367133503fee168f5bfa")
    version("4.8.2", sha256="18d8e4c500c4c4ee794f704e050cf2bbb492537532a4521d1047e7dd1ee4e374")

    depends_on("python@2.6:")
    depends_on("py-pbr", type="build", when="@4.8")
    depends_on("py-virtualenv", type=("build", "run"))
    depends_on("py-virtualenv-clone", type=("build", "run"))
    depends_on("py-stevedore", type=("build", "run"))
    # not just build-time, requires pkg_resources
    depends_on("py-setuptools", type=("build", "run"))
