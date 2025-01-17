# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Alps(CMakePackage):
    """Algorithms for Physics Simulations

    Tags: Condensed Matter Physics, Computational Physics
    """

    homepage = "https://github.com/ALPSim/ALPS"
    url = "https://github.com/ALPSim/ALPS/archive/refs/tags/v2.3.3-beta.5.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    license("BSL-1.0", checked_by="github_user1")

    version("2.3.3-beta.5", sha256="b01c537ea74b57f82dbd97e27ec62e9dce57f9ea05ba9e98f53c6ad370c5f317")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on(
        "boost@:1.82.0"
        "+chrono +date_time +filesystem +iostreams +mpi +numpy +program_options"
        "+python +regex +serialization +system +test +thread +timer"
    )
    depends_on("fftw")
    depends_on("hdf5 ~mpi+hl")
    depends_on("lapack")
    depends_on("python", type=("build", "link", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))

    extends("python")

    def cmake_args(self):
        args = []
        # Don't use Boost_ROOT_DIR option
        args.append("-DCMAKE_CXX_FLAGS={0}".format(self.compiler.cxx14_flag + " -fpermissive"))
        return args

    @run_after('install')
    def relocate_python_stuff(self):
        pyalps_dir = join(python_platlib, 'pyalps')
        with working_dir(self.prefix):
            copy_tree("pyalps", pyalps_dir)
        with working_dir(self.prefix.lib):
            copy_tree("pyalps", pyalps_dir, dirs_exist_ok=True)
            copy_tree("xml", join(pyalps_dir,"xml"))
