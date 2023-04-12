load('ext://helm_resource', 'helm_resource', 'helm_repo')

# Add PostgreSQL Helm resource (https://artifacthub.io/packages/helm/bitnami/postgresql)
helm_repo('bitnami', 'https://charts.bitnami.com/bitnami',labels=['helm-charts'])
helm_resource(
    resource_deps=['bitnami'],
    name='socialnetworkdb',
    chart='bitnami/postgresql',
    namespace='default',
    flags=[
        '--set=image.tag=12.0.0',
        '--set=auth.enablePostgresUser=true',
        '--set=auth.postgresPassword=postgres'
    ],
    port_forwards=['30011:5432'],
    labels=['database']
)