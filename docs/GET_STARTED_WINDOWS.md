# Getting Started - Windows

The following guidance describes how to execute an Ansible Playbook, and optionally connect to VS Code for code extension and amendments.

## Setup Shell, Python and Ansible

When an Ansible Playbook is executed from a Unix-based OS (e.g. macOS, Linux etc) and executes to a target host with a Windows OS, compatibility exists in various Ansible Collections/Roles/Modules. However, when an Ansible Playbook is executed from a Windows OS (i.e. [Windows OS acting as the 'Ansible Controller'](https://docs.ansible.com/ansible/latest/os_guide/windows_faq.html#can-ansible-run-on-windows)), then Ansible is incompatible with Windows due to Ansible Core's usage of the fcntl Python Module.


Therefore to execute Ansible Playbooks from a Windows OS host (e.g. Windows laptop), alternative methods are required such as:

**RECOMMENDED:** [Windows Subsystem for Linux v2 (WSL2)](https://learn.microsoft.com/en-us/windows/wsl/compare-versions) with Linux OS Distribution WSL2 Image (e.g. Ubuntu, Debian, OpenSUSE, Fedora Remix)

**ALTERNATIVE:** Virtual Machine with Linux OS Distribution (e.g. using Oracle VM VirtualBox, VMware Workstation, Windows Hyper-V)


The following focuses on the WSL2 recommended method.

> Please note if not reading this documentation on GitHub or a Markdown reader, the ` backtick denotes a command to copy - do not copy the backtick itself as Windows PowerShell syntax considers this a new line.

1. Download and Install Windows Terminal for simplified terminal usage, please see: https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701
2. From Windows Terminal, open Windows PowerShell and check if Windows Subsystem for Linux v2 (WSL2) is installed. Use `wsl --version`. An error will appear if this is not installed, a help menu will be displayed if the version is old, and newer versions will show the version details
3. If not installed, use `wsl --install` and follow the prompts. If an oudated version, use `wsl --update`. Once WSL2 is updated, reboot the device
4. Perform install of WSL2 with the Ubuntu OS using `wsl --install -d Ubuntu`. Follow all proceeding steps (password prompts etc). For additional information and troubleshooting, please see documentation for further details: https://aka.ms/wsl2-install
5. Update `apt`, using `sudo apt update`
6. Install core Python Packages, using `sudo apt install python3-pip python3-venv`
7. Upgrade `python3`, using `sudo apt upgrade python3`
8. Then check the System Python version with `python3 --version`, from which the Python virtual environment will be created
9. Create the Python virtual environment, using `python3 -m venv ~/.py_venv/py_ansible` (ensure not to use sudo, otherwise permissions will block any pip installations later on)
10. Activate the Python virtual environment, using `source ~/.py_venv/py_ansible/bin/activate`. The Shell session will now display `(py_ansible)` at the front of the Shell prompt
11. Run `python3 -m pip install --upgrade pip`
12. Install Ansible to the virtualised Python environment...
    - **RECOMMENDED:** Install Ansible Community Edition (containing Ansible Core) and other Python Packages, using `python3 -m pip install ansible ansible-lint beautifulsoup4 lxml requests passlib jmespath`
    - **ALTERNATIVE:** Install Ansible Core and other Python Packages, using `python3 -m pip install ansible-core ansible-lint beautifulsoup4 lxml requests passlib jmespath`
13. **OPTIONAL:** Confirm Ansible Core version used with `ansible --version`
14. **OPTIONAL:** Test exiting of this virtualised Python environment, using `deactivate`. The `ansible --version` will not work anymore as the Python Packages are not installed to the System Python
15. Amend the Bash Profile (`~/.bashrc`) to use the Python virtual environment automatically (when loaded by VS Code) by appending `source ~/.py_venv/py_ansible/bin/activate` to the end of the file (if added before the end of the Bash Profile, the Shell Prompt will not show the Python virtual environment has been loaded)
16. Lastly, it is strongly recommended to increase your history using Bash Profile (`~/.bashrc`) environment variables as automation for SAP can result in significant output by changing history variables to `HISTSIZE=50000` and `HISTFILESIZE=50000`


## Run an Ansible Playbook for SAP

### Download

From Windows Terminal, open Ubuntu and download the latest Ansible Playbooks for SAP from [github.com/sap-linuxlab/ansible.playbooks_for_sap/releases](https://github.com/sap-linuxlab/ansible.playbooks_for_sap/releases)

For example, `mkdir -p run_playbooks && cd run_playbooks && curl -L https://github.com/sap-linuxlab/ansible.playbooks_for_sap/archive/refs/tags/1.0.0.zip | tar -xzv`

### Execute an Ansible Playbook

1. Once downloaded, open the directory with the Ansible Playbook you want to execute. For example SAP HANA installation, `cd $PWD/run_playbooks/ansible.playbooks_for_sap-1.0.0/deploy_scenarios/sap_hana`
2. Choose your preferred method for inputting variables - Interactive Prompt, Standard (Non-Interactive). For example an Interactive Prompt, `ansible-playbook ansible_playbook.yml --extra-vars "@./ansible_extravars.yml"`. More details are covered in the main documentation under [Example execution of Ansible Playbooks for SAP](./README.md#example-execution-of-ansible-playbooks-for-sap), and is dependent on whether the desired outcome is using Existing Hosts, Hosts provisioned via Ansible to an existing environment, or using Ansible to Terraform to provision an environment and hosts


## OPTIONAL - Code extension and amendments

Optionally connect to VS Code for code extension and amendments. This is the same requirement for code development and contributions back to the open-source community.

### Ansible Core configuration

**OPTIONAL:**
By default, Ansible Core will output error or debug (-v) messages as a string. For easier readability, it is easy to configure Ansible Core to parse the error or debug messages and output as YAML that is easier to read, create/amend the `~/.ansible.cfg` file:
```ini
[defaults]
# Use the YAML callback plugin.
stdout_callback = yaml
# Use the stdout_callback when running ad-hoc commands.
bin_ansible_callbacks = True
```

### Install VS Code (IDE) and Ansible 

Install VS Code (it is strongly recommended to use the installer, and not install via the Microsoft Store app):
https://code.visualstudio.com/

Upon first open of VS Code, a prompt will be displayed: `The host 'wsl$' was not found in the list of allowed hosts. Do you want to allow it anyway?`. Use 'Permenantly allow host wsl$' and click 'Allow'.

Once installed, use the left-side icon list (by default 4th from top) to open `Extensions` (or use `Settings > Extensions`).

To ease configuration and alterations for your SAP automation requirements via Ansible Playbooks, the following are recommended Extensions:
- Ansible. Ansible Language Support, by Red Hat
- Python. Python integration, by Microsoft (default installed by Ansible extension)
- WSL. Open any folder in the WSL, by Microsoft

**OPTIONAL:**
Other popular Extensions which may help development in future include:
- One Dark Pro. Theme to make VS Code look like Atom's One Dark
- indent-rainbow. Makes indentation easier to read

**OPTIONAL:**
Other popular Extensions specific to SAP code development include:
- SAP Workbench. Theme to make VS Code look like SAP Workbench
- Standalone ABAP Development Extension Pack. Multiple extensions for standalone ABAP development (includes ABAP Language Support and Linting), by Lars Hvam
- SAP Fiori Tools - Extension Pack. Multiple extensions for SAP Fiori app development, by SAP

Restart VS Code, which will enable the Extensions.

Use the left-side icon list to open `Remote Explorer`, and under 'WSL Targets' will be the Ubuntu OS. Right-click to 'Set as Default Distro' and then 'Connect to WSL'. This will set Ubuntu Terminal as the integrated terminal for VS Code. For more information, please see https://code.visualstudio.com/docs/remote/wsl-tutorial .

Thereafter, the bottom left corner will show 'Ubuntu' after a few minutes upon opening VS Code each time.

From the VS Code Integrated Terminal (CTRL + J), all Linux commands can now be used from the Windows host machine. For example, `mkdir -p code_repos && cd code_repos && git clone https://github.com/sap-linuxlab/ansible.playbooks_for_sap` will pull from GitHub.

Once the code repo directories exist inside Ubuntu, the directories can be directly opened in VS Code by using 'Explorer' at top of the left-side panel of VS Code (or using CTRL + SHIFT + E), under the 'Connected to remote.' then click 'Open Folder' to choose from a list of directories inside Ubuntu and click 'OK'.

Thereafter, right-click of any directory in the VS Code Explorer pane and use 'Open in Integrated Terminal' to create a Shell Session in the chosen directory to execute the Ansible Playbook. For example, the `~/code_repos/ansible_playbook_repo` cloned could contain `~/code_repos/ansible_playbook_repo/playbook_01` and then `(py_ansible) user@laptop1:~/code_repos/ansible_playbook_repo/playbook_01$ ansible-playbook file.yml`.

From Windows Explorer, the Ubuntu Linux filesystem is available under 'Linux' shown in the Windows Explorer Navigation Pane on the left-side.
