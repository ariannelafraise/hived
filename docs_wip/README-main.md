# Hived
A [Linux Audit](https://github.com/linux-audit) event processing framework aiming to provide an API for making system-event-driven applications, such as security monitoring tools.

## Documentation
[Getting Started](./README-getting-started.md)
[Installation](./README-installation.md)
[Modules](./README-modules.md)

Il repose sur un modèle d’inversion de contrôle (IoC) : les développeurs peuvent enregistrer leurs propres gestionnaires d’événements, tandis que le framework se charge de recevoir, désérialiser, grouper et distribuer automatiquement les événements.
Le patron de conception Observateur est utilisé afin d'acheminer efficacement les événements.

Grâce à cet outil, il devient simple de développer des applications réagissant aux événements systèmes, notamment pour le monitoring de sécurité.


Hived is a extensible tool built on top of the Linux Audit framework that helps to setup honeypots on your linux machines.
It provides an extension/plugin API, to add custom features.

## Context
The Linux Audit framework records various system events and logs them.
The Auditd daemon sends these logs to either the `audit.log` file or Audispd.
The latter feeds those logs to registered plugins. This is where Hived comes in.
It forwards those events to audit event handlers that analyze them and act accordingly.

![audit framework diagram](./documentation/linux-audit-architecture.png)

[(source)](https://www.researchgate.net/figure/Linux-Auditd-Architecture_fig2_355181208)

### Interesting resources to better understand the Audit Framework
- [Red Hat Documentation - Chapter 7. System Auditing](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/security_guide/chap-system_auditing)
- [The Linux Audit Project (Github organization)](https://github.com/linux-audit)

## How does Hived function?
There are two main components: Hived and Hivectl.

### Hived
The daemon (registered as a plugin to Audispd) that receives all logged events and forwards them to audit event handlers.

> [!IMPORTANT]
> Running Hived on its own has no effect, it **needs** to be run by Audispd to receive events.
> However, it allows you to feed it your own logs for testing purposes.

> [!NOTE]
> You can create your own custom event handlers and notifiers by referring to the Plugin/Extension API section.

### Hivectl
A CLI tool to configure Hived.

> [!IMPORTANT]
> Hivectl needs to be run as root since it performs administrative tasks such as configuring the audit framework.
