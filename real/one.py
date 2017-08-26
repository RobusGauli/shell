from collections import namedtuple
from queue import Queue
from queue import PriorityQueue
import pygments
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition

from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.shortcuts import create_prompt_layout
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.buffer import Buffer, AcceptAction
from pygments.lexers.go import GoLexer
from pygments.token import Token
from prompt_toolkit.styles import PygmentsStyle
token = Token.Toolbar

manager = KeyBindingManager()
registry = manager.registry

#attach the handler to the key using eh simle decorarion
#create a buffer to pass on to application istance
custom_style = { Token.Toolbar: '#ffffff bg:#333333', token.On: '#666', token.Off: '#999', Token.Prompt: '#00ff00', Token.Continuation: '#00ff00'}
style = PygmentsStyle.from_defaults(style_dict=custom_style, pygments_style_cls=pygments.styles.get_style_by_name('native'))
class PBuffer(Buffer):
	def __init__(self, always_multiline, *args, **kwargs):
		self.always_multiline = always_multiline
		@Condition
		def is_multiline():
			#get the document
			if self.document.text.endswith(';') or self.document.text == 'exit' or not self.always_multiline:
				return False
			return True
		super(self.__class__, self).__init__(*args, is_multiline=is_multiline, **kwargs, accept_action=AcceptAction.RETURN_DOCUMENT)
buffer = PBuffer(always_multiline=True)

snippets = 'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Thisis cool")\n}\n'
@registry.add_binding(Keys.ControlQ)
def exit(event):
	event.cli.set_return_value('this is the valut that was returned ')

@registry.add_binding(Keys.Tab)
def _(event):
	buf = event.cli.current_buffer
	buf.insert_text(' ' * 4)

@registry.add_binding(Keys.F4)
def _(event):
	buf = event.cli.current_buffer
	buf.always_multiline = not buf.always_multiline

@registry.add_binding(Keys.ControlA)
def _(event):
	buff = event.cli.current_buffer
	buff.insert_text(snippets, move_cursor=False)
	buff.cursor_down(count=3)

get_prompt_tokens = lambda _: [(Token.Prompt, '#> ')]
get_continuation_tokens = lambda cli, width: [(Token.Continuation, '.' * (width - 1) +  ' ' )]



def get_toolbar_tokens(cli):
	result = []
	
	buff = cli.current_buffer
	text = 'Multiline: ON' if buff.always_multiline else 'Multliline: OFF'
	if buff.always_multiline:
		result.append((token.On, '[F4]  %s' % text))
	else:
		result.append((token.Off, '[F4] %s' % text))
	return result



	
layout = create_prompt_layout(
	lexer=PygmentsLexer(GoLexer),
	get_prompt_tokens=get_prompt_tokens,
	get_continuation_tokens=get_continuation_tokens,
	get_bottom_toolbar_tokens=get_toolbar_tokens,
	multiline=True	
)



def main():
	loop = create_eventloop()
	application = Application(layout=layout, key_bindings_registry=registry, buffer=buffer, style=style)
	cli = CommandLineInterface(application=application, eventloop=loop)
	while True:
		document = cli.run()
		if document.text == 'exit':
			break
		print('value retured ', document)
	print('thank you exisiting', document)

if __name__ == '__main__':
	main()
	
