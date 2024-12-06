# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpiwrapper(CMakePackage):
    """MPIwrapper wraps MPI implementations so that they can be used with
    MPItrampoline"""

    homepage = "https://github.com/eschnett/MPIwrapper"
    url = "https://github.com/eschnett/MPIwrapper/archive/refs/tags/v1.0.1.tar.gz"
    git = "https://github.com/eschnett/MPIwrapper"

    maintainers("eschnett")

    license("MIT")

    version("develop", branch="main")
    version("2.10.4", sha256="af644bf4ba69964a4f7b35fbe6b8bbc67afe7bef75ba69895a227f4f465b3eaa")
    version("2.10.3", sha256="63f34df837cb9d7cae0b5ab8c0f09e8c5a60a8c0e85f248bf34fedda6488a870")
    version("2.10.1", sha256="54b57642b14b7b2dc257f7066eec8639133e4a4d5c351b8d689e31816b872b0d")
    version("2.10.0", sha256="b866fa65905ededb8c7611ab501b1e7f608802b7e0dffd77ef8b602818a62c59")
    version("2.9.0", sha256="06a264656202fcf0275f44a1fc5ff409c797a5c43b5130b47ecd7803a9bb1166")
    version("2.8.1", sha256="e6fc1c08ad778675e5b58b91b4658b12e3f985c6d4c5c2c3e9ed35986146780e")
    version("2.8.0", sha256="df559520fa0ba123e92ce3c5086c4801d047a8bfc65c42fe971e81c5d41bfab5")
    version("2.7.0", sha256="a3ed1eb42e3ac2a0a1bc5bb9bf5aa6097d228742a7ec98bd3f30ade449afdb09")
    version("2.6.0", sha256="18b56494082e02d95bb469da57c549c25d0745ac166341abc05f81d7e7d10143")
    version("2.5.0", sha256="2b68f3a34954e76906a75fa9bd203fa11f85add64073e99703815820f178176b")
    version("2.4.0", sha256="7e338c463e067afb15a934a067a9b6a7e42abe1573fb4501c8101fc3817b8497")
    version("2.3.2", sha256="eb1d63f691eebe87f81c6c5caad379e6baa5e851dd7565d9c62c23779ef48f06")
    version("2.3.1", sha256="afb833a2d7c498aba09767dacbd3dacc6cc7a59168f481032d32c06a6e7dfa9e")
    version("2.3.0", sha256="d8addc77308c0d8cd0b580d6b571ef8a6f97bcfac626b334e966e568b3b9f8d5")
    version("2.2.2", sha256="efa16c11315c913ce71a4db14574c633730bc0b1e446f1168ee01a457408163d")
    version("2.2.1", sha256="4ce058d47e515ff3dc62a6e175a9b1f402d25cc3037be0d9c26add2d78ba8da9")
    version("2.2.0", sha256="9cc9cda6f09288b8694a82cb3a64cf8457e408eee01a612e669fee749c1cb0b8")
    version("2.0.0", sha256="cdc81f3fae459569d4073d99d068810689a19cf507d9c4e770fa91e93650dbe4")
    version("1.0.1", sha256="29d5499a1a7a358d69dd744c581e57cac9223ebde94b52fa4a2b98c730ad47ff")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi @3.1:")
