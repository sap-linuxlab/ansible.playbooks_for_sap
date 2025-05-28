# Ansible Playbook for SAP S/4HANA - Distributed Installation with High Availability and SAP Maintenance Planner

## Overview

This Ansible Playbook automates the deployment of a highly available SAP S/4HANA in a distributed environment.  

A distributed SAP system with High Availability (HA), as defined by SAP, separates the SAP ABAP Platform components from the database server, placing them on distinct hosts.  

This configuration, often referred to as a Multi-Tier Architecture, is ideal for production environments, or for scenarios requiring scalability and resource separation.  

This deployment incorporates the following High Availability features:
- SAP HANA System Replication for database redundancy and failover.
- A Pacemaker cluster for SAP HANA Database. 
- A Pacemaker cluster for SAP Central Services. 
- A load balancer for virtual IP addresses and hostnames (when `sap_vm_provision_iac_type` is not `existing_hosts`).  

**NOTE:** A key distinction of this playbook is its use of the SAP Maintenance Planner to download SAP Installation Media, instead of a file list, as used in the `sap_s4hana_distributed_ha` scenario.  


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
| Count | Component(s) |
| --- | --- |
| 1 | SAP HANA Database Server - Primary |
| 1 | SAP HANA Database Server - Secondary |
| 1 | SAP ABAP Platform - Central Services (ASCS) |
| 1 | SAP ABAP Platform - Enqueue Replication Server (ERS) |
| 1 | SAP ABAP Platform - Primary Application Server (PAS) |
| 1 | SAP ABAP Platform - Additional Application Server (AAS) |


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
   - `sap_install.sap_hana_preconfigure`
   - `sap_install.sap_netweaver_preconfigure`

8. **Configure temporary Virtual IP (VIP) after reboot:** The `sap_infrastructure.sap_vm_temp_vip` Ansible Role is used to configure temporary Virtual IP for duration of playbook execution.

### SAP Database Installation on both database hosts in parallel

9. **Install SAP HANA Database:** The `hdblcm` tool is used to install the SAP HANA Database.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Database:** The `sap_install.sap_hana_install` Ansible Role is used to install the database.

### High Availability Configuration - SAP HANA Cluster

10. **Configure SAP HANA System Replication (HSR):** The `sap_install.sap_ha_install_hana_hsr` Ansible Role is used to configure replication.

11. **Configure High Availability Pacemaker Cluster for SAP HANA Scale-Up:** The `sap_install.sap_ha_pacemaker_cluster` Ansible Role is used for cluster configuration.

### SAP NetWeaver Installation - ASCS / ERS

12. **Install SAP ABAP Platform - Central Services (ASCS):** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_ABAP_ASCS`

13. **Install SAP ABAP Platform - Enqueue Replication Server (ERS):** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_ERS`

### High Availability Configuration - ASCS / ERS Cluster

14. **Configure High Availability Pacemaker Cluster for ASCS/ERS:** The `sap_install.sap_ha_pacemaker_cluster` Ansible Role is used for cluster configuration.
    - **Default configuration:** ENSA2 with Simple Mount
    - (Optional) Classic cluster without Simple Mount can be enabled by setting variable `sap_ha_pacemaker_cluster_nwas_cs_ers_simple_mount: false`
    - (Optional) ENSA1 can be enables by setting variable `sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1: true`

### SAP NetWeaver Installation - PAS / AAS

15. **Database Load from Primary Application Server (PAS):** The `SWPM` tool is used to execute Database Load using Installation Export files.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to execute Database Load using Installation Export files.
    - **SAP SWPM Product ID Prefix:** `NW_ABAP_DB`

16. **Install SAP ABAP Platform - Primary Application Server (PAS):** The `SWPM` tool is used to install the SAP application.
    - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
    - **Install Application:** The `sap_install.sap_swpm` Ansible Role is used to install the application.
    - **SAP SWPM Product ID Prefix:** `NW_ABAP_CI`

17. **Install SAP ABAP Platform - Additional Application Server (AAS):** The `SWPM` tool is used to install the SAP application.
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

**Note:** The additional handling for Load Balancer VIPs is irrelevant for SAP HANA (hdblcm) installation procedures.


## Pacemaker Cluster Details
### SAP HANA Scale-Up
**Default:** SAP HANA System Replication Scale-Up - Performance Optimized Scenario with `SAPHanaSR-angi`.  

Example of the cluster configuration for SUSE on AWS (`crm status`):
```console
Node List:
  * Online: [ s02hana0 s02hana1 ]

Full List of Resources:
  * rsc_fence_aws       (stonith:external/ec2):  Started s02hana0
  * rsc_vip_H02_HDB90_primary   (ocf::heartbeat:aws-vpc-move-ip):        Started s02hana0
  * Clone Set: cln_SAPHanaTop_H02_HDB90 [rsc_SAPHanaTop_H02_HDB90]:
    * Started: [ s02hana0 s02hana1 ]
  * Clone Set: mst_SAPHanaCon_H02_HDB90 [rsc_SAPHanaCon_H02_HDB90] (promotable):
    * Masters: [ s02hana0 ]
    * Slaves: [ s02hana1 ]
  * Clone Set: cln_SAPHanaFil_H02_HDB90 [rsc_SAPHanaFil_H02_HDB90]:
    * Started: [ s02hana0 s02hana1 ]
```

Additional types:
- **Classic Scale-Up without `SAPHanaSR-angi`:**  
  To enable this:
    - Set the variable `sap_ha_pacemaker_cluster_saphanasr_angi_detection: false`.

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
