# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyyaml(PythonPackage):
    """PyYAML is a YAML parser and emitter for Python."""

    homepage = "https://pyyaml.org/wiki/PyYAML"
    pypi = "PyYAML/PyYAML-5.3.1.tar.gz"
    git = "https://github.com/yaml/pyyaml.git"

    license("MIT")

    version("6.0.1", sha256="bfdf460b1736c775f2ba9f6a92bca30bc2095067b8a9d77876d1fad6cc3b4a43")
    version("6.0", sha256="68fb519c14306fec9720a2a5b45bc9f0c8d1b9c72adf45c37baedfcd949c35a2")
    version("5.4.1", sha256="607774cbba28732bfa802b54baa7484215f530991055bb562efbed5b2f20a45e")
    version("5.3.1", sha256="b8eac752c5e14d3eca0e6dd9199cd627518cb5ec06add0de9d32baeee6fe645d")
    version("5.2", sha256="c0ee8eca2c582d29c3c2ec6e2c4f703d1b7f1fb10bc72317355a746057e7346c")
    version("5.1.2", sha256="01adf0b6c6f61bd11af6e10ca52b7d4057dd0be0343eb9283c878cf3af56aee4")
    version("5.1", sha256="436bc774ecf7c103814098159fbb84c2715d25980175292c648f2da143909f95")
    version("3.13", sha256="3ef3092145e9b70e3ddd2c7ad59bdd0252a94dfe3949721633e41344de00a6bf")
    version("3.12", sha256="592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab")
    version("3.11", sha256="c36c938a872e5ff494938b33b14aaa156cb439ec67548fcab3535bb78b0846e8")

    variant("libyaml", default=True, description="Use libYAML bindings")

    depends_on("python@2.7,3.5:", type=("build", "link", "run"))
    depends_on("python@3.6:", when="@6:", type=("build", "link", "run"))
    depends_on("libyaml", when="+libyaml", type="link")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", when="@6:+libyaml", type="build")

    # Includes "longintrepr.h" instead of Python.h
    conflicts("^python@3.11:", when="@:5.3")

    # https://github.com/yaml/pyyaml/issues/601
    conflicts("^py-cython@3:")

    @property
    def import_modules(self):
        modules = ["yaml"]

        if "+libyaml" in self.spec:
            modules.append("yaml.cyaml")

        return modules

    def global_options(self, spec, prefix):
        args = []

        if "+libyaml" in self.spec:
            args.append("--with-libyaml")
        else:
            args.append("--without-libyaml")

        return args
