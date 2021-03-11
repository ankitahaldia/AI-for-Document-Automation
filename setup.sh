RUN apt-get update
RUN apt-get install ffmpeg libxext6  -y
mkdir -p ~/.streamlit/
echo "[general]
email = \"parry.dilara@gmail.com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml