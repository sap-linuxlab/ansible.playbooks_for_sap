# Ansible Playbook for SAP ASCS/ERS Cluster Installation

## Overview

This Ansible Playbook automates the deployment of a highly available SAP ASCS/ERS Cluster in a distributed environment.  

This deployment incorporates the following High Availability features:
- A Pacemaker cluster for SAP Central Services. 
- A load balancer for virtual IP addresses and hostnames (when `sap_vm_provision_iac_type` is not `existing_hosts`).  

### Disclaimer
**This Ansible Playbook does not install fully functional SAP System, but rather focuses on installation of SAP ASCS/ERS Cluster for testing purpose.**


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

Additional versions can be supported by adding new entries to the `sap_software_install_dictionary` variable in the extravars file.


## System Architecture
Upon successful execution, this Ansible Playbook will provision the following host(s) (unless an Ansible Inventory is provided for existing host(s)):
| Count | Component(s) |
| --- | --- |
| 1 | SAP ABAP Platform - Central Services (ASCS) |
| 1 | SAP ABAP Platform - Enqueue Replication Server (ERS) |


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


## Deployment Process
The playbook executes the following sequence of tasks:

### Pre-Installation Tasks

1. **Provision Infrastructure (Conditional):** If the `sap_vm_provision_iac_type` variable is not set to `existing_hosts`, the playbook will provision the necessary infrastructure.

2. **Configure temporary Virtual IP (VIP):** The `sap_infrastructure.sap_vm_temp_vip` Ansible Role is used to configure temporary Virtual IP for duration of playbook execution.

3. **Configure Storage:** The `sap_install.sap_storage_setup` Ansible Role is used to configure the required storage.

4. **Download SAP Installation Media (Conditional):** If the `community.sap_launchpad` Ansible Collection is present on execution node, the playbook will download the necessary SAP installation media.

5. **Transfer SAP Installation Media:** Transfer the SAP installation media across hosts.

6. **Configure Operating System:** The following Ansible Roles are used to configure the operating system and update `/etc/hosts`, followed by a system reboot:
   - `sap_install.sap_general_preconfigure`
   - `sap_install.sap_netweaver_preconfigure`

7. **Configure temporary Virtual IP (VIP) after reboot:** The `sap_infrastructure.sap_vm_temp_vip` Ansible Role is used to configure temporary Virtual IP for duration of playbook execution.

### SAP NetWeaver Installation - ASCS / ERS

8. **Install SAP ABAP Platform - Central Services (ASCS):** The `SWPM` tool is used to install the SAP application.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
   - **SAP SWPM Product ID Prefix:** `NW_ABAP_ASCS`

9. **Install SAP ABAP Platform - Enqueue Replication Server (ERS):** The `SWPM` tool is used to install the SAP application.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
   - **SAP SWPM Product ID Prefix:** `NW_ERS`

### High Availability Configuration - ASCS / ERS Cluster

10. **Configure High Availability Pacemaker Cluster for ASCS/ERS:** The `sap_install.sap_ha_pacemaker_cluster` Ansible Role is used for cluster configuration.
    - **Default configuration:** ENSA2 with Simple Mount
    - (Optional) Classic cluster without Simple Mount can be enabled by setting variable `sap_ha_pacemaker_cluster_nwas_cs_ers_simple_mount: false`
    - (Optional) ENSA1 can be enables by setting variable `sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1: true`

### Post-Installation Tasks

11. **Post-Installation:** Perform post-installation steps, such as updating Load Balancer configuration after removal of temporary Virtual IP(s).


## Pacemaker Cluster Details
### SAP ASCS/ERS
**Default:** Enqueue Replication 2 High Availability Cluster With Simple Mount.  
This is the recommended setup for modern SAP systems, where the ERS instance can utilize a shared `/sapmnt` and does not require its own dedicated clustered file system for `/usr/sap/<SAPSID>/ERS<instance>`.  

Example of the cluster configuration for SUSE on AWS (`crm status`):
```console
Node List:
  * Online: [ s02ascs s02ers ]

Full List of Resources:
  * rsc_fence_aws       (stonith:external/ec2):  Started s02ascs
  * Resource Group: grp_S02_ASCS00:
    * rsc_vip_S02_ASCS00        (ocf::heartbeat:aws-vpc-move-ip):        Started s02ascs
    * rsc_SAPStartSrv_S02_ASCS00        (ocf::suse:SAPStartSrv):         Started s02ascs
    * rsc_SAPInstance_S02_ASCS00        (ocf::heartbeat:SAPInstance):    Started s02ascs
  * Resource Group: grp_S02_ERS10:
    * rsc_vip_S02_ERS10 (ocf::heartbeat:aws-vpc-move-ip):        Started s02ers
    * rsc_SAPStartSrv_S02_ERS10 (ocf::suse:SAPStartSrv):         Started s02ers
    * rsc_SAPInstance_S02_ERS10 (ocf::heartbeat:SAPInstance):    Started s02ers
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
