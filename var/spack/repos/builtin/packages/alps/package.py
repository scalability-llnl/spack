# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Alps(CMakePackage):
    """
    The ALPS project (Algorithms and Libraries for Physics Simulations) aims at providing generic
    parallel algorithms for classical and quantum lattice models and provides utility classes and
    algorithm for many others.
    """

    homepage = "https://github.com/ALPSim/ALPS"
    url = "https://github.com/ALPSim/ALPS/archive/refs/tags/v2.3.3-beta.5.tar.gz"

    maintainers("Sinan81")

    license("BSL-1.0", checked_by="Sinan81")

    version(
        "2.3.3-beta.6", sha256="eb0c8115b034dd7a9dd585d277c4f86904ba374cdbdd130545aca1c432583b68"
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    # update version constraint on every boost release after providing version & checksum info
    # in resources dictionary below
    depends_on(
        "boost@:1.87 +chrono +date_time +filesystem +iostreams +mpi +numpy"
        "+program_options +python +regex +serialization +system +test +thread +timer"
    )
    depends_on("fftw")
    depends_on("hdf5 ~mpi+hl")
    depends_on("lapack")
    depends_on("python", type=("build", "link", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))

    extends("python")

    # See https://github.com/ALPSim/ALPS/issues/6#issuecomment-2604912169
    # for why this is needed
    resources = {
        # boost version, shasum
        "1.87.0": "af57be25cb4c4f4b413ed692fe378affb4352ea50fbe294a11ef548f4d527d89",
        "1.86.0": "1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b",
        "1.85.0": "7009fe1faa1697476bdc7027703a2badb84e849b7b0baad5086b087b971f8617",
        "1.84.0": "cc4b893acf645c9d4b698e9a0f08ca8846aa5d6c68275c14c3e7949c24109454",
        "1.83.0": "6478edfe2f3305127cffe8caf73ea0176c53769f4bf1585be237eb30798c3b8e",
        "1.82.0": "a6e1ab9b0860e6a2881dd7b21fe9f737a095e5f33a3a874afc6a345228597ee6",
        "1.81.0": "71feeed900fbccca04a3b4f2f84a7c217186f28a940ed8b7ed4725986baf99fa",
        "1.80.0": "1e19565d82e43bc59209a168f5ac899d3ba471d55c7610c677d4ccf2c9c500c0",
    }

    for boost_version, boost_checksum in resources.items():
        resource(
            when="^boost@{0}".format(boost_version),
            name="boost_source_files",
            url="https://downloads.sourceforge.net/project/boost/boost/{0}/boost_{1}.tar.bz2".format(
                boost_version, boost_version.replace(".", "_")
            ),
            sha256=boost_checksum,
            destination="",
            placement="boost_source_files",
        )

    def cmake_args(self):
        args = []
        # Boost_ROOT_DIR option is replaced by Boost_SRC_DIR as of 2.3.3-beta.6
        args.append(
            "-DCMAKE_CXX_FLAGS={0}".format(
                self.compiler.cxx14_flag
                + " -fpermissive -DBOOST_NO_AUTO_PTR -DBOOST_FILESYSTEM_NO_CXX20_ATOMIC_REF"
                + " -DBOOST_TIMER_ENABLE_DEPRECATED"
            )
        )
        args.append(
            "-DBoost_SRC_DIR={0}".format(join_path(self.stage.source_path, "boost_source_files"))
        )
        return args

    @run_after("install")
    def relocate_python_stuff(self):
        pyalps_dir = join_path(python_platlib, "pyalps")
        with working_dir(self.prefix):
            copy_tree("pyalps", pyalps_dir)
        with working_dir(self.prefix.lib):
            copy_tree("pyalps", pyalps_dir)
            # in pip installed pyalps package, xml dir is provided under platlib/pyalps
            copy_tree("xml", join_path(pyalps_dir, "xml"))
