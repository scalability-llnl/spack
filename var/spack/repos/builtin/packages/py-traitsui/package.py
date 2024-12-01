# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTraitsui(PythonPackage):
    """The TraitsUI project contains a toolkit-independent GUI abstraction
    layer, which is used to support the "visualization" features of the Traits
    package. Thus, you can write model in terms of the Traits API and specify a
    GUI in terms of the primitives supplied by TraitsUI (views, items, editors,
    etc.), and let TraitsUI and your selected toolkit and back-end take care of
    the details of displaying them."""

    homepage = "https://docs.enthought.com/traitsui"
    pypi = "traitsui/traitsui-6.1.3.tar.gz"

    license("EPL-1.0")

    version("7.2.1", sha256="dfc39015faf0591f9927e3d4d22bd95a16d49c85db30e60acd4ba7b85c7c5d5b")
    version("6.1.3", sha256="48381763b181efc58eaf288431d1d92d028d0d97dfdd33eba7809aae8aef814f")

    variant(
        "backend",
        default="pyqt5",
        description="Default backend",
        values=("wx", "pyqt", "pyqt5", "pyside", "pyside2"),
        multi=False,
    )

    depends_on("python@3.6:", when="@7.2:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-traits@6.2:", when="@7.3:", type=("build", "run"))
    depends_on("py-traits@6.1:", when="@7.2:", type=("build", "run"))
    depends_on("py-traits@6:", when="@7.1:", type=("build", "run"))
    depends_on("py-traits", type=("build", "run"))
    depends_on("py-pyface@7.3:", when="@7.3:", type=("build", "run"))
    depends_on("py-pyface@7.1:", when="@7.1:", type=("build", "run"))
    depends_on("py-pyface@6:", type=("build", "run"))
    depends_on("py-six", when="@:6", type=("build", "run"))

    conflicts("backend=pyside", when="@7.1:")
    conflicts("backend=pyside2", when="@:7.0")

    # Backends
    with when("backend=wx"):
        depends_on("py-wxpython@4:", when="@7:", type=("build", "run"))
        depends_on("py-wxpython@2.8.10:", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
    with when("backend=pyqt"):
        depends_on("py-pyqt4@4.10:", type=("build", "run"))
        depends_on("py-pygments", type=("build", "run"))
    with when("backend=pyqt5"):
        depends_on("py-pyqt5@5:", type=("build", "run"))
        depends_on("py-pygments", type=("build", "run"))
    with when("backend=pyside"):
        depends_on("py-pyside@1.2:", type=("build", "run"))
        depends_on("py-pygments", type=("build", "run"))
    with when("backend=pyside2"):
        depends_on("py-pyside2", type=("build", "run"))
        depends_on("py-shiboken2", type=("build", "run"))
        depends_on("py-pygments", type=("build", "run"))
