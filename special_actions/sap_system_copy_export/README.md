# Ansible Playbook - SAP System Copy EXPORT

The structure of this Ansible Playbook differs from all `deploy_scenarios` in this repository:
- Designed only for targeting existing hosts

This Ansible Playbook can be executed with:
- Existing hosts

This Ansible Playbook is `EXPERIMENTAL` and only includes code for source system SAP System Export of SAP ECC EhP8 using IBM Db2.

---

## Execution of Ansible Playbook

This Ansible Playbook can only be executed against existing hosts. Upon execution, Interactive Prompts will request additional details, the user must select from the pre-defined options in the prompt.

```shell
ansible-galaxy collection install --requirements-file ./ansible_requirements.yml

TARGET_HOST_IP=""
TARGET_HOSTS_SSH_KEY_FILE="/FULL/PATH/HERE/hosts_rsa"

ansible-playbook ./ansible_playbook.yml \
--inventory "$TARGET_HOST_IP," \
--extra-vars "@ansible_extravars.yml" \
--connection 'ssh' \
--user root \
--private-key "$TARGET_HOSTS_SSH_KEY_FILE" \
--ssh-extra-args="-o ControlMaster=auto -o ControlPersist=1800s -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ForwardX11=no"
```
