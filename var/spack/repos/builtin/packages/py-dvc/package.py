# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDvc(PythonPackage):
    """Git for data scientists - manage your code and data together."""

    homepage = "https://www.dvc.org"
    pypi = "dvc/dvc-1.11.10.tar.gz"

    license("Apache-2.0")

    version("2.1.0", sha256="46cfbf0db27107fb3a2d5c643e3a948bb24539bf165ef70e77ce64283959e481")
    version("1.11.10", sha256="6b53ebf1bd5619836f131181402bb21f7b44109166e9db8f8d6a0d8c7ce9458d")
    version("1.11.6", sha256="41ba76c51c6142b28dae3aab039cb12423ba52fed6bd2a838f8308f315cfc20b")

    variant("ssh", default=False, description="Enable ssh storage support")
    variant("s3", default=False, description="Enable s3 storage support")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-ply@3.9:", type=("build", "run"))
    depends_on("py-colorama@0.3.9:", type=("build", "run"))
    depends_on("py-configobj@5.0.6:", type=("build", "run"))
    depends_on("py-gitpython@3.1:", type=("build", "run"))
    depends_on("py-dulwich@0.20.14:", type=("build", "run"), when="@:1.11.10")
    depends_on("py-dulwich@0.20.21:", type=("build", "run"), when="@2.1.0:")
    depends_on("py-pygit2@1.5.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("py-setuptools@34.0.0:", type=("build", "run"))
    depends_on("py-nanotime@0.5.2:", type=("build", "run"))
    depends_on("py-pyasn1@0.4.1:", type=("build", "run"))
    depends_on("py-voluptuous@0.11.7:", type=("build", "run"))
    depends_on("py-jsonpath-ng@1.5.1:", type=("build", "run"))
    depends_on("py-grandalf@0.6", type=("build", "run"))
    depends_on("py-distro@1.3.0:", type=("build", "run"))
    depends_on("py-appdirs@1.4.3:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.16.1:", type=("build", "run"))
    depends_on("py-toml@0.10.1:", type=("build", "run"))
    depends_on("py-funcy@1.14:", type=("build", "run"))
    depends_on("py-pathspec@0.6.0:", type=("build", "run"))
    depends_on("py-shortuuid@0.5.0:", type=("build", "run"))
    depends_on("py-tqdm@4.45.0:4", type=("build", "run"))
    depends_on("py-packaging@19.0:", type=("build", "run"))
    depends_on("py-flufl-lock@3.2:3", type=("build", "run"))
    depends_on("py-zc-lockfile@1.2.1:", type=("build", "run"))
    depends_on("py-networkx@2.1:2.4", when="@:1.11.6", type=("build", "run"))
    depends_on("py-networkx@2.1:", when="@1.11.7:", type=("build", "run"))
    depends_on("py-psutil@5.8.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("py-pydot@1.2.4:", type=("build", "run"))
    depends_on("py-flatten-dict@0.3.0:0", type=("build", "run"))
    depends_on("py-tabulate@0.8.7:", type=("build", "run"))
    depends_on("py-pygtrie@2.3.2", type=("build", "run"))
    depends_on("py-dpath@2.0.1:2", type=("build", "run"))
    depends_on("py-shtab@1.3.2:1", type=("build", "run"), when="@:1.11.10")
    depends_on("py-shtab@1.3.4:1", type=("build", "run"), when="@2.1.0:")
    depends_on("py-rich@3.0.5:", type=("build", "run"), when="@:1.11.10")
    depends_on("py-rich@10.0.0:", type=("build", "run"), when="@2.1.0:")
    depends_on("py-dictdiffer@0.8.1:", type=("build", "run"))
    depends_on("py-python-benedict@0.21.1:", type=("build", "run"))
    depends_on("py-pyparsing@2.4.7", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", type=("build", "run"))
    depends_on("py-fsspec@0.9.0", type=("build", "run"), when="@2.1.0:")
    depends_on("py-diskcache@5.2.1:", type=("build", "run"), when="@2.1.0:")

    depends_on("py-paramiko@2.7.0:+invoke", when="+ssh", type=("build", "run"))
    depends_on("py-boto3@1.9.201:", when="+s3", type=("build", "run"))
