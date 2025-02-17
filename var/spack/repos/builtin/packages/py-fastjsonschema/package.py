# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastjsonschema(PythonPackage):
    """Fast JSON schema validator for Python."""

    homepage = "https://github.com/horejsek/python-fastjsonschema"
    pypi = "fastjsonschema/fastjsonschema-2.15.1.tar.gz"

    license("BSD-3-Clause")

    version("2.21.1", sha256="794d4f0a58f848961ba16af7b9c85a3e88cd360df008c59aac6fc5ae9323b5d4")
    version("2.21.0", sha256="a02026bbbedc83729da3bfff215564b71902757f33f60089f1abae193daa4771")
    version("2.20.0", sha256="3d48fc5300ee96f5d116f10fe6f28d938e6008f59a6a025c2649475b87f76a23")
    version("2.19.1", sha256="e3126a94bdc4623d3de4485f8d468a12f02a67921315ddc87836d6e456dc789d")
    version("2.19.0", sha256="e25df6647e1bc4a26070b700897b07b542ec898dd4f1f6ea013e7f6a88417225")
    version("2.18.1", sha256="06dc8680d937628e993fa0cd278f196d20449a1adc087640710846b324d422ea")
    version("2.18.0", sha256="e820349dd16f806e4bd1467a138dced9def4bc7d6213a34295272a6cac95b5bd")
    version("2.17.1", sha256="f4eeb8a77cef54861dbf7424ac8ce71306f12cbb086c45131bcba2c6a4f726e3")
    version("2.17.0", sha256="1a68234b7a20ab35ce6600a35ce76a18bac630fc0c6443b3ae22e89fa21d8987")
    version("2.16.3", sha256="4a30d6315a68c253cfa8f963b9697246315aa3db89f98b97235e345dedfb0b8e")
    version("2.16.2", sha256="01e366f25d9047816fe3d288cbfc3e10541daf0af2044763f3d0ade42476da18")
    version("2.15.1", sha256="671f36d225b3493629b5e789428660109528f373cf4b8a22bac6fa2f8191c2d2")

    depends_on("python@3.3:3.13", when="@2.21:", type=("build", "run"))
    depends_on("python@3.3:3.12", when="@2.20:", type=("build", "run"))
    depends_on("python@3.3:3.11", when="@2.16.3:", type=("build", "run"))
    depends_on("python@3.3:", when="@2.15:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
