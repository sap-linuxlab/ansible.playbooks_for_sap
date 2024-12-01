# Ansible Playbook - SAP Business Suite (ECC) with IBM Db2, Distributed installation (no HA)

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

SAP Business Suite with IBM Db2 installation:
- Distributed System definition by SAP: every SAP AnyDB (i.e. IBM Db2) and SAP NetWeaver instance run on a separate host.
- System Topology/Architecture: a Distributed System is commonly referred as Multi-Tier Architecture.
- Note: This Ansible Playbook is not available for IBM Power Little Endian (ppc64le); all prior SAP Software without SAP HANA was for IBM Power Big Endian (ppc64) only.

SAP Business Suite, aka. SAP ECC, software versions:
EhP8

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../../docs/README.md) for the capabilities and different execution methods.

## Execution outcome

When executing this Ansible Playbook for SAP, the following hosts are provisioned (unless an Ansible Inventory is provided for existing hosts):
1. Host for SAP AnyDB (IBM Db2 database server)
2. Host for SAP NetWeaver Application Server (ABAP) - Central Services (ASCS)
3. Host for SAP NetWeaver Application Server (ABAP) - Primary Application Server (PAS)
4. Host for SAP NetWeaver Application Server (ABAP) - Additional Application Server (AAS)

The sequence of a Distributed installation is:
- `SWPM`: Install SAP NetWeaver Application Server (ABAP) - Central Services (ASCS). This runs the MS and EN.
- `SWPM`: Install SAP AnyDB Database Instance (i.e. IBM Db2 installation) and Installation Export to Database (i.e. Database Load)
- `SWPM`: Install SAP NetWeaver Application Server (ABAP) - Primary Application Server (PAS); formerly Central Instance (CI). This runs the GW and WP.
- `SWPM`: Install SAP NetWeaver Application Server (ABAP) - Additional Application Server (AAS); formerly Dialog Instance (DI). This runs additional WP.

This therefore matches to the SAP SWPM Product ID prefixes that are executed in sequence:
- `NW_ABAP_ASCS`, Central Services Instance for ABAP (ASCS) Installation
- `NW_ABAP_DB`, Database Instance Installation
- `NW_ABAP_CI`, Primary Application Server Instance Installation
- `NW_DI`, Application Server Instance Installation
