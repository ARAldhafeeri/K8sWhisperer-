# k8swhisperer

k8swhisperer is a Kubernetes operator that allows users to query pod logs using natural language. It leverages a TinyLlama model to interpret human-readable queries and converts them into parameters to retrieve the desired logs from Kubernetes pods, also a short, human readable report on the fetched logs from any pod. This project aims to make it easy for users to debug issues and read logs in crowded k8s cluster.

---

## Key Features

- Natural Language Processing (NLP): Uses TinyLlama to interpret log queries in natural language.
- Log Filtering: Supports filtering logs by parameters like tail_lines, since_time, and grep keyword.
- Kubernetes Integration: Directly interfaces with the Kubernetes API to fetch logs from pods.

---

## Install

1. **clone this repostiory**:

```bash
git clone https://github.com/ARAldhafeeri/K8sWhisperer-

```

2. **Build and Deploy**:

```bash
kubectl creat namespace k8swhi
kubectl apply -f role.yaml
```

```bash
docker build -t dockerHubUsername/k8swhi .
docker push dockerHubUsername/k8swhi
kubectl apply -f crd.yaml
kubectl run k8swhi --image=dockerHubUsername/k8swhi --restart=Never
```

---

## Example Usage

To query logs using the `k8swhisperer` operator, create a custom resource:

**`query.yaml`:**

```yaml
apiVersion: logquery.example.com/v1
kind: LogQuery
metadata:
  name: error-logs
spec:
  podName: my-app-pod
  query: "Show last 20 lines with errors from the past 10 minutes"
```

Apply the resource and check the results:

```bash
kubectl apply -f query.yaml
kubectl get logquery error-logs -o yaml
```

---

## Note

Weather this is practical to do or not, depend on the k8s cluster resources, the image is really big
8GB
tinyllama needs at minimal 3.85

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
