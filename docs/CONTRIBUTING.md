# Contributing guidelines for Ansible Playbooks for SAP

This document outlines the contribution guidelines for the Ansible Playbooks for SAP. Please read it carefully before submitting any changes.

## Guiding principle
All scenarios in `main` branch are self-contained and they should work when copied outside of Ansible Playbooks for SAP.
Example: The playbook `sap_hana_ha` should still work when `sap_hana_ha` folder is copied elsewhere.

## Terminology
- **Scenario**, means the SAP Software Solution/Product which runs upon a target Infrastructure Platform using a Deployment Topology (inc. Installation Type).  
- **Deployment Topology**, means either a Sandbox, Standard, Distributed or High Availability SAP System design has been implemented using different installation types to one or more hosts.  
- **Installation Type**, means a different component of SAP Software has been installed by hdblcm or SAP SWPM with a specific runtime design and layout (e.g. SAP HANA Scale-Up using MDC and TDI-sized storage for OLTP workloads, with High Availability using SAP HANA System Replication in Asynchronous mode).  
- **Layout**, refers to the virtual/physical hardware components such as LVM Virtual Groups with striping/mirroring using Block Storage attached to Virtual Machine/s.

## Branch Protection
The following branches are present in repository:
- `dev` - Development branch, where we merge from forks. No direct commits, only pull requests from forks.
- `stage` - Stable branch is used for releases that reflects `dev` branch. No direct commits, only pull requests from `dev`.
- `main` - Main default branch, that is created by transformation of `stage` branch. No direct commits or pull requests.

## Main branch transformation process
`dev > stage > main`

1. Changes are merged to `dev` branch from fork of `dev` using pull request.
2. Release process is triggered by pull request from `dev` to `stage`.
3. GitHub action `publish-stage-to-main.yml` will trigger on `stage` changes:
4. Clone `stage` branch to github action runner.
5. Copy `common_fragments/tasks` into all `deploy_scenarios` folders.
6. Combine extra vars fragments in following order (example for AWS):
   - `ansible_extravars_aws_ec2_vs_base.yml`
   - `common_fragments/vars/platform_vars_aws_ec2_vs.yml`
   - `ansible_extravars_aws_ec2_vs_spec.yml`
   - `common_fragments/vars/platform_images_aws_ec2_vs.yml`
7. Append all platform spec and image files to `optional/ansible_extravars_interactive.yml`.
8. Distribute `optional/ansible_requirements.yml` to all `deploy_scenarios`.
9. Remove `common_fragments` folder.
10. Compare current transformed state of `stage` branch against current `main` branch.
11. Create commit and push to `main` only if changes were detected.

### Benefits of the transformation process
- All shared variables can be defined in `common_fragments`.
- All shared tasks can be defined in `common_fragments`.
- Promotes code reuse and reduces redundancy across different scenarios.
- Simplifies maintenance by centralizing common configurations and tasks.
- Ensures consistency in configurations and task execution across various scenarios.

## Testing
Before submitting a pull request, please ensure that your changes have been thoroughly tested.  

Testing in `dev` branch requires including all relevant fragments.  

### Example for scenario on AWS:
```bash
ansible-playbook ansible_playbook.yml \
 --extra-vars "@./ansible_extravars.yml" \
 --extra-vars "@./ansible_extravars_aws_ec2_vs_base.yml" \
 --extra-vars "@./ansible_extravars_aws_ec2_vs_spec.yml" \
 --extra-vars "@../../common_fragments/vars/platform_vars_aws_ec2_vs.yml" \
 --extra-vars "@../../common_fragments/vars/platform_images_aws_ec2_vs.yml"
```


## Code Style and Documentation
Please adhere to the following guidelines:
- Follow Ansible best practices for writing playbooks, roles, and tasks.
- Use clear and descriptive names for variables, tasks, and files.
- Include comments to explain complex logic or non-obvious configurations.
- Document roles, playbooks, and variables in their respective README files.
