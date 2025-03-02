import gradio as gr
from chatbot import ChatBot

bot = ChatBot()

def respond(message, history):
    response = bot.get_answer(message)
    return gr.update(value=response, visible=True)

with gr.Blocks() as demo:
    gr.Markdown("## Eye Health Chatbot")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your Question")
    clear = gr.Button("Clear")
    
    msg.submit(respond, [msg, chatbot], [msg])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()