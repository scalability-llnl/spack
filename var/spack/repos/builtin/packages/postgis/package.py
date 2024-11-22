# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import tempfile

from spack.package import *


class Postgis(AutotoolsPackage):
    """
    PostGIS is a spatial database extender for PostgreSQL object-relational
    database. It adds support for geographic objects allowing location
    queries to be run in SQL
    """

    homepage = "https://postgis.net/"
    url = "https://download.osgeo.org/postgis/source/postgis-2.5.3.tar.gz"

    license("GPL-2.0-or-later")

    version("3.0.1", sha256="5a5432f95150d9bae9215c6d1c7bb354e060482a7c379daa9b8384e1d03e6353")
    version("3.0.0", sha256="c06fd2cd5cea0119106ffe17a7235d893c2bbe6f4b63c8617c767630973ba594")
    version("2.5.3", sha256="72e8269d40f981e22fb2b78d3ff292338e69a4f5166e481a77b015e1d34e559a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "gui",
        default=False,
        description=(
            "Build with GUI support, creating shp2pgsql-gui graphical interface " "to shp2pgsql"
        ),
    )

    # Refs:
    # https://postgis.net/docs/postgis_installation.html
    # https://postgis.net/source/

    depends_on("postgresql")
    depends_on("geos")
    depends_on("proj")
    depends_on("gdal")
    depends_on("libxml2")
    depends_on("json-c")

    depends_on("sfcgal")
    depends_on("pcre")
    depends_on("perl", type=("build", "run"))
    depends_on("protobuf-c")

    depends_on("gtkplus@:2.24.32", when="+gui")

    def patch(self):
        # https://trac.osgeo.org/postgis/ticket/4833
        if self.spec.satisfies("@:3.1.1 ^proj@6:"):
            filter_file(r"\bpj_get_release\b", "proj_info", "configure")

    def setup_build_environment(self, env):
        env.set("POSTGIS_GDAL_ENABLED_DRIVERS", "ENABLE_ALL")

    def setup_run_environment(self, env):
        env.set("POSTGIS_GDAL_ENABLED_DRIVERS", "ENABLE_ALL")

    def configure_args(self):
        args = [
            "--with-pgconfig=" + self.spec["postgresql"].prefix.bin.join("pg_config"),
            "--with-sfcgal=" + self.spec["sfcgal"].prefix.bin.join("sfcgal-config"),
            "--with-xml2config=" + self.spec["libxml2"].prefix.bin.join("xml2-config"),
            "--with-geosconfig=" + self.spec["geos"].prefix.bin.join("geos-config"),
            "--with-projdir=" + self.spec["proj"].prefix,
            "--with-jsondir=" + self.spec["json-c"].prefix,
            "--with-protobufdir=" + self.spec["protobuf-c"].prefix,
            "--with-pcredir=" + self.spec["pcre"].prefix,
            "--with-gdalconfig=" + self.spec["gdal"].prefix.bin.join("gdal-config"),
        ]
        if "+gui" in self.spec:
            args.append("--with-gui")
        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        with self.postgresql():
            make("check")

    # By default package installs under postgresql prefix.
    # Apparently this is a known bug:
    # https://postgis.net/docs/postgis_installation.html
    # The following modifacations that fixed this issue are found in
    # Guix recipe for postgis.
    # https://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/geo.scm#n720

    def install(self, spec, prefix):
        make(
            "install",
            "bindir=" + prefix.bin,
            "libdir=" + prefix.lib,
            "pkglibdir=" + prefix.lib,
            "datadir=" + prefix.share,
            "docdir=" + prefix.share.doc,
        )

        copy(
            prefix.share.extension.join("postgis.control"),
            spec["postgresql"].prefix.share.extension,
        )
        filter_file(
            "$libdir",
            prefix.lib,
            spec["postgresql"].prefix.share.extension.join("postgis.control"),
            string=True,
        )

    def test_lib_version(self):
        """Makes sure the PostGIS extension is usable from PostgreSQL."""
        with self.postgresql() as psql:
            psql("-c", "CREATE EXTENSION postgis", "postgres")
            version = psql("-c", "SELECT PostGIS_Lib_Version()", "-t", "postgres", output=str)
            check_outputs(str(self.spec.version), version)

    @contextlib.contextmanager
    def postgresql(self):
        postgresql_bin_dir = self.spec["postgresql"].prefix.bin
        initdb = which(postgresql_bin_dir.join("initdb"))
        pg_ctl = which(postgresql_bin_dir.join("pg_ctl"))
        with tempfile.TemporaryDirectory() as data_dir:
            initdb("-A", "trust", "-D", data_dir)
            pg_ctl("-D", data_dir, "start")
            try:
                psql = which(postgresql_bin_dir.join("psql"))
                yield psql
            finally:
                pg_ctl("-D", data_dir, "stop")

    @run_before("build")
    def fix_raster_bindir(self):
        makefile = FileFilter("raster/loader/Makefile")
        makefile.filter("$(DESTDIR)$(PGSQL_BINDIR)", self.prefix.bin, string=True)
        makefile = FileFilter("raster/scripts/Makefile")
        makefile.filter("$(DESTDIR)$(PGSQL_BINDIR)", self.prefix.bin, string=True)
