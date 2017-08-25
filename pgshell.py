from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.application import Application
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.shortcuts import create_prompt_layout
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.buffer import Buffer, AcceptAction
from prompt_toolkit.filters import Condition

from pygments.token import Token
from pygments.lexers.go import GoLexer

def _multiline_evaluator(text):
    text = text.strip()

    return (
        text == 'exit' or
        text == 'quit' or
        _complete_sql_command(text)
        )
_complete_sql_command = lambda sql: sql.endswith(';')

class PBuffer(Buffer):

    def __init__(self, *args, **kwargs):

        @Condition
        def is_multiline():
            #get the doc instance
            doc = self.document

            return not _multiline_evaluator(doc.text)
        super(self.__class__, self).__init__(*args, is_multiline=True,
                                             tempfile_suffix='.sql', **kwargs)



        

    
class PGCli(object):
    
    def __init__(self):
        self.event_loop = create_eventloop()
        self.cli = None
    
    def run_cli(self):
        self.cli = self._build_cli()

        try:
            while True:
                document = self.cli.run()
        except EOFError:
            print('Good bye')
    
    def _build_cli(self):

        def prompt_tokens(_):
            return [(Token.Prompt, '>>>  ')]
        
        def get_continuation_tokens(cli, width):
            continuation = '.' * (width) + ' '
            return [(Token.Continuation, continuation)]
            
        layout = create_prompt_layout(
            lexer=PygmentsLexer(GoLexer),
            get_prompt_tokens=prompt_tokens,
            get_continuation_tokens=get_continuation_tokens,
            multiline=True
        )
        buff = PBuffer(
            accept_action=AcceptAction.RETURN_DOCUMENT
        )
        application = Application(
            buffer=buff,
            layout=layout,
            ignore_case=True,
            #multiline_mode=True
        )

        cli = CommandLineInterface(application=application, 
                                   eventloop=self.event_loop)
        return cli


def main():
    cli = PGCli()
    cli.run_cli()

if __name__ == '__main__':
    main()
