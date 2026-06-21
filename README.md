# HiveSec

![Logo](./media/hivesec-square.png)

[![Upload Python Package](https://github.com/ariannelafraise/hivesec/actions/workflows/pypi.yml/badge.svg)](https://github.com/ariannelafraise/hivesec/actions/workflows/pypi.yml)
![PyPI](https://img.shields.io/pypi/v/hivesec?label=PyPi%20package)

HiveSec is an open-source Linux audit event processing framework built on top of the Linux Audit subsystem. 

It subscribes as an Audispd plugin, receiving Linux audit events in real time. These events are deserialized into high-level Python objects, allowing developers to focus on analysis rather than log parsing. The `hivesec` Python package provides the framework and programming interface for building custom applications that monitor, analyze, and respond to Linux audit events in real time.

## Data flow

```
+----------------------+
| Linux Audit          |
| (audispd)            |
+----------------------+
           |
      Audit Events
           |
           v
+----------------------+
| HiveSec Daemon       |
+----------------------+
           |
 Dispatches Events
           |
           v
+----------------------+
| AuditEventHandlers   |
+----------------------+
           ^
           |
      Registers
           |
+----------------------+
| HiveSec Applications |
+----------------------+
```

1. **Input**: The `AudispdListener` reads audit logs fed by the audispd daemon
2. **Processing**: Logs are parsed and grouped into complete `AuditEvent` objects
3. **Distribution**: Events are sent to all registered `AuditEventHandler` observers
4. **Handling**: Each handler processes events according to its own logic

## Components

### hivesecd
hivesecd is the daemon that is subscribed to Audispd as a plugin. Upon receiving Linux Audit events, it follows the Observer design pattern to distribute
them to all registered HiveSec applications.

### hivectl
hivectl is the CLI tool to interact with:
- Linux Audit (ex: adding rules)
- HiveSec applications (with their plugins)
- HiveSec (ex: registering an application)

It needs to be ran as root or with sudo, since it performs administrative actions.

## Documentation
- [Installation](./docs/installation.md)
- [Getting started: Developing HiveSec applications](./docs/development.md)

