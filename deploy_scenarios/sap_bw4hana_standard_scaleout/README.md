# Ansible Playbook for SAP BW/4HANA (Scale-Out) - Standard Installation

## Overview

This Ansible Playbook automates the deployment of an SAP BW/4HANA Standard (Scale-Out) system in a distributed environment.  

An SAP BW/4HANA Standard (Scale-Out) system, as defined by SAP, consists of an SAP ABAP Platform instances running on a dedicated host, and an SAP HANA database server running as a scale-out cluster across multiple hosts.  

This configuration, often referred to as a Three-Tier Architecture or DualHost, is ideal for production environments, or for scenarios requiring high availability and scalability.


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
- SAP BW/4HANA 2023
- SAP BW/4HANA 2021

Additional versions can be supported by adding new entries to the `sap_software_install_dictionary` variable in the extravars file.


## System Architecture
Upon successful execution, this Ansible Playbook will provision the following host(s) (unless an Ansible Inventory is provided for existing host(s)):
| Count | Component(s) |
| --- | --- |
| 1 | SAP HANA Database Server - Coordinator node |
| 2 | SAP HANA Database Server - Worker node |
| 1 | SAP HANA Database Server - Standby node |
| 1 | SAP ABAP Platform - Central Services (ASCS)<br> SAP ABAP Platform - Primary Application Server (PAS) | 


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

2. **Prepare Scale-Out Host Names:** The following scale-out variables are used to generate host names for the scale-out nodes:
   - `sap_vm_provision_calculate_sap_hana_scaleout_active_coordinator`
   - `sap_vm_provision_calculate_sap_hana_scaleout_active_worker`
   - `sap_vm_provision_calculate_sap_hana_scaleout_standby`

3. **Provision Infrastructure (Conditional):** If the `sap_vm_provision_iac_type` variable is not set to `existing_hosts`, the playbook will provision the necessary infrastructure.

4. **Configure Storage:** The `sap_install.sap_storage_setup` Ansible Role is used to configure the required storage.

5. **Download SAP Installation Media (Conditional):** If the `community.sap_launchpad` Ansible Collection is present on execution node, the playbook will download the necessary SAP installation media.

6. **Transfer SAP Installation Media:** Transfer the SAP installation media across hosts.

7. **Configure Operating System:** The following Ansible Roles are used to configure the operating system and update `/etc/hosts`, followed by a system reboot:
   - `sap_install.sap_general_preconfigure`
   - `sap_install.sap_hana_preconfigure`
   - `sap_install.sap_netweaver_preconfigure`

### SAP Database Installation

8. **Install SAP HANA Database:** The `hdblcm` tool is used to install the SAP HANA Database.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Database:** The `sap_install.sap_hana_install` Ansible Role is used to install the database.

### SAP BW/4HANA Installation 

9. **Install SAP BW/4HANA:** The `SWPM` tool is used to install the SAP application.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
   - **SAP SWPM Product ID Prefix:** `NW_ABAP_OneHost`
   - Includes Database Load using Installation Export files.


## Known errors

### SAP HANA Scale-Out Worker Group name

SAP HANA Scale-Out Worker Group name must be left as 'default' before SAP BW/4HANA installation.

SAP HANA `hdblcm` allows this to change, which is correctly reflected in `/hana/shared/H01/global/hdb/custom/config/nameserver.ini` and correctly reflected in runtime as shown by `hdbsql` SQL Query to System View (i.e. `SELECT * FROM SYS.M_LANDSCAPE_HOST_CONFIGURATION`).

However, an error occurs when SAP SWPM attempts to perform restore of the SAP BW/4HANA Export (occurs with or without standby node).

For further detail, see [SAP Note 3043860 - Recovery fails due to incorrect worker group assignment](https://me.sap.com/notes/3043860).

**Example hdblcm command parameters:**
```shell
--workergroup=workergroups_01
--addhosts=hdb-node1:role=worker:workergroup=workergroups_01:group=default,hdb-node2:role=worker:workergroup=workergroups_01:group=default,hdb-node3:role=standby:workergroup=default:group=default
```

**Example nameserver.ini output:**
```ini
[landscape]
...
roles_hdb-node0 = worker
roles_hdb-node1 = worker
roles_hdb-node2 = worker
roles_hdb-node3 = standby

workergroups_hdb-node0 = workergroups_01
workergroups_hdb-node1 = workergroups_01
workergroups_hdb-node2 = workergroups_01
workergroups_hdb-node3 = workergroups_01

failovergroup_hdb-node0 = default
failovergroup_hdb-node1 = default
failovergroup_hdb-node2 = default
failovergroup_hdb-node3 = default
```

**Example SAP SWPM output:**
```shell
SAP SWPM step perform_database_recovery_tenant error:
HdbCmdClazz 'START_DATABASE_RECOVERY_TENANT'
    Progress: indexserver[initialization (failed)
        SAP DBTech JDBC:
        [448]: recovery could not be completed:
            [111204] Recovery failed during topology update:
                Unable to update catalog master - worker groups of indexserver with volume 3 do not match the worker groups of existing host "hdb-node0":
                    default != workergroups_01
```


### SAP HANA Scale-Out Failover Group name

SAP HANA Scale-Out Worker Group name must be left as 'default' before SAP BW/4HANA installation.

SAP HANA `hdblcm` does not allow this to change or is a bug, the 'group' parameter in documentation does not appear in the config file dump and manually appending the 'group' parameter does not alter the Failover Group of the coordinator node - which means all nodes in the 'addhosts' parameter would have a different Failover Group name.

This is visible in `/hana/shared/H01/global/hdb/custom/config/nameserver.ini` which shows the SAP HANA Scale-Out Coordinator node has a different Failover Group name to all other nodes. It is also visible by `hdbsql` SQL Query to System View (i.e. `SELECT * FROM SYS.M_LANDSCAPE_HOST_CONFIGURATION`).

**Example hdblcm command parameters:**
```shell
--workergroup=default
--addhosts=hdb-node1:role=worker:workergroup=default:group=failovergroup_01,hdb-node2:role=worker:workergroup=default:group=failovergroup_01,hdb-node3:role=standby:workergroup=default:group=failovergroup_01
```

**Example nameserver.ini output:**
```ini
[landscape]
...
roles_hdb-node0 = worker
roles_hdb-node1 = worker
roles_hdb-node2 = worker
roles_hdb-node3 = standby

workergroups_hdb-node0 = default
workergroups_hdb-node1 = default
workergroups_hdb-node2 = default
workergroups_hdb-node3 = default

failovergroup_hdb-node0 = default
failovergroup_hdb-node1 = failovergroup_01
failovergroup_hdb-node2 = failovergroup_01
failovergroup_hdb-node3 = failovergroup_01
```
