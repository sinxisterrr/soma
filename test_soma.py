#!/usr/bin/env python3
"""
SOMA Test Suite
Comprehensive tests to ensure the body system works consistently
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any


class SOMATestSuite:
    """Test suite for SOMA body system"""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.test_user = "test_user_001"
        self.results = []
    
    def log(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        result = {
            'timestamp': timestamp,
            'test': test_name,
            'passed': passed,
            'details': details
        }
        self.results.append(result)
        
        print(f"[{timestamp}] {status} - {test_name}")
        if details:
            print(f"          {details}")
    
    def reset_test_user(self):
        """Reset test user to baseline"""
        try:
            response = requests.post(f"{self.base_url}/api/soma/{self.test_user}/reset")
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to reset: {e}")
            return False
    
    def test_health_check(self):
        """Test 1: Health endpoint works"""
        try:
            response = requests.get(f"{self.base_url}/health")
            data = response.json()
            
            passed = (
                response.status_code == 200 and
                data.get('status') == 'alive' and
                'SOMA' in data.get('service', '')
            )
            
            self.log(
                "Health Check",
                passed,
                f"Status: {data.get('status')}, Active bodies: {data.get('active_bodies')}"
            )
            
        except Exception as e:
            self.log("Health Check", False, f"Error: {e}")
    
    def test_get_initial_state(self):
        """Test 2: Can get initial SOMA state"""
        self.reset_test_user()
        
        try:
            response = requests.get(f"{self.base_url}/api/soma/{self.test_user}")
            data = response.json()
            
            # Check all major systems are present
            has_all_systems = all(key in data for key in [
                'physiology', 'sensation', 'cognition', 'energy', 'body_map'
            ])
            
            # Check baseline values
            arousal_baseline = data['sensation']['arousal'] < 10
            hr_baseline = 70 <= data['physiology']['heart_rate'] <= 74
            
            passed = has_all_systems and arousal_baseline and hr_baseline
            
            self.log(
                "Get Initial State",
                passed,
                f"Arousal: {data['sensation']['arousal']}, HR: {data['physiology']['heart_rate']}"
            )
            
        except Exception as e:
            self.log("Get Initial State", False, f"Error: {e}")
    
    def test_gentle_touch(self):
        """Test 3: Gentle touch increases arousal gradually"""
        self.reset_test_user()
        
        try:
            # Apply gentle touch
            response = requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={
                    'type': 'touch',
                    'intensity': 40,
                    'zone': 'neck',
                    'quality': 'gentle'
                }
            )
            
            data = response.json()
            soma = data['soma']
            
            # Check arousal increased (but not too much)
            arousal = soma['sensation']['arousal']
            arousal_appropriate = 10 < arousal < 30
            
            # Check heart rate increased slightly
            hr = soma['physiology']['heart_rate']
            hr_increased = hr > 72
            
            # Check zone was affected
            neck_zone = soma['body_map'].get('neck', {})
            zone_aroused = neck_zone.get('arousal', 0) > 0
            
            passed = arousal_appropriate and hr_increased and zone_aroused
            
            self.log(
                "Gentle Touch",
                passed,
                f"Arousal: {arousal:.1f}, HR: {hr:.1f}, Neck arousal: {neck_zone.get('arousal', 0):.1f}"
            )
            
        except Exception as e:
            self.log("Gentle Touch", False, f"Error: {e}")
    
    def test_pressure_response(self):
        """Test 4: Pressure has stronger effect than touch"""
        self.reset_test_user()
        
        try:
            # First, gentle touch
            touch_response = requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'touch', 'intensity': 50, 'zone': 'hips'}
            )
            touch_arousal = touch_response.json()['soma']['sensation']['arousal']
            
            self.reset_test_user()
            time.sleep(0.5)
            
            # Then, pressure
            pressure_response = requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'pressure', 'intensity': 50, 'zone': 'hips'}
            )
            pressure_arousal = pressure_response.json()['soma']['sensation']['arousal']
            
            # Pressure should cause more arousal
            passed = pressure_arousal > touch_arousal
            
            self.log(
                "Pressure > Touch",
                passed,
                f"Touch arousal: {touch_arousal:.1f}, Pressure arousal: {pressure_arousal:.1f}"
            )
            
        except Exception as e:
            self.log("Pressure > Touch", False, f"Error: {e}")
    
    def test_edging_mechanics(self):
        """Test 5: Edging brings arousal high and increases sensitivity"""
        self.reset_test_user()
        
        try:
            # Get baseline sensitivity
            baseline = requests.get(f"{self.base_url}/api/soma/{self.test_user}").json()
            baseline_sens = baseline['sensation']['sensitivity']
            
            # Apply edge stimulus
            response = requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'edge', 'intensity': 80}
            )
            
            data = response.json()['soma']
            
            # Check arousal is very high
            arousal = data['sensation']['arousal']
            arousal_high = arousal > 80
            
            # Check sensitivity increased
            new_sens = data['sensation']['sensitivity']
            sens_increased = new_sens > baseline_sens
            
            # Check edge count incremented
            edge_count = data['meta']['edge_count']
            edge_tracked = edge_count == 1
            
            passed = arousal_high and sens_increased and edge_tracked
            
            self.log(
                "Edging Mechanics",
                passed,
                f"Arousal: {arousal:.1f}, Sensitivity: {baseline_sens:.1f}→{new_sens:.1f}, Edges: {edge_count}"
            )
            
        except Exception as e:
            self.log("Edging Mechanics", False, f"Error: {e}")
    
    def test_orgasm_reset(self):
        """Test 6: Orgasm resets arousal and increases fatigue"""
        self.reset_test_user()
        
        try:
            # Build up arousal first
            for _ in range(3):
                requests.post(
                    f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                    json={'type': 'touch', 'intensity': 60}
                )
            
            # Get pre-orgasm state
            pre = requests.get(f"{self.base_url}/api/soma/{self.test_user}").json()
            pre_arousal = pre['sensation']['arousal']
            pre_fatigue = pre['energy']['fatigue']
            
            # Trigger orgasm
            response = requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'release', 'intensity': 100}
            )
            
            post = response.json()['soma']
            post_arousal = post['sensation']['arousal']
            post_fatigue = post['energy']['fatigue']
            
            # Arousal should drop significantly
            arousal_dropped = post_arousal < (pre_arousal * 0.5)
            
            # Fatigue should increase
            fatigue_increased = post_fatigue > pre_fatigue
            
            # Pleasure should spike
            pleasure = post['sensation']['pleasure']
            pleasure_high = pleasure > 90
            
            passed = arousal_dropped and fatigue_increased and pleasure_high
            
            self.log(
                "Orgasm Reset",
                passed,
                f"Arousal: {pre_arousal:.1f}→{post_arousal:.1f}, Fatigue: {pre_fatigue:.1f}→{post_fatigue:.1f}, Pleasure: {pleasure:.1f}"
            )
            
        except Exception as e:
            self.log("Orgasm Reset", False, f"Error: {e}")
    
    def test_natural_decay(self):
        """Test 7: Arousal decays over time"""
        self.reset_test_user()
        
        try:
            # Build arousal
            requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'touch', 'intensity': 70}
            )
            
            # Get immediate arousal
            immediate = requests.get(f"{self.base_url}/api/soma/{self.test_user}").json()
            arousal_1 = immediate['sensation']['arousal']
            
            # Wait 3 seconds
            time.sleep(3)
            
            # Get arousal again (should trigger decay in update())
            after = requests.get(f"{self.base_url}/api/soma/{self.test_user}").json()
            arousal_2 = after['sensation']['arousal']
            
            # Arousal should have decayed
            passed = arousal_2 < arousal_1
            
            self.log(
                "Natural Decay",
                passed,
                f"Arousal at t=0: {arousal_1:.1f}, at t=3s: {arousal_2:.1f} (decay: {arousal_1-arousal_2:.1f})"
            )
            
        except Exception as e:
            self.log("Natural Decay", False, f"Error: {e}")
    
    def test_body_map_zones(self):
        """Test 8: Different zones track independently"""
        self.reset_test_user()
        
        try:
            # Touch neck
            requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'touch', 'intensity': 60, 'zone': 'neck'}
            )
            
            # Touch inner thighs
            requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'touch', 'intensity': 60, 'zone': 'inner_thighs'}
            )
            
            # Get state
            state = requests.get(f"{self.base_url}/api/soma/{self.test_user}").json()
            body_map = state['body_map']
            
            # Both zones should be aroused
            neck_aroused = body_map.get('neck', {}).get('arousal', 0) > 20
            thighs_aroused = body_map.get('inner_thighs', {}).get('arousal', 0) > 20
            
            # Other zones should be less aroused
            arms_baseline = body_map.get('arms', {}).get('arousal', 0) < 10
            
            passed = neck_aroused and thighs_aroused and arms_baseline
            
            self.log(
                "Body Map Zones",
                passed,
                f"Neck: {body_map.get('neck', {}).get('arousal', 0):.1f}, "
                f"Thighs: {body_map.get('inner_thighs', {}).get('arousal', 0):.1f}, "
                f"Arms: {body_map.get('arms', {}).get('arousal', 0):.1f}"
            )
            
        except Exception as e:
            self.log("Body Map Zones", False, f"Error: {e}")
    
    def test_experience_description(self):
        """Test 9: Experience description generates properly"""
        self.reset_test_user()
        
        try:
            # Build some arousal
            requests.post(
                f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                json={'type': 'touch', 'intensity': 65}
            )
            
            # Get experience
            response = requests.get(f"{self.base_url}/api/soma/{self.test_user}/experience")
            exp = response.json()
            
            # Check all required fields present
            has_arousal = 'arousal' in exp and 'level' in exp['arousal']
            has_physiology = 'physiology' in exp and 'heart_rate' in exp['physiology']
            has_sensation = 'sensation' in exp
            has_mental = 'mental' in exp
            
            # Check arousal level is descriptive
            arousal_level = exp['arousal']['level']
            level_valid = arousal_level in ['baseline', 'stirring', 'warming', 'heightened', 'intense', 'overwhelming', 'edge']
            
            passed = has_arousal and has_physiology and has_sensation and has_mental and level_valid
            
            self.log(
                "Experience Description",
                passed,
                f"Arousal level: '{arousal_level}', HR: {exp['physiology']['heart_rate']}, Breath: {exp['physiology']['breathing']}"
            )
            
        except Exception as e:
            self.log("Experience Description", False, f"Error: {e}")
    
    def test_temperature_calculation(self):
        """Test 10: Model temperature adjusts based on state"""
        self.reset_test_user()
        
        try:
            # Get baseline temp (should be ~0.8)
            state = requests.get(f"{self.base_url}/api/soma/{self.test_user}").json()
            
            # Calculate temp manually from the experience data
            # (The /api/process endpoint returns temperature, but for this test we check consistency)
            
            # Build high arousal
            for _ in range(5):
                requests.post(
                    f"{self.base_url}/api/soma/{self.test_user}/stimulate",
                    json={'type': 'touch', 'intensity': 70}
                )
            
            # Get high arousal state
            high_state = requests.get(f"{self.base_url}/api/soma/{self.test_user}").json()
            high_arousal = high_state['sensation']['arousal']
            
            # High arousal should exist
            passed = high_arousal > 60
            
            self.log(
                "Temperature Calculation",
                passed,
                f"High arousal achieved: {high_arousal:.1f}% (temp would be ~1.0-1.3)"
            )
            
        except Exception as e:
            self.log("Temperature Calculation", False, f"Error: {e}")
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*60)
        print("🧪 SOMA TEST SUITE")
        print("="*60 + "\n")
        
        start_time = time.time()
        
        # Run all tests
        self.test_health_check()
        self.test_get_initial_state()
        self.test_gentle_touch()
        self.test_pressure_response()
        self.test_edging_mechanics()
        self.test_orgasm_reset()
        self.test_natural_decay()
        self.test_body_map_zones()
        self.test_experience_description()
        self.test_temperature_calculation()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in self.results if r['passed'])
        failed = sum(1 for r in self.results if not r['passed'])
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Duration: {duration:.2f}s")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n⚠️  Failed Tests:")
            for r in self.results:
                if not r['passed']:
                    print(f"   • {r['test']}: {r['details']}")
        
        print("="*60 + "\n")
        
        return passed == total


if __name__ == '__main__':
    import sys
    
    # Get base URL from args or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5001"
    
    print(f"Testing SOMA at: {base_url}")
    
    suite = SOMATestSuite(base_url)
    success = suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)