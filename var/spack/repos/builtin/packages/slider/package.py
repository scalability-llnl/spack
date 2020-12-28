# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Slider(MavenPackage):
    """Slider is a framework for deployment and management of these
    long-running data access applications in Hadoop."""

    homepage = "https://www.cloudera.com/products/open-source/apache-hadoop/apache-slider.html"
    url      = "http://archive.apache.org/dist/incubator/slider/0.92.0-incubating/apache-slider-0.92.0-incubating-source-release.tar.gz"
    list_url = "http://archive.apache.org/dist/incubator/slider"
    list_depth = 1

    version('0.92.0', sha256='485f02f4f9f0b270017717c9471b83b0d77d005d25261b741fb381791ce838b9')
    version('0.91.0', sha256='212a5cde6de60060c9a081f553d66940b70af4bccb469072febb554c4005bcef')
    version('0.90.2', sha256='410941f772d29f564c4bb90ca0631f29dc895f509048cb6052f8695302e3f944')

    depends_on('java@8', type=('build', 'run'))
    depends_on('python@2.7.0:2.7.99', type='run')

    def url_for_version(self, version):
        return "http://archive.apache.org/dist/incubator/slider/{0}-incubating/apache-slider-{0}-incubating-source-release.tar.gz".format(version)

    def install(self, spec, prefix):
        slider_path = join_path(self.stage.source_path,
                                'slider-assembly', 'target',
                                'slider-{0}-incubating-all'
                                .format(spec.version),
                                'slider-{0}-incubating'
                                .format(spec.version))
        with working_dir(slider_path):
            install_tree('.', prefix)
