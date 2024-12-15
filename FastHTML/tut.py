# timestamp 12:00
# https://picocss.com/docs/card
# https://docs.fastht.ml/explains/minidataapi.html
# https://mikelev.in/fasththml-websockets-database/
# https://www.danliden.com/notebooks/web_dev/fasthtml/4_databases.html
# https://github.com/AnswerDotAI/fasthtml/blob/main/examples/todos4.py

from fasthtml.common import *

MAX_NAME_CHAR = 15
MAX_MESSAGE_CHAR = 50

app,rt = fast_app()


def render_content():
  form = Form(
    Fieldset(
      Input(
        type='text',
        name='name',
        placeholder='Name',
        required=True,
        max_length=MAX_NAME_CHAR,
      ),
      Input(
        type='text',
        name='name',
        placeholder='Message',
        required=True,
        max_length=MAX_MESSAGE_CHAR,
      ),
      Button('Submit', type='submit'),
      role='group',  # stack Input horizontally
    )
  )

  return (
    Div(
      P(I(('Write something nice'))),  # italicize     
      form,
      Hr(),
      # render_message()
      render_message_list()      
      )
  )


def render_message(entry):
  return (
    Article(
      Header(f'Name: {entry["name"]}'),
      P(entry['message']),
      Footer(Small(I(f'Posted: {entry["timestamp"]}'))),
    )
  )


def render_message_list():
  messages = [
    {'name': 'John', 'message': 'Hi there!', 'timestamp': 'now'},
    {'name': 'Jane', 'message': 'Hello', 'timestamp': 'yesterday'},    
  ]

  return Div(
    *[render_message(entry) for entry in messages],  # * unpack entry one by one
  )


@rt('/')
def get(): 
  return (
    Titled('My Guest Book 😉', render_content())
  )






serve()
