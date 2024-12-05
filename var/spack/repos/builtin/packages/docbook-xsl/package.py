# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DocbookXsl(Package):
    """DocBook XSLT 1.0 Stylesheets."""

    homepage = "https://github.com/docbook/xslt10-stylesheets"
    url = "https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F1.79.2/docbook-xsl-1.79.2.tar.bz2"

    license("custom")

    version("1.79.2", sha256="316524ea444e53208a2fb90eeb676af755da96e1417835ba5f5eb719c81fa371")
    version(
        "1.78.1",
        sha256="c98f7296ab5c8ccd2e0bc07634976a37f50847df2d8a59bdb1e157664700b467",
        url="https://sourceforge.net/projects/docbook/files/docbook-xsl/1.78.1/docbook-xsl-1.78.1.tar.bz2",
    )

    depends_on("docbook-xml")
    depends_on("libxml2", type="build")

    patch("docbook-xsl-1.79.2-stack_fix-1.patch", when="@1.79.2")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    @property
    def catalog(self):
        return join_path(self.prefix, "xsl-catalog")

    @run_after("install")
    def config_docbook(self):
        catalog = self.catalog
        version = self.version
        xml_xsd = join_path(prefix, "slides", "schema", "xsd", "xml.xsd")
        xmlcatalog = which("xmlcatalog")

        # create catalog
        xmlcatalog("--noout", "--create", catalog)
        xmlcatalog(
            "--noout", "--add", "system", "https://www.w3.org/2001/xml.xsd", xml_xsd, catalog
        )
        xmlcatalog(
            "--noout", "--add", "system", "https://www.w3.org/2009/01/xml.xsd", xml_xsd, catalog
        )
        xmlcatalog("--noout", "--add", "uri", "https://www.w3.org/2001/xml.xsd", xml_xsd, catalog)
        xmlcatalog(
            "--noout", "--add", "uri", "https://www.w3.org/2009/01/xml.xsd", xml_xsd, catalog
        )

        docbook_urls = ["docbook.sourceforge.net", "cdn.docbook.org"]
        docbook_rewrites = ["rewriteSystem", "rewriteURI"]
        docbook_versions = ["current", version]
        for docbook_url in docbook_urls:
            for docbook_rewrite in docbook_rewrites:
                for docbook_version in docbook_versions:
                    xmlcatalog(
                        "--noout",
                        "--add",
                        docbook_rewrite,
                        "http://{0}/release/xsl/{1}".format(docbook_url, docbook_version),
                        "file://{0}".format(prefix),
                        catalog,
                    )

    def setup_run_environment(self, env):
        catalog = self.catalog
        env.prepend_path("XML_CATALOG_FILES", catalog, separator=" ")

    def setup_dependent_build_environment(self, env, dependent_spec):
        catalog = self.catalog
        env.prepend_path("XML_CATALOG_FILES", catalog, separator=" ")
