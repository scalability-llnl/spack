# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tools to produce reports of spec installations"""
import codecs
import collections
import functools
import time
import traceback
import os

import llnl.util.lang
import spack.build_environment
import spack.fetch_strategy
import spack.package_base
from spack.install_test import TestSuite
from spack.reporter import Reporter
from spack.reporters.cdash import CDash
from spack.reporters.junit import JUnit

report_writers = {
    None: Reporter,
    'junit': JUnit,
    'cdash': CDash
}

#: Allowed report formats
valid_formats = list(report_writers.keys())

__all__ = [
    'valid_formats',
    'collect_info'
]


def fetch_log(pkg, do_fn, dir):
    log_files = {
        '_install_task': pkg.build_log_path,
        'do_test': os.path.join(dir, TestSuite.test_log_name(pkg.spec)),
    }
    try:
        with codecs.open(log_files[do_fn.__name__], 'r', 'utf-8') as f:
            return ''.join(f.readlines())
    except Exception:
        return 'Cannot open log for {0}'.format(
            pkg.spec.cshort_spec
        )


class InfoCollector(object):
    """Decorates PackageInstaller._install_task, which is called via
    PackageBase.do_install for individual specs, to collect information
    on the installation of certain specs.

    When exiting the context this change will be rolled-back.

    The data collected is available through the ``specs``
    attribute once exited, and it's organized as a list where
    each item represents the installation of one of the spec.

    Args:
        specs (list of Spec): specs whose install information will
           be recorded
    """
    def __init__(self, wrap_class, do_fn, specs, dir):
        #: Class for which to wrap a function
        self.wrap_class = wrap_class
        #: Action to be reported on
        self.do_fn = do_fn
        #: Backup of PackageBase function
        self._backup_do_fn = getattr(self.wrap_class, do_fn)
        #: Specs that will be acted on
        self.input_specs = specs
        #: This is where we record the data that will be included
        #: in our report.
        self.specs = []
        #: Record directory for test log paths
        self.dir = dir

    def __enter__(self):
        # Initialize the spec report with the data that is available upfront.
        for input_spec in self.input_specs:
            name_fmt = '{0}_{1}'
            name = name_fmt.format(input_spec.name,
                                   input_spec.dag_hash(length=7))

            spec = {
                'name': name,
                'nerrors': None,
                'nfailures': None,
                'npackages': None,
                'time': None,
                'timestamp': time.strftime(
                    "%a, %d %b %Y %H:%M:%S", time.gmtime()
                ),
                'properties': [],
                'packages': []
            }

            self.specs.append(spec)

            Property = collections.namedtuple('Property', ['name', 'value'])
            spec['properties'].append(
                Property('architecture', input_spec.architecture)
            )
            spec['properties'].append(
                Property('compiler', input_spec.compiler))

            # Check which specs are already installed and mark them as skipped
            # only for install_task
            if self.do_fn == '_install_task':
                for dep in filter(lambda x: x.package.installed,
                                  input_spec.traverse()):
                    package = {
                        'name': dep.name,
                        'id': dep.dag_hash(),
                        'elapsed_time': '0.0',
                        'result': 'skipped',
                        'message': 'Spec already installed'
                    }
                    spec['packages'].append(package)

        def gather_info(do_fn):
            """Decorates do_fn to gather useful information for
            a CI report.

            It's defined here to capture the environment and build
            this context as the installations proceed.
            """
            @functools.wraps(do_fn)
            def wrapper(instance, *args, **kwargs):
                if isinstance(instance, spack.package_base.PackageBase):
                    pkg = instance
                elif hasattr(args[0], 'pkg'):
                    pkg = args[0].pkg
                else:
                    raise Exception

                # We accounted before for what is already installed
                installed_already = pkg.installed

                package = {
                    'name': pkg.name,
                    'id': pkg.spec.dag_hash(),
                    'elapsed_time': None,
                    'result': None,
                    'message': None,
                    'installed_from_binary_cache': False
                }

                start_time = time.time()
                value = None
                try:
                    value = do_fn(instance, *args, **kwargs)
                    package['result'] = 'success'
                    package['stdout'] = fetch_log(pkg, do_fn, self.dir)
                    package['installed_from_binary_cache'] = \
                        pkg.installed_from_binary_cache
                    if do_fn.__name__ == '_install_task' and installed_already:
                        return

                except spack.build_environment.InstallError as e:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    package['result'] = 'failure'
                    package['message'] = e.message or 'Installation failure'
                    package['stdout'] = fetch_log(pkg, do_fn, self.dir)
                    package['stdout'] += package['message']
                    package['exception'] = e.traceback

                except (Exception, BaseException) as e:
                    # Everything else is an error (the installation
                    # failed outside of the child process)
                    package['result'] = 'error'
                    package['stdout'] = fetch_log(pkg, do_fn, self.dir)
                    package['message'] = str(e) or 'Unknown error'
                    package['exception'] = traceback.format_exc()

                finally:
                    package['elapsed_time'] = time.time() - start_time

                # Append the package to the correct spec report. In some
                # cases it may happen that a spec that is asked to be
                # installed explicitly will also be installed as a
                # dependency of another spec. In this case append to both
                # spec reports.
                for s in llnl.util.lang.dedupe([pkg.spec.root, pkg.spec]):
                    name = name_fmt.format(s.name, s.dag_hash(length=7))
                    try:
                        item = next((
                            x for x in self.specs
                            if x['name'] == name
                        ))
                        item['packages'].append(package)
                    except StopIteration:
                        pass

                return value

            return wrapper

        setattr(self.wrap_class, self.do_fn, gather_info(
            getattr(self.wrap_class, self.do_fn)
        ))

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Restore the original method in PackageBase
        setattr(self.wrap_class, self.do_fn, self._backup_do_fn)

        for spec in self.specs:
            spec['npackages'] = len(spec['packages'])
            spec['nfailures'] = len(
                [x for x in spec['packages'] if x['result'] == 'failure']
            )
            spec['nerrors'] = len(
                [x for x in spec['packages'] if x['result'] == 'error']
            )
            spec['time'] = sum([
                float(x['elapsed_time']) for x in spec['packages']
            ])


class collect_info(object):
    """Collects information to build a report while installing
    and dumps it on exit.

    If the format name is not ``None``, this context manager decorates
    PackageInstaller._install_task when entering the context for a
    PackageBase.do_install operation and unrolls the change when exiting.

    Within the context, only the specs that are passed to it
    on initialization will be recorded for the report. Data from
    other specs will be discarded.

    Examples:

        .. code-block:: python

            # The file 'junit.xml' is written when exiting
            # the context
            s = [Spec('hdf5').concretized()]
            with collect_info(PackageBase, do_install, s, 'junit', 'a.xml'):
                # A report will be generated for these specs...
                for spec in s:
                    getattr(class, function)(spec)
                # ...but not for this one
                Spec('zlib').concretized().do_install()

    Args:
        class: class on which to wrap a function
        function: function to wrap
        format_name (str or None): one of the supported formats
        args (dict): args passed to function

    Raises:
        ValueError: when ``format_name`` is not in ``valid_formats``
    """
    def __init__(self, cls, function, format_name, args):
        self.cls = cls
        self.function = function
        self.filename = None
        if args.cdash_upload_url:
            self.format_name = 'cdash'
            self.filename = 'cdash_report'
        else:
            self.format_name = format_name
        # Check that the format is valid.
        if self.format_name not in valid_formats:
            raise ValueError('invalid report type: {0}'
                             .format(self.format_name))
        self.report_writer = report_writers[self.format_name](args)

    def __call__(self, type, dir=os.getcwd()):
        self.type = type
        self.dir = dir
        return self

    def concretization_report(self, msg):
        self.report_writer.concretization_report(self.filename, msg)

    def __enter__(self):
        if self.format_name:
            # Start the collector and patch self.function on appropriate class
            self.collector = InfoCollector(
                self.cls, self.function, self.specs, self.dir)
            self.collector.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.format_name:
            # Close the collector and restore the
            # original PackageInstaller._install_task
            self.collector.__exit__(exc_type, exc_val, exc_tb)

            report_data = {'specs': self.collector.specs}
            report_fn = getattr(self.report_writer, '%s_report' % self.type)
            report_fn(self.filename, report_data)
