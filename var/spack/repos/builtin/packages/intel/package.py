from spack import *
import os
import re


def filter_pick(input_list, regex_filter):
    """Returns the items in input_list that are found in the regex_filter"""
    return [l for l in input_list for m in (regex_filter(l),) if m]


def unfilter_pick(input_list, regex_filter):
    """Returns the items in input_list that are not found in the
       regex_filter"""
    return [l for l in input_list for m in (regex_filter(l),) if not m]


def get_all_components():
    """Returns a list of all the components associated with the downloaded
       Intel package"""
    all_components = []
    with open("pset/mediaconfig.xml", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.find('<Abbr>') != -1:
                component = line[line.find('<Abbr>') + 6:line.find('</Abbr>')]
                all_components.append(component)
    return all_components


class IntelInstaller(Package):
    """Base package containing common methods for installing Intel software"""

    homepage = "https://software.intel.com/en-us"
    intel_components = "ALL"
    license_required = True
    license_comment = '#'
    license_files = ['Licenses/license.lic']
    license_vars = ['INTEL_LICENSE_FILE']
    license_url = \
        'https://software.intel.com/en-us/articles/intel-license-manager-faq'

    @property
    def global_license_file(self):
        """Returns the path where a global license file should be stored."""
        if not self.license_files:
            return
        return join_path(self.global_license_dir, "intel",
                         os.path.basename(self.license_files[0]))

    def install(self, spec, prefix):

        # Remove the installation DB, otherwise it will try to install into
        # location of other Intel builds
        if os.path.exists(os.path.join(os.environ["HOME"], "intel",
                          "intel_sdp_products.db")):
            os.remove(os.path.join(os.environ["HOME"], "intel",
                      "intel_sdp_products.db"))

        if not hasattr(self, "intel_prefix"):
            self.intel_prefix = self.prefix

        silent_config_filename = 'silent.cfg'
        with open(silent_config_filename, 'w') as f:
            f.write("""
ACCEPT_EULA=accept
PSET_MODE=install
CONTINUE_WITH_INSTALLDIR_OVERWRITE=yes
PSET_INSTALL_DIR=%s
ACTIVATION_LICENSE_FILE=%s
ACTIVATION_TYPE=license_file
PHONEHOME_SEND_USAGE_DATA=no
CONTINUE_WITH_OPTIONAL_ERROR=yes
COMPONENTS=%s
""" % (self.intel_prefix, self.global_license_file, self.intel_components))

        install_script = Executable("./install.sh")
        install_script('--silent', silent_config_filename)


class Intel(IntelInstaller):
    """Intel Compilers.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # TODO: can also try the online installer (will download files on demand)
    version('16.0.2', '1133fb831312eb519f7da897fec223fa',
        url="file://%s/parallel_studio_xe_2016_composer_edition_update2.tgz"  # NOQA: ignore=E501
        % os.getcwd())
    version('16.0.3', '3208eeabee951fc27579177b593cefe9',
        url="file://%s/parallel_studio_xe_2016_composer_edition_update3.tgz"  # NOQA: ignore=E501
        % os.getcwd())

    variant('rpath', default=True, description="Add rpath to .cfg files")

    def install(self, spec, prefix):
        components = []
        all_components = get_all_components()
        regex = '(comp|openmp|intel-tbb|icc|ifort|psxe|icsxe-pset)'
        components = filter_pick(all_components, re.compile(regex).search)

        self.intel_components = ';'.join(components)
        IntelInstaller.install(self, spec, prefix)

        absbindir = os.path.split(os.path.realpath(os.path.join(
            self.prefix.bin, "icc")))[0]
        abslibdir = os.path.split(os.path.realpath(os.path.join(
            self.prefix.lib, "intel64", "libimf.a")))[0]

        # symlink or copy?
        os.symlink(self.global_license_file, os.path.join(absbindir,
                   "license.lic"))

        if spec.satisfies('+rpath'):
            for compiler_command in ["icc", "icpc", "ifort"]:
                cfgfilename = os.path.join(absbindir, "%s.cfg" %
                                           compiler_command)
                with open(cfgfilename, "w") as f:
                    f.write('-Xlinker -rpath -Xlinker %s\n' % abslibdir)

        os.symlink(os.path.join(self.prefix.man, "common", "man1"),
                   os.path.join(self.prefix.man, "man1"))
