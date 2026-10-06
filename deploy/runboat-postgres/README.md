# Runboat PostgreSQL locations

This package deploys one PostgreSQL 14 StatefulSet in each Runboat location:
`nbg1`, `fsn1`, and `hel1`. Each instance uses a single strict-local Longhorn
replica. This removes inter-datacenter storage latency, at the cost of the database
being unavailable if its node or local Longhorn replica is lost.

The nodes must have the corresponding `topology.kubernetes.io/zone` labels.
Builds run in the `runboat` namespace, while these PostgreSQL instances run in
`runboat-builds-db`.

Create the database password without committing it:

```bash
kubectl create namespace runboat-builds-db --dry-run=client -o yaml | kubectl apply -f -
kubectl -n runboat-builds-db create secret generic runboat-postgres \
  --from-literal=POSTGRES_USER=runboat-build \
  --from-literal=POSTGRES_PASSWORD='replace-me'
```

Use that same password as `PGPASSWORD` in `RUNBOAT_BUILD_SECRET_ENV`, then deploy:

```bash
kubectl apply -k deploy/runboat-postgres
kubectl -n runboat-builds-db rollout status statefulset/postgres-nbg1
kubectl -n runboat-builds-db rollout status statefulset/postgres-fsn1
kubectl -n runboat-builds-db rollout status statefulset/postgres-hel1
```

The Runboat location configuration is shown in the repository `.env.sample`. New
builds are distributed with a stable weighted hash and receive both the local
`PGHOST` and a matching node selector. Existing builds without a `runboat/location`
annotation continue using the global database configuration.
