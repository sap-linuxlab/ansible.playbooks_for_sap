# Execution workflow structure

Each Ansible Playbook for SAP is for end-to-end deployment of an SAP Software solution scenario to an Infrastructure Platform.

The Infrastructure-as-Code (IaC) provisioning activities, optionally can use Ansible or Terraform:
- When provisioning hosts using Ansible, the infrastructure platform must already be setup.
- When provisioning hosts using Ansible calling Terraform, a Minimal Landing Zone and the hosts will be provisioned.
- Alternatively both can be skipped, and the Ansible Playbook use existing hosts.

Segregation of definitions for the Infrastructure and SAP Software follows this delineation:
- Ansible Dictionary to define the Host Specification templates (i.e. CPU, RAM, Storage etc). This is statically defined in the Ansible Extravars file, for example `sap_vm_provision_aws_ec2_vs_host_specifications_dictionary` and for Cloud Hyperscaler's also `sap_vm_provision_aws_ec2_vs_host_os_image_dictionary`. Default sizes for Extra Small SAP Systems are provided.
- Ansible Dictionary to define the SAP Software installation / SAP System templates. This is statically defined in the Ansible Extravars file, for example `sap_swpm_templates_install_dictionary` and other `sap_`prefix Ansible Variables.

Within each Ansible Playbook, there are various Ansible Tasks for handling the infrastructure/hosts. Afterwards, the referenced Ansible Collection Role/s for configuration of OS and installation of SAP software is identical for each Infrastructure Platform.

<br/>

**Execution of this modular and nested structure used in these end-to-end deployment Ansible Playbooks for SAP, is shown in the example below:**

**Ansible Playbook for SAP solution scenario `ansible_playbook.yml`:**
- Non-Interactive (Standard)
    - Include multiple Ansible Extravars file
    - OPTIONAL: Include Ansible Inventory, skip all provisioning and use existing hosts
- Interactive
    - Prompt IAC Provisioning choice (Ansible, Ansible to Terraform, Existing Hosts)
    - Prompt Infrastructure Platform choice
- Execute Ansible Role `sap_vm_provision` from the Ansible Collection `sap_infrastructure`
    - Execute Ansible Tasks for the chosen Infrastructure Platform; call Infrastructure Platform APIs
        - If Ansible, loop for VM and storage provisioning per definition in the `*_host_specifications_dictionary` for the chosen Infrastructure Platform and use existing network and bastion setup
        - If Ansible to Terraform, execute Terraform Modules for SAP to bootstrap minimal landing zone  (e.g. Networking, DNS, SSH Key), then loop for VM and storage provisioning per definition in the `*_host_specifications_dictionary` for the chosen Infrastructure Platform
    - Critical OS tasks for VM, such as enable Root OS Login
- Execute various Ansible Roles from the Ansible Collection `sap_install`
    - Within each Ansible Role, execute Ansible Tasks for RHEL/SLES OS pre-configuration for SAP, SAP HANA install, SAP SWPM installs etc.
        - Ansible Tasks using built-in Ansible Modules, e.g. built-in for POSIX Shell:
            - OS CLI/binaries
            - Vendor CLI/binaries (i.e. SAP Software CLI/binaries)
        - Ansible Tasks using customized Ansible Modules:
            - Shell scripts --> OS and Vendor CLI/binaries
            - Python scripts
