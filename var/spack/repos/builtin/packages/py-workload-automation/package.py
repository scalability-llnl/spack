# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWorkloadAutomation(PythonPackage):
    """Workload Automation (WA) is a framework for executing workloads and
    collecting measurements on Android and Linux devices."""

    homepage = "https://github.com/ARM-software/workload-automation"
    url = "https://github.com/ARM-software/workload-automation/archive/v3.2.tar.gz"

    license("Apache-2.0")

    version("3.2", sha256="a3db9df6a9e0394231560ebe6ba491a513f6309e096eaed3db6f4cb924c393ea")
    version("3.1.4", sha256="217fc33a3739d011a086315ef86b90cf332c16d1b03c9dcd60d58c9fd1f37f98")
    version("3.1.3", sha256="152470808cf8dad8a833fd7b2cb7d77cf8aa5d1af404e37fa0a4ff3b07b925b2")
    version("3.1.2", sha256="8226a6abc5cbd96e3f1fd6df02891237a06cdddb8b1cc8916f255fcde20d3069")
    version("3.1.1", sha256="32a19be92e43439637c68d9146f21bb7a0ae7b8652c11dfc4b4bd66d59329ad4")
    version("3.1.0", sha256="f00aeef7a1412144c4139c23b4c48583880ba2147207646d96359f1d295d6ac3")
    version("3.0.0", sha256="8564b0c67541e3a212363403ee090dfff5e4df85770959a133c0979445b51c3c")
    version("2.7.0", sha256="e9005b9db18e205bf6c4b3e09b15a118abeede73700897427565340dcd589fbb")
    version("2.6.0", sha256="b94341fb067592cebe0db69fcf7c00c82f96b4eb7c7210e34b38473869824cce")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pexpect@3.3:", type=("build", "run"))
    depends_on("py-pyserial", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-wrapt", type=("build", "run"))
    depends_on("py-pandas@0.23.0:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-louie", type=("build", "run"))
    depends_on("py-devlib", type=("build", "run"))
