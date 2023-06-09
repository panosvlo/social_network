docker_compose('docker-compose.yaml')
# Add labels to Docker services
dc_resource('redis', labels=["redis"])
dc_resource('socialnetworkdb', labels=["database"])

# Frontend Configuration

local_resource(
  'frontend_dependencies',
  serve_cmd='cd frontend && npm install',
  labels=['dependencies'],
  deps=['./frontend/'],
)

local_resource(
  'frontend',
  serve_cmd='cd frontend && npm start',
  labels=['frontend'],
  resource_deps=['backend', 'frontend_dependencies']
)

# Backend Configuration

local_resource(
  'backend_dependencies',
  cmd='cd backend && pip install -r requirements.txt --user',
  labels=['dependencies'],
  deps=['./backend/requirements.txt'],
)

local_resource(
  'backend_migrations',
  cmd='cd backend && python manage.py migrate',
  labels=['dependencies'],
  resource_deps=['socialnetworkdb'],
  deps=['./backend/users/migrations/'],
)

local_resource(
  'backend',
  serve_cmd='cd backend && python manage.py runserver',
  labels=['backend'],
  resource_deps=['socialnetworkdb', 'backend_dependencies', 'backend_migrations'],
  deps=['./backend/'],
)

local_resource(
  'celery_worker',
  serve_cmd='cd backend && celery -A social_network worker -l info -P gevent -c 1',
  labels=['backend'],
  resource_deps=['backend'],
  deps=['./backend/users/tasks.py'],
)

local_resource(
  'celery_scheduler',
  serve_cmd='cd backend && celery -A social_network beat -l info',
  labels=['backend'],
  resource_deps=['backend'],
  deps=['./backend/social_network/settings.py'],
)