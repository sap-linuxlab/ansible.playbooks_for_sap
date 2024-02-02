# Getting Started - Azure DevOps Pipelines

The following guidance describes how to execute an Ansible Playbook from Azure DevOps Service Pipelines:

1. Log in to Microsoft Azure
2. Open [Azure DevOps Services AEX Portal](https://aex.dev.azure.com). Create an Azure DevOps Organization (e.g. `dev.azure.com/username0111`) and select where the 'Projects' host location will be (e.g. `Europe`)
3. This will automatically open the Azure DevOps Organization URL (e.g. `https://dev.azure.com/username0111`)
4. Within the Azure DevOps Organization, create a new Project with a visibility 'Private' and provide a name (e.g. `project1`)
5. Unfortunately while "MS Hosted CI/CD" Free Tier provides 1800 minutes, the error `"No hosted parallelism has been purchased or granted"` will persistently be shown for all Pipeline Jobs (given every job is Queued in Parallel, even if only 1 job or all jobs are sequential). Open the 'Project Settings' at the bottom of the navigation menu, click 'Billing' (i.e. `https://dev.azure.com/username0111/project1/_settings/buildqueue`), then click 'Set up billing' to link the Azure DevOps Service to the Azure Subscription.
6. Once the link is completed, change the 'Paid parallel jobs' to `1`. This will remove the Free Tier minutes allowance but allow all Pipeline Jobs to function. Scroll down and click 'Save'. After this change, any Pipeline Job will now show "Agent: Hosted Agent" under "Pool: Azure Pipelines"
7. Open the 'Project Settings' again, under the Pipelines section click on 'Service connections'. From the list select 'Azure Resource Manager', then select 'Service Principal (automatic)' followed by scope level as 'Subscription' (optionally selecting a specific Resource Group intended for VM deployments) and enabling 'Grant access permission to all pipelines'. Then click 'Save'
8. Hover over 'Repos' in the navigation menu, then click 'Files'. Click 'Import a repository', use Clone URL `https://github.com/sap-linuxlab/ansible.playbooks_for_sap.git` and then 'Import'. This will clone the entire code repository and show the file structure and README (which may not be formatted correctly, as Azure DevOps Service does not use GFM Markdown). Any edits in this repository are private, and are not synchronised to the GitHub origin.
    - By default the name will be the same as the Project, to alter the Repo name then open the 'Project Settings' at the bottom of the navigation menu. Scroll down on the settings to Repositories (i.e. `https://dev.azure.com/username0111/project1/_settings/repositories`)
9. At the top of repository page, a downwards arrow will show the `main` branch as the 'Default branch' in Azure DevOps (which tracks the latest release version). Click this to choose 'Tags' to select a specific release version of the Ansible Playbooks for SAP. To change the default, use the 'Repos / Branches' page
10. Hover over 'Pipelines' in the navigation menu, then click 'Pipelines' followed by 'New pipeline'. Then select the 'Azure Repos Git' and choose the repository (e.g. `project1`) that was imported. The prompt 'Configure your pipeline' will appear, choose 'Existing Azure Pipelines YAML file' and use the Path drop-down menu to select the `/docs/sample/azure_devops_pipeline_ansible.yml`. Click Continue, then Save.
11. Once saved, click Pipelines and then 'Library', click 'Secure files' and then add the SSH Key files (Hosts Private/Public and Bastion Private).
12. After this, return to the Pipelines page and click Run, then enter the Parameters, and click Run again.

_N.B. During download of installation media, the Ansible Task appears to hang but the files are being downloaded. Azure DevOps Pipelines do not output the status (e.g. loop item downloaded successfully) until the Ansible Task has fully completed, it is especially apparent during the download but the same applies to all Ansible Tasks during the Ansible Playbook execution_

> Optional: In the top right corner, click the 'Marketplace' then use 'Browse marketplace' to install the Extension for Ansible by Microsoft (i.e. `https://marketplace.visualstudio.com/items?itemName=ms-vscs-rm.vss-services-ansible`) to the Azure DevOps Organization
