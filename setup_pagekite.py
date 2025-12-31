"""
Setup Pagekite for free public tunneling
"""

import subprocess
import sys
import os

def setup_pagekite():
    """Setup Pagekite for public tunneling"""
    
    print("🚀 Setting up Pagekite for public tunneling...")
    print("📡 This will give you a reliable public URL")
    print()
    
    # Download pagekite
    try:
        print("📥 Downloading Pagekite...")
        subprocess.run(['curl', '-O', 'https://pagekite.net/pk/pagekite.py'], check=True)
        print("✅ Pagekite downloaded successfully")
        
        # Make it executable
        subprocess.run(['chmod', '+x', 'pagekite.py'], check=False)
        
        print("🔧 Starting Pagekite tunnel...")
        print("🌐 This will create a public URL for your backend")
        print()
        
        # Start pagekite
        cmd = [
            'python', 'pagekite.py',
            '--clean',
            '--frontend=pagekite.net:80',
            '--service_on=http://localhost:8000:yourapp.pagekite.net'
        ]
        
        print("🔄 Running:", ' '.join(cmd))
        subprocess.run(cmd)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try manual setup at https://pagekite.net/")

if __name__ == "__main__":
    setup_pagekite()
