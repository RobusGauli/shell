from collections import namedtuple
from queue import Queue
from queue import PriorityQueue

from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition

from prompt_toolkit.shortcuts import create_prompt_layout
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.buffer import Buffer, AcceptAction
from pygments.lexers.go import GoLexer
from pygments.token import Token

manager = KeyBindingManager()
registry = manager.registry

#attach the handler to the key using eh simle decorarion
#create a buffer to pass on to application istance

class PBuffer(Buffer):
	def __init__(self, *args, **kwargs):
		@Condition
		def is_multiline():
			#get the document
			if self.document.text.endswith(';'):
				return False
			return True
		super(self.__class__, self).__init__(*args, is_multiline=is_multiline, **kwargs, accept_action=AcceptAction.RETURN_DOCUMENT)
buffer = PBuffer()

@registry.add_binding(Keys.ControlQ)
def exit(event):
	event.cli.set_return_value('this is the valut that was returned ')

get_prompt_tokens = lambda _: [(Token.Prompt, '>>>>')]
get_continuation_tokens = lambda cli, width: [(Token.Continuation, '.' * width + ' ')]
layout = create_prompt_layout(
	lexer=PygmentsLexer(GoLexer),
	get_prompt_tokens=get_prompt_tokens,
	get_continuation_tokens=get_continuation_tokens,
	
)



def main():
	loop = create_eventloop()
	application = Application(layout=layout, key_bindings_registry=registry, buffer=buffer)
	cli = CommandLineInterface(application=application, eventloop=loop)
	while True:
		document = cli.run()
		if document == 'exit':
			break
		print('value retured ', document)
	print('thank you exisiting', document)

if __name__ == '__main__':
	main()
	
