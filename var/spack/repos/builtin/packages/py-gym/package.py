# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGym(PythonPackage):
    """OpenAI Gym is a toolkit for developing and comparing
    reinforcement learning algorithms. This is the gym open-source
    library, which gives you access to a standardized set of
    environments."""

    homepage = "https://github.com/openai/gym"
    pypi = "gym/gym-0.18.0.tar.gz"

    license("MIT")

    version("0.19.0", sha256="940069b983806e1ccc400fa6d47b4e34e462accf6a4fb0acb0a5e509ad0f502d")
    version("0.18.0", sha256="a0dcd25c1373f3938f4cb4565f74f434fba6faefb73a42d09c9dddd0c08af53e")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"), when="@0.18.0")
    depends_on("py-numpy@1.10.4:", type=("build", "run"), when="@0.18.0")
    depends_on("py-numpy@1.18.0:", type=("build", "run"), when="@0.19.0")
    depends_on("py-pyglet@1.4.0:1.5.0", type=("build", "run"), when="@0.18.0")
    depends_on("pil@:7.2.0", type=("build", "run"), when="@0.18.0")
    depends_on("py-cloudpickle@1.2.0:1.6", type=("build", "run"))
