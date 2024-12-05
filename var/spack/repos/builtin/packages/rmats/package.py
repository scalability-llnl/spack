# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from os import symlink

from spack.package import *


class Rmats(Package):
    """MATS is a computational tool to detect differential alternative
    splicing events from RNA-Seq data."""

    homepage = "https://rnaseq-mats.sourceforge.net/index.html"
    url = "https://downloads.sourceforge.net/project/rnaseq-mats/MATS/rMATS.4.0.2.tgz"

    version("4.0.2", sha256="afab002a9ae836d396909aede96318f6dab6e5818078246419dd563624bf26d1")

    depends_on("python@2.7:", type="run")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("openblas")

    def install(self, spec, prefix):
        # since the tool is a python script we install it to /usr/lib
        install_tree("rMATS-turbo-Linux-UCS4", join_path(prefix.lib, "rmats"))

        # the script has an appropriate shebang so a quick symlink will do
        set_executable(join_path(prefix.lib, "rmats/rmats.py"))
        mkdirp(prefix.bin)
        symlink(join_path(prefix.lib, "rmats/rmats.py"), join_path(prefix.bin, "rmats"))
