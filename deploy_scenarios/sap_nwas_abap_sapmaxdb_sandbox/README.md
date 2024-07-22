# Ansible Playbook - SAP NetWeaver (ABAP) with SAP MaxDB Sandbox installation

This Ansible Playbook can be executed with:
- Ansible to provision hosts
- Ansible + Terraform to provision hosts
- Existing hosts

This Ansible Playbook can be targeted at the following Infrastructure Platforms:
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- IBM Cloud
- Microsoft Azure (MS Azure)
- OVirt
- VMware

SAP NetWeaver (ABAP) with SAP MaxDB Sandbox installation:
- Sandbox System definition by SAP: all SAP MaxDB and SAP NetWeaver instances run on a single host.
- System Topology/Architecture: a Sandbox System is commonly referred as Two-Tier Architecture, may also be known as OneHost or Central System.
- Note: This Ansible Playbook is not available for IBM Power Little Endian (ppc64le); all prior SAP Software without SAP HANA was for IBM Power Big Endian (ppc64) only.

SAP NetWeaver (ABAP) software versions:
7.52 SP00, 7.50 SP00

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../../docs/README.md) for the capabilities and different execution methods.

## Execution outcome

When executing this Ansible Playbook for SAP, the following hosts are provisioned (unless an Ansible Inventory is provided for existing hosts):
1. Host for SAP MaxDB Database Server and SAP NetWeaver Application Server (ABAP) - Central Services (ASCS) and Primary Application Server (PAS)

The sequence of a Standard System installation is:
- `SWPM`: Install SAP MaxDB database server
- `SWPM`: Install SAP NetWeaver Application Server (ABAP)

This therefore matches to the SAP SWPM Product ID prefixes that are executed in sequence:
- `NW_ABAP_OneHost`, Central Services, Primary Application Server
