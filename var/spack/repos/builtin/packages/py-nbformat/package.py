# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbformat(PythonPackage):
    """The Jupyter Notebook format"""

    homepage = "https://github.com/jupyter/nbformat"
    pypi = "nbformat/nbformat-5.0.7.tar.gz"

    license("BSD-3-Clause")

    version("5.8.0", sha256="46dac64c781f1c34dfd8acba16547024110348f9fc7eab0f31981c2a3dc48d1f")
    version("5.7.0", sha256="1d4760c15c1a04269ef5caf375be8b98dd2f696e5eb9e603ec2bf091f9b0d3f3")
    version("5.4.0", sha256="44ba5ca6acb80c5d5a500f1e5b83ede8cbe364d5a495c4c8cf60aaf1ba656501")
    version("5.1.3", sha256="b516788ad70771c6250977c1374fcca6edebe6126fd2adb5a69aa5c2356fd1c8")
    version("5.0.7", sha256="54d4d6354835a936bad7e8182dcd003ca3dc0cedfee5a306090e04854343b340")
    version("4.4.0", sha256="f7494ef0df60766b7cabe0a3651556345a963b74dbc16bc7c18479041170d402")
    version("4.1.0", sha256="dbf6c0ed0cb7c5a7184536368f1dd1ada2d48fd6f016e0f9e9b69236e28c0857")
    version("4.0.1", sha256="5261c957589b9dfcd387c338d59375162ba9ca82c69e378961a1f4e641285db5")
    version("4.0.0", sha256="daf9b990e96863d120aff123361156a316757757b81a8070eb6945e4a9774b2d")

    depends_on("py-hatchling@1.5:", when="@5.6:", type="build")
    depends_on("py-hatch-nodejs-version", when="@5.6:", type="build")

    depends_on("py-fastjsonschema", when="@5.3:", type=("build", "run"))
    depends_on("py-jsonschema@2.6:", when="@5.3:", type=("build", "run"))
    depends_on("py-jsonschema@2.4,2.5.1:", type=("build", "run"))
    depends_on("py-jupyter-core", type=("build", "run"))
    depends_on("py-traitlets@5.1:", when="@5.4:", type=("build", "run"))
    depends_on("py-traitlets@4.1:", type=("build", "run"))
    depends_on("py-importlib-metadata@3.6:", when="@5.7: ^python@:3.7", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools@60:", when="@5.3:5.4", type="build")
    depends_on("py-setuptools", when="@:5.4", type="build")
    depends_on("py-ipython-genutils", when="@:5.1", type=("build", "run"))
