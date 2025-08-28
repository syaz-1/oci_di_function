OCI Function – Data Integration Task Trigger with Notification

This repository contains an Oracle Cloud Infrastructure (OCI) Function that triggers a Data Integration (DIS) Task Run and sends the results (success or failure) to an OCI Notifications Service (ONS) topic (e.g., email, Slack, PagerDuty).

Features

Triggers a Data Integration Task Run inside a workspace.

Publishes success or failure logs to an ONS Topic.

Works with any ONS subscription (email, Slack, PagerDuty, custom HTTPS).

Packaged as a serverless function deployable with OCI Functions.

🛠 Prerequisites

Before deploying, ensure you have:

OCI CLI / Fn Project CLI installed and configured.

An OCI tenancy with:

Data Integration workspace + application + task.

Notification Service topic + subscription (e.g., email).

A local OCI config file (oci_config) with proper credentials (same format as ~/.oci/config).


## Project Structure

```text
├── func.py          # Main OCI Function code
├── requirements.txt # Dependencies (oci SDK)
├── func.yaml        # Fn Project function configuration
├── config           # OCI config (copied from ~/.oci/config)
└── README.md        # Project documentation
```

Setup Instructions

1. Clone this repository

2. Update variables in func.py

    topic_id = "ocid1.onstopic.oc1....."
    workspace_id = "ocid1.disworkspace.oc1....."
    application_key = "your-application-key"
    aggregator_key = "your-task-aggregator-key"



3. Add OCI Config
    Copy your OCI CLI config into the repo:
    cp ~/.oci/config ./oci_config

    Make sure it contains:
    [DEFAULT]
    user=ocid1.user.oc1...
    fingerprint=xx:xx:xx
    key_file=/path/to/oci_api_key.pem
    tenancy=ocid1.tenancy.oc1...
    region={oci-region-id}

4. Build & Deploy Function
    fn init --runtime python <funtion-name>
    fn -v deploy --app <your-fn-app>

5. Invoke Function
    fn invoke <your-fn-app> <function-name>

 When you deploy to OCI Functions, mount the key file into the function container (using OCI Vault Secret or Object Storage if you’re just testing).

On success:

DIS Task Run is triggered.

A notification (email/Slack) is sent via ONS with task run logs.

Security Notes

Do NOT commit your oci_config or private key to GitHub.

Use environment variables or OCI Vault for production deployments.

