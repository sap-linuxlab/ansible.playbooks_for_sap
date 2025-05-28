# Ansible Playbook for SAP Business Suite (ECC) with IBM Db2 - Distributed Installation with High Availability

## Overview

This Ansible Playbook automates the deployment of a highly available SAP Business Suite (ECC) with IBM Db2 in a distributed environment.  

A distributed SAP system with High Availability (HA), as defined by SAP, separates the SAP NetWeaver Application Server components from the database server, placing them on distinct hosts.  

This configuration, often referred to as a Multi-Tier Architecture, is ideal for production environments, or for scenarios requiring scalability and resource separation.  

This deployment incorporates the following High Availability features:
- IBM Db2 HADR for database redundancy and failover.
- A Pacemaker cluster for SAP Central Services. 
- A load balancer for virtual IP addresses and hostnames (when `sap_vm_provision_iac_type` is not `existing_hosts`).  

### Disclaimer
This Ansible Playbook is using Ansible Roles in `experimental` state (`sap_ha_install_anydb_ibmdb2`).


## Supported Infrastructure Platforms
This Ansible Playbook supports the deployment on the following infrastructure platforms:

- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- IBM Cloud
- Microsoft Azure (MS Azure)

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
| 1 | SAP AnyDB Database Server - Primary |
| 1 | SAP AnyDB Database Server - Secondary |
| 1 | SAP NetWeaver Application Server (ABAP) - Central Services (ASCS) |
| 1 | SAP NetWeaver Application Server (ABAP) - Enqueue Replication Server (ERS) |
| 1 | SAP NetWeaver Application Server (ABAP) - Primary Application Server (PAS) |
| 1 | SAP NetWeaver Application Server (ABAP) - Additional Application Server (AAS) |


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

3. **Configure temporary Virtual IP (VIP):** The `sap_infrastructure.sap_vm_temp_vip` Ansible Role is used to configure temporary Virtual IP for duration of playbook execution.

4. **Configure Storage:** The `sap_install.sap_storage_setup` Ansible Role is used to configure the required storage.

5. **Download SAP Installation Media (Conditional):** If the `community.sap_launchpad` Ansible Collection is present on execution node, the playbook will download the necessary SAP installation media.

6. **Transfer SAP Installation Media:** Transfer the SAP installation media across hosts.

7. **Configure Operating System:** The following Ansible Roles are used to configure the operating system and update `/etc/hosts`, followed by a system reboot:
   - `sap_install.sap_general_preconfigure`
   - `sap_install.sap_netweaver_preconfigure`

8. **Configure temporary Virtual IP (VIP) after reboot:** The `sap_infrastructure.sap_vm_temp_vip` Ansible Role is used to configure temporary Virtual IP for duration of playbook execution.

### SAP NetWeaver Installation - ASCS / ERS

9. **Install SAP NetWeaver Application Server (ABAP) - Central Services (ASCS):** The `SWPM` tool is used to install the SAP application.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
   - **SAP SWPM Product ID Prefix:** `NW_ABAP_ASCS`

10. **Install SAP NetWeaver Application Server (ABAP) - Enqueue Replication Server (ERS):** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_ERS`

### SAP Database Installation

11. **Install SAP AnyDB Database Instance on Primary Host:** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_ABAP_DB`
    - Includes Database Load using Installation Export files.

12. **Perform Database Backup to file and transfer to Secondary Database Host:**

13. **Install SAP AnyDB Database Instance on Secondary Host:** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_ABAP_DB`

### High Availability Configuration

14. **Configure High Availability Pacemaker Cluster for IBM Db2 HADR:** The `sap_install.sap_ha_install_anydb_ibmdb2` Ansible Role is used for cluster configuration.

15. **Configure High Availability Pacemaker Cluster for ASCS/ERS:** The `sap_install.sap_ha_pacemaker_cluster` Ansible Role is used for cluster configuration.
    - **Default configuration:** ENSA2 with Simple Mount
    - (Optional) Classic cluster without Simple Mount can be enabled by setting variable `sap_ha_pacemaker_cluster_nwas_cs_ers_simple_mount: false`
    - (Optional) ENSA1 can be enables by setting variable `sap_ha_pacemaker_cluster_nwas_cs_ensa1: true`

### SAP NetWeaver Installation - PAS / AAS

16. **Install SAP NetWeaver Application Server (ABAP) - Primary Application Server (PAS):** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_ABAP_CI`

17. **Install SAP NetWeaver Application Server (ABAP) - Additional Application Server (AAS):** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_DI`

### Post-Installation Tasks

18. **Post-Installation:** Perform post-installation steps, such as updating Load Balancer configuration after removal of temporary Virtual IP(s).


## Load Balancer Integration for Virtual IP and Virtual Hostname with SAP SWPM

When a load balancer is used to provide the Virtual IP (VIP) and Virtual Hostname for SAP systems, the standard installation sequence for Linux Pacemaker and SAP SWPM must be adjusted. This is due to the way SAP SWPM interacts with virtualized network resources.

**Standard Installation Sequence (without Load Balancer):**

1.  Execute SAP SWPM.
2.  Install and configure Linux Pacemaker for SAP NetWeaver.

**Modified Installation Sequence (with Load Balancer):**

1.  Create the load balancer and configure the VIP. Initially, the health check probe will target a port without a listening service.
2.  Install and configure Linux Pacemaker for SAP NetWeaver. After a short delay, the load balancer should detect the listening service and mark the network path/host pool as healthy, making the VIP available.
3.  Execute SAP SWPM.

**Challenges with the Modified Sequence:**

The modified sequence is non-standard for SAP SWPM installations. It can lead to errors if the VIP is not available or the Virtual Hostname cannot be resolved during the SAP SWPM execution. This often requires manual intervention with precise timing or the use of `sleep` commands to ensure the VIP is ready.

**Ansible Playbook Solution:**

To address these challenges and maintain a consistent installation sequence, this Ansible Playbook implements the following approach:

1.  **Temporary Port Listener:** The load balancer and VIP are created, and the health check probe is configured to use a temporary port listener (using `netcat`). This ensures the load balancer immediately marks the network path/host pool as healthy, making the VIP available.
2.  **Secondary IP:** If required, a secondary IP address is appended to the default OS network interface.
3.  **SAP SWPM Execution:** SAP SWPM is executed.
4.  **Pacemaker Installation:** Linux Pacemaker is installed and configured for SAP NetWeaver. Pacemaker will detect the secondary IP address on the default OS network interface and take over its management.
5.  **Load Balancer Update:** The load balancer is updated to use the correct health check probe port configured by Linux Pacemaker.

**Note:** This load balancer handling is specific to SAP NetWeaver and is not required for SAP AnyDB using IBM Db2.


## Pacemaker Cluster Details
### IBM Db2 HADR
The `sap_install.sap_ha_install_anydb_ibmdb2` Ansible Role (currently in an `experimental` state, as noted in the Disclaimer) is used to configure a Pacemaker cluster for managing the IBM Db2 High Availability Disaster Recovery (HADR) environment.
This cluster typically provides:
- Automated failover of the Db2 database from the primary to the standby host.
- Management of a virtual IP address that always points to the active primary database server.
- STONITH/Fencing mechanisms to ensure data integrity during failover scenarios.

The specific Pacemaker resources, their names, and configuration details are determined by the `sap_install.sap_ha_install_anydb_ibmdb2` role. For precise information on the cluster configuration implemented by this role, please refer to its documentation or examine the cluster status after deployment (e.g., using `crm_mon -1r` on a cluster node).


### SAP ASCS/ERS
**Default:** Enqueue Replication 2 High Availability Cluster With Simple Mount.  
This is the recommended setup for modern SAP systems, where the ERS instance can utilize a shared `/sapmnt` and does not require its own dedicated clustered file system for `/usr/sap/<SAPSID>/ERS<instance>`.  

Example of the cluster configuration for SUSE on AWS (`crm status`):
```console
```

**Additional Cluster Types / Configurations:**
The default ASCS/ERS cluster can be customized using variables in your `ansible_extravars.yml` file:
- **Classic ENSA2 (without Simple Mount):**  
  This configuration uses ENSA2 but manages the ASCS and ERS file systems (`/usr/sap/<SAPSID>/ASCS<instance>` and `/usr/sap/<SAPSID>/ERS<instance>`) as separate clustered resources.  
  To enable this:
    - Set the variable `sap_ha_pacemaker_cluster_nwas_cs_ers_simple_mount: false`.
    - Ensure the `sap_storage_setup_host_type` variable is configured to define separate storage for the ASCS and ERS hosts respectively.
        - For the ASCS host (often grouped as `nwas_ascs`): `sap_storage_setup_host_type: ['nwas_abap_ascs']`
        - For the ERS host (often grouped as `nwas_ers`): `sap_storage_setup_host_type: ['nwas_abap_ers']`
- **Classic ENSA1:**  
  This configuration uses the older Enqueue Replication Server 1 (ENSA1) architecture.  
  To enable this:
    - Set the variable `sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1: true`.
    - Ensure the `sap_storage_setup_host_type` variable is configured to define separate storage for the ASCS and ERS hosts respectively.
        - For the ASCS host (often grouped as `nwas_ascs`): `sap_storage_setup_host_type: ['nwas_abap_ascs']`
        - For the ERS host (often grouped as `nwas_ers`): `sap_storage_setup_host_type: ['nwas_abap_ers']`
