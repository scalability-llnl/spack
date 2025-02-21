# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfghjkl(PythonPackage):
    """ASDL: Automatic Second-order Differentiation (for Fisher, Gradient covariance, Hessian,
    Jacobian, and Kernel) Library."""

    homepage = "https://github.com/kazukiosawa/asdl"
    pypi = "asdfghjkl/asdfghjkl-0.1a4.tar.gz"

    license("MIT")

    version("0.1a4", sha256="a934411a0ffdee6fcdccb19672196498ea6a8e55e3e67abbe67200c84b46ddee")

    depends_on("py-setuptools@42:")

    with default_args(type=("build", "run")):
        depends_on("py-torch@1.13:")
        depends_on("py-numpy")
