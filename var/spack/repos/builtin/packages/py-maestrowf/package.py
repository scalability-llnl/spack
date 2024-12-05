# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMaestrowf(PythonPackage):
    """A general purpose workflow conductor for running multi-step
    simulation studies."""

    homepage = "https://github.com/LLNL/maestrowf/"
    pypi = "maestrowf/maestrowf-1.1.8.tar.gz"
    git = "https://github.com/LLNL/maestrowf/"
    tags = ["radiuss"]

    maintainers("FrankD412")

    license("MIT")

    # git branches
    version("develop", branch="develop")
    version("master", branch="master")

    # pypi releases
    version("1.1.9", sha256="92d964fee7c944a2b08bb6148cbab66d0b8a02893d281d395971368cc2ecf957")
    version("1.1.8", sha256="fa8f8eb8dd3adfb9646d7b0dfd498a00423d2131adbc8dbc8016c4159b2ec1d5")
    version("1.1.7", sha256="ff1b6696f30254b105fcadd297ad437c0c666ebc70124b231a713b89f47f4e94")
    version("1.1.6", sha256="9812e67d9bd83c452cc99d82fbceb3017b5e36dafdf52eda939748bad4a88756")
    version("1.1.4", sha256="6603b93494e8e9d939a4ab40ecdfe7923a85960a8a8bddea4734e230d8144016")
    version("1.1.3", sha256="9812e67d9bd83c452cc99d82fbceb3017b5e36dafdf52eda939748bad4a88756")
    version("1.1.2", sha256="6998ba2c6ee4ef205c6d47d98cf35d5eaa184e1e859cc41b4120e2aa12c06df3")
    version("1.1.1", sha256="689ed42ba1fb214db0594756ff6015e466470103f726a5e5bf4d21c1086ad2b1")
    version("1.1.0", sha256="1bfec546831f2ef577d7823bb50dcd12622644dad0d3d761998eafd0905b6977")
    version("1.0.1", sha256="dd42ffeac1f0492a576c630b37e5d3593273e59664407f2ebf78d49322d37146")

    depends_on("py-setuptools", type=("build"), when="@:1.1.8")
    depends_on("py-poetry-core@1.0.8:", type=("build"), when="@1.1.9:")
    depends_on("py-coloredlogs", type=("build", "run"), when="@1.1.7:")
    depends_on("py-dill", type=("build", "run"), when="@1.1.7:")
    depends_on("py-filelock", type=("build", "run"), when="@1.1.0:")
    depends_on("py-jsonschema@3.2.0:", type=("build", "run"), when="@1.1.7:")
    depends_on("py-pyyaml@4.2:", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"), when="@1.1.9:")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"), when="@1.1.0:")
