''' A simple shell CLI '''
import sys
import sqlite3
import random

import prompt_toolkit as pt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import AbortAction
from pygments.lexers import SqlLexer
from pygments.token import Token
from pygments.style import Style
from pygments.styles.default import DefaultStyle


class DocumentStyle(Style):
    '''style representation'''
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)
    
completion_words = [
    'select',
    'create',
    'update',
    'delete',
    'drop',
    'from',
    'where',
    'table',
    'join',
    'import',
    'import "fmt"'
]

completer = WordCompleter(completion_words, ignore_case=True)
random_sayings = 'Hi Hello Sorry Thanks Welcome'.split()
bottom_toolbar_tokens= lambda cli: [(Token.Toolbar, random.choice(random_sayings))]

def main(database):
    '''testing'''
    connection = sqlite3.connect(database)
    history = InMemoryHistory()
    while True:
        try:
            text = pt.prompt('>', history=history, lexer=SqlLexer,
                                        completer=completer,
                                        style=DocumentStyle,
                                        # on_abort=AbortAction.RETRY,
                                        display_completions_in_columns=True,
                                        get_title=lambda : 'Interactive REPL',
                                        get_bottom_toolbar_tokens=bottom_toolbar_tokens)
        except (EOFError, KeyboardInterrupt):
            break
            
        completion_words.append(text)
        with connection:
            messages = connection.execute(text)
            for message in messages:
                print(message)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        db = ':memory:'
    else:
        db = sys.argv[1]
    main(db)
