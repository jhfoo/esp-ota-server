# esp-ota-server (STATUS: INCOMPLETE)
Host and manage your ESP IoT server

## Goals
- Empower one to manage their own IoT device (ESP8266, ESP32) code independently and wirelessly.

## Implementation
- Devices register with the server with:
  - DeviceId
  - Access key
- Devices are assigned to groups internally. Each group maps to a code repo (GitHub) 
- A .otaignore file identifies files excluded from OTA download
- Server polls code repos for commit changes

## Supported languages
- Micropython
- Lua (roadmap)
- Javascript (roadmap)
