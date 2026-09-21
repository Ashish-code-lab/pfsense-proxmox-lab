"""
WSGI Entry point for pfSense Lab on Proxmox VE.
"""

from pfsense_lab import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
