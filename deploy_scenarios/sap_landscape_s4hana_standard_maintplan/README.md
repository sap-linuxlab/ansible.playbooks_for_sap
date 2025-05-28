# Ansible Playbook for SAP Landscape Single Track 3-System for SAP S/4HANA - Standard installation with SAP Maintenance Planner

## Overview

This Ansible Playbook automates the deployment of a pre-defined SAP S/4HANA Single Track 3-System Landscape with a Standard installation.  

This landscape is comprised of three distinct systems: Development, Test, and Production.  
Each system is deployed on two dedicated hosts, one for the SAP HANA database server and one for the SAP ABAP Platform, which includes both the Central Services (ASCS) and the Primary Application Server (PAS).  

This Single Track 3-System Landscape, as defined by SAP, is a standard configuration that provides a clear separation between the Development, Test, and Production environments.  
Each system has its own dedicated pair of hosts, ensuring complete isolation and resource independence. This configuration is commonly referred to as a Three-Tier Architecture, and each system can also be known as DualHost.  

**NOTE:** A key distinction of this playbook is its use of the SAP Maintenance Planner to download SAP Installation Media, instead of a file list, as used in the `sap_landscape_s4hana_standard` scenario.  


## Supported Infrastructure Platforms
This Ansible Playbook supports the deployment on the following infrastructure platforms:

- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- IBM Cloud
- IBM Cloud, IBM Power Virtual Servers
- Microsoft Azure (MS Azure)
- IBM PowerVM
- OVirt
- VMware


## Supported SAP Software
This playbook includes support for the following software versions:
- SAP S/4HANA 2023
- SAP S/4HANA 2022
- SAP S/4HANA 2021

Additional versions can be supported by adding new entries to the `sap_software_install_dictionary` variable in the extravars file.


## System Architecture
Upon successful execution, this Ansible Playbook will provision the following host(s) (unless an Ansible Inventory is provided for existing host(s)):
| Count | Environment | Component(s) |
| --- | --- | --- |
| 1 | Development | SAP HANA Database Server |
| 1 | Development | SAP ABAP Platform - Central Services (ASCS)<br> SAP ABAP Platform - Primary Application Server (PAS) |
| 1 | Test | SAP HANA Database Server |
| 1 | Test | SAP ABAP Platform - Central Services (ASCS)<br> SAP ABAP Platform - Primary Application Server (PAS) |
| 1 | Production | SAP HANA Database Server |
| 1 | Production | SAP ABAP Platform - Central Services (ASCS)<br> SAP ABAP Platform - Primary Application Server (PAS) |


## Playbook Execution
Before running the playbook, please read the main [README](https://github.com/sap-linuxlab/ansible.playbooks_for_sap/blob/main/README.md) for detailed instructions, prerequisites, and best practices.

### Recommendations
It is recommended to execute this Ansible Playbook with parameter `--forks=6`, because this Ansible Playbook is provisioning 6 hosts.
Default value of `5` could impact provisioning speed.

### Provisioning and Installation
This method provisions a new host(s) and installs the SAP system.

1.  **Prepare the `ansible_extravars.yml` file:** This file contains the configuration for the SAP system.
2.  **Prepare the infrastructure-specific `ansible_extravars_*.yml` file:** This file contains the configuration for the target infrastructure.
3.  **Execute the playbook:** Run the following command.

```bash
ansible-playbook ansible_playbook.yml \
 --extra-vars "@./ansible_extravars.yml" \
 --extra-vars "@./ansible_extravars_aws_ec2_vs.yml"
```

### Installation on Existing Hosts
This method is used to install the SAP system on an existing host(s).

1.  **Prepare the `ansible_extravars.yml` file:** This file contains the configuration for the SAP system.
2.  **Prepare the `optional/ansible_extravars_existing_hosts.yml` file:** This file contains the configuration for the existing host(s).
3.  **Prepare the `optional/ansible_inventory_noninteractive.yml` file:** Ensure that your inventory file is properly configured to target the existing host.
4.  **Execute the playbook:** Run the following command.

```bash
ansible-playbook ansible_playbook.yml \
 --extra-vars "@./ansible_extravars.yml" \
 --extra-vars "@./optional/ansible_extravars_existing_hosts.yml" \
 --inventory "./optional/ansible_inventory_noninteractive.yml"
```

### Interactive Execution
This method is not supported due to complexity of this scenario.


## Deployment Process
The playbook executes the following sequence of tasks:

### Pre-Installation Tasks

1. **Provision Infrastructure (Conditional):** If the `sap_vm_provision_iac_type` variable is not set to `existing_hosts`, the playbook will provision the necessary infrastructure.

2. **Configure Storage:** The `sap_install.sap_storage_setup` Ansible Role is used to configure the required storage.

3. **Download SAP Installation Media (Conditional):** If the `community.sap_launchpad` Ansible Collection is present on execution node, the playbook will download the necessary SAP installation media.

4. **Configure Operating System:** The following Ansible Roles are used to configure the operating system and update `/etc/hosts`, followed by a system reboot:
   - `sap_install.sap_general_preconfigure`
   - `sap_install.sap_hana_preconfigure`
   - `sap_install.sap_netweaver_preconfigure`

### SAP Database Installation in parallel

5. **Install SAP HANA Database:** The `hdblcm` tool is used to install the SAP HANA Database.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Database:** The `sap_install.sap_hana_install` Ansible Role is used to install the database.

### SAP S/4HANA Installation in parallel

6. **Install SAP S/4HANA:** The `SWPM` tool is used to install the SAP application.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
   - **SAP SWPM Product ID Prefix:** `NW_ABAP_OneHost`
   - Includes Database Load using Installation Export files.
