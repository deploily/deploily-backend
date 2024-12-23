# Deploily-backend
Backend for deploily platform

## Installation 

```bash
# Get the code
git clone git@github.com:deploily/deploily-backend.git

# Go to the docker folder
cd deploily-backend/docker

# Copy the fake env vars
cp .env.example .env

# Pull the latest images
docker compose pull

# Start the services (in detached mode)
docker compose up -d
```


## Useful links
- [https://supabase.com/docs/guides/self-hosting/docker](https://supabase.com/docs/guides/self-hosting/docker)