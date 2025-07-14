# Documentation of Ansible Playbooks for SAP

This Readme document contains additional instructions for using Ansible Playbooks for SAP.

Table of Contents:
- [Operating System Requirements](#operating-system-requirements)
- [Available Scenarios](#available-scenarios)
- [Prepare the Password Variables](#prepare-the-password-variables)
- [Prepare the execution node](#prepare-the-execution-node)
- [Prepare the Infrastructure Platform for provisioning](#prepare-the-infrastructure-platform-for-provisioning)
- [Customization of Ansible Playbooks for SAP](#customization-of-ansible-playbooks-for-sap)
- [Playbook Execution](#playbook-execution)
- [Provisioned Infrastructure Platform Resources](#provisioned-infrastructure-platform-resources)

Related documents:
- [Getting Started - Windows](./GET_STARTED_WINDOWS.md)
- [Getting Started - macOS](./GET_STARTED_MACOS.md)
- [Getting Started - Azure DevOps Pipelines](./GET_STARTED_AZURE_DEVOPS.md)
- [FAQ](./FAQ.md)


## Operating System Requirements
### Control Nodes
Operating system:
- Any operating system with required Python and Ansible versions.

Python: 3.11 or higher  
Ansible: 9 or higher  
Ansible-core: 2.16 or higher  

### Managed Nodes
Operating system:
- SUSE Linux Enterprise Server for SAP Applications 15 SP5+ (SLE4SAP)
- Red Hat Enterprise Linux for SAP Solutions 8.x 9.x (RHEL4SAP)

Python: 3.9 or higher

Additional information:
- RHEL for _SAP Applications_ may have incompatibility, depending on selected scenario, due to missing OS Packages for SAP HANA, High Availability and extended patching (EUS/E4S)
- RHEL for _SAP Solutions_ may be labelled 'RHEL for SAP with High Availability and Update Services (HA-US)' on Cloud Hyperscalers

Requirements for using Existing Hosts:
- **NOTE: Operating system needs to have access to required package repositories either directly or via subscription registration.**


## Available Scenarios
| <br/><br/><br/><br/>Scenario name | Amazon Web Services (AWS) | Google Cloud| Microsoft Azure | IBM Cloud<br/>[x86_64] | IBM Cloud<br/>[ppc64le] | IBM PowerVC | KubeVirt | OVirt KVM | VMware vCenter |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| <br/>***Deploy Scenario - Sandbox*** |
| sap_bw4hana_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ecc_hana_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ecc_ibmdb2_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ecc_oracledb_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ecc_sapase_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ecc_sapmaxdb_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ides_ecc_hana_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ides_ecc_ibmdb2_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_nwas_abap_hana_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_nwas_abap_ibmdb2_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_nwas_abap_oracledb_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_nwas_abap_sapase_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_nwas_abap_sapmaxdb_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_nwas_java_ibmdb2_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_nwas_java_sapase_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_foundation_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_sandbox_maintplan | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_solman_sapase_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_solman_saphana_sandbox | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| <br/>***Deploy Scenario - Composites*** |
| sap_bw4hana_standard_scaleout | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_ecc_ibmdb2_distributed | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_hana | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| sap_hana_ha | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :warning: |
| sap_hana_scaleout | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_landscape_s4hana_standard | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_landscape_s4hana_standard_maintplan | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_distributed | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_distributed_ha | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :warning: |
| sap_s4hana_distributed_ha_maintplan | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :warning: |
| sap_s4hana_distributed_maintplan | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_foundation_standard | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_standard | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| sap_s4hana_standard_maintplan | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <br/>***Special Actions*** |
| sap_nwas_abap_ascs_ers_cluster | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| sap_download_install_media | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| sap_sda | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| sap_system_copy_export | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| sap_system_copy_restore_hana_sandbox | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| sap_webdispatcher_standalone | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :white_check_mark: | :white_check_mark: |
| <br/>***Provisioning via Ansible to Terraform*** |
| | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning: | :warning: | N/A | N/A | :warning: |

<sub>**Key:**</sub>
- :white_check_mark: <sub>Ready and Tested</sub>
- :warning: <sub>Work in Progress</sub>
- :no_entry_sign: <sub>Not provided by SAP</sub>
- <sub>N/A: Not Applicable</sub>


## Prepare the Password Variables
Each scenario contains a range of variable files, such as `ansible_extravars.yml`, which include password variables.  

**IMPORTANT:** All SAP passwords must be replaced with complex and secure values, adhering to SAP best practices. Empty or invalid password variables will result in playbook failure.  

More information about SAP Passwords is available at [FAQ section](./FAQ.md#sap-system-password-recommendations)

### Securing Passwords with Ansible Vault (Recommended)
For secure management of sensitive data like passwords, **Ansible Vault is strongly recommended.**  
While optional, using Vault encrypts your variables, preventing them from being stored in plaintext.

**NOTE: Variables set in extravars files take precedence over Ansible Vault variables. Ensure that you remove them or comment them out in extravars file!** 

Here's a quick start guide for using Ansible Vault:
1. **Move Sensitive Variables to a Vault File:**
   - Comment out or remove sensitive variables (like passwords) from your regular variable files (e.g., ansible_extravars.yml). These variables are often initially defined as empty strings ('') as placeholders.
   - Create a new, dedicated Ansible Vault file for these sensitive variables (e.g., ansible_vault.yml). Populate this file with your sensitive variables and their actual, secure values.

2. **Encrypt an ansible vault file:**
    ```bash
    ansible-vault encrypt ansible_vault.yml
    ```
    You will be prompted to set and confirm a new Vault password.

3. **View an encrypted file:**
    ```bash
    ansible-vault view ansible_vault.yml
    ```

4. **Edit an encrypted file:**
    ```bash
    ansible-vault edit ansible_vault.yml
    ```

5. **Run a playbook with Vault:**
    You will need to provide your Vault password when running the playbook.
    This is simplified example and it does not contain all extravars files.
    ```bash
    ansible-playbook ansible_playbook.yml -e "@.ansible_vault.yml" -i ansible_inventory_noninteractive.yml --ask-vault-pass
    ```

For more comprehensive details on Ansible Vault, including advanced usage like encrypting individual variables or integrating with CI/CD, please refer to the [official Ansible documentation on Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html).


## Prepare the execution node

### Preparations - Requirements

The following are the requirements for successful execution of an Ansible Playbook, please read these and configure accordingly on your Ansible execution/controller host.

- Ensure Ansible Core 2.16+ and Python 3.11+ (i.e. CPython distribution) are available
    - It is recommended to avoid using the default OS system Python. Instead the suggestion is to create and activate a Python virtual environment for the current shell session<br>(e.g. `python -m venv /tmp/playbooks_sap && source /tmp/playbooks_sap/bin/activate && python -m pip install ansible-core`).
    - Ansible discovers the Python interpreter automatically, if a specific Python version is required on the host executing the Ansible Playbook then it is recommended to use Ansible special variable `ansible_python_interpreter` for the localhost in the Ansible Inventory file.<br> This will avoid Ansible being instructed to look for the customized Python path on the target/remote hosts (which likely will be default /usr/bin/python) and cause errors such as `/bin/sh: python3: command not found`.

- Ensure all Python Packages are available for Ansible to use:
    - If Ansible Playbook provisioning to AWS, use `python -m pip install boto3`
    - If Ansible Playbook provisioning to Google Cloud, use `python -m pip install google-auth`
    - If Ansible Playbook provisioning to MS Azure, use `python -m pip install -r https://github.com/ansible-collections/azure/blob/dev/requirements.txt`
    - If Ansible Playbook provisioning to IBM PowerVM, use `python -m pip install openstacksdk`
    - If Ansible Playbook provisioning to OVirt, use `python -m pip install ovirt-engine-sdk-python`
    - If Ansible Playbook provisioning to VMware, use `python -m pip install aiohttp`

- Ensure Ansible Collections are installed (a requirements file is included with each Ansible Playbook) `ansible-galaxy collection install --requirements-file ./ansible_requirements.yml`

- Ensure OS Packages are installed and available for Ansible to call (for commands not provided by Ansible Collections/Roles/Modules):
    - If Ansible Playbook provisioning to AWS, **install AWS CLI** to perform IAM activities for High Availability
    - If Ansible Playbook provisioning to Google Cloud, **install GCloud CLI** to perform activities for High Availability
    - If Ansible Playbook provisioning to IBM Cloud, **install Terraform (v1.5.5 and below)** to provision and **install IBM Cloud CLI** to perform activities for High Availability
        - _Terraform install is required, it is used on-the-fly by the legacy Ansible Collection `ibm.cloudcollection` - used until the `ibm.cloud` Ansible Collection full functionality is available_

- The SSH Private Key files used by Ansible have the correct file permissions (`chmod 400`) for SSH connections.

- OPTIONAL: when running Ansible, you may silence warnings from Ansible which are irrelevant for this Ansible Playbook:
```shell
export ANSIBLE_LOCALHOST_WARNING=False
export ANSIBLE_INVENTORY_UNPARSED_WARNING=False
```

- OPTIONAL: by default, Ansible Core will output error or debug (-v) messages as a string. For easier readability, it is easy to configure Ansible Core to parse the error or debug messages and output as YAML that is easier to read, create/amend the `~/.ansible.cfg` file:
```ini
[defaults]
# Use the YAML callback plugin.
stdout_callback = yaml
# Use the stdout_callback when running ad-hoc commands.
bin_ansible_callbacks = True
```

### Preparations - SAP User ID credentials (Optional)
The download of the SAP Installation Media Software from SAP to the target host, will be executed if the `community.sap_launchpad` Ansible Collection is installed on Ansible Control Node (i.e. where Ansible is executed from, such as a laptop or AWX etc).  

The SAP software files must be obtained from SAP directly, and requires valid license agreements with SAP in order to access these files.  

An SAP Company Number (SCN) contains one or more Installation Number/s, providing licenses for specified SAP Software. When an SAP User ID is created within the SAP Customer Number (SCN), the administrator must provide SAP Download authorizations for the SAP User ID.  

Login credentials for the SAP User ID (e.g. S-User) have two login approaches:  
- **SAP Universal ID**: an email address is assigned many SAP User IDs. Select the SAP User ID, and use the password of the SAP Universal ID.
   - Do **NOT** use the SAP User ID legacy `Account Password` from the [SAP Universal ID Account Manager](https://account.sap.com/manage/accounts).
- **Legacy**: an SAP User ID is isolated. Use the SAP User ID and the associated password.

For further information regarding connection errors, please see the FAQ section [Errors with prefix 'SAP SSO authentication failed - '](./docs/FAQ.md#errors-with-prefix-sap-sso-authentication-failed---).

**NOTE: The `community.sap_launchpad` Ansible Collection supports only S-Users without Multi Factor Authentication.**


## Prepare the Infrastructure Platform for provisioning
This section is not required when using Existing Hosts with `sap_vm_provision_iac_platform: existing_hosts`.

### Preparations - Ansible for provisioning VMs

If selecting Ansible to perform provisioning of Infrastructure, please ensure the Infrastructure Platform is setup (e.g. relevant Subnets, SSH Keys etc); this is dependent on the target Infrastructure Platform. See below for the drop-down list of each Infrastructure Platform.

For further details on the output, please see [Host provisioning via Ansible](#host-provisioning-via-ansible), under section Infrastructure Platform provisioned resources by Ansible Playbooks for SAP.


### Design assumptions with execution impact

- Throughout Ansible Playbook, use of Ansible Play option `any_errors_fatal: true` to enforce abort on all hosts if there is any error (and therefore stop Ansible Playbook).<br> Please see [Using Ansible Playbooks - Error handling in playbooks - Aborting a play on all hosts](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html#aborting-a-play-on-all-hosts) for further information.
- For Hyperscaler Cloud Service Providers that use Resource Groups (IBM Cloud, Microsoft Azure):
    - Virtual Machine and associated resources (Disks, Network Interfaces, Load Balancer etc.) will be provisioned to the same Resource Group as the targeted network/subnet.
    - Optional: Private DNS may be allocated to another Resource Group, and an optional variable is provided for this.


<details>
<summary><b>Amazon Web Services (AWS):</b></summary>

- VPC
    - VPC Access Control List (ACL)
    - VPC Subnets
    - VPC Security Groups
- Route53 (Private DNS)
- Internet Gateway (SNAT)
- EFS (NFS)
- Bastion host (AWS EC2 VS)
- Key Pair for hosts

</details>

<details>
<summary><b>Google Cloud (GCP):</b></summary>

- VPC Network
    - VPC Subnetwork
- Compute Firewall
- Compute Router
    - SNAT
- DNS Managed Zone (Private DNS)
- Filestore (NFS)
- Bastion host (GCP CE VM)

</details>

<details>
<summary><b>Microsoft Azure:</b></summary>

- Resource Group <sub><sup><i>(optional: Private DNS may be allocated to separate Resource Group, see `sap_infrastructure` documentation)</i></sup></sub>
- VNet
    - VNet Subnet
    - VNet Network Security Group (NSG)
- Private DNS Zone
- NAT Gateway (SNAT)
- Storage Account
    - Azure Files (aka. File Storage Share, NFS)
    - Private Endpoint Connection
- Bastion host (MS Azure VM)
- Key Pair for hosts

</details>

<details>
<summary><b>IBM Cloud:</b></summary>

- Resource Group <sub><sup><i>(optional: Private DNS may be allocated to separate Resource Group, see `sap_infrastructure` documentation)</i></sup></sub>
- VPC
    - VPC Access Control List (ACL)
    - VPC Subnets
    - VPC Security Groups
- Private DNS
- Public Gateway (SNAT)
- File Share (NFS)
- Bastion host (IBM Cloud VS)
- Key Pair for hosts

</details>

<details>
<summary><b>IBM Cloud, IBM Power VS:</b></summary>

- Resource Group <sub><sup><i>(optional: Private DNS may be allocated to separate Resource Group, see `sap_infrastructure` documentation)</i></sup></sub>
- IBM Power Workspace
    - VLAN Subnet
    - Cloud Connection (from secure enclave to IBM Cloud)
- Private DNS Zone
- Public Gateway (SNAT)
- Bastion host (IBM Cloud VS or IBM Power VS)
- Key Pair for hosts (in IBM Power Workspace)

</details>

<details>
<summary><b>IBM PowerVC:</b></summary>

- Host Group Shared Processor Pool
- Storage Template
- Network Configuration (for SEA or SR-IOV)
- VM OS Image
- Key Pair for hosts

</details>

<details>
<summary><b>KubeVirt:</b></summary>

- `TODO`

</details>

<details>
<summary><b>OVirt:</b></summary>

- `TODO`

</details>

<details>
<summary><b>VMware vCenter:</b></summary>

- Datacenter (SDDC)
    - Cluster
        - Hosts
- NSX
- Datastore
- Content Library
    - VM Template

</details>


### Preparations - Ansible to Terraform for provisioning minimal landing zone and VMs

If selecting Terraform to perform provisioning of Infrastructure, please install Terraform v1.5.5 and below for the relevant Operating System.

The Ansible Playbooks for SAP use the `sap_infrastructure` Ansible Collection, which for Ansible to Terraform make use of the [Terraform Modules for SAP](https://github.com/sap-linuxlab/terraform.modules_for_sap); these are backwards compatible down to Terraform v1.0.0.

For further details on the output, please see [Infrastructure setup and Host provisioning via Terraform](#infrastructure-setup-and-host-provisioning-via-terraform), under section Infrastructure Platform provisioned resources by Ansible Playbooks for SAP.

N.B. The Linux Foundation's [OpenTofu](https://opentofu.org/docs/intro/install/) and accompanying [OpenTofu Registry](https://opentofu.org/registry/) have not been tested. It is anticipated that LF OpenTofu would work immediately - however, further testing of both the Ansible Role [cloud.terraform](https://galaxy.ansible.com/ui/repo/published/cloud/terraform/) to control the execution and the underlying [Terraform Modules for SAP](https://github.com/sap-linuxlab/terraform.modules_for_sap) with LF OpenTofu is out-of-scope at this time. The suggestion remains to use Terraform v1.0.0 - v1.5.5 developed under the Mozilla Public License (MPL).


### Preparations - Recommended Infrastructure Platform authorizations

The Ansible Playbooks for SAP are designed to use limited delegated administration privileges, as much as possible. Particularly for Ansible to Terraform provisioning, the following are a recommended authorizations to a target Infrastructure Platform.

See below for the drop-down list of each Infrastructure Platform.


<details>
<summary><b>Amazon Web Services (AWS):</b></summary>

The AWS User and associated key/secret will need to be assigned, by the Cloud Account Administrator. A recommended minimum of AWS IAM user authorization is achieved with the following AWS CLI commands:
```shell
# Login
aws configure

# Create AWS IAM Policy Group
aws iam create-group --group-name 'ag-sap-automation'
aws iam attach-group-policy --group-name 'ag-sap-automation' --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess
aws iam attach-group-policy --group-name 'ag-sap-automation' --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
aws iam attach-group-policy --group-name 'ag-sap-automation' --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess
```

</details>

<details>
<summary><b>Google Cloud (GCP):</b></summary>

Google Cloud Platform places upper limit quotas for different resources and limits `'CPUS_ALL_REGIONS'` and `'SSD_TOTAL_GB'` may be too low if using a new GCP Account or a new target GCP Region. Please check `gcloud compute regions describe us-central1 --format="table(quotas:format='table(metric,limit,usage)')"` before provisioning to a GCP Region, and manually request quota increases for these limits in the target GCP Region using instructions on https://cloud.google.com/docs/quota#requesting_higher_quota (from GCP Console or contact with GCP Support Team).

The Google Cloud User credentials (Client ID and Client Secret) JSON file with associated authorizations will need to be assigned, by the Cloud Account Administrator. Thereafter, please manually open and activate various APIs for the GCP Project to avoid HTTP 403 errors during provisioning:
- Enable the Compute Engine API, using https://console.cloud.google.com/apis/api/compute.googleapis.com/overview
- Enable the Cloud DNS API, using https://console.cloud.google.com/apis/api/dns.googleapis.com/overview
- Enable the Network Connectivity API, using https://console.cloud.google.com/apis/library/networkconnectivity.googleapis.com
- Enable the Cloud Filestore API, using https://console.cloud.google.com/apis/library/file.googleapis.com
- Enable the Service Networking API (Private Services Connection to Filestore), using https://console.cloud.google.com/apis/library/servicenetworking.googleapis.com

</details>

<details>
<summary><b>Microsoft Azure:</b></summary>

The Azure Application Service Principal and associated Client ID and Client Secret will need to be assigned, by the Cloud Account Administrator. A recommended minimum of Azure AD Role authorizations is achieved with the following MS Azure CLI commands:

```shell
# Login
az login

# Show Tenant and Subscription ID
export AZ_SUBSCRIPTION_ID=$(az account show | jq .id --raw-output)
export AZ_TENANT_ID=$(az account show | jq .tenantId --raw-output)

# Create Azure Application, includes Client ID
export AZ_CLIENT_ID=$(az ad app create --display-name ansible-terraform | jq .appId --raw-output)

# Create Azure Service Principal, instantiation of Azure Application
export AZ_SERVICE_PRINCIPAL_ID=$(az ad sp create --id $AZ_CLIENT_ID | jq .objectId --raw-output)

# ALT: Obtain existing Azure Application (Client ID) and the Azure Application's instantiation (Service Principal)
# See Azure AAD 'App Registrations' blade
# See Azure AAD IAM 'Enterprise Application' blade
export AZ_CLIENT_ID=$(az ad app list --display-name "NAME" | jq .[].appId --raw-output)
export AZ_SERVICE_PRINCIPAL_ID=$(az ad sp show --id "$AZ_CLIENT_ID" | jq .id --raw-output)

# Assign default Azure AD Role with privileges for creating Azure Virtual Machines
az role assignment create --assignee "$AZ_SERVICE_PRINCIPAL_ID" \
--role "Virtual Machine Contributor" \
--role "Contributor" \
--scope "/subscriptions/$AZ_SUBSCRIPTION_ID" \
--subscription "$AZ_SUBSCRIPTION_ID"

# Reset Azure Application, to provide the Client ID and Client Secret to use the Azure Service Principal
az ad sp credential reset --name $AZ_CLIENT_ID
```

Note: MS Azure VMs provisioned will contain Hyper-V Hypervisor virtual interfaces using eth* on the OS, and when Accelerated Networking (AccelNet) is enabled for the MS Azure VM then the Mellanox SmartNIC/DPU SR-IOV Virtual Function (VF) may use enP* on the OS. For further information, see [MS Azure - How Accelerated Networking works](https://learn.microsoft.com/en-us/azure/virtual-network/accelerated-networking-how-it-works). During High Availability executions, failures may occur and may require additional variable 'sap_ha_pacemaker_cluster_vip_client_interface' to be defined.

</details>

<details>
<summary><b>IBM Cloud:</b></summary>

The IBM Cloud Account User (or Service ID) and associated API Key will need to be assigned, by the Cloud Account Administrator. A recommended minimum of IBM Cloud IAM user authorization is achieved with the following IBM Cloud CLI commands:

```shell
# Login (see alternatives for user/password and SSO using ibmcloud login --help)
ibmcloud login --apikey=

# Create IBM Cloud IAM Access Group
ibmcloud iam access-group-create 'ag-sap-automation'
ibmcloud iam access-group-policy-create 'ag-sap-automation' --roles Editor --service-name=is
ibmcloud iam access-group-policy-create 'ag-sap-automation' --roles Editor,Manager --service-name=transit
ibmcloud iam access-group-policy-create 'ag-sap-automation' --roles Editor,Manager --service-name=dns-svcs

# Access to create an IBM Cloud Resource Group (Ansible to Terraform)
ibmcloud iam access-group-policy-create 'ag-sap-automation' --roles Administrator --resource-type=resource-group

# Assign to a specified Account User or Service ID
ibmcloud iam access-group-user-add 'ag-sap-automation' <<<IBMid>>>
ibmcloud iam access-group-service-id-add 'ag-sap-automation' <<<SERVICE_ID_UUID>>>
```

Alternatively, use the IBM Cloud web console:
- Open cloud.ibm.com - click Manage on navbar, click Access IAM, then on left nav menu click Access Groups
- Create an Access Group, with the following policies:
  - IAM Services > VPC Infrastructure Services > click All resources as scope + Platform Access as Editor
  - IAM Services > DNS Services > click All resources as scope + Platform Access as Editor + Service access as Manager
  - IAM Services > Transit Gateway > click All resources as scope + Platform Access as Editor + Service access as Manager
  - `[OPTIONAL]` IAM Services > All Identity and Access enabled services > click All resources as scope + Platform Access as Viewer + Resource group access as Administrator
  - `[OPTIONAL]` Account Management > Identity and Access Management > click Platform access as Editor
  - `[OPTIONAL]` Account Management > IAM Access Groups Service > click All resources as scope + Platform Access as Editor

</details>

<details>
<summary><b>IBM PowerVC:</b></summary>

The recommended [IBM PowerVC Security Role](https://www.ibm.com/docs/en/powervc/latest?topic=security-managing-roles) is 'Administrator assistant' (admin_assist), because the 'Virtual machine manager' (vm_manager) role is not able to create IBM PowerVM Compute Template (required for setting OpenStack extra_specs specific to the IBM PowerVM hypervisor infrastructure platform, such as Processing Units). Note that the 'Administrator assistant' does not have the privilege to delete Virtual Machines.

</details>


### Preparations - Recommended Infrastructure Platform configuration

<details>
<summary><b>VMware vCenter:</b></summary>

The VM Template must be prepared with cloud-init. This process is subjective to VMware, cloud-init and Guest OS (RHEL / SLES) versions; success will vary. This requires:

- Edit the default cloud-init configuration file, found at `/etc/cloud/cloud.cfg`. It must contain the data source for VMware (and not OVF), and force use of cloud-init metadata and userdata files. Note: appending key `network: {config: disabled}` may cause network `v1` to be incorrectly used instead of network [`v2`](https://cloudinit.readthedocs.io/en/latest/reference/network-config-format-v2.html) in the cloud-init metadata YAML to follow.
  ```yaml
  # Enable VMware VM Guest OS Customization with cloud-init (set to true for traditional customization)
  disable_vmware_customization: false

  # Use allow raw data to directly use the cloud-init metadata and user data files provided by the VMware VM Customization Specification
  # Wait 120 seconds for VMware VM Customization file to be available
  datasource:
    VMware:
      allow_raw_data: true
      vmware_cust_file_max_wait: 60
  ```
- Update `cloud-init` and `open-vm-tools` OS Package
- Enable DHCP on the OS Network Interface (e.g. eth0, ens192 etc.)
- Prior to VM shutdown and marking as a VMware VM Template, run commands:
    - `vmware-toolbox-cmd config set deployPkg enable-custom-scripts true`
    - `vmware-toolbox-cmd config set deployPkg wait-cloudinit-timeout 60`
    - `sudo cloud-init clean --seed --logs` to remove cloud-init logs, remove cloud-init seed directory /var/lib/cloud/seed.
        - If using cloud-init versions prior to 22.3.0 then do not use `--machine-id` parameter.
        - Reportedly, the `--machine-id` parameter which removes `/etc/machine-id` may on first reboot cause the OS Network Interfaces to be `DOWN` which causes the DHCP Request to silently error.
- Once VM is shutdown, then run 'Clone > Clone as Template to Library'
- After provisioning the VM Template via Ansible, debug by checking:
    - `/var/log/vmware-imc/toolsDeployPkg.log`
    - `/var/log/cloud-init-output.log`
    - `/var/log/cloud-init.log`
    - `/var/lib/cloud/instance/user-data.txt`
    - `/var/lib/cloud/instance/cloud-config.txt`
    - `/var/run/cloud-init/instance-data.json`
    - `/var/run/cloud-init/status.json`
- See documentation for further information:
    - [VMware KB 59557 - How to switch vSphere Guest OS Customization engine for Linux virtual machine](https://kb.vmware.com/s/article/59557)
    - [VMware KB 90331 - How does vSphere Guest OS Customization work with cloud-init to customize a Linux VM](https://kb.vmware.com/s/article/90331)
    - [VMware KB 91809 - VMware guest customization key cloud-init changes](https://kb.vmware.com/s/article/91809)
    - [VMware KB 74880 - Setting the customization script for virtual machines in vSphere 7.x and 8.x](https://kb.vmware.com/s/article/74880)
    - [vSphere Web Services SDK Programming Guide - Guest Customization Using cloud-init](https://developer.vmware.com/docs/18555/GUID-75E27FA9-2E40-4CBF-BF3D-22DCFC8F11F7.html)
    - [cloud-init documentation - Reference - Datasources - VMware](https://cloudinit.readthedocs.io/en/latest/reference/datasources/vmware.html)


In addition, the provisioned Virtual Machine must be accessible from the Ansible Controller (i.e. device where Ansible Playbook for SAP is executed must be able to reach the provisioned host).

When VMware vCenter and vSphere clusters with VMware NSX virtualized network overlays using Segments (e.g. 192.168.0.0/16) connected to Tier-0/Tier-1 Gateways (which are bound to the backbone network subnet, e.g. 10.0.0.0/8), it is recommended to:
- Use DHCP Server and attach to Subnet for the target VM. For example, create DHCP Server (e.g. NSX > Networking > Networking Profiles > DHCP Profile), set DHCP in the Gateway (e.g. NSX > Networking > Gateway > Edit > DHCP Config), then set for the Subnet (e.g. NSX > Networking > Segment > <<selected subnet>> > Set DHCP Config) which the VMware VM Template is attached to; this allows subsequent cloned VMs to obtain an IPv4 Address
- Use DNAT configuration for any VMware NSX Segments (e.g. NSX-T Policy NAT Rule)
- For outbound internet connectivity, use SNAT configuration (e.g. rule added on NSX Gateway) set for the Subnet which the VMware VM Template is attached to. Alternatively, use a Web Forward Proxy.

N.B. When VMware vCenter and vSphere clusters with direct network subnet IP allocations to the VMXNet network adapter (no VMware NSX network overlays), the above actions may not be required.

</details>



## Customization of Ansible Playbooks for SAP

### Host Specification Plan alterations

Every Ansible Playbook for SAP is for a specific SAP Solution Scenario, each with an Ansible Dictionary which define the host specification plans for an Infrastructure Platform.

The host specification plan can contain multiple hosts, with different host specifications (cpu, memory, storage etc). These host specification plans are altered/customized to each Infrastructure Platform.

As a baseline infrastructure (hardware) host/s sizing, only the following are provided in each Ansible Playbooks for SAP:

| Host Specification Plan | SAP Solution Scenarios applicable |
| --- | --- |
| `xsmall_256gb` | SAP S/4HANA, SAP Business Suite on HANA (SoH, aka. ECC on HANA) and SAP HANA |
| `xsmall_anydb_32vcpu` | SAP Business Suite (ECC) and SAP AnyDB <br/><sub>(SAP ASE, SAP MaxDB, IBM Db2, Oracle DB)</sub> |
| `xsmall_nwas_16vcpu` | SAP NetWeaver AS only |
| `tiny_64gb` | SAP HANA only (infrequent usage) |

For Hyperscaler Cloud Service Providers, the baseline infrastructure (hardware) host/s sizing use the following Profile/Types of Virtual Machines:

- 32 vCPU x 256GB DRAM for SAP HANA
    - Amazon Web Services: `r7i.8xlarge`
    - Google Cloud Platform: `n2-highmem-32`
    - IBM Cloud, Intel: `mx2-32x256`
    - IBM Cloud, IBM Power: `ush1-4x256`
    - Microsoft Azure: `Standard_M32ls`
- 32 vCPU x 128GB DRAM for SAP AnyDB
    - Amazon Web Services: `m7i.8xlarge`
    - Google Cloud Platform: `n2-standard-32`
    - IBM Cloud, Intel: `bx2-32x128`
    - Microsoft Azure: `Standard_D32s_v5`
- 16 vCPU x 32GB DRAM for SAP NetWeaver _(minimum 1:2 ratio for vCPU:RAM)_
    - Amazon Web Services: `c6id.4xlarge`
    - Google Cloud Platform: `n2-standard-16` _(lowest certified 16 vCPU uses 64 GB DRAM)_
    - IBM Cloud, Intel: `cx2-16x32`
    - IBM Cloud, IBM Power: `cnp-2x32`
    - Microsoft Azure: `Standard_D16s_v5` _(lowest certified 16 vCPU uses 64 GB DRAM)_

> Note: See below for default swap sizes, with reference to SAP Note 1597355 - Swap-space recommendation for Linux.
> - For SAP HANA, swap is 2GiB.
> - For SAP NetWeaver, swap is 64GiB.
> - For SAP AnyDB, IBM Db2 swap is 128GiB (minimum) else swap is 96GiB.
> - For Sandbox (OneHost DB and NWAS), swap is 96GiB.

It is easily possible to extend each Ansible Playbook for SAP with additional host specifications, such as:

| Host Specification Plan | SAP Solution Scenarios applicable |
| --- | --- |
| `small_512gb` | SAP HANA and SAP S/4HANA |
| `medium_1024gb` | SAP HANA and SAP S/4HANA |
| `large_2048gb` | SAP HANA and SAP S/4HANA |
| `xlarge_3072gb` | SAP HANA and SAP S/4HANA |
| `xxlarge_6144gb` | SAP HANA and SAP S/4HANA |

For example, the Ansible Playbook `sap_s4hana_sandbox` appending a host specification plan `small_512gb` on AWS could be defined as:

```yaml
sap_vm_provision_aws_ec2_vs_host_specifications_dictionary:

  small_512gb:

    s4h01: # Hostname, must be 13 characters or less
      sap_host_type: hana_primary # hana_primary, hana_secondary, nwas_ascs, nwas_ers, nwas_pas, nwas_aas
      virtual_machine_profile: r5.16xlarge
      disable_ip_anti_spoofing: true

      sap_storage_setup_sid: "{{ sap_system_sid }}"
      sap_storage_setup_nwas_abap_ascs_instance_nr: "{{ sap_system_nwas_abap_ascs_instance_nr }}"

      sap_storage_setup_host_type:
        - hana_primary
        - nwas_abap_ascs
        - nwas_abap_pas

      storage_definition:
        - name: hana_data
          mountpoint: /hana/data
          disk_size: 615                 # size in GB, integer
          filesystem_type: xfs           # default: xfs
        - name: hana_log
          mountpoint: /hana/log
          disk_size: 256                 # size in GB, integer
          filesystem_type: xfs           # default: xfs
        - name: hana_shared
          mountpoint: /hana/shared
          disk_size: 640                 # size in GB, integer
          filesystem_type: xfs           # default: xfs
        - name: usr_sap
          mountpoint: /usr/sap
          disk_size: 256                 # size in GB, integer
          filesystem_type: xfs           # default: xfs
        - name: sapmnt
          mountpoint: /sapmnt
          disk_size: 192                  # size in GB, integer
          filesystem_type: xfs           # default: xfs
        - name: swap
          disk_size: 160
          filesystem_type: swap          # must be swap filesystem
        - name: software
          mountpoint: /software
          disk_size: 100                 # size in GB, integer
          filesystem_type: xfs           # default: xfs
```

### Using NFS with Prepared Software
The playbooks validate if the Ansible Collection `community.sap_launchpad` is present before attempting to download SAP installation media.  
However, you can execute all playbooks without downloading software by leveraging an NFS mount.  
This approach is beneficial when you already have the necessary SAP software available on a network share, allowing for faster and more efficient deployments.

To use this method, modify the `storage_definition` section within the `host_specifications_dictionary` variable to include the NFS mount details.

**Example for AWS:**
```yaml
#### Ansible Dictionary for host specifications ####
sap_vm_provision_aws_ec2_vs_host_specifications_dictionary:
  xsmall_256gb:
    h01hana:
      storage_definition:

        - name: software
          mountpoint: /software
          nfs_path: ''
          nfs_server: "fs-example.efs.eu-central-1.amazonaws.com:/sap_hana_2_sps07"
          nfs_filesystem_type: nfs4
          nfs_mount_options: "nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,acl"
```


## Playbook Execution

The following execution examples are dependent on whether the desired outcome is using Existing Hosts, Hosts provisioned via Ansible to an existing environment, or using Ansible to Terraform to provision an environment and hosts.

Please ensure the tasks in the following section has been completed:
- [Prepare the execution node](#prepare-the-execution-node)
- [Prepare the Infrastructure Platform for provisioning](#prepare-the-infrastructure-platform-for-provisioning)

For first-time user how-to guidance, please also see:
- [Getting Started - Windows](./GET_STARTED_WINDOWS.md)
- [Getting Started - macOS](./GET_STARTED_MACOS.md)
- [Getting Started - Azure DevOps Pipelines](./GET_STARTED_AZURE_DEVOPS.md)


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


## Provisioned Infrastructure Platform Resources

Various SAP Software solution scenario and Infrastructure Platforms are available using the Ansible Playbooks for SAP.

###  Resources provisioned by Ansible

When Ansible is used for provisioning hosts on an existing setup of an Infrastructure Platform, the following is an overview of the Infrastructure-as-Code (IaC) provisioning:

| Infrastructure Platform | **Amazon Web Services (AWS)** | **Google Cloud** | **Microsoft Azure** | **IBM Cloud** | **IBM Cloud** | **IBM PowerVC** | **KubeVirt** | **OVirt KVM** | **VMware vCenter** |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| &emsp;&emsp;*Product* | EC2 Virtual Server | VM | VM | Virtual Server | IBM Power Virtual Server | VM <br/><sub>(aka. LPAR)</sub> | VM | VM | VM |
| <br/>***Host Provision*** |   |   |   |   |   |   |   |
| <sub>Create DNS Records (i.e. A, CNAME, PTR)</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <sub>Create Storage Volumes</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub>Create Host/s</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <br/>***High Availability*** |   |   |   |   |   |   |   |   |   |
| <sub>Create Resources (e.g. Load Balancer)</sub> | N/A | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A | N/A |

<sub>**Key:**</sub>
- :white_check_mark: <sub>Ready and Tested</sub>
- :warning: <sub>Work in Progress</sub>
- :no_entry_sign: <sub>Capability not provided by vendor (or construct concept does not exist)</sub>
- <sub>N/A: Not Applicable</sub>


### Resources provisioned by Terraform

When Ansible uses Terraform to provision minimal landing zone and host/s, the following is an overview of the Infrastructure-as-Code (IaC) provisioning, for full details please see the underlying [Terraform Modules for SAP documentation](https://github.com/sap-linuxlab/terraform.modules_for_sap#terraform-modules-for-sap).

| Infrastructure Platform | **Amazon Web Services (AWS)** | **Google Cloud** | **Microsoft Azure** | **IBM Cloud** | **IBM Cloud** | **IBM PowerVC** | **KubeVirt** | **OVirt KVM** | **VMware vCenter** |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| &emsp;&emsp;*Product* | EC2 Virtual Server | VM | VM | Virtual Server | IBM Power Virtual Server | LPAR | VM | VM | VM |
| <br/><br/>***Account Init*** |   |   |   |   |   |   |   |   |   |
| <sub>Create Resource Group. Or reuse existing Resource Group</sub> | :no_entry_sign: | :no_entry_sign: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <sub>Create Networks (VPC/VNet), Subnets, and Internet Access. Or reuse existing VPC/VNet</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <br/>***Account Bootstrap<br/>(aka. minimal landing zone)*** |   |   |   |   |   |   |   |   |   |
| <sub>Create Private DNS, Network Security</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <sub>Create Network Interconnectivity hub</sub> | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <sub>Create TLS key pair for SSH and Import to Platform</sub> | :white_check_mark: | :no_entry_sign: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :no_entry_sign: | :no_entry_sign: | :white_check_mark: |
| <br/>***Bastion Injection*** |   |   |   |   |   |   |   |   |   |
| <sub>Create Subnet and Network Security for Bastion</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <sub>Create Bastion host and Public IP address</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <br/>***Host Network Access for SAP*** |   |   |   |   |   |   |   |   |   |
| <sub>Append Network Security rules for SAP</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <br/>***Host Provision*** |   |   |   |   |   |   |   |   |   |
| <sub>Create DNS Records (i.e. A, CNAME, PTR)</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | N/A | N/A | N/A | N/A |
| <sub>Create Storage Volumes (Profile or Custom IOPS)</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :warning:<br/><sub>no custom IOPS</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <sub>Create Host/s</sub> | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| <br/>***High Availability*** |   |   |   |   |   |   |   |   |   |
| <sub>Create Resources (e.g. Load Balancer)</sub> | N/A | :x: | :x: | :x: | N/A | N/A | N/A | N/A | N/A |

<sub>**Key:**</sub>
- :white_check_mark: <sub>Ready and Tested</sub>
- :warning: <sub>Work in Progress</sub>
- :x: <sub>Not available</sub>
- :no_entry_sign: <sub>Capability not provided by vendor (or construct concept does not exist)</sub>
- <sub>N/A: Not Applicable</sub>
