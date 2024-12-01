# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyface(PythonPackage):
    """The pyface project contains a toolkit-independent GUI abstraction layer,
    which is used to support the "visualization" features of the Traits
    package. Thus, you can write code in terms of the Traits API (views, items,
    editors, etc.), and let pyface and your selected toolkit and back-end take
    care of the details of displaying them."""

    homepage = "https://docs.enthought.com/pyface"
    pypi = "pyface/pyface-6.1.2.tar.gz"

    license("EPL-1.0")

    version("7.3.0", sha256="a7031ec4cfff034affc822e47ff5e6c1a0272e576d79465cdbbe25f721740322")
    version("6.1.2", sha256="7c2ac3d5cbec85e8504b3b0b63e9307be12c6d710b46bae372ce6562d41f4fbc")

    variant(
        "backend",
        default="pyqt5",
        description="Default backend",
        values=("wx", "pyqt", "pyqt5", "pyside", "pyside2"),
        multi=False,
    )

    depends_on("py-setuptools", type="build")
    depends_on("py-importlib-metadata", when="@7.2:", type=("build", "run"))
    depends_on("py-importlib-resources@1.1:", when="@7.2:", type=("build", "run"))
    depends_on("py-traits@6.2:", when="@7.3:", type=("build", "run"))
    depends_on("py-traits@6:", when="@7:", type=("build", "run"))
    depends_on("py-traits", type=("build", "run"))

    conflicts("backend=pyside", when="@7.3:")
    conflicts("backend=pyside2", when="@:6")

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
