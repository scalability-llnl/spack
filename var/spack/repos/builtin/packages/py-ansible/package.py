# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsible(PythonPackage):
    """
    Ansible is a radically simple IT automation platform that makes your
    applications and systems easier to deploy.
    """

    homepage = "https://github.com/ansible"
    url = "https://github.com/ansible/ansible/archive/v2.9.1.tar.gz"

    license("GPL-3.0-or-later")

    version("2.16.3", sha256="1ea5d3110f19d11bd1f330ab00bcc0dbfc51a5146349da849b8496be50b0bff7")
    version("2.9.2", sha256="27673726435e8773ef031ef6ffb121b8ec75b85b07b7684454b430c3c9a848a9")
    version("2.9.1", sha256="087a7644890e27c26171b0d24fc5d64024f12201ffb81d222aaa5704987e4c12")
    version("2.9.0", sha256="a2a9b1a74f3d47b82f9ea9da10ebf3573fa10c1783b7ed9b7eb937c7052fcb13")
    version("2.8.7", sha256="1f7c765bf2a60e3f8d634a7eb3739a70522ba93a77e9266b07c119d29e08d484")
    version("2.8.6", sha256="94c96aaf781417c073b340381c83992e4880f2a660b46888530909bc7c57ef71")
    version("2.7.15", sha256="84f020f3b09575536fb200a3ff8e9bc98dce1ba3d8dd830134691237c9cb9a85")
    version("2.7.14", sha256="92f0be1de4f9d1c0a3a35963fb853a6d7831360fd1e734cb36d601495a71770c")
    version("2.6.20", sha256="55962e79e24a67a5534bf08aa0482d5f7322ad3f112a3ebffc4a58ae02b82277")

    depends_on("python@3.8:", type=("build", "run"), when="@2.12.0:")
    depends_on("python@3.9:", type=("build", "run"), when="@2.14.0:")
    depends_on("python@3.10:", type=("build", "run"), when="@2.16.0:")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@39.2.0:", type="build", when="@2.13.0:")
    depends_on("py-setuptools@45.2.0:", type="build", when="@2.14.9:")
    depends_on("py-setuptools@66.1.0:", type="build", when="@2.16.0:")

    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jinja2@3:", type=("build", "run"), when="@2.13.0:")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", type=("build", "run"))
    depends_on("py-cryptography", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"), when="@2.10.0:")
    depends_on("py-resolvelib@0.5.3:1.0", type=("build", "run"), when="@2.11.0:")
