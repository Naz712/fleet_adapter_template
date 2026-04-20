# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


'''
    The RobotAPI class is a wrapper for API calls to the robot. Here users
    are expected to fill up the implementations of functions which will be used
    by the RobotCommandHandle. For example, if your robot has a REST API, you
    will need to make http request calls to the appropriate endpoints within
    these functions.
'''


from urllib.error import HTTPError

import requests


class RobotAPI:
    # The constructor below accepts parameters typically required to submit
    # http requests. Users should modify the constructor as per the
    # requirements of their robot's API
    def __init__(self, config_yaml):
        self.prefix = config_yaml['prefix']
        self.user = config_yaml['user']
        self.password = config_yaml['password']
        self.timeout = 5.0
        self.debug = False
        self.last_nav_task = None

    def localize(self, robot_name: str, pose, map_name: str):
        '''
        Relocalize the ev1 after power-on using operator-provided coordinates.
        Tells the robot where it currently IS — does not move the robot.
        Returns True if robot accepted the request, else False.
        Assumed endpoint: POST /ev1/localize
        '''
        if pose is None or len(pose) != 3:
            raise ValueError(
                f'Invalid pose for {robot_name}: '
                f'expected [x, y, yaw], got {pose}'
            )
        url = self.prefix + f'/ev1/localize?robot_name={robot_name}'
        position_json = {}
        position_json['x'] = pose[0]
        position_json['y'] = pose[1]
        position_json['yaw'] = pose[2]
        position_json['map_name'] = map_name
        try:
            response = requests.post(url, json=position_json, timeout=self.timeout)
            if self.debug:
                print(f'localize response: {response.json()}')
            if response.status_code == 200:
                return True
        except HTTPError as http_err:
            print(f'HTTP error in localize for {robot_name}: {http_err}')
        except Exception as err:
            print(f'Other error in localize for {robot_name}: {err}')
        return False

    def navigate(self, robot_name: str, pose, map_name: str, speed_limit=0.0):
        '''
        Request the ev1 to navigate to pose [x, y, yaw] on the given map.
        Returns True if the robot accepted the request, else False.
        Assumed endpoint: POST /ev1/navigate
        '''
        if pose is None or len(pose) != 3:
            raise ValueError(
                f'Invalid pose for {robot_name}: '
                f'expected [x, y, yaw], got {pose}'
            )
        
        self.last_nav_task = {
            'robot_name': robot_name,
            'pose': pose,
            'map_name': map_name,
            'speed_limit': speed_limit
        }
        url = self.prefix + f'/ev1/navigate?robot_name={robot_name}'
        data = {
            'map_name': map_name,
            'destination': {
                'x': pose[0],
                'y': pose[1],
                'yaw': pose[2]
            },
            'speed_limit': speed_limit
        }
        try:
            response = requests.post(url, json=data, timeout=self.timeout)
            if self.debug:
                print(f'navigate response: {response.json()}')
            if response.status_code == 200:
                return True
        except HTTPError as http_err:
            print(f'HTTP error in navigate for {robot_name}: {http_err}')
        except Exception as err:
            print(f'Other error in navigate for {robot_name}: {err}')
        return False

    def stop(self, robot_name: str):
        '''
        Command the ev1 to stop immediately.
        Returns True if robot accepted the stop command, else False.
        '''
        url = self.prefix + f'/ev1/stop?robot_name={robot_name}'
        try:
            response = requests.post(url, timeout=self.timeout)  # added timeout
            if response.status_code == 200:
                return True
        except HTTPError as http_err:
            print(f'HTTP error in stop for {robot_name}: {http_err}')
        except Exception as err:
            print(f'Other error in stop for {robot_name}: {err}')
        return False

    def resume(self, robot_name: str):
        '''
        Resume navigation after a stop by re-issuing the last navigate command.
        Returns True if successful, else False.
        '''
        if self.last_nav_task is None:
            print(f'Resume failed for {robot_name}: no previous task stored')
            return False
        print(f'Resuming: re-issuing last navigate command for {robot_name}')
        return self.navigate(**self.last_nav_task)
    

class RobotUpdateData:
    ''' Update data for a single robot. '''
    def __init__(self,
                 robot_name: str,
                 map: str,
                 position: list,
                 battery_soc: float,
                 requires_replan: bool = False):
        self.robot_name = robot_name
        self.position = position        # [x, y, yaw]
        self.map = map                  # e.g. 'L1'
        self.battery_soc = battery_soc  # 0.0 to 1.0
        self.requires_replan = requires_replan
