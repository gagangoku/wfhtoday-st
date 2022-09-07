nohup ./venv/bin/streamlit run Home.py --theme.base dark --server.port 8503 2>&1 > logs/$(date '+%Y-%m-%dT%H:%M:%S').log &
