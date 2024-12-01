# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlBioEnsemblVariation(Package):
    """The Ensembl Variation Perl API and SQL schema."""

    homepage = "http://www.ensembl.org/info/docs/api/variation/"
    url = "https://github.com/Ensembl/ensembl-variation/archive/release/112.zip"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    for vers, sha in [
        ("112", "ad75ff0a9efbf2d5c10ab5087d414bac685819664d01fbe4a9765393bd742a7c"),
        ("111", "b2171b3f5f82a2b7e849c0ec8dc254f4bace4b3faba1b3ab75c5eea596e33bef"),
        ("110", "210d627dcb867d9fda3a0d94428da256f394c32e34df5171b9b9e604507e1f05"),
    ]:
        version(vers, sha256=sha)
        depends_on(f"perl-bio-ensembl@{vers}", when=f"@{vers}")
        depends_on(f"perl-bio-ensembl-io@{vers}", when=f"@{vers}+tools", type="run")
        depends_on(f"perl-bio-ensembl-funcgen@{vers}", when=f"@{vers}", type="run")

    extends("perl")

    variant("sql", default=False, description="Install SQL files")
    variant("schema", default=False, description="Install schema documentation")
    variant("nextflow", default=False, description="Install nextflow workflows")
    variant("scripts", default=False, description="Install additional scripts")
    variant("tools", default=False, description="Install additional tools")
    variant("ld", default=False, description="Compile LD calculation tools")

    depends_on("perl-bioperl@1.6.924")
    depends_on("perl-bio-bigfile")
    depends_on("perl-bio-db-hts")
    depends_on("perl-sereal")
    depends_on("perl-json")
    depends_on("perl-set-intervaltree")
    depends_on("perl-string-approx")
    depends_on("perl-xml-hash-xs")
    depends_on("perl-xml-libxml")
    depends_on("perl-date-manip")

    with when("+ld"):
        depends_on("htslib", type="build")
        depends_on("gmake", type="build")

    phases = ("build", "install")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+ld"):
            env.set("HTSLIB_DIR", self.spec["htslib"].prefix.include)

    def build(self, spec, prefix):
        if spec.satisfies("+ld"):
            make = which("make")
            with working_dir("C_code"):
                make()
        if spec.satisfies("+tools"):
            # Fix the fact that phenotype_annotation isn't executable
            chmod = which("chmod")
            chmod("+x", "tools/phenotype_annotation/phenotype_annotation")

    def install(self, spec, prefix):
        install_tree("modules", prefix.lib.perl5)

        mkdirp(prefix.share.ensembl.variation)
        for extra in ["sql", "schema", "nextflow", "scripts"]:
            if spec.satisfies(f"+{extra}"):
                target = join_path(prefix.share.ensembl, extra)
                install_tree(extra, target)

        for requested, targets in {
            "+ld": ["C_code/calc_genotypes", "C_code/ld_vcf"],
            "+tools": [
                "tools/linkage_disequilibrium/ld_tool",
                "tools/variant_simulator/simulate_variation",
                "tools/phenotype_annotation/phenotype_annotation",
            ],
        }.items():
            if spec.satisfies(requested):
                mkdirp(prefix.bin)
                for target in targets:
                    install(target, prefix.bin)
