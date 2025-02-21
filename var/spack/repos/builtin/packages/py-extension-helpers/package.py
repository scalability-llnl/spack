# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyExtensionHelpers(PythonPackage):
    """The extension-helpers package includes convenience helpers to
    assist with building Python packages with compiled C/Cython
    extensions. It is developed by the Astropy project but is intended
    to be general and usable by any Python package."""

    homepage = "https://github.com/astropy/extension-helpers"
    pypi = "extension-helpers/extension_helpers-1.2.0.tar.gz"

    license("BSD-3-Clause")

    version("1.2.0", sha256="e7d9c8f71804edd7ecd05b5d59a5b504f6e24867970abfc12771242eed76ebcc")
    version(
        "0.1",
        sha256="ac8a6fe91c6d98986a51a9f08ca0c7945f8fd70d95b662ced4040ae5eb973882",
        # 0.1 uses dash in the tarball name
        url="https://files.pythonhosted.org/packages/81/78/056daee475dfc41cc0b62540388703cddcae4d4f6bef10c6ce1aea76ebaf/extension-helpers-0.1.tar.gz",
    )

    depends_on("c", type="build")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"), when="@1.2.0:")

    depends_on("py-setuptools@30.3:", type="build")
    depends_on("py-setuptools@43.0.0:", type="build", when="@1.2.0:")
    depends_on("py-setuptools-scm@6.2:", type="build", when="@1.2.0:")

    depends_on("py-setuptools@40.2:", type=("build", "run"), when="@1.2.0:")
    depends_on("py-tomli@1.0.0:", type=("build", "run"), when="@1.2.0: ^python@:3.10")
