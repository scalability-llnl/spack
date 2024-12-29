# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shc(AutotoolsPackage):
    """A generic shell script compiler. Shc takes a script,
    which is specified on the command line and produces C
    source code. The generated source code is then compiled
    and linked to produce a stripped binary executable."""

    homepage = "https://neurobin.org/projects/softwares/unix/shc/"
    url = "https://github.com/neurobin/shc/archive/refs/tags/4.0.3.tar.gz"

    license("GPL-3.0-or-later")

    version("4.0.3", sha256="7d7fa6a9f5f53d607ab851d739ae3d3b99ca86e2cb1425a6cab9299f673aee16")
    version("4.0.2", sha256="881b9a558466529dcdba79b7fafed028ee02a9afc0371fc1e11a26f1f586a4a6")
    version("4.0.1", sha256="494666df8b28069a7d73b89f79919bdc04e929a176746c98c3544a639978ba52")
    version("4.0.0", sha256="750f84441c45bd589acc3b0f0f71363b0001818156be035da048e1c2f8d6d76b")
    version("3.9.8", sha256="8b31e1f2ceef3404217b9578fa250a8a424f3eaf03359dd7951cd635c889ad79")
