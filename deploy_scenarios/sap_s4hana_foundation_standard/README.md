# Ansible Playbook - SAP S/4HANA Foundation (for SAP HANA-only Add-Ons and Custom Apps) Standard installation

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
- KubeVirt
- OVirt
- VMware

SAP S/4HANA Foundation (for SAP HANA-only Add-Ons and Custom Apps) installation:
- Standard System definition by SAP: all main SAP NetWeaver instances (except the SAP HANA database instance) run on a single host.
- System Topology/Architecture: a Standard System is commonly referred as Three-Tier Architecture, may also be known as DualHost.
- `NOTE:` SAP S/4HANA Foundation only includes SAP ABAP Platform [re-named after SAP NetWeaver AS (ABAP) 7.55 release]. It is not intended to be used as Standalone for custom ABAP development with the new ABA Layer (replaces 'Classic ABA' Layer). For full list of compatible and supported Add-Ons with SAP S/4HANA Foundation (**not including ADS or ESR**), please see [Please see SAP Note 3143630 - SAP S/4HANA FOUNDATION 2022: Release Information](https://me.sap.com/notes/3143630).

SAP S/4HANA software versions:
2023, 2022, 2021

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../../docs/README.md) for the capabilities and different execution methods.

## Execution outcome

When executing this Ansible Playbook for SAP, the following hosts are provisioned (unless an Ansible Inventory is provided for existing hosts):
1. Host for SAP HANA Database Server
2. Host for SAP ABAP Platform (formerly SAP NetWeaver AS [ABAP]) - Central Services (ASCS) and Primary Application Server (PAS)

The sequence of a Standard System installation is:
- `hdblcm`: Install SAP HANA database server
- `SWPM`: Install SAP ABAP Platform (formerly SAP NetWeaver AS [ABAP]) and Installation Export to Database (i.e. Database Load)

This therefore matches to the SAP SWPM Product ID prefixes that are executed in sequence:
- `NW_ABAP_OneHost`, Central Services, Database Instance Installation, Primary Application Server
