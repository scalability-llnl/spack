# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDecorator(PythonPackage):
    """The aim of the decorator module it to simplify the usage of decorators
    for the average programmer, and to popularize decorators by showing
    various non-trivial examples."""

    homepage = "https://github.com/micheles/decorator"
    pypi = "decorator/decorator-5.1.0.tar.gz"

    license("BSD-2-Clause")

    version("5.1.1", sha256="637996211036b6385ef91435e4fae22989472f9d571faba8927ba8253acbc330")
    version("5.1.0", sha256="e59913af105b9860aa2c8d3272d9de5a56a4e608db9a2f167a8480b323d529a7")
    version("5.0.9", sha256="72ecfba4320a893c53f9706bebb2d55c270c1e51a28789361aa93e4a21319ed5")
    version("4.4.2", sha256="e3a62f0520172440ca0dcc823749319382e377f37f140a0b99ef45fecb84bfe7")
    version("4.4.0", sha256="86156361c50488b84a3f148056ea716ca587df2f0de1d34750d35c21312725de")
    version("4.3.2", sha256="33cd704aea07b4c28b3eb2c97d288a06918275dac0ecebdaf1bc8a48d98adb9e")
    version("4.3.0", sha256="c39efa13fbdeb4506c476c9b3babf6a718da943dab7811c206005a4a956c080c")
    version("4.0.9", sha256="90022e83316363788a55352fe39cfbed357aa3a71d90e5f2803a35471de4bba8")

    depends_on("python@3.5:", when="@5.0.1:", type=("build", "run"))
    depends_on("python@2.6:2.8,3.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
