# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sepp(Package):
    """SEPP stands for SATe-enabled phylogenetic placement"""

    homepage = "https://github.com/smirarab/sepp"

    url = "https://github.com/smirarab/sepp/archive/refs/tags/4.5.1.tar.gz"
    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("4.5.1", sha256="51e052569ae89f586a1a94c804f09fe1b7910a3ffff7664e2005f18c7d3f717b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-dendropy@4:", type=("build", "run"))

    depends_on("java@1.8:", type="run")
    depends_on("pasta@1:", type="run")
    depends_on("blast-plus@2.10.1:", type="run")

    extends("python")

    def install(self, spec, prefix):
        dirs = ["sepp", "tools"]
        for d in dirs:
            install_tree(d, join_path(prefix, d))
        files = ["default.main.config", "*.py"]
        for f in files:
            install(f, prefix)
        with working_dir(prefix):
            prefix_string = "--prefix=" + prefix
            python("setup.py", "config", "-c")
            python("setup.py", "install", prefix_string)
            python("setup.py", "upp", "-c")
            for f in ["merge_script.py", "run_ensemble.py"]:
                install(f, prefix.bin)
                set_executable(join_path(prefix.bin, f))
            remove_files = [
                "merge_script.py",
                "run_ensemble.py",
                "run_sepp.py",
                "run_upp.py",
                "setup.py",
                "split_sequences.py",
                "distribute_setup.py",
                "home.path",
                "default.main.config",
            ]
            for f in remove_files:
                force_remove(f)
            dirs = ["sepp", "tools", "build", "dist", "__pycache__", "sepp.egg-info"]
            for d in dirs:
                remove_linked_tree(d)
