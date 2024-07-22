# Ansible Playbook - SAP BW/4HANA Standard (Scale-Out) installation

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

SAP BW/4HANA installation:
- Standard System definition by SAP: all main SAP NetWeaver instances (except the SAP HANA database instance) run on a single host.
- System Topology/Architecture: a Standard System is commonly referred as Three-Tier Architecture, may also be known as DualHost.
- SAP HANA installed as Scale-Out cluster

SAP BW/4HANA software versions:
2023, 2021

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../../docs/README.md) for the capabilities and different execution methods.

## Execution outcome

When executing this Ansible Playbook for SAP, the following hosts are provisioned (unless an Ansible Inventory is provided for existing hosts):
1. Host for SAP HANA Database Server, Coordinator node
2. Host for SAP HANA Database Server, Worker node
3. Host for SAP HANA Database Server, Worker node
4. Host for SAP HANA Database Server, Standby node
5. Host for SAP NetWeaver Application Server (ABAP) - Central Services (ASCS) and Primary Application Server (PAS)

The sequence of a Standard System installation is:
- `hdblcm`: Install SAP HANA database server
- `SWPM`: Install SAP NetWeaver Application Server (ABAP) and Installation Export to Database (i.e. Database Load)

This therefore matches to the SAP SWPM Product ID prefixes that are executed in sequence:
- `NW_ABAP_OneHost`, Central Services, Database Instance Installation, Primary Application Server


## Known errors

### SAP HANA Scale-Out Worker Group name

SAP HANA Scale-Out Worker Group name must be left as 'default' before SAP BW/4HANA installation.

SAP HANA `hdblcm` allows this to change, which is correctly reflected in `/hana/shared/H01/global/hdb/custom/config/nameserver.ini` and correctly reflected in runtime as shown by `hdbsql` SQL Query to System View (i.e. `SELECT * FROM SYS.M_LANDSCAPE_HOST_CONFIGURATION`).

However, an error occurs when SAP SWPM attempts to perform restore of the SAP BW/4HANA Export (occurs with or without standby node).

For further detail, see [SAP Note 3043860 - Recovery fails due to incorrect worker group assignment](https://me.sap.com/notes/3043860).

**Example hdblcm command parameters:**
```shell
--workergroup=workergroups_01
--addhosts=hdb-node1:role=worker:workergroup=workergroups_01:group=default,hdb-node2:role=worker:workergroup=workergroups_01:group=default,hdb-node3:role=standby:workergroup=default:group=default
```

**Example nameserver.ini output:**
```ini
[landscape]
...
roles_hdb-node0 = worker
roles_hdb-node1 = worker
roles_hdb-node2 = worker
roles_hdb-node3 = standby

workergroups_hdb-node0 = workergroups_01
workergroups_hdb-node1 = workergroups_01
workergroups_hdb-node2 = workergroups_01
workergroups_hdb-node3 = workergroups_01

failovergroup_hdb-node0 = default
failovergroup_hdb-node1 = default
failovergroup_hdb-node2 = default
failovergroup_hdb-node3 = default
```

**Example SAP SWPM output:**
```shell
SAP SWPM step perform_database_recovery_tenant error:
HdbCmdClazz 'START_DATABASE_RECOVERY_TENANT'
    Progress: indexserver[initialization (failed)
        SAP DBTech JDBC:
        [448]: recovery could not be completed:
            [111204] Recovery failed during topology update:
                Unable to update catalog master - worker groups of indexserver with volume 3 do not match the worker groups of existing host "hdb-node0":
                    default != workergroups_01
```


### SAP HANA Scale-Out Failover Group name

SAP HANA Scale-Out Worker Group name must be left as 'default' before SAP BW/4HANA installation.

SAP HANA `hdblcm` does not allow this to change or is a bug, the 'group' parameter in documentation does not appear in the config file dump and manually appending the 'group' parameter does not alter the Failover Group of the coordinator node - which means all nodes in the 'addhosts' parameter would have a different Failover Group name.

This is visible in `/hana/shared/H01/global/hdb/custom/config/nameserver.ini` which shows the SAP HANA Scale-Out Coordinator node has a different Failover Group name to all other nodes. It is also visible by `hdbsql` SQL Query to System View (i.e. `SELECT * FROM SYS.M_LANDSCAPE_HOST_CONFIGURATION`).

**Example hdblcm command parameters:**
```shell
--workergroup=default
--addhosts=hdb-node1:role=worker:workergroup=default:group=failovergroup_01,hdb-node2:role=worker:workergroup=default:group=failovergroup_01,hdb-node3:role=standby:workergroup=default:group=failovergroup_01
```

**Example nameserver.ini output:**
```ini
[landscape]
...
roles_hdb-node0 = worker
roles_hdb-node1 = worker
roles_hdb-node2 = worker
roles_hdb-node3 = standby

workergroups_hdb-node0 = default
workergroups_hdb-node1 = default
workergroups_hdb-node2 = default
workergroups_hdb-node3 = default

failovergroup_hdb-node0 = default
failovergroup_hdb-node1 = failovergroup_01
failovergroup_hdb-node2 = failovergroup_01
failovergroup_hdb-node3 = failovergroup_01
```
