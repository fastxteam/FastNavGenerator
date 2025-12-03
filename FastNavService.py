#!/usr/bin/env python3
"""
FastNav Windows Service
Simplified version
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import os
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler


class FastNavService(win32serviceutil.ServiceFramework):
    """Windows Service for FastNav"""

    _svc_name_ = "FastNavWebService"
    _svc_display_name_ = "FastNav Web Service"
    _svc_description_ = "Auto-generate and serve navigation website"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYSERVICE_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    def main(self):
        port = 8080
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Generate website if needed
        self.generate_website()

        # Start HTTP server
        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=os.getcwd(), **kwargs)

            def log_message(self, format, *args):
                pass  # Silent logging

        server = HTTPServer(('', port), Handler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        # Keep service running
        while self.is_running:
            time.sleep(1)
        server.shutdown()

    def generate_website(self):
        """Generate website if needed"""
        try:
            if not os.path.exists('index.html'):
                import subprocess
                subprocess.run([sys.executable, 'FastNavGenerator.py',
                                '--config', 'FastNavGenerator.json',
                                '--output', 'index.html'],
                               capture_output=True, timeout=30)
        except:
            pass  # Silently fail


def install_service():
    """Install service"""
    try:
        win32serviceutil.InstallService(
            None,
            FastNavService._svc_name_,
            FastNavService._svc_display_name_,
            description=FastNavService._svc_description_,
            startType=win32service.SERVICE_AUTO_START
        )
        print("[SUCCESS] Service installed")
        print("[INFO] Commands:")
        print("  Start: net start FastNavWebService")
        print("  Stop: net stop FastNavWebService")
        print("  Remove: sc delete FastNavWebService")
    except Exception as e:
        print(f"[ERROR] Installation failed: {e}")


def remove_service():
    """Remove service"""
    try:
        win32serviceutil.RemoveService(FastNavService._svc_name_)
        print("[SUCCESS] Service removed")
    except Exception as e:
        print(f"[ERROR] Removal failed: {e}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FastNavService)
        servicemanager.StartServiceCtrlDispatcher()
    elif sys.argv[1] == 'install':
        install_service()
    elif sys.argv[1] == 'remove':
        remove_service()
    elif sys.argv[1] == 'debug':
        # Debug mode
        service = FastNavService([''])
        service.SvcDoRun()