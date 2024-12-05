# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArrow(PythonPackage):
    """Arrow is a Python library that offers a sensible and human-friendly
    approach to creating, manipulating, formatting and converting dates,
    times and timestamps. It implements and updates the datetime type,
    plugging gaps in functionality and providing an intelligent module API
    that supports many common creation scenarios. Simply put, it helps you
    work with dates and times with fewer imports and a lot less code."""

    homepage = "https://arrow.readthedocs.io/en/latest/"
    pypi = "arrow/arrow-0.16.0.tar.gz"

    license("Apache-2.0")

    version("1.3.0", sha256="d4540617648cb5f895730f1ad8c82a65f2dad0166f57b75f3ca54759c4d67a85")
    version("1.2.3", sha256="3934b30ca1b9f292376d9db15b19446088d12ec58629bc3f0da28fd55fb633a1")
    version("1.2.2", sha256="05caf1fd3d9a11a1135b2b6f09887421153b94558e5ef4d090b567b47173ac2b")
    version("1.2.1", sha256="c2dde3c382d9f7e6922ce636bf0b318a7a853df40ecb383b29192e6c5cc82840")
    version("0.16.0", sha256="92aac856ea5175c804f7ccb96aca4d714d936f1c867ba59d747a8096ec30e90a")
    version("0.14.7", sha256="67f8be7c0cf420424bc62d8d7dc40b44e4bb2f7b515f9cc2954fb36e35797656")
    version("0.14.1", sha256="2d30837085011ef0b90ff75aa0a28f5c7d063e96b7e76b6cbc7e690310256685")

    depends_on("python@3.8:", type=("build", "run"), when="@1.3:")
    depends_on("python@3.6:", type=("build", "run"), when="@1.2.1:")
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"), when="@:0.16.0")
    depends_on("py-setuptools", type="build", when="@:1.2")
    depends_on("py-flit-core@3.2:3", type="build", when="@1.3:")
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"), when="@1.2.1:1.2 ^python@:3.7")
    depends_on("py-python-dateutil@2.7.0:", type=("build", "run"), when="@1.2.1:")
    depends_on("py-types-python-dateutil@2.8.10:", type=("build", "run"), when="@1.3:")
