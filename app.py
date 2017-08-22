from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys

from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.dimension import LayoutDimension as D

from prompt_toolkit.filters import Condition, HasFocus, IsReturning

from pygments.token import Token

layout = VSplit([
  Window(content=BufferControl(buffer_name=DEFAULT_BUFFER)),
  Window(width=D.exact(1),
        content=FillControl('|', token=Token.Line)),
  Window(content=TokenListControl(
    get_tokens=lambda cli: [(Token, 'Hello world')]
  )),
  Window(content=BufferControl(buffer_name=DEFAULT_BUFFER))
])

manager = KeyBindingManager()
registry = manager.registry

@registry.add_binding(Keys.ControlQ, eager=True)
def exit_(event):
  '''
  Pressing Ctrl-Q will exit the user interface.abs
  '''
  #event.cli.set_return_value(None)
  print(event)


is_searching = Condition(lambda cli: cli.is_searching)

prompt_manager = KeyBindingManager.for_prompt()
@prompt_manager.registry.add_binding(Keys.ControlT, filter=~IsReturning(), eager=True)
def _(event):
  print('yea right there')

loop = create_eventloop()
application = Application(key_bindings_registry=registry, layout=layout, mouse_support=True)
cli = CommandLineInterface(application=application, eventloop=loop)

#running the event loop
cli.run()
print('Exiting')

