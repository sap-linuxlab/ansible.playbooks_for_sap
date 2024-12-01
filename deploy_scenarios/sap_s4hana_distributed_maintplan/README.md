# Ansible Playbook - SAP S/4HANA Distributed installation (no HA), using SAP Maintenance Planner

This Ansible Playbook can be executed with:
- Ansible to provision hosts
- Ansible + Terraform to provision hosts
- Existing hosts

This Ansible Playbook can be targeted at the following Infrastructure Platforms:
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- IBM Cloud
- IBM Cloud, IBM Power Virtual Servers
- Microsoft Azure (MS Azure)
- IBM PowerVM
- OVirt
- VMware

SAP S/4HANA installation:
- Distributed System definition by SAP: every SAP HANA and SAP NetWeaver instance run on a separate host.
- System Topology/Architecture: a Distributed System is commonly referred as Multi-Tier Architecture.

SAP S/4HANA software versions:
2023, 2022, 2021

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../../docs/README.md) for the capabilities and different execution methods.

## Execution outcome

When executing this Ansible Playbook for SAP, the following hosts are provisioned (unless an Ansible Inventory is provided for existing hosts):
1. Host for SAP HANA Database Server
2. Host for SAP NetWeaver Application Server (ABAP) - Central Services (ASCS)
3. Host for SAP NetWeaver Application Server (ABAP) - Primary Application Server (PAS)
4. Host for SAP NetWeaver Application Server (ABAP) - Additional Application Server (AAS)

The sequence of a Distributed installation is:
- `hdblcm`: Install SAP HANA database server
- `SWPM`: Install SAP NetWeaver Application Server (ABAP) - Central Services (ASCS). This runs the MS and EN.
- `SWPM`: Install Installation Export to Database (i.e. Database Load)
- `SWPM`: Install SAP NetWeaver Application Server (ABAP) - Primary Application Server (PAS); formerly Central Instance (CI). This runs the GW and WP.
- `SWPM`: Install SAP NetWeaver Application Server (ABAP) - Additional Application Server (AAS); formerly Dialog Instance (DI). This runs additional WP.

This therefore matches to the SAP SWPM Product ID prefixes that are executed in sequence:
- `NW_ABAP_ASCS`, Central Services Instance for ABAP (ASCS) Installation
- `NW_ABAP_DB`, Database Instance Installation
- `NW_ABAP_CI`, Primary Application Server Instance Installation
- `NW_DI`, Application Server Instance Installation
