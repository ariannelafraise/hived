# HiveSec API Documentation

## Overview

HiveSec is an open-source Linux Audit Event processing framework built on top of the Linux audit subsystem. It provides a Python package (published on PyPI as `hivesec`) that enables developers to create custom applications for monitoring, analyzing, and responding to Linux audit events in real-time.

The framework uses the **Observer Design Pattern** to decouple event sources from event handlers, making it easy to plug in custom processing logic.

---

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    HiveSec Framework                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐          ┌─────────────────────────┐  │
│  │   Audispd        │ ----- >  │  AuditEventDispatcher   │  │
│  │   Listener       │  Events  │       (Subject)         │  │
│  └──────────────────┘          └────────────┬────────────┘  │
│                            Observe & React  │               │
│  ┌──────────────────┐            ┌──────────┴─────────────┐ │
│  │   External       │ -------- > │   AuditEventHandler    │ │
│  │   Applications   │  Register  │      (Observers)       │ │
│  └──────────────────┘            └────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input**: The `AudispdListener` reads audit logs fed by audispd daemon
2. **Processing**: Logs are parsed and grouped into complete `AuditEvent` objects
3. **Distribution**: Events are sent to all registered `AuditEventHandler` observers
4. **Handling**: Each handler processes events according to its own logic

---

## Installation

### Prerequisites

- Linux system with Linux Audit installed

### Installing the API Package

```bash
pip install hivesec
```

Or from source:

```bash
cd api
python -m pip install .
```

---

## Quick Start Guide

### Creating Your First Event Handler

1. **Install the package** in your development environment or external app directory

2. **Create a handler class** that inherits from `AuditEventHandler`:

```python
from hivesec import AuditEventHandler, AuditEvent

class MySecurityHandler(AuditEventHandler):
    """Example security event handler"""
    
    def _applies_to(self, event: AuditEvent) -> bool:
        """Check if this event should be handled"""
        for record in event.records:
            if "auth" not in record.get_field_value("syscall").lower():
                return False
        return True
    
    def handle(self, event: AuditEvent):
        """Process the audit event"""
        print(f"Processing security event with {len(event.records)} records")
```

3. **Register your handler** by adding it to `/etc/hivesec/apps`

---

## API Reference

### Core Classes

#### `AuditEvent`

Represents a complete audit event composed of multiple records.

**Attributes:**
- `records`: List of [`AuditRecord`](#auditrecord) objects belonging to this event

---

#### `AuditRecord`

Represents a single audit log record. Can be accessed as either a string or a dictionary.

**Attributes:**
- `_as_string`: Original string representation (with quotes preserved for consistency with auditd logs)
- `_fields`: Dictionary of parsed key-value fields

---

#### `AuditEventObserver`

Abstract base class defining the observer interface. This is what your handlers should inherit from (typically through [`AuditEventHandler`](#auditeventhandler)).

---

#### `AuditEventHandler`

The primary interface for creating custom audit event handlers. Inherits from both [`AuditEventObserver`](#auditeventobserver) and implements additional functionality.
