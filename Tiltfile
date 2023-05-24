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

helm_resource(
    resource_deps=['bitnami'],
    name='redis',
    chart='bitnami/redis',
    namespace='default',
    flags=[
        '--set=image.tag=4.0.10',
        '--set=master.count=1',
        '--set=replica.replicaCount=0',
        '--set=auth.enabled=false',
        '--set=auth.sentinel=false',
        '--set=cluster.enabled=standalone',
    ],
    port_forwards=['6379:6379'],
    labels=['redis']
)

local_resource(
  'frontend',
  cmd='npm start',
  dir='./frontend/',
  deps=['./frontend/'],
  allow_parallel=True,
  labels=['frontend']
)

local_resource(
  'backend',
  cmd='python manage.py runserver',
  dir='./backend/',
  deps=['./backend/'],
  allow_parallel=True,
  labels=['backend'],
  resource_deps=['socialnetworkdb'],
)

local_resource(
  'celery_worker',
  cmd='celery -A social_network worker -l info -P gevent',
  dir='./backend/',
  allow_parallel=True,
  labels=['backend'],
  resource_deps=['socialnetworkdb'],
)

# The below stays in Pending, needs to be run from the command line
# local_resource(
# 'celery_beat',
# cmd='celery -A social_network beat -l info',
# dir='./backend/',
# allow_parallel=True,
# labels=['backend'],
# resource_deps=['socialnetworkdb'],
# )




