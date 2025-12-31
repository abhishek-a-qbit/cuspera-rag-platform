"""
Public tunnel using serveo.net - free public URL
"""

import subprocess
import time
import sys
import os

def create_public_tunnel():
    """Create a public tunnel using serveo.net"""
    
    print("🚀 Creating public tunnel using serveo.net...")
    print("📡 This will give you a public URL that works with Streamlit Cloud")
    print()
    
    # Use serveo.net for free public tunneling
    try:
        # Run ssh command to create tunnel
        cmd = ['ssh', '-R', '80:localhost:5000', 'serveo.net']
        
        print("🔗 Running command: ssh -R 80:localhost:5000 serveo.net")
        print("🌐 This will create a public URL for your local server")
        print()
        print("⚠️  If prompted for 'yes/no', type 'yes' and press Enter")
        print("⚠️  The public URL will be shown in the output below")
        print("📋 Copy that URL and use it in Streamlit Cloud")
        print()
        print("🔄 Tunnel starting...")
        
        # Start the tunnel
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        
        # Monitor output for the public URL
        for line in iter(process.stdout.readline, ''):
            print(line.strip())
            
            # Look for the public URL in the output
            if 'serveo.net' in line and 'http' in line:
                print(f"\n🎉 PUBLIC URL FOUND: {line.strip()}")
                print("📋 Use this URL in Streamlit Cloud as API_URL")
                print()
            
            # Keep the tunnel running
            if process.poll() is not None:
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Tunnel stopped by user")
        if process:
            process.terminate()
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        print("💡 Alternative: Use ngrok or localtunnel")

if __name__ == "__main__":
    create_public_tunnel()
