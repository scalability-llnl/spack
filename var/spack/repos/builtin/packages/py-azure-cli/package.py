# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCli(PythonPackage):
    """Microsoft Azure Command-Line Tools."""

    homepage = "https://github.com/Azure/azure-cli"
    pypi = "azure-cli/azure-cli-2.9.1.tar.gz"

    version('2.9.1', sha256='749d850f73ea8956ab510288c1061dd7066180a8583081a6d560fdc7ac8314d6')

    depends_on('py-setuptools', type='build')
    depends_on('py-antlr4-python3-runtime@4.7.2:4.7', type=('build', 'run'))
    depends_on('py-azure-batch@9.0:9', type=('build', 'run'))
    depends_on('py-azure-cli-command-modules-nspkg@2.0:2', type=('build', 'run'))
    depends_on('py-azure-cli-core@2.9.1', type=('build', 'run'))
    depends_on('py-azure-cli-nspkg@3.0.3:3', type=('build', 'run'))
    depends_on('py-azure-cosmos@3.0.2:3', type=('build', 'run'))
    depends_on('py-azure-datalake-store@0.0.48:0.0', type=('build', 'run'))
    depends_on('py-azure-functions-devops-build@0.0.22:0.0', type=('build', 'run'))
    depends_on('py-azure-graphrbac@0.60.0:0.60', type=('build', 'run'))
    depends_on('py-azure-keyvault@1.1:1', type=('build', 'run'))
    depends_on('py-azure-mgmt-advisor@2.0.1:2', type=('build', 'run'))
    depends_on('py-azure-mgmt-apimanagement@0.1.0:0.1', type=('build', 'run'))
    depends_on('py-azure-mgmt-applicationinsights@0.1.1:0.1', type=('build', 'run'))
    depends_on('py-azure-mgmt-appconfiguration@0.4.0:0.4', type=('build', 'run'))
    depends_on('py-azure-mgmt-authorization@0.52.0:0.52', type=('build', 'run'))
    depends_on('py-azure-mgmt-batch@9.0.0:9.0', type=('build', 'run'))
    depends_on('py-azure-mgmt-batchai@2.0:2', type=('build', 'run'))
    depends_on('py-azure-mgmt-billing@0.2:0', type=('build', 'run'))
    depends_on('py-azure-mgmt-botservice@0.2.0:0.2', type=('build', 'run'))
    depends_on('py-azure-mgmt-cdn@4.1.0rc1', type=('build', 'run'))
    depends_on('py-azure-mgmt-cognitiveservices@6.2.0:6.2', type=('build', 'run'))
    depends_on('py-azure-mgmt-compute@13.0:13', type=('build', 'run'))
    depends_on('py-azure-mgmt-consumption@2.0:2', type=('build', 'run'))
    depends_on('py-azure-mgmt-containerinstance@1.4:1', type=('build', 'run'))
    depends_on('py-azure-mgmt-containerregistry@3.0.0rc14', type=('build', 'run'))
    depends_on('py-azure-mgmt-containerservice@9.0.1:9.0', type=('build', 'run'))
    depends_on('py-azure-mgmt-cosmosdb@0.15.0:0.15', type=('build', 'run'))
    depends_on('py-azure-mgmt-datalake-analytics@0.2.1:0.2', type=('build', 'run'))
    depends_on('py-azure-mgmt-datalake-store@0.5.0:0.5', type=('build', 'run'))
    depends_on('py-azure-mgmt-datamigration@0.1.0:0.1', type=('build', 'run'))
    depends_on('py-azure-mgmt-deploymentmanager@0.2.0:0.2', type=('build', 'run'))
    depends_on('py-azure-mgmt-devtestlabs@4.0:4', type=('build', 'run'))
    depends_on('py-azure-mgmt-dns@2.1:2', type=('build', 'run'))
    depends_on('py-azure-mgmt-eventgrid@3.0.0rc7', type=('build', 'run'))
    depends_on('py-azure-mgmt-eventhub@4.0.0:4', type=('build', 'run'))
    depends_on('py-azure-mgmt-hdinsight@1.5.1:1.5', type=('build', 'run'))
    depends_on('py-azure-mgmt-imagebuilder@0.4.0:0.4', type=('build', 'run'))
    depends_on('py-azure-mgmt-iotcentral@3.0.0:3.0', type=('build', 'run'))
    depends_on('py-azure-mgmt-iothub@0.12.0:0.12', type=('build', 'run'))
    depends_on('py-azure-mgmt-iothubprovisioningservices@0.2.0:0.2', type=('build', 'run'))
    depends_on('py-azure-mgmt-keyvault@2.2.0:2.2', type=('build', 'run'))
    depends_on('py-azure-mgmt-kusto@0.3.0:0.3', type=('build', 'run'))
    depends_on('py-azure-mgmt-loganalytics@0.7.0:0.7', type=('build', 'run'))
    depends_on('py-azure-mgmt-managedservices@1.0:1', type=('build', 'run'))
    depends_on('py-azure-mgmt-managementgroups@0.1:0', type=('build', 'run'))
    depends_on('py-azure-mgmt-maps@0.1.0:0.1', type=('build', 'run'))
    depends_on('py-azure-mgmt-marketplaceordering@0.1:0', type=('build', 'run'))
    depends_on('py-azure-mgmt-media@2.1:2', type=('build', 'run'))
    depends_on('py-azure-mgmt-monitor@0.10.0:0.10', type=('build', 'run'))
    depends_on('py-azure-mgmt-msi@0.2:0', type=('build', 'run'))
    depends_on('py-azure-mgmt-netapp@0.8.0:0.8', type=('build', 'run'))
    depends_on('py-azure-mgmt-network@11.0.0:11.0', type=('build', 'run'))
    depends_on('py-azure-mgmt-policyinsights@0.5.0:0.5', type=('build', 'run'))
    depends_on('py-azure-mgmt-privatedns@0.1.0:0.1', type=('build', 'run'))
    depends_on('py-azure-mgmt-rdbms@2.2.0:2.2', type=('build', 'run'))
    depends_on('py-azure-mgmt-recoveryservices@0.4.0:0.4', type=('build', 'run'))
    depends_on('py-azure-mgmt-recoveryservicesbackup@0.6.0:0.6', type=('build', 'run'))
    depends_on('py-azure-mgmt-redhatopenshift@0.1.0', type=('build', 'run'))
    depends_on('py-azure-mgmt-redis@7.0.0:7.0', type=('build', 'run'))
    depends_on('py-azure-mgmt-relay@0.1.0:0.1', type=('build', 'run'))
    depends_on('py-azure-mgmt-reservations@0.6.0', type=('build', 'run'))
    depends_on('py-azure-mgmt-search@2.0:2', type=('build', 'run'))
    depends_on('py-azure-mgmt-security@0.4.1:0.4', type=('build', 'run'))
    depends_on('py-azure-mgmt-servicebus@0.6.0:0.6', type=('build', 'run'))
    depends_on('py-azure-mgmt-servicefabric@0.4.0:0.4', type=('build', 'run'))
    depends_on('py-azure-mgmt-signalr@0.4.0:0.4', type=('build', 'run'))
    depends_on('py-azure-mgmt-sql@0.19.0:0.19', type=('build', 'run'))
    depends_on('py-azure-mgmt-sqlvirtualmachine@0.5.0:0.5', type=('build', 'run'))
    depends_on('py-azure-mgmt-storage@11.1.0:11.1', type=('build', 'run'))
    depends_on('py-azure-mgmt-trafficmanager@0.51.0:0.51', type=('build', 'run'))
    depends_on('py-azure-mgmt-web@0.47.0:0.47', type=('build', 'run'))
    depends_on('py-azure-multiapi-storage@0.3.2:0.3', type=('build', 'run'))
    depends_on('py-azure-loganalytics@0.1.0:0.1', type=('build', 'run'))
    depends_on('py-azure-storage-common@1.4:1', type=('build', 'run'))
    depends_on('py-cryptography@2.3.1:2', type=('build', 'run'))
    depends_on('py-fabric@2.4:2', type=('build', 'run'))
    depends_on('py-jsmin@2.2.2:2.2', type=('build', 'run'))
    depends_on('py-pytz@2019.1', type=('build', 'run'))
    depends_on('py-scp@0.13.2:0.13', type=('build', 'run'))
    depends_on('py-sshtunnel@0.1.4:0.1', type=('build', 'run'))
    depends_on('py-urllib3@1.18:1+secure', type=('build', 'run'))
    depends_on('py-vsts-cd-manager@1.0.2:1.0', type=('build', 'run'))
    depends_on('py-websocket-client@0.56.0:0.56', type=('build', 'run'))
    depends_on('py-xmltodict@0.12:0', type=('build', 'run'))
    depends_on('py-javaproperties@0.5.1', type=('build', 'run'))
    depends_on('py-jsondiff@1.2.0', type=('build', 'run'))
