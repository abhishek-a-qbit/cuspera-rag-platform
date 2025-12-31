# Setup Cloudflare Tunnel for free public URL
Write-Host "Setting up Cloudflare Tunnel..."

# Install cloudflared
winget install --id Cloudflare.cloudflared -e

# Create tunnel
cloudflared tunnel login
cloudflared tunnel create cuspera-api

# Create config file
$config = @"
tunnel: cuspera-api
credentials-file: C:\Users\$env:USERNAME\.cloudflared\cuspera-api.json

ingress:
  - hostname: your-custom-name.trycloudflare.com
    service: http://localhost:8000
  - service: http_status:404
"@

$config | Out-File -FilePath "C:\Users\$env:USERNAME\.cloudflared\config.yml" -Encoding UTF8

Write-Host "Tunnel setup complete!"
Write-Host "Run: cloudflared tunnel run cuspera-api"
"
