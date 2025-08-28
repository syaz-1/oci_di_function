import oci
import json
import os

def handler(ctx, data):
    # === Common configuration ===
    config_path = os.path.join(os.path.dirname(__file__), "oci_config")
    topic_id = "ocid1.onstopic.oc1.ap-sydney-1.XXXX"
    workspace_id = "ocid1.disworkspace.oc1.ap-sydney-1.XXX"
    application_key = "XXXXXXXXXX"
    aggregator_key = "XXXXXXXXXXXXXX"

    try:
        # Load config
        config = oci.config.from_file(config_path, "DEFAULT")

        # Create clients
        dis_client = oci.data_integration.DataIntegrationClient(config)
        ons_client = oci.ons.NotificationDataPlaneClient(config)

        # Prepare task run
        task_run_details = oci.data_integration.models.CreateTaskRunDetails(
            registry_metadata=oci.data_integration.models.RegistryMetadata(
                aggregator_key=aggregator_key
            )
        )

        # Trigger task run
        response = dis_client.create_task_run(
            workspace_id=workspace_id,
            application_key=application_key,
            create_task_run_details=task_run_details
        )

        log_data = json.dumps(response.data.__dict__, indent=2, default=str)

        # Send success notification
        ons_client.publish_message(
            topic_id,
            oci.ons.models.MessageDetails(
                title="Data Integration Task Run SUCCESS",
                body=log_data[:5000]  # Limit body length for email safety
            )
        )

        return json.dumps({
            "status": "success",
            "task_run": response.data.__dict__
        }, indent=2, default=str)

    except Exception as e:
        # Try to send failure notification if config & ONS work
        try:
            if 'ons_client' not in locals():
                config = oci.config.from_file(config_path, "DEFAULT")
                ons_client = oci.ons.NotificationDataPlaneClient(config)
            ons_client.publish_message(
                topic_id,
                oci.ons.models.MessageDetails(
                    title="Data Integration Task Run FAILED",
                    body=str(e)
                )
            )
        except:
            pass

        return json.dumps({
            "status": "error",
            "message": str(e)
        })
