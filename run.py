#!/usr/bin/env python
"""
Local Development Server
Run: python run.py
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║         🛒 SuperMarket Mini App - LOCAL SERVER            ║
    ╚════════════════════════════════════════════════════════════╝
    
    ✅ Server Running: http://localhost:{port}
    📱 API: http://localhost:{port}/api/products
    🛒 Mini App: http://localhost:{port}
    ⏹️  Stop: Press CTRL+C
    
    Logs:
    """)
    app.run(debug=True, port=port, host='0.0.0.0')
