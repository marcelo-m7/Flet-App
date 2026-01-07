# Production Deployment Guide

## Overview
This guide covers deploying the Flet-App using Docker and Docker Compose for production environments.

## Prerequisites
- Docker 20.10+
- Docker Compose 1.29+
- (Optional) Docker Swarm or Kubernetes for orchestration

## Quick Start with Docker Compose

### 1. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit with your production values
nano .env
```

**Production Environment Variables:**
```env
# Database
DB_HOST=mysql  # Use 'mysql' when running in Docker Compose
DB_USER=todo_user
DB_PASSWORD=your_secure_password
DB_NAME=todoapp

# MySQL Root Password (for initialization only)
MYSQL_ROOT_PASSWORD=your_root_password

# Flet App
FLET_PORT=8000
FLET_HOST=0.0.0.0

# Security
FERNET_KEY=your_generated_fernet_key
```

### 2. Generate Fernet Key (for encryption)
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
Add the output to your `.env` file as `FERNET_KEY`.

### 3. Deploy
```bash
# Build and start services
docker-compose up -d

# Verify services are running
docker-compose ps

# Check logs
docker-compose logs -f flet_app
docker-compose logs -f mysql
```

### 4. Stop Services
```bash
docker-compose down

# Remove all volumes (destructive)
docker-compose down -v
```

## Building Standalone Docker Image

### Build
```bash
docker build -t flet-app:latest .
```

### Run
```bash
docker run -d \
  --name flet-app \
  -p 8000:8000 \
  -e DB_HOST=mysql \
  -e DB_USER=todo_user \
  -e DB_PASSWORD=secure_password \
  -e DB_NAME=todoapp \
  flet-app:latest
```

## Production Considerations

### Security
- [ ] Use strong, unique passwords in `.env`
- [ ] Store `.env` in a secure vault (AWS Secrets Manager, HashiCorp Vault, etc.)
- [ ] Do NOT commit `.env` to version control
- [ ] Enable MySQL user authentication with minimal privileges
- [ ] Use HTTPS/SSL in reverse proxy (Nginx, Apache)
- [ ] Enable Fernet encryption for sensitive data

### Database
- [ ] Back up MySQL data regularly
- [ ] Use named volumes for persistent storage: `docker volume create flet_db_data`
- [ ] Run MySQL container with resource limits
- [ ] Use a separate managed database service (RDS, Cloud SQL) in production
- [ ] Enable MySQL slow query logging and monitoring

### Monitoring & Logging
- [ ] Configure Docker logging driver (JSON-file, Splunk, etc.)
- [ ] Use health checks (included in docker-compose.yml)
- [ ] Monitor container resource usage
- [ ] Set up log aggregation (ELK, Datadog, CloudWatch)

### Reverse Proxy Setup (Nginx Example)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://flet-app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Kubernetes Deployment (Optional)

### Create ConfigMap for database config
```bash
kubectl create configmap flet-config \
  --from-env-file=.env
```

### Deploy with Helm or raw manifests
See `k8s/` directory for Kubernetes manifests (to be created).

## Troubleshooting

### App can't connect to database
```bash
# Check database service health
docker-compose exec mysql mysqladmin -u root -p${MYSQL_ROOT_PASSWORD} ping

# Verify network connectivity
docker-compose exec flet_app ping mysql

# Check environment variables
docker-compose exec flet_app env | grep DB_
```

### MySQL won't start
```bash
# Check MySQL logs
docker-compose logs mysql

# Verify init script ran
docker-compose exec mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "SHOW TABLES FROM todoapp;"
```

### Permission denied errors
```bash
# Fix Docker socket permissions (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

## Scaling

### Horizontal Scaling with Docker Compose
```yaml
# Scale the app service to 3 replicas
docker-compose up -d --scale flet_app=3
```

### Load Balancer Configuration
Deploy Nginx or HAProxy in front to distribute traffic:
```
[Load Balancer:80] -> [App:8000, App:8001, App:8002] -> [MySQL:3306]
```

## Backup and Restore

### Backup MySQL Database
```bash
docker-compose exec mysql mysqldump -u ${DB_USER} -p${DB_PASSWORD} todoapp > backup.sql
```

### Restore from Backup
```bash
docker-compose exec -T mysql mysql -u ${DB_USER} -p${DB_PASSWORD} todoapp < backup.sql
```

## Additional Resources
- [Flet Documentation](https://flet.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MySQL Docker Hub](https://hub.docker.com/_/mysql)
