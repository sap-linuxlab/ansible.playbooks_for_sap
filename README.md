# Ansible Playbooks for SAP

Use Ansible to deploy various SAP Software solution scenarios onto different Hyperscaler Cloud Service Providers and Hypervisors platforms.

These Ansible Playbooks for SAP are designed to be:
- simple to understand,
- highly reconfigurable and extendable,
- self-enclosed for a specific scenario,
- result in an equal installation performed to any Infrastructure Platform (Hyperscaler Cloud Service Providers and Hypervisor platforms),
- use either Ansible or Terraform to provision Infrastructure,
- use Ansible for configuration of OS and installation of SAP Software,
- and `licensed for corporate usage` by SAP Customers, SAP Service Partners and SAP Technology Partners

> <sub>Note: Ansible Playbooks for SAP optionally use Ansible > Terraform. To instead use Terraform > Ansible, see [Terraform Templates for SAP](https://github.com/sap-linuxlab/terraform.templates_for_sap)</sub>

**Please read the [full documentation](/docs#readme) for how-to guidance, requirements, and all other details. Summary documentation is below:**
- [Ansible Playbooks for SAP - execution workflow summary diagram](#ansible-playbooks-for-sap---execution-workflow-summary-diagram)
- [Ansible Playbooks for SAP - available scenarios summary](#ansible-playbooks-for-sap---available-scenarios-summary)
- [Ansible Playbooks for SAP - deployments choice summary](#ansible-playbooks-for-sap---deployments-choice-summary)
- [Disclaimer](#disclaimer)

---

## Ansible Playbooks for SAP - execution workflow summary diagram

![Ansible Playbooks for SAP execution flow](./docs/images/ansible_playbooks_sap_summary.svg)

---

## Ansible Playbooks for SAP - available scenarios summary

**Ansible Playbooks are available for Operating Systems:**
- SUSE Linux Enterprise Server for SAP (SLES4SAP)
- Red Hat Enterprise Linux for SAP (RHEL4SAP)

**Ansible Playbooks are available for Infrastructure Platforms:**
- AWS EC2 Virtual Server instances
- Google Cloud Compute Engine Virtual Machines
- IBM Cloud, Intel Virtual Servers
- IBM Cloud, Power Virtual Servers
- Microsoft Azure Virtual Machines
- IBM PowerVM Virtual Machines (LPARs)
- OVirt (e.g. Red Hat Enterprise Linux KVM)
- KubeVirt (e.g. Red Hat OpenShift Virtualization, SUSE Rancher with Harvester HCI) `[Experimental]`
- VMware vSphere Virtual Machines `[Beta]`

**Ansible Playbooks are available for SAP Software Solution Scenarios:**

- SAP HANA (2.0 SPSx)
    - Standard (Scale-Up)
    - High Availability (performance optimized)
    - Scale-Out
- SAP S/4HANA (2023, 2022, 2021, 2020, 1909)
    - Sandbox
    - Sandbox via Maintenance Planner
    - Standard
    - Standard via Maintenance Planner
    - Distributed
    - Distributed via Maintenance Planner
    - Distributed High Availability
    - Distributed High Availability via Maintenance Planner
- SAP Landscape for SAP S/4HANA (2023, 2022, 2021, 2020, 1909)
    - 3-System Standard
    - 3-System Standard via Maintenance Planner
- SAP S/4HANA Foundation (2023, 2022, 2021), for SAP HANA-only Add-Ons and Custom Apps
    - Sandbox
    - Standard
- SAP ECC on HANA (EhP8, EhP7)
    - Sandbox
- SAP ECC (EhP8)
    - with IBM Db2, Sandbox
    - with IBM Db2, Distributed
    - with Oracle DB, Sandbox
    - with SAP ASE, Sandbox
    - with SAP MaxDB, Sandbox
- SAP BW/4HANA (2023, 2021)
    - Sandbox
    - Standard (Scale-Out)
- SAP IDES for ECC on HANA (EhP8)
    - Sandbox
- SAP IDES for ECC (EhP8, EhP7)
    - with IBM Db2, Sandbox
- SAP NetWeaver (ABAP)
    - with SAP HANA, Sandbox
    - with IBM Db2, Sandbox
    - with Oracle DB, Sandbox
    - with SAP ASE, Sandbox
    - with SAP MaxDB, Sandbox
- SAP NetWeaver (JAVA)
    - with IBM Db2, Sandbox
    - with SAP ASE, Sandbox
- SAP SolMan (ABAP/JAVA)
    - with SAP HANA, Sandbox
    - with SAP ASE, Sandbox


**Ansible Playbooks available with Special Actions for SAP Software:**

- SAP Web Dispatcher, Standalone (with SAP Kernel Part II for SAP HANA)
- SAP SolMan Diagnostics Agent (SDA) `[Experimental]`
- Download SAP Software installation media
- System Copy Export, IBM Db2 `[Experimental]`
- System Copy Restore (SAP ECC on HANA or SAP S/4HANA), Sandbox  `[Experimental]`

---

## Ansible Playbooks for SAP - deployments choice summary

> **Get Started:** See full documentation section [Example execution of Ansible Playbooks for SAP](/docs##example-execution-of-ansible-playbooks-for-sap)

Below is a summary of the execution method and deployment options:

| Execution Method | Ansible with existing host/s | Ansible provisions host/s | Ansible uses Terraform to provision minimal landing zone and host/s<br/>`[Beta]` |
| --- | --- | --- | --- |
| Interactive variable prompts<br/>`[Coming Soon]` | Not Available | Enter `ansible` <br/>when prompted to<br/>`Please choose Infrastructure-as-Code automation from list` | Enter `ansible_to_terraform` <br/>when prompted to<br/>`Please choose Infrastructure-as-Code automation from list` |
| Standard (non-interactive) | In Extra Vars file, set <br/><sub>`sap_vm_provision_iac_type: existing_hosts`</sub> | In Extra Vars file, set <br/><sub>`sap_vm_provision_iac_type: ansible`</sub> | In Extra Vars file, set <br/><sub>`sap_vm_provision_iac_type: ansible_to_terraform`</sub> |
| | | |
| | **Summary:**</br>SAP installation :white_check_mark:<br/>Provisions hosts :x:<br/>Infrastructure setup :x:<br/> | **Summary:**</br>SAP installation :white_check_mark:<br/>Provisions hosts :white_check_mark:<br/>Infrastructure setup :x:<br/> | **Summary:**</br>SAP installation :white_check_mark:<br/>Provisions hosts :white_check_mark:<br/>Infrastructure setup :white_check_mark:<br/> |
| | **Intended usage:**<br/>SAP installation to existing host/s, using an existing setup on an Infrastructure Platform.<br/><br/>Target hosts are defined using an Ansible Inventory file.<br/><br/><br/> | **Intended usage:**<br/>SAP installation to host/s provisioned by Ansible, using an existing setup on an Infrastructure Platform.<br/><br/>Target hosts are defined using a dynamically generated Ansible Inventory created during runtime (after hosts are provisioned). | **Intended usage:**<br/>SAP installation to host/s provisioned by executing Terraform to create a minimal setup on an Infrastructure Platform.<br/><br/>Target hosts are defined using a dynamically generated Ansible Inventory created during runtime (after hosts are provisioned). |

---

## Disclaimer

These are common SAP Software Solution Scenarios which are codified using Ansible to provide for Infrastructure-as-Code (IaC) Automation for SAP and Configuration-as-Code (CaC) Automation for SAP. These can be extended as needed for bespoke requirements.

This does not intend (and can not) replicate every SAP software deployment scenario, and does not replace any existing SAP installation procedures detailed in the [SAP Help Portal](https://help.sap.com) or [SAP Notes on SAP ONE Support](https://launchpad.support.sap.com). However, with the Ansible Role for SAP SWPM it is possible to install any SAP Software which is supported by SAP Software Provisioning Manager (SWPM 1.0/2.0).

For move-fast activities, such as rapid provisioning and administration testing tasks (latest software releases and revision/patch levels, system copy restore to Cloud etc.), these Ansible Playbooks for SAP can be amended to suit these requirements.

For greater support in automating the lifecycle of SAP Systems themselves, it is recommended to consider [SAP Landscape Management Enterprise Edition](https://www.sap.com/uk/products/landscape-management.html).

For greater demo and evaluation of SAP Software business functionality, it is recommended to consider [SAP Cloud Appliance Library](https://www.sap.com/products/cloud-appliance-library.html).

---

## License

- [Apache 2.0](./LICENSE)

## Contributors

Key contributors are shown within the [contributors](./docs/CONTRIBUTORS.md) file.
