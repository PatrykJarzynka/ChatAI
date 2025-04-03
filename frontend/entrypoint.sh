#!/bin/sh

# Ustawianie domyślnych wartości dla zmiennych
if [ -z "$REDIRECT_URL" ]; then
  echo "REDIRECT_URL is not set. Using default value."
  export REDIRECT_URL="http://localhost:80/callback"
fi

if [ -z "$API_URL" ]; then
  echo "API_URL is not set. Using default value."
  export API_URL="http://127.0.0.1:8000"
fi

if [ -z "$GOOGLE_CLIENT_ID" ]; then
  echo "GOOGLE_CLIENT_ID is not set. Using default value."
  export GOOGLE_CLIENT_ID="268450421384-sh5e3buktug7k543dlg1soqpbb9otoi5.apps.googleusercontent.com"
fi

if [ -z "$AZURE_CLIENT_ID" ]; then
  echo "AZURE_CLIENT_ID is not set. Using default value."
  export AZURE_CLIENT_ID="d6efa951-4ad7-4e71-bf5d-1e8ef0615e92"
fi

mkdir -p /usr/share/nginx/html/assets

# Generowanie pliku config.js z dynamicznymi zmiennymi
cat <<EOF > /usr/share/nginx/html/assets/config.js
window._env = {
  API_URL: "$API_URL",
  REDIRECT_URL: "$REDIRECT_URL",
  GOOGLE_CLIENT_ID: "$GOOGLE_CLIENT_ID",
  AZURE_CLIENT_ID: "$AZURE_CLIENT_ID",
};
EOF

echo "Generated /usr/share/nginx/html/assets/config.js:"
cat /usr/share/nginx/html/assets/config.js

# Uruchomienie Nginx
exec "$@"
