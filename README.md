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
- CalDAV server (e.g., SOGo or iCloud)
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

```bash
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
USERNAME="user@example.com"
PASSWORD="password"
CALENDAR_URL="https://example.com/SOGo/dav/user/Calendar/"

ALL4SCHOOLS_URL="https://example.com/"
ALL4SCHOOLS_USERNAME="username"
ALL4SCHOOLS_PASSWORD="password"

DAYS_TO_ADD=14
DAYS_TO_UPDATE=7

INTERVAL_MINUTES=5

PRINT_BAR_LENGTH=40
SLEEP_PRINT_DELAY_SECONDS=10
```

### How to Obtain Calendar URL

  ### SOGo
  1. Log in to your SOGo calendar.
  2. Select the calendar you want to use.
  3. Click on the three dots next to the calendar name.
  4. Choose "Links to this calendar" and copy the CalDAV URL.

  ### iCloud
  1. Create an app-specific password under [App-Specific Passwords](https://account.apple.com/account/manage).
  2. Use the following Python script to list your iCloud calendars and obtain the CalDAV URL:
  
  ```python
  # list_icloud_calendars.py
  import caldav
  import argparse

  def list_icloud_calendars(username, app_specific_password):
      """
      List iCloud calendars for a given username and app-specific password.

      Args:
          username (str): The iCloud username.
          app_specific_password (str): The app-specific password for iCloud.

      Returns:
          None
      """
      # URL of the iCloud CalDAV server
      caldav_url = 'https://caldav.icloud.com/'

      # Connect to the iCloud CalDAV server
      client = caldav.DAVClient(url=caldav_url, username=username, password=app_specific_password)
      principal = client.principal()

      # Get the calendar
      calendars = principal.calendars()
      for calendar in calendars:
          print(f"Calendar Name: \033[94m{calendar.name}\033[0m\nURL: \033[92m{calendar.url}\033[0m\n")

  if __name__ == "__main__":
      parser = argparse.ArgumentParser(description='List iCloud calendars.')
      parser.add_argument('-u', '--user', required=True, help='iCloud username')
      parser.add_argument('-p', '--password', required=True, help='iCloud app-specific password')

      args = parser.parse_args()
      list_icloud_calendars(args.user, args.password)
  ```

  3. Run the script with your iCloud username and app-specific password to list your calendars and their URLs.
  4. Copy the URL for the correct calendar.

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
