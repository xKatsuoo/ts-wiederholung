import unittest
from flask import Flask
from flask_testing import TestCase
from unittest.mock import patch, MagicMock
from app import app

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    #health
    def test_health(self):
        response = self.client.get("/healthz")
        self.assert200(response)
        self.assertEqual('OK', response.text)


    #status
    @patch('subprocess.run')
    def test_latency_check_status_success(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0, stdout=b'\u25cf latency_check.service - Latenz Check Service\n     Loaded: loaded (/home/ubuntu/.config/systemd/user/latency_check.service; enabled; vendor preset: enabled)\n     Active: active (running) since Thu 2024-01-04 23:33:10 UTC; 2s ago\n    Process: 85765 ExecStartPre=/bin/bash -c echo \"Starting latency check at $(date)\" >> /tmp/latency_check.log (code=exited, status=0/SUCCESS)\n   Main PID: 85767 (latency_check.s)\n      Tasks: 7 (limit: 1121)\n     Memory: 1.9M\n        CPU: 19ms\n     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/latency_check.service\n             \u251c\u250085767 /bin/bash /home/ubuntu/latency_check.sh\n             \u251c\u250085774 /bin/bash /home/ubuntu/latency_check.sh\n             \u251c\u250085775 /bin/bash /home/ubuntu/latency_check.sh\n             \u251c\u250085776 ping -c 5 google.com\n             \u251c\u250085777 tail -1\n             \u251c\u250085778 awk \"{print \\$4}\"\n             \u2514\u250085779 cut -d / -f 2\n\nJan 04 23:33:10 ip-10-0-2-64 systemd[85086]: Starting Latenz Check Service...\nJan 04 23:33:10 ip-10-0-2-64 systemd[85086]: Started Latenz Check Service.\n', stderr=b'')
        response = self.client.get("/service/latency_check")
        self.assert200(response)
        self.assertEqual(True, response.json['success'])
        self.assertIn('Active: active (running)', response.json['message'])
    
    @patch('subprocess.run')
    def test_latency_check_status_restarting(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=3, stdout=b'\u25cf latency_check.service - Latenz Check Service\n     Loaded: loaded (/home/ubuntu/.config/systemd/user/latency_check.service; enabled; vendor preset: enabled)\n     Active: activating (auto-restart) since Thu 2024-01-04 23:32:50 UTC; 18s ago\n    Process: 85716 ExecStartPre=/bin/bash -c echo \"Starting latency check at $(date)\" >> /tmp/latency_check.log (code=exited, status=0/SUCCESS)\n    Process: 85718 ExecStart=/home/ubuntu/latency_check.sh (code=exited, status=0/SUCCESS)\n   Main PID: 85718 (code=exited, status=0/SUCCESS)\n        CPU: 21ms\n', stderr=b'')
        response = self.client.get("/service/latency_check")
        self.assert200(response)
        self.assertEqual(True, response.json['success'])
        self.assertIn('Active: activating (auto-restart)', response.json['message'])
    
    @patch('subprocess.run')
    def test_latency_check_status_failure(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=1, stdout=b'', stderr=b'Unit latency_checkiaservice.service could not be found.\n')
        response = self.client.get("/service/latency_check")
        self.assert200(response)
        self.assertEqual(False, response.json['success'])
        self.assertEqual('Unit latency_checkiaservice.service could not be found.\n', response.json['message'])



    #start
    @patch('subprocess.run')
    def test_latency_check_start_success(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0, stdout=b'', stderr=b'')
        response = self.client.get("/service/latency_check/start")
        self.assert200(response)
        self.assertEqual(True, response.json['success'])
        self.assertEqual('', response.json['message'])

    @patch('subprocess.run')
    def test_latency_check_start_failure(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=1, stdout=b'', stderr=b'Failed to start latency_checks.service: Unit latency_checks.service not found.\n')
        response = self.client.get("/service/latency_check/start")
        self.assert200(response)
        self.assertEqual(False, response.json['success'])
        self.assertEqual('Failed to start latency_checks.service: Unit latency_checks.service not found.\n', response.json['message'])

    #stop
    @patch('subprocess.run')
    def test_latency_check_stop_success(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=0, stdout=b'', stderr=b'')
        response = self.client.get("/service/latency_check/stop")
        self.assert200(response)
        self.assertEqual(True, response.json['success'])
        self.assertEqual('', response.json['message'])

    @patch('subprocess.run')
    def test_latency_check_stop_failure(self, mock_subprocess):
        mock_subprocess.return_value = MagicMock(returncode=1, stdout=b'', stderr=b'Failed to stop latency_checka.service: Unit latency_checka.service not loaded.\n')
        response = self.client.get("/service/latency_check/stop")
        self.assert200(response)
        self.assertEqual(False, response.json['success'])
        self.assertEqual('Failed to stop latency_checka.service: Unit latency_checka.service not loaded.\n', response.json['message'])

if __name__ == '__main__':
    unittest.main()
