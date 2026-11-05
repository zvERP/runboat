# Runboat PostgreSQL

A single PostgreSQL 14 StatefulSet in the `runboat-builds-db` namespace, used by all
builds (which run in the `runboat` namespace). Its volume is a strict-local Longhorn
volume with one replica, so the pod is pinned to one node with
`kubernetes.io/hostname`: the database is unavailable if that node is lost, which is
acceptable for disposable builds.

1. The node is set in `postgres.yaml` (`kubernetes.io/hostname: dedicado-ovh-gra2`,
   a control-plane node, hence the control-plane toleration).
2. `cp postgres.env.sample postgres.env` and set a password. Use the same password
   as `PGPASSWORD` in `RUNBOAT_BUILD_SECRET_ENV`.
3. Deploy, either on its own or together with the controller from `deploy/`:

```bash
kubectl apply -k deploy/runboat-postgres
kubectl -n runboat-builds-db rollout status statefulset/postgres
```

Builds reach it at `postgres.runboat-builds-db.svc.cluster.local:5432`.
