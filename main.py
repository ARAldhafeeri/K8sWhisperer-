import kubernetes
import kopf
from kubernetes.client import CoreV1Api
from ollama import Ollama


@kopf.on.create('logquery.k8swhi.com', 'v1', 'logqueries')
@kopf.on.update('logquery.k8swhi.com', 'v1', 'logqueries')
async def handle_logquery(spec, namespace, name, **kwargs):
    # Extract the pod name and the query from the custom resource spec.
    pod_name = spec.get('podName')
    query = spec.get('query')
    
    if not pod_name or not query:
        raise kopf.PermanentError("podName and query must be provided")

    try:
        tinyllama = Ollama("tinyllama", temperature=0.0)
    except Exception as e:
        raise kopf.PermanentError(f"Tiny Llama initialization failed: {str(e)}")

    api = CoreV1Api()
    try:
        logs = api.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
        )
    except Exception as e:
        raise kopf.PermanentError(f"Failed to retrieve logs: {str(e)}")

    prompt = (
        f"You are helpful logs anlaysis, parse the log and perform user query"
        f"User Query: {query}\n\n"
        f"Logs from pod '{pod_name}' in namespace '{namespace}':\n"
        f"{logs}"
    )

    try:
        output = tinyllama(prompt)
    except Exception as e:
        raise kopf.PermanentError(f"Error during Tiny Llama processing: {str(e)}")

    api = kubernetes.client.CustomObjectsApi()  
    obj = api.get_namespaced_custom_object( 
        group="logquery.k8swhi.com",
        version="v1",
        namespace=namespace,
        plural="logqueries",
        name=name
    )

    obj['status'] = {
        'answer': output.encode('utf-8').decode('ascii', 'ignore'),
        'phase': 'Processed',
        'truncated': len(output) >= 3000
    }
    api.patch_namespaced_custom_object( 
        group="logquery.k8swhi.com",
        version="v1",
        namespace=namespace,
        plural="logqueries",
        name=name,
        body=obj
    )

    return obj['status'] 