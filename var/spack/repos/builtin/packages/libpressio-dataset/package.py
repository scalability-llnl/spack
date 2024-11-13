# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioDataset(CMakePackage):
    """A set of libraries for LibPressio to easily load datasets"""

    homepage = "https://github.com/robertu94/libpressio_dataset"
    url = "https://github.com/robertu94/libpressio_dataset/archive/refs/tags/0.0.2.tar.gz"
    git = "https://github.com/robertu94/libpressio_dataset"

    maintainers = ["robertu94"]

    version("0.0.9", sha256="743edf3bda7a174ed9953388b7975d463384001b9c6e04d07e7adc8012d10f5a")
    version("0.0.8", sha256="5e0adac22b8c96f26b93e253bb9d30623bf357da608c10bddad3871c4e9dbe17")
    version("0.0.7", sha256="203b36b337d23b789658162ecc024d7acf60fbff2fdc5b946c0854998e03e7bf")
    version("0.0.6", sha256="24c07ac329714587d0778e6a2bf598aa8005de374595c36180de81ab020d55fc")
    version("0.0.5", sha256="07906545207831515ad7ce1ad99994887f458c2e2f422fd5ea7569a5b0d072ad")
    version("0.0.4", sha256="ff65e9c45fac607c7e48d305694c79996a1eb20c409ca3e1af59aad0c6e16f57")
    version("0.0.3", sha256="b821bd880159c93fe5a960f4b51927a3963b1f0d2b91dc2f6c4655d644e8a28b")
    version("0.0.2", sha256="b5d62260cc596a6239a721bda12293bce34f86266c203a573d3afa8fe0876c2f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("hdf5", default=False, description="add support for hdf5")
    variant("shared", default=True, description="build shared libaries")

    depends_on("libpressio@0.99.4:", when="@0.0.9:")
    depends_on("libpressio@0.93.0:", when="@0.0.3:0.0.8")
    depends_on("libpressio@0.91.1:", when="@:0.0.2")
    depends_on("hdf5", when="+hdf5")

    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("LIBPRESSIO_DATASET_HAS_HDF5", "hdf5"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        return args
