# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DocbookXml(Package):
    """Docbook DTD XML files."""

    homepage = "https://www.oasis-open.org/docbook"
    url = "https://www.oasis-open.org/docbook/xml/4.5/docbook-xml-4.5.zip"
    list_url = "https://www.oasis-open.org/docbook/xml/"
    list_depth = 1

    license("MIT")

    version("4.5", sha256="4e4e037a2b83c98c6c94818390d4bdd3f6e10f6ec62dd79188594e26190dc7b4")
    version("4.4", sha256="02f159eb88c4254d95e831c51c144b1863b216d909b5ff45743a1ce6f5273090")
    version("4.3", sha256="23068a94ea6fd484b004c5a73ec36a66aa47ea8f0d6b62cc1695931f5c143464")
    version("4.2", sha256="acc4601e4f97a196076b7e64b368d9248b07c7abf26b34a02cca40eeebe60fa2")

    depends_on("libxml2", type="build")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    @property
    def catalog(self):
        return join_path(self.prefix, "xml-catalog")

    @run_after("install")
    def config_docbook(self):
        catalog = self.catalog
        version = self.version
        docbook = join_path(prefix, "docbook")
        ent_dir = join_path(prefix, "ent")
        xmlcatalog = which("xmlcatalog")

        # create docbook
        xmlcatalog("--noout", "--create", docbook)
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            f"-//OASIS//DTD DocBook XML CALS Table Model V{version}//EN",
            f"file://{prefix}/calstblx.dtd",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            f"-//OASIS//DTD DocBook XML V{version}//EN",
            f"file://{prefix}/docbookx.dtd",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "-//OASIS//DTD XML Exchange Table Model 19990315//EN",
            f"file://{prefix}/soextblx.dtd",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            f"-//OASIS//ENTITIES DocBook XML Character Entities V{version}//EN",
            f"file://{prefix}/dbcentx.mod",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "-//OASIS//ENTITIES DocBook XML Additional General Entities "
            "V{0}//EN".format(version),
            f"file://{prefix}/dbgenent.mod",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            f"-//OASIS//ELEMENTS DocBook XML Document Hierarchy V{version}//EN",
            f"file://{prefix}/dbhierx.mod",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            f"-//OASIS//ENTITIES DocBook XML Notations V{version}//EN",
            f"file://{prefix}/dbnotnx.mod",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            f"-//OASIS//ELEMENTS DocBook XML Information Pool V{version}//EN",
            f"file://{prefix}/dbpoolx.mod",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            f"-//OASIS//ELEMENTS DocBook XML HTML Tables V{version}//EN",
            f"file://{prefix}/htmltblx.mod",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Math Symbols: Arrow " "Relations//EN",
            f"file://{ent_dir}/isoamsa.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Math Symbols: Binary " "Operators//EN",
            f"file://{ent_dir}/isoamsb.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN",
            f"file://{ent_dir}/isoamsc.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Math Symbols: " "Negated Relations//EN",
            f"file://{ent_dir}/isoamsn.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN",
            f"file://{ent_dir}/isoamso.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN",
            f"file://{ent_dir}/isoamsr.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Box and Line Drawing//EN",
            f"file://{ent_dir}/isobox.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Russian Cyrillic//EN",
            f"file://{ent_dir}/isocyr1.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN",
            f"file://{ent_dir}/isocyr2.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Diacritical Marks//EN",
            f"file://{ent_dir}/isodia.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Greek Letters//EN",
            f"file://{ent_dir}/isogrk1.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Monotoniko Greek//EN",
            f"file://{ent_dir}/isogrk2.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Greek Symbols//EN",
            f"file://{ent_dir}/isogrk3.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN",
            f"file://{ent_dir}/isogrk4.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Latin 1//EN",
            f"file://{ent_dir}/isolat1.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Added Latin 2//EN",
            f"file://{ent_dir}/isolat2.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN",
            f"file://{ent_dir}/isonum.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES Publishing//EN",
            f"file://{ent_dir}/isopub.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "public",
            "ISO 8879:1986//ENTITIES General Technical//EN",
            f"file://{ent_dir}/isotech.ent",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "rewriteSystem",
            f"https://www.oasis-open.org/docbook/xml/{version}",
            f"file://{prefix}",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "rewriteURI",
            f"https://www.oasis-open.org/docbook/xml/{version}",
            f"file://{prefix}",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "rewriteSystem",
            "https://www.oasis-open.org/docbook/xml/current",
            f"file://{prefix}",
            docbook,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "rewriteURI",
            "https://www.oasis-open.org/docbook/xml/current",
            f"file://{prefix}",
            docbook,
        )

        # create catalog
        xmlcatalog("--noout", "--create", catalog)
        xmlcatalog(
            "--noout",
            "--add",
            "delegatePublic",
            "-//OASIS//ENTITIES DocBook XML",
            f"file://{docbook}",
            catalog,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "delegatePublic",
            "-//OASIS//DTD DocBook XML",
            f"file://{docbook}",
            catalog,
        )
        xmlcatalog(
            "--noout", "--add", "delegatePublic", "ISO 8879:1986", f"file://{docbook}", catalog
        )
        xmlcatalog(
            "--noout",
            "--add",
            "delegateSystem",
            "https://www.oasis-open.org/docbook/",
            f"file://{docbook}",
            catalog,
        )
        xmlcatalog(
            "--noout",
            "--add",
            "delegateURI",
            "https://www.oasis-open.org/docbook/",
            f"file://{docbook}",
            catalog,
        )

        # map all versions to current version
        dtversions = ["4.1", "4.1.1", "4.1.2", "4.2", "4.3", "4.4", "4.5"]
        for dtversion in dtversions:
            xmlcatalog(
                "--noout",
                "--add",
                "public",
                f"-//OASIS//DTD DocBook XML V{dtversion}//EN",
                f"http://www.oasis-open.org/docbook/xml/{dtversion}/docbookx.dtd",
                docbook,
            )
            xmlcatalog(
                "--noout",
                "--add",
                "rewriteSystem",
                f"http://www.oasis-open.org/docbook/xml/{dtversion}",
                f"file://{prefix}",
                docbook,
            )
            xmlcatalog(
                "--noout",
                "--add",
                "rewriteURI",
                f"http://www.oasis-open.org/docbook/xml/{dtversion}",
                f"file://{prefix}",
                docbook,
            )
            xmlcatalog(
                "--noout",
                "--add",
                "delegateSystem",
                f"http://www.oasis-open.org/docbook/xml/{dtversion}",
                f"file://{docbook}",
                catalog,
            )
            xmlcatalog(
                "--noout",
                "--add",
                "delegateURI",
                f"http://www.oasis-open.org/docbook/xml/{dtversion}",
                f"file://{docbook}",
                catalog,
            )

    def setup_run_environment(self, env):
        catalog = self.catalog
        env.prepend_path("XML_CATALOG_FILES", catalog, separator=" ")

    def setup_dependent_build_environment(self, env, dependent_spec):
        catalog = self.catalog
        env.prepend_path("XML_CATALOG_FILES", catalog, separator=" ")
