# app.py
from flask import Flask, request, render_template_string
import paramiko
import os

app = Flask(__name__)

# Use the existing index.html file as template
with open('index.html', 'r') as file:
    HTML = file.read()

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        ip = request.form["ip"]
        username = request.form["username"]
        password = request.form["password"]
        
        try:
            # Connect to the remote server
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)
            
            # Upload the script.sh file
            sftp = ssh.open_sftp()
            local_path = 'script.sh'
            remote_path = '/tmp/script.sh'
            sftp.put(local_path, remote_path)
            sftp.close()
            
            # Make the script executable and run it
            ssh.exec_command(f"chmod +x {remote_path}")
            stdin, stdout, stderr = ssh.exec_command(f"sh {remote_path}")
            
            # Get the output
            script_output = stdout.read().decode()
            script_errors = stderr.read().decode()
            
            # Filter out home directory error
            if script_errors:
                script_errors = '\n'.join([line for line in script_errors.split('\n') 
                                         if 'Could not chdir to home directory' not in line])
            
            # Add server info to output
            output = f"=== Execution Details ===\n"
            output += f"Server IP: {ip}\n"
            output += f"Username: {username}\n"
            output += f"========================\n\n"
            output += script_output
            if script_errors.strip():
                output += "\nErrors:\n" + script_errors
                
            # Clean up
            ssh.exec_command(f"rm {remote_path}")
            ssh.close()
        except Exception as e:
            output = f"Error: {e}"

    return render_template_string(HTML, output=output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)