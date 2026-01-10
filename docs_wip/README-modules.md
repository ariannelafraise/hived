Specific plugin commands can be accessed by specifying the name of the plugin as such:
```bash
# hivectl [plugin name] [command]
```

## Plugin/Extension API
> [!IMPORTANT]
> Refer to the UML class diagram shown earlier to better understand this section.

There are three ways of adding your own functionalities: event handlers, notifiers and hivectl plugins.
### Event handlers
These are loaded dynamically by AudispdListener from the `event_handlers` directory. The Observer design pattern is used 
to feed every new event received by AudispdListener all event handlers. 

They should implement the EventHandler interface that defines two methods: applies_to(e: Event) and handle(e: Event).

- handle() is the method that will be called on each new event.
- applies_to() should be called at the beginning of handle() to decide if the event handler should act on or ignore the event.

Code example:
```python
class ExampleEventHandler(EventHandler):
    def _applies_to(self, event: Event) -> bool:
        logs_str = ""
        for log in event.logs:
            logs_str += log.as_string
        if "key=\"example\"" in logs_str:
            return True
        return False

    def handle(self, event: Event):
        if not self._applies_to(event):
            return

        [do stuff]
```
### Notifiers
These can be used by event handlers to send out notifications, like emails.

They should implement the Notifier interface, as utility classes (they are not meant to be instantiated).
It defines the notify(sender: str, message: str) method, which fires the notification.

Code example:
```python
class ExampleNotifier(Notifier):
    @staticmethod
    def notify(sender: str, message: str):
        [send out notification]
```
### Hivectl plugins
These are loaded dynamically by Hivectl from the `plugins` directory. They extend Hivectl's functionalities by adding
commands using the argparse library. Hivectl calls the init_args_parser 

They should implement the Plugin interface, as utility classes (they are not meant to be instantiated).
It defines two methods: init_args_parser(subparser: argparse._SubParsersAction) and handle_command(args: argparse.Namespace).

- init_args_parser() adds its own command subparser Hivectl's main parser. Hivectl calls this function for each plugin and feeds it its main parser.
- handle_command() handles all commands received by the plugins subparser.

Code example:
```python
class ExamplePlugin(Plugin):
    @staticmethod
    def init_args_parser(subparser: argparse._SubParsersAction):
        parser = subparser.add_parser("example-plugin")
        parser.set_defaults(func=ExamplePlugin.handle_command) # Defines the handle_command() method as the handling function
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-v', '--version', help='View currently installed version.', action='version', version=f"example-plugin v1")
        group.add_argument('-w', '--hello', help='Say hello', action="store_true")

    @staticmethod
    def handle_command(args: argparse.Namespace):
        if args.hello:
            print("Hello, World!")
```
