# FAQ

Table of Contents:
- [Customized deployments of Ansible Playbooks for SAP](#customized-deployments-of-ansible-playbooks-for-sap)
- [SAP Software Download common errors](#sap-software-download-common-errors)
- [SAP System Password Recommendations](#sap-system-password-recommendations)
- [High Availability](#high-availability)


## Customized deployments of Ansible Playbooks for SAP
---

### <samp>I'm an SAP Customer, can I use and amend this code for custom business purposes?</samp>

**Yes.** All code is under the Apache license, you can extend and use for internal purposes without any concerns. All feedback and contributions back to the project are appreciated.

### <samp>I'm an SAP Services Partner, can I use and amend this code to create new products/offerings for customers?</samp>

**Yes.** All code is under the Apache license you can extend and use for commercial purposes without any concerns. All feedback and contributions back to the project are appreciated.

### <samp>How to provision larger SAP Systems?</samp>

Please read [Customization of Ansible Playbooks for SAP](./README.md#customization-of-ansible-playbooks-for-sap) in the main documentation. The host specifications are completely customisable.

### <samp>How to use custom OS Images on each Cloud Hyperscaler?</samp>

Each Ansible Playbook for SAP used with a Cloud Hyperscaler, includes an OS Image lookup by name for all available OS Images from the Cloud Service Provider.

The Ansible Extravars file contains a list these OS Image lookup names (such as `sles-15-2-sap-ha` or `rhel-8-4-sap-ha`) and refer to a regex pattern specific to that Cloud Hyperscaler to retrieve the latest OS Image for the specific OS distribution version (i.e. major.minor release). This list can be appended to with custom OS Images as required.

### <samp>How to deploy to specific locations on each Cloud Hyperscaler?</samp>

Each Ansible Playbook for SAP used with a Cloud Hyperscaler, provides the user with the choice of Region and Availability Zone.

In principle, each Cloud Service Provider uses the same geographical location logic:
- Region (alt. Location Display Name)
  - Availability Zone (aka. Data center)
    - Placement segmentation within a Data center; known by various names e.g. Placement Groups / Physical Fault Domains / Pods etc.

<br/>

## SAP Software Download common errors
---

### <samp>SAP Software installation media downloads have error 'SAP SSO authentication failed - 401 Client Error'</samp>

SAP software installation media must be obtained from SAP directly, and requires valid license agreements with SAP in order to access these files.

The error HTTP 401 refers to either:
- Unauthorized, the SAP User ID being used belongs to an SAP Company Number (SCN) with one or more Installation Number/s which do not have license agreements for these files
- Unauthorized, the SAP User ID being used does not have SAP Download authorizations
- Unauthorized, the SAP User ID is part of an SAP Universal ID and must use the password of the SAP Universal ID
  - In addition, if a SAP Universal ID is used then the recommendation is to check and reset the SAP User ID ‘Account Password’ in the [SAP Universal ID Account Manager](https://account.sap.com/manage/accounts), which will help to avoid any potential conflicts.

This is documented:
- full detail under [Ansible Collection for SAP Launchpad - Requirements, Dependencies and Testing](https://github.com/sap-linuxlab/community.sap_launchpad#requirements-dependencies-and-testing)

### <samp>SAP Software installation media from SAP Maintenance Planner fails with 'download link `https://softwaredownloads.sap.com/file/___` is not available'</samp>

SAP has refreshed the installation media (new revisions or patch levels) for the files in your SAP Maintenance Planner stack, and you will need to update / create a new plan to re-generate the up to date files.

### <samp>SAP Software installation media downloads from SAP Maintenance Planner fails with 'SAP SSO authentication failed - 404 Client Error: Not Found for url: `https://origin.softwaredownloads.sap.com/tokengen/?file=___`'</samp>

SAP has refreshed the installation media (new revisions or patch levels) for the files in your SAP Maintenance Planner stack, and you will need to update / create a new plan to re-generate the up to date files.

### <samp>SAP Software Center search has error 'An exception has occurred - no result found for `FILENAME_HERE.SAR`'</samp>

SAP has refreshed the installation media (new revisions or patch levels), this filename cannot be found and you will need to search for the updated filename (usually an increment, e.g. `_0` to `_1` otherwise the file cannot be downloaded.

### <samp>SAP Software installation media pre-check (dry-run) or downloads have error 'SAP SSO authentication failed - 403 Client Error: Forbidden for url: `https://softwaredownloads.sap.com/file/___`'</samp>

SAP Software Center is likely experiencing temporary problems, please try again later. The Ansible Collection for SAP Launchpad will always attempt 3 retries if a HTTP 403 error code is received, if after 3 attempts the file is not available then a failure will occur.

<br/>

## SAP System Password Recommendations
---

Ansible Playbooks for SAP do not use any default password and they must be set before executing playbooks.

### SAP Databases

#### SAP HANA

* **Length:** Between 6 and 64 characters (recommended by SAP).
* **Avoid Characters (observed issues during SAP installations/SWPM):**
    * Space character (` `) is generally not advisable.
    * **Note:** SAP HANA is generally more flexible with special characters, but the most common issues arise from characters that conflict with shell or client parsing.
* **Example:** `HanaP@ssw0rd!`
    * **WARNING: This is an example password and MUST NOT be used in any production or sensitive environment.**
* **References:**
    * [SAP HANA Security Guide for SAP HANA Platform - Password Policy](https://help.sap.com/docs/SAP_HANA_PLATFORM/b3ee5778bc2e4a089d3299b82ec762a7/dce2826dbb571014be628d6279aeeaa3.html?locale=en-US)
    * [SAP Note 2969917 - Can't use special characters like ! @ # $ % & in HANA user's password](https://me.sap.com/notes/2969917)

#### SAP Sybase ASE

* **Length:** Typically 6 to 30 characters (can be customized by policy).
* **Avoid Characters (observed issues during SAP installations/SWPM):**
    * Spaces, single quotes (`'`), double quotes (`"`), backticks (`` ` ``), backslashes (`\`).
    * **Other potentially problematic characters:** `(`, `)`, `[`, `]`, `{`, `}`, `;`, `:`, `,`, `.`, `/`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `+`, `=`, `<`, `>`, `?`, `|`, `~`.
* **Example:** `ASEP@ssw0rd!`
    * **WARNING: This is an example password and MUST NOT be used in any production or sensitive environment.**

#### SAP MaxDB

* **Length:** Varies by policy, typically 6 to 18 characters (check database-specific policy).
* **Avoid Characters (observed issues during SAP installations/SWPM):**
    * `#`, `$`, `_`, `>`
    * **Also avoid:** Spaces and language-specific characters (e.g., umlauts).
* **First Character Restriction:** Must not begin with a digit (`0-9`) or `_` (underscore).
* **Example:** `MaxDBPassw0rd!`
    * **WARNING: This is an example password and MUST NOT be used in any production or sensitive environment.**

#### IBM Db2

* **Length:** Typically 6 to 18 characters (can be customized by policy).
* **Avoid Characters (observed issues during SAP installations/SWPM):**
    * Spaces, double quotes (`"`), single quotes (`'`), backslashes (`\`).
    * **Other potentially problematic characters:** `(`, `)`, `;`, `|`, `<`, `>`, `!`, `#`, `&`, `*`, `?`, `~`, `$`, `%`.
* **Example:** `Db2P@ssw0rd!`
    * **WARNING: This is an example password and MUST NOT be used in any production or sensitive environment.**

#### Oracle DB

* **Length:** Varies by policy, typically 8 to 30 characters (check database-specific or policy).
* **Avoid Characters (observed issues during SAP installations/SWPM):**
    * `$`, `@`, `/`, `\`, `%`, `,`, `;`
    * **Also avoid:** Spaces.
    * **Note:** The double quote character (`"`) itself is often problematic if passwords require quoting.
* **First Character Restriction:** Must not begin with a digit (`0-9`) or `_` (underscore).
* **Example:** `OraP@ssw0rd!`
    * **WARNING: This is an example password and MUST NOT be used in any production or sensitive environment.**


### SAP System, SAP NetWeaver (Application)

* **Length:** Between 3 and 40 characters (based on default profile parameters `login/min_password_*` and `login/password_*`).
* **Characters to Avoid / Handle with Extreme Caution (observed issues with SAP NetWeaver application/tools):**
    * **Highly Problematic (avoid if possible):** Spaces (` `), backslash (`\`), double quotes (`"`), single quotes (`'`). These often cause parsing errors or require complex escaping.
    * **Potentially Problematic (test carefully):** `(`, `)`, `{`, `}`, `[`, `]`, `!`, `?`, `’`, `*`, `+`, `~`, `/`, `<`, `>`, `|`, `;`, `:`
    * **Note:** The exact set of allowed/disallowed characters can be customized via Profile Parameters (e.g., `login/password_compliance_lib` and other `login/password_*` settings).
* **Example:** `ExampleNetW$123`
    * **WARNING: This is an example password and MUST NOT be used in any production or sensitive environment.**

**References:**  
For SAP NetWeaver Application Server (ABAP) see document [Password Rules - User and Role Administration - SAP NetWeaver Application Server for ABAP 7.52](https://help.sap.com/docs/SAP_NETWEAVER_AS_ABAP_752/c6e6d078ab99452db94ed7b3b7bbcccf/4ac3efb58c352470e10000000a42189c.html?locale=en-US).  

For further information, please see [User Guides for System Provisioning with Software Provisioning Manager](https://help.sap.com/docs/SOFTWARE_PROVISIONING_MANAGER/30839dda13b2485889466316ce5b39e9/4901b2032db94b64bac87454dd94805b.html) which contains a list of different guides under two sections:

1. Installation Option of Software Provisioning Manager 2.0
    - Installation Guides - Application Server Systems - Software Provisioning Manager 2.0
2. Installation Option of Software Provisioning Manager 1.0
    - Installation Guides - Application Server Systems - Software Provisioning Manager 1.0

On each of these pages (for SWPM 1.0/2.0) there are documents (HTML/PDF) in a table with choice for `Database, Product Release, Operating System Platform, Technical Track`.  
- Each document contains layered sections 'Planning > Basic Installation Parameters > SAP System Parameters' with Password limitation information.  

For example, [SAP System Parameters - Installation of SAP ABAP Systems on UNIX : SAP HANA 2.0 - SWPM 2.0](https://help.sap.com/docs/SLTOOLSET/39c32e9783f6439e871410848f61544c/fe3f4554f82b1d5de10000000a44538d.html).  

Please note, these guides are different than those listed on [Guide Finder for SAP NetWeaver and ABAP Platform](https://help.sap.com/docs/r/nwguidefinder).

## High Availability
---

### For SAP HANA and SAP NetWeaver High Availability, what approach is used?

High Availability is achieved through STONITH (Shoot The Other Node In The Head) fencing, multiple configuration approaches that can be summarised by usage of:

1. Fencing Agents to Infrastructure Platform Authoritative Status API; this verifies health status and execute compute actions (power off) using a vendor-defined API
2. Fencing Agent for STONITH Block Device (SBD); this verifies health status using a shared disk between all HA Cluster Nodes (e.g. iSCSI, Multi-Write Block Storage / Virtual Disk) or alternatively a Watchdog, and execute self-fencing
3. Fencing Agent for Distributed Replicated Block Device (DRBD); this verifies health status using an NFS Server accessible from all HA Cluster Nodes, and execute self-fencing

The host nodes are halted using one of these approaches, to avoid an inconsistent state.

There are variances to each approach, for each Infrastructure Platform, for different SAP Software Scenarios and different Business Continuity Plans with their associated technical risk profiles (for example, HA only vs HA-DR). As such, the correct configuration of High Availability for an SAP System incorporates a range of decisions and cost implications.

The foremost recommendation (and frequently lowest cost) by each Infrastructure Platform vendor, is to leverage each vendor's respective Fencing Agent (e.g. `fence_aws`).

The Ansible Playbooks for SAP and the underlying `sap_install` Ansible Collection focus on this configuration approach, using the Fencing Agents to Infrastructure Platform Authoritative Status API. This is subject to further requests from the community and associated development contributions.
