# Interactive Prompts for Ansible Playbooks for SAP

## Description
This folder contains a set of tasks that provide interactive prompts for deployment scenarios in Ansible Playbooks for SAP.

These prompts dynamically gather user input during playbook execution, eliminating the need to predefine all configuration variables.


## Variables for Controlling Interactive Prompts
The interactive prompts in this folder use the following variables to determine which questions to ask the user during playbook execution.<br>
These variables are defined in `optional/ansible_extravars_interactive.yml` in supported deployment scenarios.<br>
Changing these variables can result in execution without all required variables.

### sap_playbook_interactive_product
- **Type:** `string`<br>
- **Description:** Specifies the name of the SAP Product<br>
- **Note:** Some scenarios are using similar product name, if there are no differences in prompts. Example: `sap4hana` for both `sap4hana` and `bw4hana`<br>
- **Available options:** `bw4hana, ecc, s4hana, nwas_abap, nwas_java, solman`<br>
- **Example:** `s4hana`

### sap_playbook_interactive_database
- **Type:** `string`<br>
- **Description:** Specifies the name of the SAP Database<br>
- **Available options:** `hana, ibmdb2, sapase, oracledb, sapmaxdb`<br>
- **Example:** `hana`

### sap_playbook_interactive_layout
- **Type:** `string`<br>
- **Description:** Specifies the deployment topology (layout) of the SAP System<br>
- **Available options:** `sandbox, standard_scaleout, standard, distributed, distributed_ha, hana_ha, hana_scaleout`<br>
- **Example:** `distributed_ha`


## Supported scenarios
This table lists the supported combinations of SAP products, databases, and layouts, along with the corresponding Ansible groups.

| Scenario                               | Product    | Database   | Layout            | Ansible Groups |
| -------------------------------------- | ---------- | ---------- | ----------------- | --- |
| sap_bw4hana_sandbox                    | bw4hana    | hana       | sandbox           | hana_primary |
| sap_bw4hana_standard_scaleout          | bw4hana    | hana       | standard_scaleout | hana_primary, nwas_pas |
| sap_ecc_hana_sandbox                   | ecc        | hana       | sandbox           | hana_primary  |
| sap_ecc_ibmdb2_distributed             | ecc        | ibmdb2     | distributed       | anydb_primary, nwas_ascs, nwas_pas, nwas_aas  |
| sap_ecc_ibmdb2_distributed_ha          | ecc        | ibmdb2     | distributed_ha    | anydb_primary, anydb_secondary, nwas_ascs, nwas_ers, nwas_pas, nwas_aas  |
| sap_ecc_ibmdb2_sandbox                 | ecc        | ibmdb2     | sandbox           | nwas_pas |
| sap_ecc_oracledb_sandbox               | ecc        | oracledb   | sandbox           | nwas_pas |
| sap_ecc_sapase_sandbox                 | ecc        | sapase     | sandbox           | nwas_pas  |
| sap_ecc_sapmaxdb_sandbox               | ecc        | sapmaxdb   | sandbox           | nwas_pas |
| sap_hana                               | hana       | hana       | sandbox           | hana_primary |
| sap_hana_ha                            | hana       | hana       | hana_ha           | hana_primary, hana_secondary |
| sap_hana_scaleout                      | hana       | hana       | hana_scaleout     | hana_primary |
| sap_ides_ecc_hana_sandbox              | ecc        | hana       | sandbox           | hana_primary |
| sap_ides_ecc_ibmdb2_sandbox            | ecc        | ibmdb2     | sandbox           | nwas_pas |
| sap_nwas_abap_hana_sandbox             | nwas_abap  | hana       | sandbox           | hana_primary |
| sap_nwas_abap_ibmdb2_sandbox           | nwas_abap  | ibmdb2     | sandbox           | nwas_pas |
| sap_nwas_abap_oracledb_sandbox         | nwas_abap  | oracledb   | sandbox           | nwas_pas |
| sap_nwas_abap_sapase_sandbox           | nwas_abap  | sapase     | sandbox           | nwas_pas |
| sap_nwas_abap_sapmaxdb_sandbox         | nwas_abap  | sapmaxdb   | sandbox           | nwas_pas |
| sap_nwas_java_ibmdb2_sandbox           | nwas_java  | ibmdb2     | sandbox           | nwas_pas |
| sap_nwas_java_sapase_sandbox           | nwas_java  | sapase     | sandbox           | nwas_pas |
| sap_s4hana_distributed                 | s4hana     | hana       | distributed       | hana_primary, nwas_ascs, nwas_pas, nwas_aas |
| sap_s4hana_distributed_ha              | s4hana     | hana       | distributed_ha    | hana_primary, hana_secondary, nwas_ascs, nwas_ers, nwas_pas, nwas_aas |
| sap_s4hana_distributed_ha_maintplan    | s4hana     | hana       | distributed_ha    | hana_primary, hana_secondary, nwas_ascs, nwas_ers, nwas_pas, nwas_aas |
| sap_s4hana_distributed_maintplan       | s4hana     | hana       | distributed       | hana_primary, nwas_ascs, nwas_pas, nwas_aas |
| sap_s4hana_foundation_sandbox          | s4hana     | hana       | sandbox           | hana_primary |
| sap_s4hana_foundation_standard         | s4hana     | hana       | standard          | hana_primary, nwas_pas |
| sap_s4hana_sandbox                     | s4hana     | hana       | sandbox           | hana_primary |
| sap_s4hana_sandbox_maintplan           | s4hana     | hana       | sandbox           | hana_primary |
| sap_s4hana_standard                    | s4hana     | hana       | standard          | hana_primary, nwas_pas |
| sap_s4hana_standard_maintplan          | s4hana     | hana       | standard          | hana_primary, nwas_pas |

**NOTE** Ansible Groups are a list of defined `sap_host_type` variables in `host_specifications_dictionary`.

## Execution
Interactive Prompts are the first play in a deployment scenario, and they run if their files are present.

```yaml
- name: Ansible Play to Interactively gather all mandatory variables
  hosts: localhost
  gather_facts: false
  pre_tasks:

    - name: Block for collection for interactive prompts
      when:
        - sap_playbook_interactive_product is defined and sap_playbook_interactive_product | length > 0
        - sap_playbook_interactive_database is defined and sap_playbook_interactive_database | length > 0
        - sap_playbook_interactive_layout is defined and sap_playbook_interactive_layout | length > 0
      block:
        - name: Check if interactive tasks are available
          ansible.builtin.stat:
            path: optional/tasks/interactive/main.yml
          register: sap_playbook_interactive_tasks_availability
          ignore_errors: true

        - name: Execute collection of interactive inputs
          ansible.builtin.include_tasks:
            file: optional/tasks/interactive/main.yml
          when: sap_playbook_interactive_tasks_availability.stat.exists
```

### Execution Flow
1. Gather `sap_vm_provision_iac_type`, `sap_vm_provision_iac_platform` and `sap_software_product`.
2. Gather variables defined in `host_specifications_dictionary` variable.
3. Process the `host_specifications_dictionary` to determine the required Ansible groups.
4. Gather infrastructure platform variables using task file in `platforms` folder.
5. Gather database variables using task file in `databases` folder.
   - Gather High Availability variables when `sap_playbook_interactive_layout: distributed_ha or hana_ha`.
6. Gather SWPM variables.
   - Gather High Availability variables when `sap_playbook_interactive_layout: distributed_ha`.
7. (Optional) Gather `community.sap_launchpad` variables if collection is detected.
   - The `community.sap_launchpad` collection is used for downloading SAP Installation Media.

### Default values
Many variables allow you to skip the prompt and use a default value.</br>
Example: `Press enter to skip and use the default value ('n').`

Each default value is carefully chosen based on the selected deployment scenario.</br>

### Variable validation
Each variable is validated, including defined variables, to ensure that:
- The variable is not empty or placeholder value.
- The variable is of the expected length, if applicable (e.g., SAP System ID being 3 characters).
- The variable is of the expected type, if applicable (e.g., Boolean instead of String).
- The variable has an expected value when available options are presented.

### Error handling
Following errors are handled by validations:

1. **Missing or Empty Dictionary**: A required dictionary is not defined or is empty. This can occur if a dictionary like `sap_software_install_dictionary` is missing or has no entries. Example:
    ```console
    Variable 'sap_software_install_dictionary' is undefined or empty.
    Correct this variable in extra vars and re-run the playbook.
    ```

2. **Invalid value (Defined in extra vars)**: A defined variable fails validation. Example:
    ```console
    Invalid value for variable 'sap_software_product': wrong_product
    Available options: sap_bw4hana_2023_sandbox sap_bw4hana_2022_sandbox sap_bw4hana_2021_sandbox
    Correct this variable in extra vars or remove it from extra vars to enable interactive prompt.
    ```

3. **Invalid value (User Input)**: User input from a prompt fails validation. Example:
    ```console
    Invalid value for variable 'sap_software_product': wrong_product
    Available options: sap_bw4hana_2023_sandbox sap_bw4hana_2022_sandbox sap_bw4hana_2021_sandbox
    Re-run the playbook and provide a valid input.
    ```

## License
Apache 2.0

## Maintainers
- [Marcel Mamula](https://github.com/marcelmamula)
