import sys
sys.path.insert(0, 'fleet_adapter_template/fleet_adapter_template')

from RobotClientAPI import RobotAPI

config = {
    'prefix': 'http://localhost:8080',
    'user': 'test',
    'password': 'test'
}

api = RobotAPI(config)
robot = 'ev1'

print('--- Test 1: localize ---')
result = api.localize(robot, [3.5, 7.0, 0.5], 'L1')
print(f'Result: {result}')

print('--- Test 2: navigate ---')
result = api.navigate(robot, [10.0, 8.0, 0.0], 'L1')
print(f'Result: {result}')

print('--- Test 3: stop ---')
result = api.stop(robot)
print(f'Result: {result}')

print('--- Test 4: resume ---')
result = api.resume(robot)
print(f'Result: {result}')

print('--- Test 5: bad pose ---')
try:
    api.navigate(robot, [1.0, 2.0], 'L1')
except ValueError as e:
    print(f'Caught expected error: {e}')