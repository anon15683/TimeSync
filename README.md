# TimeSync - All4Schools Schedule Integration
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/devfox1/timesync?sort=date)  
![Docker Pulls](https://img.shields.io/docker/pulls/devfox1/timesync)  
![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/devfox1/timesync?sort=date)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/xXxNIKIxXx/TimeSync/docker-image.yml)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/xXxNIKIxXx/TimeSync)  
![GitHub last commit](https://img.shields.io/github/last-commit/xXxNIKIxXx/TimeSync)

Automatically sync your All4Schools schedule with any CalDAV calendar application using Docker. Keep your school schedule organized across all your devices!

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Deployment Options](#deployment-options)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features
✓ Sync your All4Schools class schedule automatically

✓ Compatible with any CalDAV server (SOGo, Nextcloud, iCloud)

✓ Configurable update intervals

✓ Secure credential management

✓ Docker containerized

✓ Easy deployment

## Requirements
- Docker installed on your system
- CalDAV server (e.g., SOGo)
- All4Schools login credentials

## Deployment Options
Choose one of these methods to deploy TimeSync:

### Option 1: Docker Hub
Create a compose.yml file:
```yaml
services:
  timesync:
    image: devfox1/timesync:latest
    container_name: timesync
    restart: unless-stopped
    env_file:
      - .env
```

### Option 2: GitHub Packages
Create a compose.yml file:
```yaml
services:
  timesync:
    image: ghcr.io/xxxnikixxx/timesync:latest
    container_name: timesync
    restart: unless-stopped
    env_file:
      - .env
```

### Option 3: GitHub Local

Clone from github using:
```
git clone https://github.com/xXxNIKIxXx/TimeSync.git
```

Create a compose.yml file:
```yaml
services:
  timesync:
    container_name: timesync
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    env_file:
      - .env
```


## Configuration
Create a .env file:
```bash
SOGO_URL="https://example.com/SOGo/dav/user/"
SOGO_USERNAME="user@example.com"
SOGO_PASSWORD="password"
SOGO_CALENDAR_URL="https://example.com/SOGo/dav/user/Calendar/"

ALL4SCHOOLS_LOGIN_URL="https://example.com/modules/Login.aspx"
ALL4SCHOOLS_USERNAME="username"
ALL4SCHOOLS_PASSWORD="password"
ALL4SCHOOLS_VIEWSTATE="viewstate"
ALL4SCHOOLS_EVENTVALIDATION="eventvalidation"
ALL4SCHOOLS_API_URL="https://example.com/api/api/Schedule/GetSchedule"

DAYS_TO_ADD=14
DAYS_TO_UPDATE=7

INTERVAL_MINUTES=5

PRINT_BAR_LENGTH=40
SLEEP_PRINT_DELAY_SECONDS=10
```

## Usage
Start the container:
```bash
docker compose up -d
```

Check logs:
```bash
docker compose logs -f
```

Stop the container:
```bash
docker compose stop
```

Update to latest version:
```bash
docker compose pull
docker compose up -d
```

## Troubleshooting
Common issues and solutions:

1. Authentication errors:
   - Verify all credentials in `.env`
   - Check SOGo server accessibility
   - Ensure All4Schools endpoints are correct

2. Connection problems:
   - Confirm all URLs are valid
   - Check network connectivity
   - Verify SSL certificates if using HTTPS

3. Sync failures:
   - Review container logs
   - Verify API compatibility
   - Check rate limiting settings

## Contributing
Pull requests are welcome! To contribute:
1. Fork the repository
2. Create your feature branch
3. Submit a pull request
