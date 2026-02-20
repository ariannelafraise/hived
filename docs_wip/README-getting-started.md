Will explain how Hived works, how logs are parsed and made available to applications. Link to Installation & Modules documentation.

## How does Hived function?
There are two main components: Hived and Hivectl.

### Hived
The daemon registered as a plugin to Audispd that receives audit events and forwards them to modules using the Observer design pattern.

> [!IMPORTANT]
> Running Hived on its own has no effect, it **needs** to be run by Audispd to receive events.
> However, it allows you to feed it your own logs for testing purposes.

### Hivectl
A CLI tool to configure Hived. Applications can add their own commands for .....

> [!IMPORTANT]
> Hivectl needs to be run as root since it performs administrative tasks such as configuring the audit framework.
