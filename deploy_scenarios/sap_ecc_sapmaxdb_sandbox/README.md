# Ansible Playbook for SAP Business Suite with SAP MaxDB - Sandbox Installation

## Overview

This Ansible Playbook automates the deployment an SAP Business Suite (ECC) with SAP MaxDB in a single-host environment.  

A single-host system, as defined by SAP, consolidates all SAP Database and SAP NetWeaver instances onto a single host.  

This configuration, often referred to as a Two-Tier Architecture, OneHost, or Central System, is ideal for development, testing, and demonstration purposes.  


## Supported Infrastructure Platforms
This Ansible Playbook supports the deployment on the following infrastructure platforms:

- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- IBM Cloud
- Microsoft Azure (MS Azure)
- OVirt
- VMware

### Considerations for ppc64le
This Ansible Playbook is not available for IBM Power Little Endian (ppc64le).
- All prior SAP Software without SAP HANA was for IBM Power Big Endian (ppc64) only.


## Supported SAP Software
This playbook includes support for the following software versions:
- EHP8 for SAP ERP 6.0

Additional versions can be supported by adding new entries to the `sap_software_install_dictionary` variable in the extravars file.


## System Architecture
Upon successful execution, this Ansible Playbook will provision the following host(s) (unless an Ansible Inventory is provided for existing host(s)):
| Count | Component(s) |
| --- | --- |
| 1 | SAP AnyDB Database Server<br> SAP NetWeaver Application Server (ABAP) - Central Services (ASCS)<br> SAP NetWeaver Application Server (ABAP) - Primary Application Server (PAS) |


## Playbook Execution
Before running the playbook, please read the main [README](https://github.com/sap-linuxlab/ansible.playbooks_for_sap/blob/main/README.md) for detailed instructions, prerequisites, and best practices.

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
This method allows you to provide input during the execution of the playbook.

1.  **Prepare the `optional/ansible_extravars_interactive.yml` file:** This file contains the essential set of variables for initiating Interactive Prompts.
2.  **Execute the playbook:** Run the following command.

```bash
ansible-playbook ansible_playbook.yml \
 --extra-vars "@./optional/ansible_extravars_interactive.yml"
```


## Deployment Process
The playbook executes the following sequence of tasks:

### Pre-Installation Tasks

1. **Collect User Inputs (Conditional):** If the `ansible_extravars_interactive.yml` file is used, the playbook will prompt for user input to gather necessary configuration details.

2. **Provision Infrastructure (Conditional):** If the `sap_vm_provision_iac_type` variable is not set to `existing_hosts`, the playbook will provision the necessary infrastructure.

3. **Configure Storage:** The `sap_install.sap_storage_setup` Ansible Role is used to configure the required storage.

4. **Download SAP Installation Media (Conditional):** If the `community.sap_launchpad` Ansible Collection is present on execution node, the playbook will download the necessary SAP installation media.

5. **Configure Operating System:** The following Ansible Roles are used to configure the operating system and update `/etc/hosts`, followed by a system reboot:
   - `sap_install.sap_general_preconfigure`
   - `sap_install.sap_netweaver_preconfigure`

### SAP Business Suite (ECC) with SAP MaxDB Installation

6. **Install SAP Business Suite (ECC):** The `SWPM` tool is used to install the SAP application.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
   - **SAP SWPM Product ID Prefix:** `NW_ABAP_OneHost`
   - AnyDB Database is installed together with SAP NetWeaver.
   - Includes Database Load using Installation Export files.
