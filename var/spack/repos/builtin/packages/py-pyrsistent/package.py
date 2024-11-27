# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrsistent(PythonPackage):
    """Pyrsistent is a number of persistent collections
    (by some referred to as functional data structures).
    Persistent in the sense that they are immutable."""

    homepage = "https://github.com/tobgu/pyrsistent/"
    pypi = "pyrsistent/pyrsistent-0.15.7.tar.gz"

    license("MIT")

    version("0.19.3", sha256="1a2994773706bbb4995c31a97bc94f1418314923bd1048c6d964837040376440")
    version("0.18.1", sha256="d4d61f8b993a7255ba714df3aca52700f8125289f84f704cf80916517c46eb96")
    version("0.18.0", sha256="773c781216f8c2900b42a7b638d5b517bb134ae1acbebe4d1e8f1f41ea60eb4b")
    version("0.16.0", sha256="28669905fe725965daa16184933676547c5bb40a5153055a8dee2a4bd7933ad3")
    version("0.15.7", sha256="cdc7b5e3ed77bed61270a47d35434a30617b9becdf2478af76ad2c6ade307280")
    version("0.14.0", sha256="297714c609506494650eea704d70cbe1b156259a578a98b97864ab9a8cbad39f")

    depends_on("c", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools@42:", when="@0.18.0:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-six", when="@:0.17", type=("build", "run"))

    conflicts("python@3.10:", when="@0.14")
