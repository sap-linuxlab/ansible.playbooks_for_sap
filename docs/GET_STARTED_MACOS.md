# Getting Started - macOS

The following guidance describes how to execute an Ansible Playbook, and optionally connect to VS Code for code extension and amendments.

## Setup Shell, Python and Ansible

1. Follow instructions to install [Homebrew from https://brew.sh](https://brew.sh/) as a package manager for macOS
2. **OPTIONAL:** It is recommended to install Bash 5.x shell (instead of default Zsh 5.9 using ~/.zprofile and alternative Bash 3.2 using ~/.bashrc on macOS). Use `brew install bash`
    - Confirm Zsh default version, use `$ /bin/zsh --version` and output `zsh 5.9`
    - Confirm Bash default version, use `$ /bin/bash --version` and output `GNU bash, version 3.2.57(1)-release`
    - Confirm Bash 5.x version, use `$ /opt/homebrew/bin/bash --version` and output `GNU bash, version 5.2.21(1)-release`
3. **OPTIONAL:** It is recommended to install iTerm, a macOS Terminal Replacement. Use `brew install --cask iterm2`
4. **OPTIONAL:** It is recommended to install various OS Packages. Use `brew install git grep jq terraform yq`
5. **NOT RECOMMENDED:** Use Homebrew to directly install Ansible Community Edition (containing Ansible Core). _It is not recommended because this can result in an unclean installation of Homebrew and the Python version later on - which requires significant effort to resolve._
6. It is recommended to install a later version of Python3 for the user such as Python 3.12 (to avoid conflicts with the System Python default to Python 3.9.x on macOS). Use `brew install python@3.12`
7. Use the Python3 installed by Homebrew, to create a Python virtual environment. Use `/opt/homebrew/bin/python3 -m venv ~/.py_venv/py_ansible`. In this example, built-in venv is used but other virtual methods are possible (such as pyenv-virtualenv).
8. Activate the Python virtual environment, using `source ~/.py_venv/py_ansible/bin/activate`. The Shell session will now display `(py_ansible)` at the front of the Shell prompt
9. Run `python3 -m pip install --upgrade pip`
10. Install Ansible to the virtualised Python environment...
    - **RECOMMENDED:** Install Ansible Community Edition (containing Ansible Core) and other Python Packages, using `python3 -m pip install ansible ansible-lint beautifulsoup4 lxml requests passlib jmespath`
    - **ALTERNATIVE:** Install Ansible Core and other Python Packages, using `python3 -m pip install ansible-core ansible-lint beautifulsoup4 lxml requests passlib jmespath`
11. **OPTIONAL:** Confirm Ansible Core version used with `ansible --version`
12. **OPTIONAL:** Test exiting of this virtualised Python environment, using `deactivate`. The `ansible --version` will not work anymore as the Python Packages are not installed to the System Python
13. Lastly, it is strongly recommended to increase your history using Bash Profile (`~/.bashrc`) environment variables as automation for SAP can result in significant output by changing history variables to `HISTSIZE=50000` and `HISTFILESIZE=50000`


## Run an Ansible Playbook for SAP

### Download

From iTerm or the macOS default Terminal, download the latest Ansible Playbooks for SAP from [github.com/sap-linuxlab/ansible.playbooks_for_sap/releases](https://github.com/sap-linuxlab/ansible.playbooks_for_sap/releases)

For example, `mkdir -p ~/run_playbooks && cd ~/run_playbooks && curl -L https://github.com/sap-linuxlab/ansible.playbooks_for_sap/archive/refs/tags/1.0.0.zip | tar -xzv`

### Execute an Ansible Playbook

1. Once downloaded, open the directory with the Ansible Playbook you want to execute. For example SAP HANA installation, `cd ~/run_playbooks/ansible.playbooks_for_sap-1.0.0/deploy_scenarios/sap_hana`
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

Install VS Code for macOS:
https://code.visualstudio.com/

Upon first open of VS Code, a prompt will be displayed: `The host 'wsl$' was not found in the list of allowed hosts. Do you want to allow it anyway?`. Use 'Permenantly allow host wsl$' and click 'Allow'.

Once installed, use the left-side icon list (by default 4th from top) to open `Extensions` (or use `Settings > Extensions`).

To ease configuration and alterations for your SAP automation requirements via Ansible Playbooks, the following are recommended Extensions:
- Ansible. Ansible Language Support, by Red Hat
- Python. Python integration, by Microsoft (default installed by Ansible extension)

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

Open `Settings` to configure default VS Code settings, under the 'User' tab:
- Features - Terminal - Integrated - **"Default Profile: Osx"** - 'bash' (/opt/homebrew/bin/bash --login)
- Features - Terminal - Integrated - **"Scrollback"** - '50000'
- Extensions - Ansible - Python - **"Default Interpreter Path"** - '~/.py_venv/py_ansible/bin/python3'
- Extensions - Ansible - Python - **"Activation Script"** - '~/.py_venv/py_ansible/bin/activate'
- Extensions - Python - Default Interpreter Path - '~/.py_venv/py_ansible/bin/python3'
- Extensions - Python - **"Venv Path"** - '~/.py_venv'

After which, the VS Code settings file for 'User' (~/Library/Application Support/Code/User/settings.json) will look similar to:
```json
{
    "terminal.integrated.defaultProfile.osx": "bash",
    "terminal.integrated.scrollback": 50000,
    "ansible.python.interpreterPath": "~/.py_venv/py_ansible/bin/python3",
    "ansible.python.activationScript": "~/.py_venv/py_ansible/bin/activate",
    "python.defaultInterpreterPath": "~/.py_venv/py_ansible/bin/python3",
    "python.venvPath": "~/.py_venv",
}
```

**CAUTION:**

Unfortunately, in newer versions of VS Code the default may not be respected in the integrated terminal (CMD + J) when a new VS Code window is created / when VS Code is restarted; the default will work when any Python file is opened and parsed by VS Code.

The end user is forced to open the Command Palette (CMD + SHIFT + P) and run 'Python: Select Interpreter' where the user will be presented the option 'Use Python from python.defaultInterpreterPath' - and then the integrated terminal will reflect the selected Python environment. Or activate the Python virtual environment manually with `source ~/.py_venv/py_ansible/bin/activate`.

As a workaround, append `source ~/.py_venv/py_ansible/bin/activate` to .bash_profile used by Bash 5.x installed via Homebrew (used by iTerm), and this will force this Python environment to always be used by VS Code.

**NOTE:**

If iTerm opens with Zsh or Bash but does not respect the .bash_profile settings, then change `Settings - Profiles - Default - General` 'Command' with default set to '/opt/homebrew/bin/bash' from using the 'Command' in the drop-down to using the 'Custom Shell' in the drop-down.
