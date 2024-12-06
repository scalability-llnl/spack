# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbsphinx(PythonPackage):
    """nbsphinx is a Sphinx extension that provides a source parser for
    *.ipynb files.
    """

    # It should be noted that in order to have nbsphinx work,
    # one must create a Spack view of the dependencies.

    homepage = "https://nbsphinx.readthedocs.io"
    pypi = "nbsphinx/nbsphinx-0.8.0.tar.gz"

    license("MIT")

    version("0.8.8", sha256="b5090c824b330b36c2715065a1a179ad36526bff208485a9865453d1ddfc34ec")
    version("0.8.7", sha256="ff91b5b14ceb1a9d44193b5fc3dd3617e7b8ab59c788f7710049ce5faff2750c")
    version("0.8.1", sha256="24d59aa3a1077ba58d9769c64c38fb05b761a1af21c1ac15f6393500cd008ea6")
    version("0.8.0", sha256="369c16fe93af14c878d61fb3e81d838196fb35b27deade2cd7b95efe1fe56ea0")

    # https://nbsphinx.readthedocs.io/en/latest/installation.html
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-nbconvert@:5.3,5.5:", type=("build", "run"))
    depends_on("py-traitlets", type=("build", "run"))
    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-sphinx@1.8:", type=("build", "run"))
    depends_on("pandoc", type="run")
