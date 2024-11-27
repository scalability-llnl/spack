# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ycsb(MavenPackage):
    """Yahoo! Cloud Serving Benchmark."""

    homepage = "https://research.yahoo.com/news/yahoo-cloud-serving-benchmark/"
    url = "https://github.com/brianfrankcooper/YCSB/archive/0.17.0.tar.gz"
    git = "https://github.com/brianfrankcooper/YCSB.git"

    license("Apache-2.0")

    version("master", branch="master")
    version("0.17.0", sha256="5dd1a3d4dd7ac336eadccc83b097c811e142cfe1b23fc278f247054a1892c0e0")
    version("0.16.0", sha256="4296fd5e90d7d6d7dfcbad90039ddf16e785706a07f99c1c8a06e6ee06440f71")
    version("0.15.0", sha256="50b83c11f1a2f19f45e3cc6781f952c69944d1221dfec72169c3587802fc7fbb")
    version("0.14.0", sha256="456bcc9fa3d5d66d76fffa9cec34afd4528d9f02aa8a8d1135f511650516d5cb")
    version("0.13.0", sha256="21cb8078a0fe2d8d909145744ca15848dbb6757e98a7fdc97fb4049f82f4afbc")

    # Note: this package fails to build with maven@3.8.4 because maven
    # stopped supporting http URLs in dependencies. This is why an earlier
    # version of this package was adding the dependency on mongodb-async-driver
    # and calling "mvn install:install-file ..." to make it available to maven
    # before building YCSB. However there are more dependencies that require
    # such a "manual" installation for YCSB to correctly build. I have left
    # the mondodb-async-driver dependency and its installation procedure commented
    # for reference, in case someone eventually wants to make this package work
    # with a newer maven by going through all the dependencies that need manual
    # installation one by one.

    depends_on("tar", type="build")
    depends_on("maven@3.1.0:3.6.3", type="build")
    # depends_on("mongodb-async-driver", type="build")

    def build(self, spec, prefix):
        mvn = which("mvn")
        # jar_name = (
        #     "target/mongodb-async-driver-" + spec["mongodb-async-driver"].version.string + ".jar"
        # )
        # path = join_path(self.spec["mongodb-async-driver"].prefix, jar_name)
        # mvn(
        #     "install:install-file",
        #     "-Dfile={0}".format(path),
        #     "-DgroupId=com.allanbank",
        #     "-DartifactId=mongodb-async-driver",
        #     "-Dversion=%s" % spec["mongodb-async-driver"].version.string,
        #     "-Dpackaging=jar",
        # )
        mvn("package", "-am", "-DskipTests")

    def install(self, spec, prefix):
        # The build process builds a tar.gz archive in distribution/target
        # that can easily be installed by untaring it into the install prefix.
        from glob import glob

        distribution = "distribution/target/ycsb-*.tar.gz"
        with working_dir(self.build_directory):
            dist_file = glob(distribution)[0]
        tar = which("tar")
        tar("xf", dist_file, "-C", prefix, "--strip-components=1")
