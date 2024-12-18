# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PySip(PythonPackage):
    """A Python bindings generator for C/C++ libraries."""

    homepage = "https://www.riverbankcomputing.com/software/sip"
    pypi = "sip/sip-6.4.0.tar.gz"

    license("GPL-2.0-or-later")

    version("6.8.5", sha256="5dddd5966e9875d89ecde9d3e6ac63225f9972e4d25c09e20fa22f1819409c70")
    version("6.7.9", sha256="35d51fc10f599d3696abb50f29d068ad04763df7b77808c76b74597660f99b17")
    version("6.6.2", sha256="0e3efac1c5dfd8e525ae57140927df26993e13f58b89d1577c314f4105bfd90d")
    version("6.4.0", sha256="42ec368520b8da4a0987218510b1b520b4981e4405086c1be384733affc2bcb0")
    version("5.5.0", sha256="5d024c419b30fea8a6de8c71a560c7ab0bc3c221fbfb14d55a5b865bd58eaac5")
    version("4.19.25", sha256="3d36986f7327b7b966bb6eacf22bcf6e4d0a3d24e392276ef92af89988818062")
    version("4.19.21", sha256="3bfd58e875a87471c00e008f25a01d8312885aa01efc4f688e5cac861c8676e4")
    version("4.19.20", sha256="475f85277a6601c406ade508b6c935b9f2a170c16fd3ae9dd4cdee7a4f7f340d")
    version("4.19.19", sha256="348cd6229b095a3090e851555814f5147bffcb601cec891f1038eb6b38c9d856")
    version("4.19.18", sha256="e274a8b9424047c094a40a8e70fc5e596c191cb8820472846d7bf739e461b2e8")
    version("4.19.15", sha256="02bff1ac89253e12cdf1406ad39f841d0e264b0d96a7de13dfe9e29740df2053")
    version("4.19.13", sha256="92193fcf990503bf29f03e290efc4ee1812d556efc18acf5c8b88c090177a630")

    depends_on("c", type="build")  # generated

    variant(
        "module",
        default="sip",
        when="@:4",
        description="Name of private SIP module",
        values=str,
        multi=False,
    )

    depends_on("py-ply", type=("build", "run"), when="@6.6:")

    with when("@5:"):
        depends_on("python", type=("build", "link", "run"))
        depends_on("py-packaging", type=("build", "run"))
        depends_on("py-setuptools@64:", type=("build", "run"), when="@6.8.4:")
        depends_on("py-setuptools@30.3:", type=("build", "run"), when="@:6.8.3")
        depends_on("py-setuptools-scm@8:", type="build", when="@6.8.4:")
        depends_on("py-tomli", type=("build", "run"), when="@6.7: ^python@:3.10")
        depends_on("py-toml", type=("build", "run"), when="@:6.6")

    with when("@:4"):
        # Requires distutils
        depends_on("python@:3.11", type=("build", "link", "run"))
        depends_on("flex", type="build")
        depends_on("bison", type="build")

    def url_for_version(self, version):
        if version < Version("5"):
            url = "https://www.riverbankcomputing.com/hg/sip/archive/{0}.tar.gz"
            return url.format(version.dotted)
        return super().url_for_version(version)

    @when("@:4")
    def install(self, spec, prefix):
        if not os.path.exists("configure.py"):
            python("build.py", "prepare")

        args = [
            "--sip-module={0}".format(spec.variants["module"].value),
            "--bindir={0}".format(prefix.bin),
            "--destdir={0}".format(python_platlib),
            "--incdir={0}".format(join_path(prefix, spec["python"].package.include)),
            "--sipdir={0}".format(prefix.share.sip),
            "--stubsdir={0}".format(python_platlib),
        ]
        python("configure.py", *args)
        make()
        make("install")

    @run_after("install")
    def extend_path_setup(self):
        # https://github.com/spack/spack/issues/14121
        # https://github.com/spack/spack/pull/15297
        # Same code comes by default with py-pyqt5 and py-pyqt6
        if self.spec.satisfies("@5:"):
            return

        module = self.spec.variants["module"].value
        if module == "sip":
            return

        module = module.split(".")[0]
        text = f"""
# Support {module} sub-packages that have been created by setuptools.
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
"""
        with open(join_path(python_platlib, module, "__init__.py"), "w") as f:
            f.write(text)
