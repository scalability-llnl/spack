# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import codecs
import hashlib
import os.path
import platform
import re
import socket
import time
import xml.sax.saxutils
from six import iteritems, text_type
from six.moves.urllib.request import build_opener, HTTPHandler, Request
from six.moves.urllib.parse import urlencode

from llnl.util.filesystem import working_dir
import llnl.util.tty as tty
from ordereddict_backport import OrderedDict
import spack.build_environment
import spack.fetch_strategy
import spack.package
from spack.error import SpackError
from spack.reporter import Reporter
from spack.util.crypto import checksum
from spack.util.executable import which
from spack.util.log_parse import parse_log_events

__all__ = ['CDash']

# Mapping Spack phases to the corresponding CTest/CDash phase.
map_phases_to_cdash = {
    'autoreconf': 'configure',
    'cmake':      'configure',
    'configure':  'configure',
    'edit':       'configure',
    'build':      'build',
    'install':    'build'
}

# Initialize data structures common to each phase's report.
cdash_phases = set(map_phases_to_cdash.values())
cdash_phases.add('update')


class CDash(Reporter):
    """Generate reports of spec installations for CDash.

    To use this reporter, pass the ``--cdash-upload-url`` argument to
    ``spack install``::

        spack install --cdash-upload-url=\\
            https://mydomain.com/cdash/submit.php?project=Spack <spec>

    In this example, results will be uploaded to the *Spack* project on the
    CDash instance hosted at https://mydomain.com/cdash.
    """

    def __init__(self, args):
        Reporter.__init__(self, args)
        tty.set_verbose(args.verbose)
        self.success = True
        self.template_dir = os.path.join('reports', 'cdash')
        self.cdash_upload_url = args.cdash_upload_url

        if self.cdash_upload_url:
            self.buildid_regexp = re.compile("<buildId>([0-9]+)</buildId>")
        self.phase_regexp = re.compile(r"Executing phase: '(.*)'")

        self.authtoken = None
        if 'SPACK_CDASH_AUTH_TOKEN' in os.environ:
            tty.verbose("Using CDash auth token from environment")
            self.authtoken = os.environ.get('SPACK_CDASH_AUTH_TOKEN')

        if getattr(args, 'spec', ''):
            packages = args.spec
        elif getattr(args, 'specs', ''):
            packages = args.specs
        else:
            packages = []
            for file in args.specfiles:
                with open(file, 'r') as f:
                    s = spack.spec.Spec.from_yaml(f)
                    packages.append(s.format())
        self.install_command = ' '.join(packages)
        self.base_buildname = args.cdash_build or self.install_command
        self.site = args.cdash_site or socket.gethostname()
        self.osname = platform.system()
        self.endtime = int(time.time())
        if args.cdash_buildstamp:
            self.buildstamp = args.cdash_buildstamp
        else:
            buildstamp_format = "%Y%m%d-%H%M-{0}".format(args.cdash_track)
            self.buildstamp = time.strftime(buildstamp_format,
                                            time.localtime(self.endtime))
        self.buildIds = OrderedDict()
        self.revision = ''
        git = which('git')
        with working_dir(spack.paths.spack_root):
            self.revision = git('rev-parse', 'HEAD', output=str).strip()
        self.multiple_packages = False

    def build_report_for_package(self, directory_name, package, duration):
        if 'stdout' not in package:
            # Skip reporting on packages that did not generate any output.
            return

        self.current_package_name = package['name']
        if self.multiple_packages:
            self.buildname = "{0} - {1}".format(
                self.base_buildname, package['name'])
        else:
            self.buildname = self.base_buildname
        report_data = self.initialize_report(directory_name)
        for phase in cdash_phases:
            report_data[phase] = {}
            report_data[phase]['loglines'] = []
            report_data[phase]['status'] = 0
            report_data[phase]['endtime'] = self.endtime

        # Track the phases we perform so we know what reports to create.
        # We always report the update step because this is how we tell CDash
        # what revision of Spack we are using.
        phases_encountered = ['update']

        # Generate a report for this package.
        current_phase = ''
        cdash_phase = ''
        for line in package['stdout'].splitlines():
            match = None
            if line.find("Executing phase: '") != -1:
                match = self.phase_regexp.search(line)
            if match:
                current_phase = match.group(1)
                if current_phase not in map_phases_to_cdash:
                    current_phase = ''
                    continue
                cdash_phase = \
                    map_phases_to_cdash[current_phase]
                if cdash_phase not in phases_encountered:
                    phases_encountered.append(cdash_phase)
                report_data[cdash_phase]['loglines'].append(
                    text_type("{0} output for {1}:".format(
                        cdash_phase, package['name'])))
            elif cdash_phase:
                report_data[cdash_phase]['loglines'].append(
                    xml.sax.saxutils.escape(line))

        # Move the build phase to the front of the list if it occurred.
        # This supports older versions of CDash that expect this phase
        # to be reported before all others.
        if "build" in phases_encountered:
            build_pos = phases_encountered.index("build")
            phases_encountered.insert(0, phases_encountered.pop(build_pos))

        self.starttime = self.endtime - duration
        for phase in phases_encountered:
            report_data[phase]['starttime'] = self.starttime
            report_data[phase]['log'] = \
                '\n'.join(report_data[phase]['loglines'])
            errors, warnings = parse_log_events(report_data[phase]['loglines'])
            # Cap the number of errors and warnings at 50 each.
            errors = errors[:50]
            warnings = warnings[:50]
            nerrors = len(errors)

            if phase == 'configure' and nerrors > 0:
                report_data[phase]['status'] = 1
                self.success = False

            if phase == 'build':
                # Convert log output from ASCII to Unicode and escape for XML.
                def clean_log_event(event):
                    event = vars(event)
                    event['text'] = xml.sax.saxutils.escape(event['text'])
                    event['pre_context'] = xml.sax.saxutils.escape(
                        '\n'.join(event['pre_context']))
                    event['post_context'] = xml.sax.saxutils.escape(
                        '\n'.join(event['post_context']))
                    # source_file and source_line_no are either strings or
                    # the tuple (None,).  Distinguish between these two cases.
                    if event['source_file'][0] is None:
                        event['source_file'] = ''
                        event['source_line_no'] = ''
                    else:
                        event['source_file'] = xml.sax.saxutils.escape(
                            event['source_file'])
                    return event

                # Convert errors to warnings if the package reported success.
                if package['result'] == 'success':
                    warnings = errors + warnings
                    errors = []
                else:
                    self.success = False

                report_data[phase]['errors'] = []
                report_data[phase]['warnings'] = []
                for error in errors:
                    report_data[phase]['errors'].append(clean_log_event(error))
                for warning in warnings:
                    report_data[phase]['warnings'].append(
                        clean_log_event(warning))

            if phase == 'update':
                report_data[phase]['revision'] = self.revision

            # Write the report.
            report_name = phase.capitalize() + ".xml"
            if self.multiple_packages:
                report_file_name = package['name'] + "_" + report_name
            else:
                report_file_name = report_name
            phase_report = os.path.join(directory_name, report_file_name)

            with codecs.open(phase_report, 'w', 'utf-8') as f:
                env = spack.tengine.make_environment()
                if phase != 'update':
                    # Update.xml stores site information differently
                    # than the rest of the CTest XML files.
                    site_template = os.path.join(self.template_dir, 'Site.xml')
                    t = env.get_template(site_template)
                    f.write(t.render(report_data))

                phase_template = os.path.join(self.template_dir, report_name)
                t = env.get_template(phase_template)
                f.write(t.render(report_data))
            self.upload(phase_report)

    def build_report(self, directory_name, input_data):
        # Do an initial scan to determine if we are generating reports for more
        # than one package. When we're only reporting on a single package we
        # do not explicitly include the package's name in the CDash build name.
        num_packages = 0
        for spec in input_data['specs']:
            # Do not generate reports for packages that were installed
            # from the binary cache.
            spec['packages'] = [
                x for x in spec['packages']
                if 'installed_from_binary_cache' not in x or
                   not x['installed_from_binary_cache']
            ]
            for package in spec['packages']:
                if 'stdout' in package:
                    num_packages += 1
                    if num_packages > 1:
                        self.multiple_packages = True
                        break
            if self.multiple_packages:
                break

        # Generate reports for each package in each spec.
        for spec in input_data['specs']:
            duration = 0
            if 'time' in spec:
                duration = int(spec['time'])
            for package in spec['packages']:
                self.build_report_for_package(
                    directory_name, package, duration)
        self.finalize_report()

    def test_report_for_package(self, directory_name, package, duration):
        if 'stdout' not in package:
            # Skip reporting on packages that did not generate any output.
            return

        self.current_package_name = package['name']
        self.buildname = "{0} - {1}".format(
            self.base_buildname, package['name'])

        report_data = self.initialize_report(directory_name)

        for phase in ('test', 'update'):
            report_data[phase] = {}
            report_data[phase]['loglines'] = []
            report_data[phase]['status'] = 0
            report_data[phase]['endtime'] = self.endtime

        # Track the phases we perform so we know what reports to create.
        # We always report the update step because this is how we tell CDash
        # what revision of Spack we are using.
        phases_encountered = ['test', 'update']

        # Generate a report for this package.
        # The first line just says "Testing package name-hash"
        report_data['test']['loglines'].append(
            text_type("{0} output for {1}:".format(
                'test', package['name'])))
        for line in package['stdout'].splitlines()[1:]:
            report_data['test']['loglines'].append(
                xml.sax.saxutils.escape(line))

        self.starttime = self.endtime - duration
        for phase in phases_encountered:
            report_data[phase]['starttime'] = self.starttime
            report_data[phase]['log'] = \
                '\n'.join(report_data[phase]['loglines'])
            errors, warnings = parse_log_events(report_data[phase]['loglines'])
            # Cap the number of errors and warnings at 50 each.
            errors = errors[0:49]
            warnings = warnings[0:49]

            if phase == 'test':
                # Convert log output from ASCII to Unicode and escape for XML.
                def clean_log_event(event):
                    event = vars(event)
                    event['text'] = xml.sax.saxutils.escape(event['text'])
                    event['pre_context'] = xml.sax.saxutils.escape(
                        '\n'.join(event['pre_context']))
                    event['post_context'] = xml.sax.saxutils.escape(
                        '\n'.join(event['post_context']))
                    # source_file and source_line_no are either strings or
                    # the tuple (None,).  Distinguish between these two cases.
                    if event['source_file'][0] is None:
                        event['source_file'] = ''
                        event['source_line_no'] = ''
                    else:
                        event['source_file'] = xml.sax.saxutils.escape(
                            event['source_file'])
                    return event

                # Convert errors to warnings if the package reported success.
                if package['result'] == 'success':
                    warnings = errors + warnings
                    errors = []

                report_data[phase]['errors'] = []
                report_data[phase]['warnings'] = []
                for error in errors:
                    report_data[phase]['errors'].append(clean_log_event(error))
                for warning in warnings:
                    report_data[phase]['warnings'].append(
                        clean_log_event(warning))

            if phase == 'update':
                report_data[phase]['revision'] = self.revision

            # Write the report.
            report_name = phase.capitalize() + ".xml"
            report_file_name = package['name'] + "_" + report_name
            phase_report = os.path.join(directory_name, report_file_name)

            with codecs.open(phase_report, 'w', 'utf-8') as f:
                env = spack.tengine.make_environment()
                if phase != 'update':
                    # Update.xml stores site information differently
                    # than the rest of the CTest XML files.
                    site_template = os.path.join(self.template_dir, 'Site.xml')
                    t = env.get_template(site_template)
                    f.write(t.render(report_data))

                phase_template = os.path.join(self.template_dir, report_name)
                t = env.get_template(phase_template)
                f.write(t.render(report_data))
            self.upload(phase_report)

    def test_report(self, directory_name, input_data):
        # Generate reports for each package in each spec.
        for spec in input_data['specs']:
            duration = 0
            if 'time' in spec:
                duration = int(spec['time'])
            for package in spec['packages']:
                self.test_report_for_package(
                    directory_name, package, duration)
        self.finalize_report()

    def concretization_report(self, directory_name, msg):
        self.buildname = self.base_buildname
        report_data = self.initialize_report(directory_name)
        report_data['update'] = {}
        report_data['update']['starttime'] = self.endtime
        report_data['update']['endtime'] = self.endtime
        report_data['update']['revision'] = self.revision
        report_data['update']['log'] = msg

        env = spack.tengine.make_environment()
        update_template = os.path.join(self.template_dir, 'Update.xml')
        t = env.get_template(update_template)
        output_filename = os.path.join(directory_name, 'Update.xml')
        with open(output_filename, 'w') as f:
            f.write(t.render(report_data))
        # We don't have a current package when reporting on concretization
        # errors so refer to this report with the base buildname instead.
        self.current_package_name = self.base_buildname
        self.upload(output_filename)
        self.success = False
        self.finalize_report()

    def initialize_report(self, directory_name):
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        report_data = {}
        report_data['buildname'] = self.buildname
        report_data['buildstamp'] = self.buildstamp
        report_data['install_command'] = self.install_command
        report_data['osname'] = self.osname
        report_data['site'] = self.site
        return report_data

    def upload(self, filename):
        if not self.cdash_upload_url:
            return

        # Compute md5 checksum for the contents of this file.
        md5sum = checksum(hashlib.md5, filename, block_size=8192)

        opener = build_opener(HTTPHandler)
        with open(filename, 'rb') as f:
            params_dict = {
                'build': self.buildname,
                'site': self.site,
                'stamp': self.buildstamp,
                'MD5': md5sum,
            }
            encoded_params = urlencode(params_dict)
            url = "{0}&{1}".format(self.cdash_upload_url, encoded_params)
            request = Request(url, data=f)
            request.add_header('Content-Type', 'text/xml')
            request.add_header('Content-Length', os.path.getsize(filename))
            if self.authtoken:
                request.add_header('Authorization',
                                   'Bearer {0}'.format(self.authtoken))
            # By default, urllib2 only support GET and POST.
            # CDash needs expects this file to be uploaded via PUT.
            request.get_method = lambda: 'PUT'
            response = opener.open(request)
            if self.current_package_name not in self.buildIds:
                resp_value = response.read()
                if isinstance(resp_value, bytes):
                    resp_value = resp_value.decode('utf-8')
                match = self.buildid_regexp.search(resp_value)
                if match:
                    buildid = match.group(1)
                    self.buildIds[self.current_package_name] = buildid

    def finalize_report(self):
        if self.buildIds:
            print("View your build results here:")
            for package_name, buildid in iteritems(self.buildIds):
                # Construct and display a helpful link if CDash responded with
                # a buildId.
                build_url = self.cdash_upload_url
                build_url = build_url[0:build_url.find("submit.php")]
                build_url += "buildSummary.php?buildid={0}".format(buildid)
                print("{0}: {1}".format(package_name, build_url))
        if not self.success:
            raise SpackError("Errors encountered, see above for more details")
