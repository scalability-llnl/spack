# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.cmake import CMakeBuilder
from spack.package import *
from spack.util.environment import filter_system_paths


class Gdal(CMakePackage, AutotoolsPackage, PythonExtension):
    """GDAL: Geospatial Data Abstraction Library.

    GDAL is a translator library for raster and vector geospatial data formats that
    is released under an MIT style Open Source License by the Open Source Geospatial
    Foundation. As a library, it presents a single raster abstract data model and
    single vector abstract data model to the calling application for all supported
    formats. It also comes with a variety of useful command line utilities for data
    translation and processing.
    """

    homepage = "https://www.gdal.org/"
    url = "https://download.osgeo.org/gdal/3.2.0/gdal-3.2.0.tar.xz"
    list_url = "https://download.osgeo.org/gdal/"
    list_depth = 1

    maintainers("adamjstewart")

    license("MIT")

    version("3.9.3", sha256="34a037852ffe6d2163f1b8948a1aa7019ff767148aea55876c1339b22ad751f1")
    version("3.9.2", sha256="bfbcc9f087f012c36151c20c79f8eac9529e1e5298fbded79cd5a1365f0b113a")
    version("3.9.1", sha256="aff3086fee75f5773e33a5598df98d8a4d10be411f777d3ce23584b21d8171ca")
    version("3.9.0", sha256="577f80e9d14ff7c90b6bfbc34201652b4546700c01543efb4f4c3050e0b3fda2")
    version("3.8.5", sha256="e8b4df2a8a7d25272f867455c0c230459545972f81f0eff2ddbf6a6f60dcb1e4")
    version("3.8.4", sha256="0c53ced95d29474236487202709b49015854f8e02e35e44ed0f4f4e12a7966ce")
    version("3.8.3", sha256="ae2d160f65016e208eca34ff14490ec4511f1fa03fd386ac130449d15e82929d")
    version("3.8.2", sha256="dc2921ee1cf7a5c0498e94d15fb9ab9c9689c296363a1d021fc3293dd242b4db")
    version("3.8.1", sha256="75a20b23879bfa3d8c0db68e1d6f8b924f7f9d97f5fed089b01a72e404293900")
    version("3.8.0", sha256="ec0f78d9dc32352aeac6edc9c3b27a991b91f9dc6f92c452207d84431c58757d")
    version("3.7.3", sha256="e0a6f0c453ea7eb7c09967f50ac49426808fcd8f259dbc9888140eb69d7ffee6")
    version("3.7.2", sha256="40c0068591d2c711c699bbb734319398485ab169116ac28005d8302f80b923ad")
    version("3.7.1", sha256="9297948f0a8ba9e6369cd50e87c7e2442eda95336b94d2b92ef1829d260b9a06")
    version("3.7.0", sha256="af4b26a6b6b3509ae9ccf1fcc5104f7fe015ef2110f5ba13220816398365adce")
    version("3.6.4", sha256="889894cfff348c04ac65b462f629d03efc53ea56cf04de7662fbe81a364e3df1")
    version("3.6.3", sha256="3cccbed883b1fb99b913966aa3a650ad930e7c3afc714f5823f9754176ee49ea")
    version("3.6.2", sha256="35f40d2e08061b342513cdcddc2b997b3814ef8254514f0ef1e8bc7aa56cf681")
    version("3.6.1", sha256="68f1c03547ff7152289789db7f67ee634167c9b7bfec4872b88406b236f9c230")
    version("3.6.0", sha256="f7afa4aa8d32d0799e011a9f573c6a67e9471f78e70d3d0d0b45b45c8c0c1a94")
    version("3.5.3", sha256="d32223ddf145aafbbaec5ccfa5dbc164147fb3348a3413057f9b1600bb5b3890")
    version("3.5.2", sha256="0874dfdeb9ac42e53c37be4184b19350be76f0530e1f4fa8004361635b9030c2")
    version("3.5.1", sha256="d12c30a9eacdeaab493c0d1c9f88eb337c9cbb5bb40744c751bdd5a5af166ab6")
    version("3.5.0", sha256="d49121e5348a51659807be4fb866aa840f8dbec4d1acba6d17fdefa72125bfc9")
    version("3.4.3", sha256="02a27b35899e1c4c3bcb6007da900128ddd7e8ab7cd6ccfecf338a301eadad5a")
    version("3.4.2", sha256="16baf03dfccf9e3f72bb2e15cd2d5b3f4be0437cdff8a785bceab0c7be557335")
    version("3.4.1", sha256="332f053516ca45101ef0f7fa96309b64242688a8024780a5d93be0230e42173d")
    version("3.4.0", sha256="ac7bd2bb9436f3fc38bc7309704672980f82d64b4d57627d27849259b8f71d5c")
    version("3.3.3", sha256="1e8fc8b19c77238c7f4c27857d04857b65d8b7e8050d3aac256d70fa48a21e76")
    version("3.3.2", sha256="630e34141cf398c3078d7d8f08bb44e804c65bbf09807b3610dcbfbc37115cc3")
    version("3.3.1", sha256="48ab00b77d49f08cf66c60ccce55abb6455c3079f545e60c90ee7ce857bccb70")
    version("3.3.0", sha256="190c8f4b56afc767f43836b2a5cd53cc52ee7fdc25eb78c6079c5a244e28efa7")
    version("3.2.3", sha256="d9ec8458fe97fd02bf36379e7f63eaafce1005eeb60e329ed25bb2d2a17a796f")
    version("3.2.2", sha256="a7e1e414e5c405af48982bf4724a3da64a05770254f2ce8affb5f58a7604ca57")
    version("3.2.1", sha256="6c588b58fcb63ff3f288eb9f02d76791c0955ba9210d98c3abd879c770ae28ea")
    version("3.2.0", sha256="b051f852600ffdf07e337a7f15673da23f9201a9dbb482bd513756a3e5a196a6")
    version("3.1.4", sha256="7b82486f71c71cec61f9b237116212ce18ef6b90f068cbbf9f7de4fc50b576a8")
    version("3.1.3", sha256="161cf55371a143826f1d76ce566db1f0a666496eeb4371aed78b1642f219d51d")
    version("3.1.2", sha256="767c8d0dfa20ba3283de05d23a1d1c03a7e805d0ce2936beaff0bb7d11450641")
    version("3.1.1", sha256="97154a606339a6c1d87c80fb354d7456fe49828b2ef9a3bc9ed91771a03d2a04")
    version("3.1.0", sha256="e754a22242ccbec731aacdb2333b567d4c95b9b02d3ba1ea12f70508d244fcda")
    version("3.0.4", sha256="5569a4daa1abcbba47a9d535172fc335194d9214fdb96cd0f139bb57329ae277")
    version("3.0.3", sha256="e20add5802265159366f197a8bb354899e1693eab8dbba2208de14a457566109")
    version("3.0.2", sha256="c3765371ce391715c8f28bd6defbc70b57aa43341f6e94605f04fe3c92468983")
    version("3.0.1", sha256="45b4ae25dbd87282d589eca76481c426f72132d7a599556470d5c38263b09266")
    version("3.0.0", sha256="ad316fa052d94d9606e90b20a514b92b2dd64e3142dfdbd8f10981a5fcd5c43e")
    with default_args(deprecated=True):
        version("2.4.4", sha256="a383bd3cf555d6e1169666b01b5b3025b2722ed39e834f1b65090f604405dcd8")
        version("2.4.3", sha256="d52dc3e0cff3af3e898d887c4151442989f416e839948e73f0994f0224bbff60")
        version("2.4.2", sha256="dcc132e469c5eb76fa4aaff238d32e45a5d947dc5b6c801a123b70045b618e0c")
        version("2.4.1", sha256="fd51b4900b2fc49b98d8714f55fc8a78ebfd07218357f93fb796791115a5a1ad")
        version("2.4.0", sha256="c3791dcc6d37e59f6efa86e2df2a55a4485237b0a48e330ae08949f0cdf00f27")
        version("2.3.3", sha256="c3635e41766a648f945d235b922e3c5306e26a2ee5bbd730d2181e242f5f46fe")
        version("2.3.2", sha256="3f6d78fe8807d1d6afb7bed27394f19467840a82bc36d65e66316fa0aa9d32a4")
        version("2.3.1", sha256="9c4625c45a3ee7e49a604ef221778983dd9fd8104922a87f20b99d9bedb7725a")
        version("2.3.0", sha256="6f75e49aa30de140525ccb58688667efe3a2d770576feb7fbc91023b7f552aa2")
        version("2.2.4", sha256="441eb1d1acb35238ca43a1a0a649493fc91fdcbab231d0747e9d462eea192278")
        version("2.2.3", sha256="a328d63d476b3653f5a25b5f7971e87a15cdf8860ab0729d4b1157ba988b8d0b")
        version("2.2.2", sha256="eb25d6ee85f4f5ac1d5581958f8c6eed9b1d50746f82866fe92e507541def35b")
        version("2.2.1", sha256="927098d54083ac919a497f787b835b099e9a194f2e5444dbff901f7426b86066")
        version("2.2.0", sha256="0d4c326862e0f118e17418c042c2bcd037b25abd3fb198e1fc5d40b11a9fc8ea")
        version("2.1.4", sha256="e06a7ae4c4ed2fd678cd045ff50a10ff5002f3b81cdfcd8ab03c39ce962d9b63")
        version("2.1.3", sha256="b489793627e6cb8d2ff8d7737b61daf58382fe189fae4c581ddfd48c04b49005")
        version("2.1.2", sha256="b597f36bd29a2b4368998ddd32b28c8cdf3c8192237a81b99af83cc17d7fa374")
        version("2.1.1", sha256="87ce516ce757ad1edf1e21f007fbe232ed2e932af422e9893f40199711c41f92")
        version("2.1.0", sha256="568b43441955b306364fcf97fb47d4c1512ac6f2f5f76b2ec39a890d2418ee03")
        version("2.0.3", sha256="3c6c5ade299c7a52fc9c5d2111110c97032e1f0c2593ce6091c364b1a43b442a")
        version("2.0.2", sha256="90f838853cc1c07e55893483faa7e923e4b4b1659c6bc9df3538366030a7e622")
        version("2.0.1", sha256="2564c91ed8ed36274ee31002a25798f5babc4221e879cb5013867733d80f9920")
        version("2.0.0", sha256="91704fafeea2349c5e268dc1e2d03921b3aae64b05ee01d59fdfc1a6b0ffc061")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Optional dependencies
    variant("archive", default=False, when="@3.7:", description="Optional for vsi7z VFS driver")
    variant(
        "armadillo",
        default=False,
        description="Speed up computations related to the Thin Plate Spline transformer",
    )
    variant(
        "arrow", default=False, when="build_system=cmake", description="Required for Arrow driver"
    )
    variant(
        "basisu", default=False, when="@3.6:", description="Required for BASISU and KTX2 drivers"
    )
    variant("blosc", default=False, when="@3.4:", description="Required for Zarr driver")
    variant("brunsli", default=False, when="@3.4:", description="Required for MRF driver")
    variant("bsb", default=False, when="@:2", description="Required for BSB driver")
    variant("cfitsio", default=False, description="Required for FITS driver")
    variant("crnlib", default=False, description="Required for DDS driver")
    variant("curl", default=True, description="Required for network access")
    variant("cryptopp", default=False, when="@2.1:", description="Required for EEDAI driver")
    variant("deflate", default=False, when="@3.2:", description="Required for Deflate compression")
    variant("dods", default=False, when="@:3.4", description="Required for DODS driver")
    variant("ecw", default=False, description="Required for ECW driver")
    variant("epsilon", default=False, when="@:3.2", description="Required for EPSILON driver")
    variant("expat", default=True, description="Required for XML parsing in many OGR drivers")
    variant("filegdb", default=False, description="Required for FileGDB driver")
    variant("fme", default=False, when="@:3.4", description="Required for FME driver")
    variant("freexl", default=False, description="Required for XLS driver")
    variant("fyba", default=False, description="Required for SOSI driver")
    variant("geos", default=True, description="Required for geometry processing operations in OGR")
    variant("gif", default=False, description="Required for GIF driver")
    variant("grass", default=False, when="@:3.4", description="Required for GRASS driver")
    variant("grib", default=False, when="@:2", description="Required for GRIB driver")
    variant("gta", default=False, description="Required for GTA driver")
    variant("heif", default=False, when="@3.2:", description="Required for HEIF driver")
    variant("hdf4", default=False, description="Required for HDF4 driver")
    variant("hdf5", default=False, description="Required for HDF5, BAG, and KEA drivers")
    variant(
        "hdfs", default=False, when="@2.4:", description="Required for Hadoop filesystem support"
    )
    variant("iconv", default=False, description="Required for text encoding conversion")
    variant("idb", default=False, description="Required for IDB driver")
    variant("ingres", default=False, when="@:3.4", description="Required for Ingres driver")
    variant("jasper", default=False, when="@:3.4", description="Optional JPEG-2000 library")
    variant("jpeg", default=True, description="Required for JPEG driver")
    variant("jxl", default=False, when="@3.4:", description="Required for JPEGXL driver")
    variant("kdu", default=False, description="Required for JP2KAK and JPIPKAK drivers")
    variant("kea", default=False, description="Required for KEA driver")
    variant("lerc", default=False, when="@2.4:", description="Required for LERC compression")
    variant("libaec", default=False, when="@3.8:", description="Optional for GRIB driver")
    variant("libcsf", default=False, description="Required for PCRaster driver")
    variant("libkml", default=False, description="Required for LIBKML driver")
    variant("liblzma", default=False, description="Required for Zarr driver")
    variant("libqb3", default=False, when="@3.6:", description="Required for MRF driver")
    variant(
        "libxml2", default=False, description="Required for XML validation in many OGR drivers"
    )
    variant("luratech", default=False, when="@2.2:", description="Required for JP2Lura driver")
    variant("lz4", default=False, when="@3.4:", description="Required for Zarr driver")
    variant("mdb", default=False, when="@:3.4", description="Required for MDB driver")
    variant("mongocxx", default=False, when="@2.1:", description="Required for MongoDBv3 driver")
    variant("mrf", default=False, when="@2.1:2", description="Required for MRF driver")
    variant("mrsid", default=False, description="Required for MrSID driver")
    variant(
        "mrsid_lidar", default=False, when="@:3.4", description="Required for MrSID/MG4 driver"
    )
    variant(
        "mssql_ncli",
        default=False,
        when="build_system=cmake",
        description="Required for MSSQLSpatial driver",
    )
    variant(
        "mssql_odbc",
        default=False,
        when="build_system=cmake",
        description="Required for MSSQLSpatial driver",
    )
    variant("mysql", default=False, description="Required for MySQL driver")
    variant("netcdf", default=False, description="Required for NetCDF driver")
    variant("odbc", default=False, description="Required for many OGR drivers")
    variant(
        "odbccpp",
        default=False,
        when="build_system=cmake",
        description="Required for SAP HANA driver",
    )
    variant("ogdi", default=False, description="Required for OGDI driver")
    variant(
        "opencad", default=False, when="build_system=cmake", description="Required for CAD driver"
    )
    variant("opencl", default=False, description="Required to accelerate warping computations")
    variant("openexr", default=False, when="@3.1:", description="Required for EXR driver")
    variant("openjpeg", default=False, description="Required for JP2OpenJPEG driver")
    variant("openssl", default=False, when="@2.3:", description="Required for EEDAI driver")
    variant("oracle", default=False, description="Required for OCI and GeoRaster drivers")
    variant(
        "parquet",
        default=False,
        when="build_system=cmake",
        description="Required for Parquet driver",
    )
    variant("pcidsk", default=False, description="Required for PCIDSK driver")
    variant(
        "pcre2", default=False, description="Required for REGEXP operator in drivers using SQLite3"
    )
    variant("pdfium", default=False, when="@2.1:", description="Possible backend for PDF driver")
    variant("png", default=True, description="Required for PNG driver")
    variant("podofo", default=False, description="Possible backend for PDF driver")
    variant("poppler", default=False, description="Possible backend for PDF driver")
    variant(
        "postgresql",
        default=False,
        description="Required for PostgreSQL and PostGISRaster drivers",
    )
    variant(
        "qhull",
        default=False,
        when="@2.1:",
        description="Used for linear interpolation of gdal_grid",
    )
    variant("rasdaman", default=False, when="@:3.6", description="Required for Rasdaman driver")
    variant(
        "rasterlite2", default=False, when="@2.2:", description="Required for RasterLite2 driver"
    )
    variant("rdb", default=False, when="@3.1:", description="Required for RDB driver")
    variant("sde", default=False, when="@:3.1", description="Required for SDE driver")
    variant("sfcgal", default=False, when="@2.2:", description="Provides 3D geometry operations")
    variant("spatialite", default=False, description="Required for SQLite and GPKG drivers")
    variant("sqlite3", default=True, description="Required for SQLite and GPKG drivers")
    variant("teigha", default=False, description="Required for DWG and DGNv8 drivers")
    variant("tiledb", default=False, when="@3:", description="Required for TileDB driver")
    variant("webp", default=False, description="Required for WEBP driver")
    variant(
        "xercesc",
        default=False,
        description="Required for XML parsing capabilities in many OGR drivers",
    )
    variant("zstd", default=False, when="@2.3:", description="Required for Zarr driver")

    # Language bindings
    variant("python", default=False, description="Build Python bindings")
    variant("java", default=False, description="Build Java bindings")
    variant("csharp", default=False, when="build_system=cmake", description="Build C# bindings")
    variant("perl", default=False, when="@:3.4", description="Build Perl bindings")
    variant("php", default=False, when="@:2.3", description="Build PHP bindings")

    # Build system
    build_system(
        conditional("cmake", when="@3.5:"), conditional("autotools", when="@:3.5"), default="cmake"
    )

    with when("build_system=cmake"):
        generator("ninja")
        depends_on("cmake@3.16:", type="build", when="@3.9:")
        depends_on("cmake@3.9:", type="build")

    with when("build_system=autotools"):
        depends_on("gmake", type="build")

    # Required dependencies
    # Versions come from gdal_check_package in cmake/helpers/CheckDependentLibraries.cmake
    depends_on("pkgconfig@0.25:", type="build")
    depends_on("proj@6.3.1:", when="@3.9:")
    depends_on("proj@6:", when="@3:")
    depends_on("proj@:6", when="@2.5:2")
    depends_on("proj@:5", when="@2.4")
    depends_on("proj@:4", when="@:2.3")
    depends_on("zlib-api")
    depends_on("libtiff@4.1:", when="@3.9:")
    depends_on("libtiff@4:", when="@3:")
    depends_on("libtiff@3.6.0:")  # 3.9.0+ needed to pass testsuite
    depends_on("libgeotiff@1.5:", when="@3:")
    depends_on("libgeotiff@1.2.1:1.5", when="@2.4.1:2")
    depends_on("libgeotiff@1.2.1:1.4", when="@:2.4.0")
    depends_on("json-c")
    depends_on("json-c@0.12.1", when="@:2.2")

    # Optional dependencies
    depends_on("libarchive", when="+archive")
    depends_on("armadillo", when="+armadillo")
    depends_on("blas", when="+armadillo")
    depends_on("lapack", when="+armadillo")
    depends_on("arrow", when="+arrow")
    # depends_on("basis-universal", when="+basisu")
    depends_on("c-blosc", when="+blosc")
    depends_on("brunsli", when="+brunsli")
    # depends_on('bsb', when='+bsb')
    depends_on("cfitsio", when="+cfitsio")
    depends_on("crunch", when="+crnlib")
    depends_on("curl@7.68:", when="@3.9:+curl")
    depends_on("curl", when="+curl")
    depends_on("cryptopp", when="+cryptopp")
    depends_on("libdeflate", when="+deflate")
    # depends_on('dods', when='+dods')
    # depends_on('ecw', when='+ecw')
    # depends_on('libepsilon', when='+epsilon')
    depends_on("expat@1.95:", when="+expat")
    # depends_on('filegdb', when='+filegdb')
    # depends_on('fme', when='+fme')
    depends_on("freexl", when="+freexl")
    depends_on("fyba", when="+fyba")
    depends_on("geos@3.8:", when="@3.9:+geos")
    depends_on("geos@3.1:", when="+geos")
    depends_on("giflib", when="+gif")
    depends_on("grass@5.7:", when="+grass")
    depends_on("grib-api", when="+grib")
    depends_on("libgta", when="+gta")
    depends_on("libheif@1.1:", when="+heif")
    depends_on("hdf", when="+hdf4")
    depends_on("hdf5@1.10:", when="@3.9:+hdf5")
    depends_on("hdf5@:1.13", when="@:3.5+hdf5")
    depends_on("hdf5@:1.12", when="@:3.4+hdf5")
    depends_on("hdf5+cxx", when="@3.8:+hdf5+kea")
    depends_on("hdf5+cxx", when="@:3.7+hdf5")
    depends_on("hadoop", when="+hdfs")
    depends_on("iconv", when="+iconv")
    # depends_on('idb', when='+idb')
    # depends_on('ingres', when='+ingres')
    depends_on("jasper@1.900.1", patches=[patch("uuid.patch")], when="+jasper")
    depends_on("jpeg", when="+jpeg")
    depends_on("libjxl", when="+jxl")
    # depends_on('kakadu', when='+kdu')
    depends_on("kealib", when="+kea")
    depends_on("lerc", when="+lerc")
    depends_on("libaec", when="+libaec")
    # depends_on('libcsf', when='+libcsf')
    depends_on("libkml@1.3:", when="+libkml")
    depends_on("xz", when="+liblzma")
    depends_on("qb3", when="+libqb3")
    depends_on("libxml2", when="+libxml2")
    # depends_on('luratech', when='+luratech')
    depends_on("lz4", when="+lz4")
    depends_on("jackcess@1.2", type="run", when="+mdb")
    depends_on("mongo-cxx-driver", when="+mongocxx")
    # depends_on('bsoncxx', when='+mongocxx')
    # depends_on('mrf', when='+mrf')
    # depends_on('mrsid', when='+mrsid')
    # depends_on('lizardtech-lidar', when='+mrsid_lidar')
    # depends_on('mssql_ncli', when='+mssql_ncli')
    # depends_on('mssql_odbc', when='+mssql_odbc')
    depends_on("mysql", when="+mysql")
    depends_on("netcdf-c@4.7:", when="@3.9:+netcdf")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("unixodbc", when="+odbc")
    # depends_on('odbc-cpp-wrapper', when='+odbccpp')
    # depends_on('ogdi', when='+ogdi')
    # depends_on('lib-opencad', when='+opencad')
    depends_on("opencl", when="+opencl")
    depends_on("openexr@2.2:", when="+openexr")
    depends_on("openjpeg@2.3.1:", when="@3.9:+openjpeg")
    depends_on("openjpeg", when="+openjpeg")
    depends_on("openssl", when="+openssl")
    depends_on("oracle-instant-client", when="+oracle")
    depends_on("parquet-cpp", when="+parquet")
    # depends_on('pcidsk', when='+pcidsk')
    depends_on("pcre2", when="@3.5:+pcre2")
    depends_on("pcre", when="@:3.4+pcre2")
    # depends_on('pdfium', when='+pdfium')
    depends_on("libpng@1.6:", when="@3.9:+png")
    depends_on("libpng", when="+png")
    # depends_on('podofo', when='+podofo')
    depends_on("poppler@0.86:", when="@3.9:+poppler")
    depends_on("poppler@0.24:", when="@3:+poppler")
    depends_on("poppler@:0.63", when="@:2.3+poppler")
    depends_on("poppler@:0.71", when="@:2.4+poppler")
    depends_on("poppler@:21", when="@:3.4.1+poppler")
    depends_on("poppler", when="+poppler")
    depends_on("postgresql", when="+postgresql")
    depends_on("qhull", when="+qhull")
    depends_on("qhull@2015:", when="@3.5:+qhull")
    depends_on("qhull@:2020.1", when="@:3.3+qhull")
    # depends_on('rasdaman', when='+rasdaman')
    # depends_on('rasterlite2@1.1:', when='@3.7:+rasterlite2')
    # depends_on('rasterlite2', when='+rasterlite2')
    # depends_on('rdblib', when='+rdb')
    # depends_on('sde', when='+sde')
    depends_on("sfcgal", when="+sfcgal")
    depends_on("libspatialite@4.1.2:", when="@3.7:+spatialite")
    depends_on("libspatialite", when="+spatialite")
    depends_on("sqlite@3.31:", when="@3.9:+sqlite3")
    depends_on("sqlite@3:", when="+sqlite3")
    # depends_on('teigha', when='+teigha')
    # depends_on('tiledb@2.15:', when='@3.9:+tiledb')
    # depends_on('tiledb@2.7:', when='@3.7:+tiledb')
    # depends_on('tiledb', when='+tiledb')
    depends_on("libwebp", when="+webp")
    depends_on("xerces-c@3.1:", when="+xercesc")
    depends_on("zstd", when="+zstd")

    # Language bindings
    # FIXME: Allow packages to extend multiple packages
    # See https://github.com/spack/spack/issues/987
    extends("python", when="+python")
    # extends('openjdk', when='+java')
    # extends('perl', when='+perl')

    # swig/python/pyproject.toml (3.9+)
    # swig/python/setup.py.in (3.5-3.8)
    # swig/python/osgeo/__init__.py (3.4-)
    depends_on("python", type=("build", "link", "run"), when="+python")
    # Uses distutils
    depends_on("python@:3.11", type=("build", "link", "run"), when="@:3.4+python")
    # swig/python/pyproject.toml (3.9+)
    # swig/python/setup.py (3.8-)
    depends_on("py-setuptools@67:", type="build", when="@3.9:+python")
    depends_on("py-setuptools@:57", type="build", when="@:3.2+python")  # needs 2to3
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("py-numpy@1.0.0:", type=("build", "run"), when="+python")
    # https://github.com/OSGeo/gdal/issues/9751
    depends_on("py-numpy@:1", when="@:3.8+python", type=("build", "run"))
    depends_on("swig", type="build", when="+python")
    depends_on("java@7:", type=("build", "link", "run"), when="@3.2:+java")
    depends_on("java@6:", type=("build", "link", "run"), when="@2.4:+java")
    depends_on("java@5:", type=("build", "link", "run"), when="@2.1:+java")
    depends_on("java@4:", type=("build", "link", "run"), when="@:2.0+java")
    depends_on("ant", type="build", when="+java")
    depends_on("swig", type="build", when="+java")
    depends_on("perl", type=("build", "run"), when="+perl")
    depends_on("swig", type="build", when="+perl")
    depends_on("php", type=("build", "link", "run"), when="+php")
    depends_on("swig", type="build", when="+php")

    # https://gdal.org/development/rfc/rfc88_googletest.html
    depends_on("googletest@1.10:", type="test")

    # https://gdal.org/development/rfc/rfc98_build_requirements_gdal_3_9.html
    with default_args(when="@3.9:", msg="GDAL requires C++17 support"):
        conflicts("%gcc@:7")
        conflicts("%clang@:4")
        conflicts("%msvc@:19.14")

    # https://gdal.org/development/rfc/rfc68_cplusplus11.html
    with default_args(when="@2.3:", msg="GDAL requires C++11 support"):
        conflicts("%gcc@:4.8.0")
        conflicts("%clang@:3.2")
        conflicts("%msvc@:13")

    # https://github.com/OSGeo/gdal/issues/8693
    conflicts("%gcc@11:", when="@:3.6")

    # https://github.com/OSGeo/gdal/issues/5994
    conflicts("~png", when="@3:3.5.0")
    conflicts("~jpeg", when="@3:3.5.0")
    # TODO: investigate build issues
    conflicts("+brunsli", when="@3.4")
    conflicts("+qhull", when="@2.1")
    conflicts("+mdb", when="~java", msg="MDB driver requires Java")

    # TODO: add packages for the following dependencies
    conflicts("+bsb")
    conflicts("+dods")
    conflicts("+ecw")
    conflicts("+epsilon")
    conflicts("+filegdb")
    conflicts("+fme")
    conflicts("+idb")
    conflicts("+ingres")
    conflicts("+kdu")
    conflicts("+libcsf")
    conflicts("+luratech")
    conflicts("+mrf")
    conflicts("+mrsid")
    conflicts("+mrsid_lidar")
    conflicts("+mssql_ncli")
    conflicts("+mssql_odbc")
    conflicts("+odbccpp")
    conflicts("+ogdi")
    conflicts("+opencad")
    conflicts("+pcidsk")
    conflicts("+pdfium")
    conflicts("+podofo")
    conflicts("+rasdaman")
    conflicts("+rasterlite2")
    conflicts("+rdb")
    conflicts("+sde")
    conflicts("+teigha")
    conflicts("+tiledb")

    # https://github.com/OSGeo/gdal/issues/3782
    patch(
        "https://github.com/OSGeo/gdal/pull/3786.patch?full_index=1",
        when="@3.3.0",
        level=2,
        sha256="9f9824296e75b34b3e78284ec772a5ac8f8ba92c17253ea9ca242caf766767ce",
    )

    # https://github.com/spack/spack/issues/41299
    # ensures the correct build specific libproj is used with cmake builds (gdal >=3.5.0)
    patch(
        "https://patch-diff.githubusercontent.com/raw/OSGeo/gdal/pull/8964.patch?full_index=1",
        when="@3.5:3.8",
        sha256="52459dc9903ced5005ba81515762a55cd829d8f5420607405c211c4a77c2bf79",
    )

    executables = ["^gdal-config$"]

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)("--version", output=str, error=str).rstrip()

    def setup_run_environment(self, env):
        if self.spec.satisfies("+java"):
            class_paths = find(self.prefix, "*.jar")
            classpath = os.pathsep.join(class_paths)
            env.prepend_path("CLASSPATH", classpath)

        # `spack test run gdal+python` requires these for the Python bindings
        # to find the correct libraries
        libs = []
        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            libs.extend(filter_system_paths(query.libs.directories))
        if sys.platform == "darwin":
            env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", ":".join(libs))
        else:
            env.prepend_path("LD_LIBRARY_PATH", ":".join(libs))

    def patch(self):
        if self.spec.satisfies("+java platform=darwin"):
            filter_file("linux", "darwin", "swig/java/java.opt", string=True)
            filter_file("-lazy-ljvm", "-ljvm", "configure", string=True)


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        # https://gdal.org/build_hints.html
        args = [
            # Only use Spack-installed dependencies
            self.define("GDAL_USE_EXTERNAL_LIBS", False),
            self.define("GDAL_USE_INTERNAL_LIBS", False),
            # Required dependencies
            self.define("GDAL_USE_GEOTIFF", True),
            self.define("GDAL_USE_JSONC", True),
            self.define("GDAL_USE_TIFF", True),
            self.define("GDAL_USE_ZLIB", True),
            # zlib-ng + deflate64 doesn't compile (heavily relies on zlib)
            # but since zlib-ng is faster than zlib, it deflate shouldn't
            # be necessary.
            self.define("ENABLE_DEFLATE64", "zlib-ng" not in self.spec),
            # Optional dependencies
            self.define_from_variant("GDAL_USE_ARCHIVE", "archive"),
            self.define_from_variant("GDAL_USE_ARMADILLO", "armadillo"),
            self.define_from_variant("GDAL_USE_ARROW", "arrow"),
            self.define_from_variant("GDAL_USE_BASISU", "basisu"),
            self.define_from_variant("GDAL_USE_BLOSC", "blosc"),
            self.define_from_variant("GDAL_USE_BRUNSLI", "brunsli"),
            self.define_from_variant("GDAL_USE_CFITSIO", "cfitsio"),
            self.define_from_variant("GDAL_USE_CRNLIB", "crnlib"),
            self.define_from_variant("GDAL_USE_CRYPTOPP", "cryptopp"),
            self.define_from_variant("GDAL_USE_CURL", "curl"),
            self.define_from_variant("GDAL_USE_DEFLATE", "deflate"),
            self.define_from_variant("GDAL_USE_ECW", "ecw"),
            self.define_from_variant("GDAL_USE_EXPAT", "expat"),
            self.define_from_variant("GDAL_USE_FILEGDB", "filegdb"),
            self.define_from_variant("GDAL_USE_FREEXL", "freexl"),
            self.define_from_variant("GDAL_USE_FYBA", "fyba"),
            self.define_from_variant("GDAL_USE_GEOS", "geos"),
            self.define_from_variant("GDAL_USE_GIF", "gif"),
            self.define_from_variant("GDAL_USE_GTA", "gta"),
            self.define_from_variant("GDAL_USE_HEIF", "heif"),
            self.define_from_variant("GDAL_USE_HDF4", "hdf4"),
            self.define_from_variant("GDAL_USE_HDF5", "hdf5"),
            self.define_from_variant("GDAL_USE_HDFS", "hdfs"),
            self.define_from_variant("GDAL_USE_ICONV", "iconv"),
            self.define_from_variant("GDAL_USE_IDB", "idb"),
            self.define_from_variant("GDAL_USE_JPEG", "jpeg"),
            self.define_from_variant("GDAL_USE_JXL", "jxl"),
            self.define_from_variant("GDAL_USE_KDU", "kdu"),
            self.define_from_variant("GDAL_USE_KEA", "kea"),
            self.define_from_variant("GDAL_USE_LERC", "lerc"),
            self.define_from_variant("GDAL_USE_LIBAEC", "libaec"),
            self.define_from_variant("GDAL_USE_LIBCSF", "libcsf"),
            self.define_from_variant("GDAL_USE_LIBKML", "libkml"),
            self.define_from_variant("GDAL_USE_LIBLZMA", "liblzma"),
            self.define_from_variant("GDAL_USE_LIBQB3", "libqb3"),
            self.define_from_variant("GDAL_USE_LIBXML2", "libxml2"),
            self.define_from_variant("GDAL_USE_LURATECH", "luratech"),
            self.define_from_variant("GDAL_USE_LZ4", "lz4"),
            self.define_from_variant("GDAL_USE_MONGOCXX", "mongocxx"),
            self.define_from_variant("GDAL_USE_MRSID", "mrsid"),
            self.define_from_variant("GDAL_USE_MSSQL_NCLI", "mssql_ncli"),
            self.define_from_variant("GDAL_USE_MSSQL_ODBC", "mssql_odbc"),
            self.define_from_variant("GDAL_USE_MYSQL", "mysql"),
            self.define_from_variant("GDAL_USE_NETCDF", "netcdf"),
            self.define_from_variant("GDAL_USE_ODBC", "odbc"),
            self.define_from_variant("GDAL_USE_ODBCCPP", "odbccpp"),
            self.define_from_variant("GDAL_USE_OGDI", "ogdi"),
            self.define_from_variant("GDAL_USE_OPENCAD", "opencad"),
            self.define_from_variant("GDAL_USE_OPENCL", "opencl"),
            self.define_from_variant("GDAL_USE_OPENEXR", "openexr"),
            self.define_from_variant("GDAL_USE_OPENJPEG", "openjpeg"),
            self.define_from_variant("GDAL_USE_OPENSSL", "openssl"),
            self.define_from_variant("GDAL_USE_ORACLE", "oracle"),
            self.define_from_variant("GDAL_USE_PARQUET", "parquet"),
            self.define_from_variant("GDAL_USE_PCRE2", "pcre2"),
            self.define_from_variant("GDAL_USE_PDFIUM", "pdfium"),
            self.define_from_variant("GDAL_USE_PNG", "png"),
            self.define_from_variant("GDAL_USE_PODOFO", "podofo"),
            self.define_from_variant("GDAL_USE_POPPLER", "poppler"),
            self.define_from_variant("GDAL_USE_POSTGRESQL", "postgresql"),
            self.define_from_variant("GDAL_USE_QHULL", "qhull"),
            self.define_from_variant("GDAL_USE_RASDAMAN", "rasdaman"),
            self.define_from_variant("GDAL_USE_RASTERLITE2", "rasterlite2"),
            self.define_from_variant("GDAL_USE_RDB", "rdb"),
            self.define_from_variant("GDAL_USE_SFCGAL", "sfcgal"),
            self.define_from_variant("GDAL_USE_SPATIALITE", "spatialite"),
            self.define_from_variant("GDAL_USE_SQLITE3", "sqlite3"),
            self.define_from_variant("GDAL_USE_TEIGHA", "teigha"),
            self.define_from_variant("GDAL_USE_TILEDB", "tiledb"),
            self.define_from_variant("GDAL_USE_WEBP", "webp"),
            self.define_from_variant("GDAL_USE_XERCESC", "xercesc"),
            self.define_from_variant("GDAL_USE_ZSTD", "zstd"),
            # Language bindings
            self.define_from_variant("BUILD_PYTHON_BINDINGS", "python"),
            self.define_from_variant("BUILD_JAVA_BINDINGS", "java"),
            self.define_from_variant("BUILD_CSHARP_BINDINGS", "csharp"),
        ]

        # Remove empty strings
        args = [arg for arg in args if arg]

        return args


class AutotoolsBuilder(AutotoolsBuilder):
    def setup_build_environment(self, env):
        # Needed to install Python bindings to GDAL installation
        # prefix instead of Python installation prefix.
        # See swig/python/GNUmakefile for more details.
        env.set("PREFIX", self.prefix)
        env.set("DESTDIR", "/")

    def with_or_without(self, name, variant=None, package=None, attribute=None):
        if not variant:
            variant = name

        if not self.pkg.has_variant(variant):
            msg = '"{}" is not a variant of "{}"'
            raise KeyError(msg.format(variant, self.name))

        if variant not in self.spec.variants:
            return ""

        if self.spec.variants[variant].value:
            if package:
                value = self.spec[package].prefix
                if attribute == "command":
                    value = self.spec[package].command.path
                elif attribute == "libs":
                    value = self.spec[package].libs.directories[0]
                return "--with-{}={}".format(name, value)
            else:
                return "--with-{}".format(name)
        else:
            return "--without-{}".format(name)

    def configure_args(self):
        # https://trac.osgeo.org/gdal/wiki/BuildHints
        args = [
            "--prefix={}".format(self.prefix),
            # Required dependencies
            "--with-geotiff={}".format(self.spec["libgeotiff"].prefix),
            "--with-libjson-c={}".format(self.spec["json-c"].prefix),
            "--with-libtiff={}".format(self.spec["libtiff"].prefix),
            "--with-libz={}".format(self.spec["zlib-api"].prefix),
            # Optional dependencies
            self.with_or_without("armadillo", package="armadillo"),
            self.with_or_without("blosc", package="c-blosc"),
            self.with_or_without("brunsli"),
            self.with_or_without("bsb"),
            self.with_or_without("cfitsio", package="cfitsio"),
            self.with_or_without("dds", variant="crnlib", package="crunch"),
            self.with_or_without("curl", package="curl", attribute="command"),
            self.with_or_without("cryptopp", package="cryptopp"),
            self.with_or_without("libdeflate", variant="deflate", package="libdeflate"),
            self.with_or_without("dods-root", variant="dods", package="dods"),
            self.with_or_without("ecw", package="ecw"),
            self.with_or_without("epsilon", package="libepsilon"),
            self.with_or_without("expat", package="expat"),
            self.with_or_without("fgdb", variant="filegdb", package="filegdb"),
            self.with_or_without("fme", package="fme"),
            self.with_or_without("freexl", package="freexl"),
            self.with_or_without("sosi", variant="fyba", package="fyba"),
            self.with_or_without("geos", package="geos", attribute="command"),
            self.with_or_without("gif", package="giflib"),
            self.with_or_without("grass", package="grass"),
            self.with_or_without("grib"),
            self.with_or_without("libgrass", variant="grass"),
            self.with_or_without("gta", package="gta"),
            self.with_or_without("heif"),
            self.with_or_without("hdf4", package="hdf"),
            self.with_or_without("hdf5", package="hdf5"),
            self.with_or_without("hdfs", package="hadoop"),
            self.with_or_without("idb", package="idb"),
            self.with_or_without("ingres", package="ingres"),
            self.with_or_without("jasper", package="jasper"),
            self.with_or_without("jpeg", package="jpeg"),
            self.with_or_without("jxl"),
            self.with_or_without("kakadu", variant="kdu"),
            self.with_or_without("kea", package="kealib", attribute="command"),
            self.with_or_without("lerc", package="lerc"),
            self.with_or_without("pcraster", variant="libcsf", package="libcsf"),
            self.with_or_without("libkml", package="libkml"),
            self.with_or_without("liblzma"),
            self.with_or_without("jp2lura", variant="luratech", package="luratech"),
            self.with_or_without("lz4", package="lz4"),
            self.with_or_without("mdb"),
            self.with_or_without("mrf"),
            self.with_or_without("mrsid", package="mrsid"),
            self.with_or_without("mrsid_lidar", package="lizardtech-lidar"),
            self.with_or_without("mysql", package="mysql", attribute="command"),
            self.with_or_without("netcdf", package="netcdf-c"),
            self.with_or_without("odbc", package="unixodbc"),
            self.with_or_without("hana", variant="odbccpp", package="odbc-cpp-wrapper"),
            self.with_or_without("ogdi", package="ogdi"),
            self.with_or_without("opencl"),
            self.with_or_without("exr", variant="openexr"),
            self.with_or_without("openjpeg"),
            self.with_or_without("crypto", variant="openssl", package="openssl"),
            self.with_or_without("oci", variant="oracle", package="oracle-instant-client"),
            self.with_or_without("pcidsk", package="pcidsk"),
            self.with_or_without("pcre", variant="pcre2"),
            self.with_or_without("pdfium", package="pdfium"),
            self.with_or_without("png", package="libpng"),
            self.with_or_without("podofo", package="podofo"),
            self.with_or_without("poppler", package="poppler"),
            self.with_or_without("qhull"),
            self.with_or_without("rasdaman", package="rasdaman"),
            self.with_or_without("rasterlite2", package="rasterlite2"),
            self.with_or_without("rdb", package="rdb"),
            self.with_or_without("sde", package="sde"),
            self.with_or_without("spatialite", package="libspatialite"),
            self.with_or_without("sqlite3", package="sqlite"),
            self.with_or_without("sfcgal", package="sfcgal", attribute="command"),
            self.with_or_without("tiledb", package="tiledb"),
            self.with_or_without("webp", package="libwebp"),
            self.with_or_without("xerces", variant="xercesc", package="xerces-c"),
            self.with_or_without("zstd", package="zstd"),
            # Language bindings
            self.with_or_without("python", package="python", attribute="command"),
            self.with_or_without("java", package="java"),
            self.with_or_without("jvm-lib", variant="mdb", package="java", attribute="libs"),
            self.with_or_without("jvm-lib-add-rpath", variant="mdb"),
            self.with_or_without("perl"),
            self.with_or_without("php"),
        ]
        if self.spec.satisfies("+iconv"):
            if self.spec["iconv"].name == "libiconv":
                args.append(f"--with-libiconv-prefix={self.spec['iconv'].prefix}")
            else:
                args.append("--without-libiconv-prefix")

        # Renamed or modified flags
        if self.spec.satisfies("@3:"):
            args.extend(
                [
                    self.with_or_without("xml2", variant="libxml2"),
                    self.with_or_without("mongocxxv3", variant="mongocxx"),
                    self.with_or_without("pg", variant="postgresql"),
                ]
            )
        else:
            args.extend(
                [
                    self.with_or_without(
                        "xml2", variant="libxml2", package="libxml2", attribute="command"
                    ),
                    self.with_or_without("mongocxx", variant="mongocxx"),
                    self.with_or_without(
                        "pg", variant="postgresql", package="postgresql", attribute="command"
                    ),
                ]
            )

        if self.spec.satisfies("@2.3:"):
            args.append("--with-proj={}".format(self.spec["proj"].prefix))

        if self.spec.satisfies("@2.2:"):
            args.append(self.with_or_without("teigha", package="teigha"))
        else:
            args.append(self.with_or_without("dwgdirect", variant="teigha", package="teigha"))

        if self.spec.satisfies("+hdf4"):
            hdf4 = self.spec["hdf"]
            if "+external-xdr" in hdf4 and hdf4["rpc"].name == "libtirpc":
                args.append("LIBS=" + hdf4["rpc"].libs.link_flags)

        # Remove empty strings
        args = [arg for arg in args if arg]

        return args

    def build(self, pkg, spec, prefix):
        # https://trac.osgeo.org/gdal/wiki/GdalOgrInJavaBuildInstructionsUnix
        make()
        if spec.satisfies("+java"):
            with working_dir("swig/java"):
                make()

    def check(self):
        # no top-level test target
        if self.spec.satisfies("+java"):
            with working_dir("swig/java"):
                make("test")

    def install(self, pkg, spec, prefix):
        make("install")
        if spec.satisfies("+java"):
            with working_dir("swig/java"):
                make("install")
                install("*.jar", prefix)

        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)
