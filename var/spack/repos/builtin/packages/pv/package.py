# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pv(AutotoolsPackage):
    """Pipe Viewer - is a terminal-based tool for monitoring the progress
    of data through a pipeline
    """

    homepage = "https://www.ivarch.com/programs/pv.shtml"
    url = "https://www.ivarch.com/programs/sources/pv-1.6.6.tar.gz"

    license("GPL-3.0-or-later", when="@1.8.0:", checked_by="RemiLacroix-IDRIS")
    license("Artistic-2.0", when="@:1.7.24", checked_by="RemiLacroix-IDRIS")

    version("1.8.5", sha256="d22948d06be06a5be37336318de540a2215be10ab0163f8cd23a20149647b780")
    version("1.6.20", sha256="b5f1ee79a370c5287e092b6e8f1084f026521fe0aecf25c44b9460b870319a9e")
    version("1.6.6", sha256="94defb4183ae07c44219ba298d43c4991d6e203c29f74393d72ecad3b090508a")

    depends_on("c", type="build")  # generated
