# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NeicFinitefault(PythonPackage):
    """Wavelet and simulated Annealing SliP inversion (WASP).
    This code uses a nonlinear simulated annealing inversion method to
    model slip amplitude, rake, rupture time, and rise time on a discretized
    fault plane, finding the solution that best fits the observations in
    the wavelet domain."""

    homepage = "https://code.usgs.gov/ghsc/neic/algorithms/neic-finitefault"

    url = "https://code.usgs.gov/ghsc/neic/algorithms/neic-finitefault/-/archive/0.1.0/neic-finitefault-0.1.0.tar.gz"
    git = "https://code.usgs.gov/ghsc/neic/algorithms/neic-finitefault"

    maintainers("snehring")

    license("CC0-1.0", checked_by="snehring")

    version("20240410", commit="ef6a1a92d60549100885112e24a18e38d8d4ce0b")
    version("0.1.0", sha256="36b400dfc418bf78a3099f6fc308681c87ae320e6d71c7d0e98a2738e72fb570")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    resource(
        name="fd_bank",
        url="https://zenodo.org/records/7236739/files/fd_bank",
        sha256="fe0f1a392cb9b6623c981de2a4fae405d9820b14e274e287e64731aede8ecb40",
        expand=False,
        when="@0.1.0:",
    )
    resource(
        name="LITHO1.0.nc",
        url="https://ds.iris.edu/files/products/emc/emc-files/LITHO1.0.nc",
        sha256="4429bdf3fc2a5402064b40b059faf3a79d9ce0818feb1b13122e169af56f4b43",
        expand=False,
        when="@0.1.0:",
    )
    resource(
        name="tectonicplates",
        url="https://github.com/fraxen/tectonicplates/archive/339b0c56563c118307b1f4542703047f5f698fae.zip",
        sha256="694ebf7090db07e47b07f1ae21175c4a5fa9c85bb79815680e439c1032407b95",
        when="@0.1.0:",
    )

    depends_on("python@3.9:3.12", type=("build", "run"))

    depends_on("py-poetry-core@1:", type="build")

    depends_on("py-cartopy@0.21.1:0", type=("build", "run"))
    depends_on("py-ipykernel@6.15:6", type=("build", "run"))
    depends_on("py-matplotlib@3.8.3:3", type=("build", "run"))
    depends_on("py-matplotlib@3.7.2:3", type=("build", "run"), when="@0.1.0")
    depends_on("py-netcdf4@1.6.4:1~mpi", type=("build", "run"))
    depends_on("py-numpy@1.25:1", type=("build", "run"))
    depends_on("py-obspy@1.4:1", type=("build", "run"))
    depends_on("py-pygmt@0.9:0.9", type=("build", "run"))
    depends_on("py-pyproj@3.3:3", type=("build", "run"))
    depends_on("py-scipy@1.11.1:1", type=("build", "run"))
    depends_on("py-shapely@=1.7.1", type=("build", "run"))
    depends_on("py-pyrocko@=2023.6.29", type=("build", "run"))
    depends_on("py-typer@0.9", type=("build", "run"))
    depends_on("py-okada-wrapper@=18.12.07.3", type=("build", "run"))

    # non python deps
    depends_on("geos@=3.11.2", type=("build", "run"))
    depends_on("gmt@=6.4.0", type=("build", "run"))
    depends_on("proj@=9.2.0", type=("build", "run"))
    # not a direct dep, but we do need gdal to have these variants
    depends_on("gdal+jpeg+jxl+openjpeg", type=("build", "run"))

    parallel = False

    patch("fortran-filename-length.patch")

    @run_before("install")
    def build(self):
        # place resources, couldn't figure out another way to do this
        # that didn't result in symlinks
        relevant_resources = [
            resource
            for resource_spec, resource_list in self.resources.items()
            if self.spec.intersects(resource_spec)
            for resource in resource_list
        ]
        for resource in relevant_resources:
            res_path = resource.fetcher.stage.source_path
            if resource.name == "fd_bank":
                res_dst = join_path(self.build_directory, "fortran_code", "gfs_nm", "long")
            elif resource.name == "LITHO1.0.nc":
                res_dst = join_path(self.build_directory, "fortran_code", "info")
            elif resource.name == "tectonicplates":
                res_dst = self.build_directory

            res_dst = join_path(res_dst, resource.name)

            if resource.name == "tectonicplates":
                copy_tree(res_path, res_dst)
            else:
                copy(join_path(res_path, resource.name), res_dst)

        # everything about this seems to assume it's going to reside where it's compiled
        mkdirp(self.prefix)
        install_tree(".", self.prefix)

        with working_dir(self.prefix.fortran_code):
            with open(join_path("gfs_nm", "long", "low.in"), mode="a") as f:
                f.write(f"\n{self.prefix.fortran_code.gfs_nm.long.fd_bank}")
            # compile fortran code
            with working_dir("bin_inversion_gfortran_f95"):
                make("clean")
                make()
            with working_dir("bin_str_f95"):
                make("clean")
                make()
            with working_dir("src_dc_f95"):
                make("clean")
                make()

    @run_after("install")
    def generate_config_file(self):
        file = f"""[PATHS]
code_path = {self.prefix}
surf_gf_bank = {join_path(self.prefix.fortran_code.gfs_nm.long, "low.in")}
modelling = {self.prefix.fortran_code.bin_inversion_gfortran_f95}
get_near_gf = {self.prefix.fortran_code.bin_str_f95}
compute_near_gf = {self.prefix.fortran_code.src_dc_f95}
info = {self.prefix.fortran_code.info}
cartopy_files = {self.prefix.tectonicplates}"""

        with working_dir(self.prefix):
            with open("config.ini", mode="w") as f:
                f.write(file)
        symlink(
            join_path(self.prefix, "config.ini"),
            join_path(
                self.prefix.lib, f"python{self.spec['python'].version.up_to(2)}", "config.ini"
            ),
        )
