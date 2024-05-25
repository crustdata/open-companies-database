#!/bin/bash
ADMIN_EMAIL="admin@opencompaniesdb.local"
ADMIN_PASSWORD="OpenCompanyDatabase@1"

echo "⌚︎ Waiting for Metabase to start"
while (! curl -s -m 5 http://localhost:3000/api/session/properties -o /dev/null); do sleep 5; done
echo "😎 Creating admin user"

SETUP_TOKEN=$(curl -s -m 5 -X GET \
    -H "Content-Type: application/json" \
    http://localhost:3000/api/session/properties \
    | jq -r '.["setup-token"]'
)

MB_TOKEN=$(curl -s -X POST \
    -H "Content-type: application/json" \
    http://localhost:3000/api/setup \
    -d '{
    "token": "'${SETUP_TOKEN}'",
    "user": {
        "email": "'${ADMIN_EMAIL}'",
        "first_name": "Metabase",
        "last_name": "Admin",
        "password": "'${ADMIN_PASSWORD}'"
    },
    "prefs": {
        "allow_tracking": false,
        "site_name": "Metawhat"
    }
}' | jq -r '.id')

echo -e "\n👥 Creating some basic users: "
curl -s "http://localhost:3000/api/user" \
    -H 'Content-Type: application/json' \
    -H "X-Metabase-Session: ${MB_TOKEN}" \
    -d '{"first_name":"Basic","last_name":"User","email":"basic@somewhere.com","login_attributes":{"region_filter":"WA"},"password":"'${ADMIN_PASSWORD}'"}'
echo -e "\n👥 Basic users created!"


# Get Metabase session token
SESSION_TOKEN=$(curl -X POST -H "Content-Type: application/json" -d '{
  "username": "'${ADMIN_EMAIL}'",
  "password": "'${ADMIN_PASSWORD}'"
}' http://localhost:3000/api/session | jq -r '.id')

echo "SESSION_TOKEN: $SESSION_TOKEN"

# Configure data source
curl -X POST -H "Content-Type: application/json" -H "X-Metabase-Session: $SESSION_TOKEN" -d '{
  "name": "Your Database",
  "engine": "postgres",
  "details": {
    "host": "db",
    "port": 5432,
    "dbname": "open_companies_db",
    "user": "user",
    "password": "password",
    "ssl": false,
    "additional-options": ""
  },
  "is_full_sync": true
}' http://localhost:3000/api/database
