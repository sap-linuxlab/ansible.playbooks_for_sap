# Ansible Playbook - SAP Business Suite (ECC) with IBM Db2, Distributed installation (with HA)

This Ansible Playbook uses an Ansible Role which is `experimental`.

This Ansible Playbook can be executed with:
- Ansible to provision hosts
- Ansible + Terraform to provision hosts
- Existing hosts

This Ansible Playbook can be targeted at the following Infrastructure Platforms:
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- IBM Cloud
- Microsoft Azure (MS Azure)

SAP Business Suite with IBM Db2 installation:
- Distributed System definition by SAP: every SAP AnyDB (i.e. IBM Db2) and SAP NetWeaver instance run on a separate host.
- System Topology/Architecture: a Distributed System is commonly referred as Multi-Tier Architecture.
- Note: This Ansible Playbook is not available for IBM Power Little Endian (ppc64le); all prior SAP Software without SAP HANA was for IBM Power Big Endian (ppc64) only.

SAP Business Suite, aka. SAP ECC, software versions:
EhP8

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../docs/README.md) for the capabilities and different execution methods.

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

> N.B. Optionally, instead of default ENSA2 the High Availability for SAP NetWeaver ASCS/ERS can use ENSA1 by using `sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1: true`


### Execution sequence

- Infrastructure Provision
- Set temporary Virtual IP
- `sap_storage_setup` Ansible Role for SAP Storage Setup
- Perform Preflight Checks
- Download Install Media
- Transfer Install Media to other hosts
- Update /etc/hosts
- Run Ansible Roles for preconfiguration
    - `sap_general_preconfigure` Ansible Role
    - `sap_netweaver_preconfigure` Ansible Role
    - Reboot (removes temporary Virtual IP)
- Set temporary Virtual IP
- Run Ansible Roles for SAP NetWeaver hosts
    - `sap_install_media_detect` Ansible Role
    - `sap_swpm` Ansible Role for NWAS ASCS HA
    - `sap_swpm` Ansible Role for NWAS ERS
- Run Ansible Roles for SAP AnyDB hosts
    - `sap_install_media_detect` Ansible Role
    - `sap_swpm` Ansible Role for DB Install and DB Load
    - Perform Database Backup to file
    - Transfer Database Backup to secondary node
    - `sap_swpm` Ansible Role for DB Install of secondary node
    - Restore Database Backup to secondary node
    - `sap_ha_install_anydb_ibmdb2` Ansible Role for IBM Db2 HADR with Integrated Linux Pacemaker
- Run Ansible Roles for SAP NetWeaver hosts
    - `sap_ha_pacemaker_cluster` Ansible Role (inc. Virtual IP setup)
    - `sap_swpm` Ansible Role for PAS
    - `sap_swpm` Ansible Role for AAS
- Post-deployment Infrastructure amendments (e.g. Load Balancer Health Check Probe port number changes)

---

## Note regarding Load Balancer for Virtual IP and Virtual Hostname for SAP SWPM

When using Load Balancers for providing the Virtual IP (VIP) and Virtual Hostname, the sequence of Linux Pacemaker installation is often reversed due to SAP SWPM installation procedures.

For example, usual sequence:
- Execute SAP SWPM
- Install Linux Pacemaker and configurations for SAP NetWeaver etc

For example, sequence when using Load Balancers:
- Create Load Balancer and VIP, using Health Check Probe to Port (which won't have a listening service on the host)
- Install Linux Pacemaker and configurations for SAP NetWeaver etc (listening service now available, after a few minutes the LB should mark network path / hosts pool as Healthy and VIP will become available)
- Execute SAP SWPM

This is a non-standard sequence for installations using SAP SWPM, and is prone to errors without the correct timings / sleep commands to wait for VIP availability and successful resolution of the Virtual Hostname.

Therefore for this Ansible Playbook, the following handling is used to retain the correct structure applicable to the usual sequence (permitting the Ansible Playbook to be executed on existing hosts), but adjusting for hosts on Infrastructure Platforms using Load Balancers for VIPs:
- Create Load Balancer and VIP, using Health Check Probe with a temporary port listener using netcat (which will always be listening) and the mark network path / hosts pool as Healthy with VIP immediately available
- As required, append Secondary IP to the default OS network interface
- Execute SAP SWPM
- Install Linux Pacemaker and configurations for SAP NetWeaver etc (will identify secondary ip attached to default OS network interface, and will takeover management)
- Amend Load Balancer to use Health Check Probe of the listening port configured with Linux Pacemaker

> The additional handling for Load Balancer VIPs is irrelevant for SAP AnyDB using IBM Db2 installation procedures.
