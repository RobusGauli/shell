'''dict_keys(['__module__', '__doc__', '__slots__', '__init__', '__repr__', 'text', 'cursor_position',
'selection', 'current_char', 'char_before_cursor', 'text_before_cursor', 'text_after_cursor', 'current_l
ine_before_cursor', 'current_line_after_cursor', 'lines', '_line_start_indexes', 'lines_from_current', '
line_count', 'current_line', 'leading_whitespace_in_current_line', '_get_char_relative_to_cursor', 'on_f
irst_line', 'on_last_line', 'cursor_position_row', 'cursor_position_col', '_find_line_start_index', 'tra
nslate_index_to_position', 'translate_row_col_to_index', 'is_cursor_at_the_end', 'is_cursor_at_the_end_o
f_line', 'has_match_at_current_position', 'find', 'find_all', 'find_backwards', 'get_word_before_cursor'
, 'find_start_of_previous_word', 'find_boundaries_of_current_word', 'get_word_under_cursor', 'find_next_word_beginning', 'find_next_word_ending', 'find_previous_word_beginning', 'find_previous_word_ending', 'find_next_matching_line', 'find_previous_matching_line', 'get_cursor_left_position', 'get_cursor_right_position', 'get_cursor_up_position', 'get_cursor_down_position', 'find_enclosing_bracket_right', 'find_enclosing_bracket_left', 'find_matching_bracket_position', 'get_start_of_document_position', 'get_end_of_document_position', 'get_start_of_line_position', 'get_end_of_line_position', 'last_non_blank_of_current_line_position', 'get_column_cursor_position', 'selection_range', 'selection_ranges', 'selection_range_at_line', 'cut_selection', 'paste_clipboard_data', 'empty_line_count_at_the_end', 'start_of_paragraph', 'end_of_paragraph', 'insert_after', 'insert_before', '_cache', '_cursor_position', '_selection', '_text']
'''


''' CLI -->
'application', 'eventloop', '_is_running', 'output', 'input', 'buffers', 'editing_mode', 'quoted_insert', 'v
i_state', 'renderer', 'render_counter', 'max_render_postpone_time', '_invalidated', 'input_processor', '_async_completers
', '_sub_cli', 'on_buffer_changed', 'on_initialize', 'on_input_timeout', 'on_invalidate', 'on_render', 'on_reset', 'on_st
art', 'on_stop', '_exit_flag', '_abort_flag', '_return_value', 'search_state']
'''

'''
EVENT --> 
'data', 'input_processor', 'cli', 'current_buffer', 'arg',
'arg_present', 'append_to_arg_count'
'''
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator, ValidationError

from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict

from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import EditingMode

from prompt_toolkit.buffer import indent
manager = KeyBindingManager.for_prompt()

@manager.registry.add_binding(Keys.Tab)
def _(event):
  '''toggle between multiline and single line '''
  cli = event.cli
  #print(event.__class__.__dict__.keys())
  #print(event.current_buffer.__dict__)
  #indent(event.current_buffer, from_row=0, to_row=4)
  print(event.current_buffer.is_multiline)
def get_bottom_toolbar_tokens(cli):
  text = 'there ' if cli.editing_mode == EditingMode.VI else 'Emacs'

  return [(Token.Toolbar, text)]
style = style_from_dict({
  Token.Toolbar: '#ffffff bg:#333333'
})

class NumberValidator(Validator):
  def validate(self, document):
    text = document.text
    
    if text and not text.isdigit():
      #default index 
      index = 0
      for i, c in enumerate(text):
        if not c.isdigit() and c != ' ':
          break
      raise ValidationError(message='this input contains nonnumeric', cursor_position=i)
class MyCustomCompleter(Completer):
  '''Custom completion class'''

  def get_completions(self, doc, complete_event):
    if doc.text == 'yes':
      #print(doc.__class__.__name__)
      doc = doc.insert_after('yeah i am inserder')
      yield Completion('yeah', start_position=-2)
    else:
      yield Completion('completion', start_position=0)
    

text = prompt('>>', completer=MyCustomCompleter(), 
              validator=NumberValidator(),
              get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
              style=style,
              key_bindings_registry=manager.registry
              )