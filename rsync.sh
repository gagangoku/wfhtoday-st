# Linode
rsync -r -avzh --exclude '.streamlit' --exclude '.idea' --exclude 'build' --exclude 'dist' --exclude 'venv' --exclude '.git' ./ gagan@api.liquidco.in:~/liquidco/wfhtoday-st/

# Gcp
rsync -Pa -e "ssh -t -i /Users/gagandeep/.ssh/google_compute_engine -o CheckHostIP=no -o HashKnownHosts=no -o HostKeyAlias=compute.8593189175368638566 -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/Users/gagandeep/.ssh/google_compute_known_hosts" --exclude venv --exclude .git ./ gagandeep@gcp.liquidco.in:~/wfhtoday-st/
