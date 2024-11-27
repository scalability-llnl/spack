# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import codecs
import collections
import hashlib
import os.path
import platform
import posixpath
import re
import socket
import time
import xml.sax.saxutils
from typing import Dict, Optional
from urllib.parse import urlencode
from urllib.request import HTTPSHandler, Request, build_opener

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack
import spack.paths
import spack.platforms
import spack.spec
import spack.tengine
import spack.util.git
from spack.error import SpackError
from spack.util.crypto import checksum
from spack.util.log_parse import parse_log_events
from spack.util.web import ssl_create_default_context

from .base import Reporter
from .extract import extract_test_parts

# Mapping Spack phases to the corresponding CTest/CDash phase.
# TODO: Some of the phases being lumped into configure in the CDash tables
# TODO:   really belong in a separate column, such as "Setup".
# TODO: Would also be nice to have `stage` as a separate phase that could
# TODO:   be lumped into that new column instead of configure, for example.
MAP_PHASES_TO_CDASH = {
    "autoreconf": "configure",  # AutotoolsBuilder
    "bootstrap": "configure",  # CMakeBuilder
    "build": "build",
    "build_processes": "build",  # Openloops
    "cmake": "configure",  # CMakeBuilder
    "configure": "configure",
    "edit": "configure",  # MakefileBuilder
    "generate_luarocks_config": "configure",  # LuaBuilder
    "hostconfig": "configure",  # Lvarray
    "initconfig": "configure",  # CachedCMakeBuilder
    "install": "build",
    "meson": "configure",  # MesonBuilder
    "preprocess": "configure",  # LuaBuilder
    "qmake": "configure",  # QMakeBuilder
    "unpack": "configure",  # LuaBuilder
}

# Initialize data structures common to each phase's report.
CDASH_PHASES = set(MAP_PHASES_TO_CDASH.values())
CDASH_PHASES.add("update")
# CDash request timeout in seconds
SPACK_CDASH_TIMEOUT = 45

CDashConfiguration = collections.namedtuple(
    "CDashConfiguration", ["upload_url", "packages", "build", "site", "buildstamp", "track"]
)


def build_stamp(track, timestamp):
    buildstamp_format = "%Y%m%d-%H%M-{0}".format(track)
    return time.strftime(buildstamp_format, time.localtime(timestamp))


class CDash(Reporter):
    """Generate reports of spec installations for CDash.

    To use this reporter, pass the ``--cdash-upload-url`` argument to
    ``spack install``::

        spack install --cdash-upload-url=\\
            https://mydomain.com/cdash/submit.php?project=Spack <spec>

    In this example, results will be uploaded to the *Spack* project on the
    CDash instance hosted at https://mydomain.com/cdash.
    """

    def __init__(self, configuration: CDashConfiguration):
        #: Set to False if any error occurs when building the CDash report
        self.success = True

        # Jinja2 expects `/` path separators
        self.template_dir = "reports/cdash"
        self.cdash_upload_url = configuration.upload_url

        if self.cdash_upload_url:
            self.buildid_regexp = re.compile("<buildId>([0-9]+)</buildId>")
        self.phase_regexp = re.compile(r"Executing phase: '(.*)'")

        self.authtoken = None
        if "SPACK_CDASH_AUTH_TOKEN" in os.environ:
            tty.verbose("Using CDash auth token from environment")
            self.authtoken = os.environ.get("SPACK_CDASH_AUTH_TOKEN")

        self.install_command = " ".join(configuration.packages)
        self.base_buildname = configuration.build or self.install_command
        self.site = configuration.site or socket.gethostname()
        self.osname = platform.system()
        self.osrelease = platform.release()
        self.target = spack.platforms.host().target("default_target")
        self.starttime = int(time.time())
        self.endtime = self.starttime
        self.buildstamp = (
            configuration.buildstamp
            if configuration.buildstamp
            else build_stamp(configuration.track, self.starttime)
        )
        self.buildIds: Dict[str, str] = {}
        self.revision = ""
        git = spack.util.git.git()
        with working_dir(spack.paths.spack_root):
            self.revision = git("rev-parse", "HEAD", output=str).strip()
        self.generator = "spack-{0}".format(spack.get_version())
        self.multiple_packages = False

    def report_build_name(self, pkg_name):
        return (
            "{0} - {1}".format(self.base_buildname, pkg_name)
            if self.multiple_packages
            else self.base_buildname
        )

    def build_report_for_package(self, report_dir, package, duration):
        if "stdout" not in package:
            # Skip reporting on packages that do not generate output.
            return

        self.current_package_name = package["name"]
        self.buildname = self.report_build_name(self.current_package_name)
        report_data = self.initialize_report(report_dir)
        for phase in CDASH_PHASES:
            report_data[phase] = {}
            report_data[phase]["loglines"] = []
            report_data[phase]["status"] = 0
            report_data[phase]["starttime"] = self.starttime

        # Track the phases we perform so we know what reports to create.
        # We always report the update step because this is how we tell CDash
        # what revision of Spack we are using.
        phases_encountered = ["update"]

        # Generate a report for this package.
        current_phase = ""
        cdash_phase = ""
        for line in package["stdout"].splitlines():
            match = None
            if line.find("Executing phase: '") != -1:
                match = self.phase_regexp.search(line)
            if match:
                current_phase = match.group(1)
                if current_phase not in MAP_PHASES_TO_CDASH:
                    current_phase = ""
                    continue
                cdash_phase = MAP_PHASES_TO_CDASH[current_phase]
                if cdash_phase not in phases_encountered:
                    phases_encountered.append(cdash_phase)
                report_data[cdash_phase]["loglines"].append(
                    str("{0} output for {1}:".format(cdash_phase, package["name"]))
                )
            elif cdash_phase:
                report_data[cdash_phase]["loglines"].append(xml.sax.saxutils.escape(line))

        # something went wrong pre-cdash "configure" phase b/c we have an exception and only
        # "update" was encounterd.
        # dump the report in the configure line so teams can see what the issue is
        if len(phases_encountered) == 1 and package["exception"]:
            # TODO this mapping is not ideal since these are pre-configure errors
            # we need to determine if a more appropriate cdash phase can be utilized
            # for now we will add a message to the log explaining this
            cdash_phase = "configure"
            phases_encountered.append(cdash_phase)

            log_message = (
                "Pre-configure errors occured in Spack's process that terminated the "
                "build process prematurely.\nSpack output::\n{0}".format(
                    xml.sax.saxutils.escape(package["exception"])
                )
            )

            report_data[cdash_phase]["loglines"].append(log_message)

        # Move the build phase to the front of the list if it occurred.
        # This supports older versions of CDash that expect this phase
        # to be reported before all others.
        if "build" in phases_encountered:
            build_pos = phases_encountered.index("build")
            phases_encountered.insert(0, phases_encountered.pop(build_pos))

        self.endtime = self.starttime + duration
        for phase in phases_encountered:
            report_data[phase]["endtime"] = self.endtime
            report_data[phase]["log"] = "\n".join(report_data[phase]["loglines"])
            errors, warnings = parse_log_events(report_data[phase]["loglines"])

            # Convert errors to warnings if the package reported success.
            if package["result"] == "success":
                warnings = errors + warnings
                errors = []

            # Cap the number of errors and warnings at 50 each.
            errors = errors[:50]
            warnings = warnings[:50]
            nerrors = len(errors)

            if nerrors > 0:
                self.success = False
                if phase == "configure":
                    report_data[phase]["status"] = 1

            if phase == "build":
                # Convert log output from ASCII to Unicode and escape for XML.
                def clean_log_event(event):
                    event = vars(event)
                    event["text"] = xml.sax.saxutils.escape(event["text"])
                    event["pre_context"] = xml.sax.saxutils.escape("\n".join(event["pre_context"]))
                    event["post_context"] = xml.sax.saxutils.escape(
                        "\n".join(event["post_context"])
                    )
                    # source_file and source_line_no are either strings or
                    # the tuple (None,).  Distinguish between these two cases.
                    if event["source_file"][0] is None:
                        event["source_file"] = ""
                        event["source_line_no"] = ""
                    else:
                        event["source_file"] = xml.sax.saxutils.escape(event["source_file"])
                    return event

                report_data[phase]["errors"] = []
                report_data[phase]["warnings"] = []
                for error in errors:
                    report_data[phase]["errors"].append(clean_log_event(error))
                for warning in warnings:
                    report_data[phase]["warnings"].append(clean_log_event(warning))

            if phase == "update":
                report_data[phase]["revision"] = self.revision

            # Write the report.
            report_name = phase.capitalize() + ".xml"
            if self.multiple_packages:
                report_file_name = package["name"] + "_" + report_name
            else:
                report_file_name = report_name
            phase_report = os.path.join(report_dir, report_file_name)

            with codecs.open(phase_report, "w", "utf-8") as f:
                env = spack.tengine.make_environment()
                if phase != "update":
                    # Update.xml stores site information differently
                    # than the rest of the CTest XML files.
                    site_template = posixpath.join(self.template_dir, "Site.xml")
                    t = env.get_template(site_template)
                    f.write(t.render(report_data))

                phase_template = posixpath.join(self.template_dir, report_name)
                t = env.get_template(phase_template)
                f.write(t.render(report_data))
            self.upload(phase_report)

    def build_report(self, report_dir, specs):
        # Do an initial scan to determine if we are generating reports for more
        # than one package. When we're only reporting on a single package we
        # do not explicitly include the package's name in the CDash build name.
        self.multiple_packages = False
        num_packages = 0
        for spec in specs:
            # Do not generate reports for packages that were installed
            # from the binary cache.
            spec["packages"] = [
                x
                for x in spec["packages"]
                if "installed_from_binary_cache" not in x or not x["installed_from_binary_cache"]
            ]
            for package in spec["packages"]:
                if "stdout" in package:
                    num_packages += 1
                    if num_packages > 1:
                        self.multiple_packages = True
                        break
            if self.multiple_packages:
                break

        # Generate reports for each package in each spec.
        for spec in specs:
            duration = 0
            if "time" in spec:
                duration = int(spec["time"])
            for package in spec["packages"]:
                self.build_report_for_package(report_dir, package, duration)
        self.finalize_report()

    def extract_standalone_test_data(self, package, phases, report_data):
        """Extract stand-alone test outputs for the package."""

        testing = {}
        report_data["testing"] = testing
        testing["starttime"] = self.starttime
        testing["endtime"] = self.starttime
        testing["generator"] = self.generator
        testing["parts"] = extract_test_parts(package["name"], package["stdout"].splitlines())

    def report_test_data(self, report_dir, package, phases, report_data):
        """Generate and upload the test report(s) for the package."""
        for phase in phases:
            # Write the report.
            report_name = phase.capitalize() + ".xml"
            report_file_name = "_".join([package["name"], package["id"], report_name])
            phase_report = os.path.join(report_dir, report_file_name)

            with codecs.open(phase_report, "w", "utf-8") as f:
                env = spack.tengine.make_environment()
                if phase not in ["update", "testing"]:
                    # Update.xml stores site information differently
                    # than the rest of the CTest XML files.
                    site_template = posixpath.join(self.template_dir, "Site.xml")
                    t = env.get_template(site_template)
                    f.write(t.render(report_data))

                phase_template = posixpath.join(self.template_dir, report_name)
                t = env.get_template(phase_template)
                f.write(t.render(report_data))

            tty.debug("Preparing to upload {0}".format(phase_report))
            self.upload(phase_report)

    def test_report_for_package(self, report_dir, package, duration):
        if "stdout" not in package:
            # Skip reporting on packages that did not generate any output.
            tty.debug("Skipping report for {0}: No generated output".format(package["name"]))
            return

        self.current_package_name = package["name"]
        if self.base_buildname == self.install_command:
            # The package list is NOT all that helpful in this case
            self.buildname = "{0}-{1}".format(self.current_package_name, package["id"])
        else:
            self.buildname = self.report_build_name(self.current_package_name)
        self.endtime = self.starttime + duration

        report_data = self.initialize_report(report_dir)
        report_data["hostname"] = socket.gethostname()
        phases = ["testing"]
        self.extract_standalone_test_data(package, phases, report_data)

        self.report_test_data(report_dir, package, phases, report_data)

    def test_report(self, report_dir, specs):
        """Generate reports for each package in each spec."""
        tty.debug("Processing test report")
        for spec in specs:
            duration = 0
            if "time" in spec:
                duration = int(spec["time"])
            for package in spec["packages"]:
                self.test_report_for_package(report_dir, package, duration)

        self.finalize_report()

    def test_skipped_report(
        self, report_dir: str, spec: spack.spec.Spec, reason: Optional[str] = None
    ):
        """Explicitly report spec as being skipped (e.g., CI).

        Examples are the installation failed or the package is known to have
        broken tests.

        Args:
            report_dir: directory where the report is to be written
            spec: spec being tested
            reason: optional reason the test is being skipped
        """
        output = "Skipped {0} package".format(spec.name)
        if reason:
            output += "\n{0}".format(reason)

        package = {"name": spec.name, "id": spec.dag_hash(), "result": "skipped", "stdout": output}
        self.test_report_for_package(report_dir, package, duration=0.0)

    def concretization_report(self, report_dir, msg):
        self.buildname = self.base_buildname
        report_data = self.initialize_report(report_dir)
        report_data["update"] = {}
        report_data["update"]["starttime"] = self.starttime
        report_data["update"]["endtime"] = self.endtime
        report_data["update"]["revision"] = self.revision
        report_data["update"]["log"] = msg

        env = spack.tengine.make_environment()
        update_template = posixpath.join(self.template_dir, "Update.xml")
        t = env.get_template(update_template)
        output_filename = os.path.join(report_dir, "Update.xml")
        with open(output_filename, "w") as f:
            f.write(t.render(report_data))
        # We don't have a current package when reporting on concretization
        # errors so refer to this report with the base buildname instead.
        self.current_package_name = self.base_buildname
        self.upload(output_filename)
        self.success = False
        self.finalize_report()

    def initialize_report(self, report_dir):
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)
        report_data = {}
        report_data["buildname"] = self.buildname
        report_data["buildstamp"] = self.buildstamp
        report_data["install_command"] = self.install_command
        report_data["generator"] = self.generator
        report_data["osname"] = self.osname
        report_data["osrelease"] = self.osrelease
        report_data["site"] = self.site
        report_data["target"] = self.target
        return report_data

    def upload(self, filename):
        if not self.cdash_upload_url:
            print("Cannot upload {0} due to missing upload url".format(filename))
            return

        # Compute md5 checksum for the contents of this file.
        md5sum = checksum(hashlib.md5, filename, block_size=8192)

        opener = build_opener(HTTPSHandler(context=ssl_create_default_context()))
        with open(filename, "rb") as f:
            params_dict = {
                "build": self.buildname,
                "site": self.site,
                "stamp": self.buildstamp,
                "MD5": md5sum,
            }
            encoded_params = urlencode(params_dict)
            url = "{0}&{1}".format(self.cdash_upload_url, encoded_params)
            request = Request(url, data=f)
            request.add_header("Content-Type", "text/xml")
            request.add_header("Content-Length", os.path.getsize(filename))
            if self.authtoken:
                request.add_header("Authorization", "Bearer {0}".format(self.authtoken))
            try:
                # By default, urllib2 only support GET and POST.
                # CDash expects this file to be uploaded via PUT.
                request.get_method = lambda: "PUT"
                response = opener.open(request, timeout=SPACK_CDASH_TIMEOUT)
                if self.current_package_name not in self.buildIds:
                    resp_value = response.read()
                    if isinstance(resp_value, bytes):
                        resp_value = resp_value.decode("utf-8")
                    match = self.buildid_regexp.search(resp_value)
                    if match:
                        buildid = match.group(1)
                        self.buildIds[self.current_package_name] = buildid
            except Exception as e:
                print("Upload to CDash failed: {0}".format(e))

    def finalize_report(self):
        if self.buildIds:
            tty.msg("View your build results here:")
            for package_name, buildid in self.buildIds.items():
                # Construct and display a helpful link if CDash responded with
                # a buildId.
                build_url = self.cdash_upload_url
                build_url = build_url[0 : build_url.find("submit.php")]
                build_url += "buildSummary.php?buildid={0}".format(buildid)
                tty.msg("{0}: {1}".format(package_name, build_url))
        if not self.success:
            raise SpackError("Errors encountered, see above for more details")
