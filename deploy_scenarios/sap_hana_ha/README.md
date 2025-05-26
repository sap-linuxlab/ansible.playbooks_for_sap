# Ansible Playbook for SAP HANA Scale-Up Database with High Availability

## Overview

This Ansible Playbook automates the deployment of a highly available SAP HANA Scale-Up Database in a distributed environment.  

A highly available SAP HANA Scale-Up system, as defined by SAP, consists of a primary SAP HANA database server and a secondary SAP HANA database server configured for System Replication, running on separate hosts.  

This configuration provides high availability through SAP HANA System Replication and is ideal for production environments or scenarios requiring database-level redundancy and failover.


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
- SAP HANA 2.0 SPS07
- SAP HANA 2.0 SPS06

Additional versions can be supported by adding new entries to the `sap_software_install_dictionary` variable in the extravars file.


## System Architecture
Upon successful execution, this Ansible Playbook will provision the following host(s) (unless an Ansible Inventory is provided for existing host(s)):
| Count | Component(s) |
| --- | --- |
| 1 | SAP HANA Database Server - Primary |
| 1 | SAP HANA Database Server - Secondary |


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
   - `sap_install.sap_hana_preconfigure`

### SAP Database Installation on both database hosts in parallel

6. **Install SAP HANA Database:** The `hdblcm` tool is used to install the SAP HANA Database.
   - **Detect Installation Media:** The `sap_install.sap_install_media_detect` Ansible Role is used to detect the provided SAP installation media.
   - **Install Database:** The `sap_install.sap_hana_install` Ansible Role is used to install the database.

### High Availability Configuration

7. **Configure SAP HANA System Replication (HSR):** The `sap_install.sap_ha_install_hana_hsr` Ansible Role is used to configure replication.

8. **Configure High Availability Pacemaker Cluster for SAP HANA Scale-Up:** The `sap_install.sap_ha_pacemaker_cluster` Ansible Role is used for cluster configuration.

### Post-Installation Tasks

9. **Post-Installation:** Perform post-installation steps, such as updating Load Balancer configuration after removal of temporary Virtual IP(s).


## Pacemaker Cluster Details
### SAP HANA Scale-Up
**Default:** SAP HANA System Replication Scale-Up - Performance Optimized Scenario with `SAPHanaSR-angi`.  

Example of the cluster configuration for SUSE on AWS (`crm status`):
```console
Node List:
  * Online: [ h02hana0 h02hana1 ]

Full List of Resources:
  * rsc_fence_aws       (stonith:external/ec2):  Started h02hana0
  * rsc_vip_H02_HDB90_primary   (ocf::heartbeat:aws-vpc-move-ip):        Started h02hana0
  * Clone Set: cln_SAPHanaTop_H02_HDB90 [rsc_SAPHanaTop_H02_HDB90]:
    * Started: [ h02hana0 h02hana1 ]
  * Clone Set: mst_SAPHanaCon_H02_HDB90 [rsc_SAPHanaCon_H02_HDB90] (promotable):
    * Masters: [ h02hana0 ]
    * Slaves: [ h02hana1 ]
  * Clone Set: cln_SAPHanaFil_H02_HDB90 [rsc_SAPHanaFil_H02_HDB90]:
    * Started: [ h02hana0 h02hana1 ]
```

Additional types:
- **Classic Scale-Up without `SAPHanaSR-angi`:**  
  To enable this:
    - Set the variable `sap_ha_pacemaker_cluster_saphanasr_angi_detection: false`.
