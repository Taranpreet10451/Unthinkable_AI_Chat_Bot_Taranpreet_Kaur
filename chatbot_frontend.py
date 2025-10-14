import os
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["GRADIO_ANALYTICS_COLLECT_IP"] = "False"
import gradio as gr
import requests
import uuid

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:5000/chat"
RESET_URL = "http://127.0.0.1:5000/reset"
HEALTH_URL = "http://127.0.0.1:5000/health"
BOT_TITLE = "AI Customer Support Bot"
BOT_DESCRIPTION = "Welcome to Unthinkable Solutions AI Customer Support! How can I help you today?"

# --- Backend helpers ---
def send_to_backend(message: str, session_id: str):
    if not session_id:
        session_id = str(uuid.uuid4())
    try:
        r = requests.post(BACKEND_URL, json={"session_id": session_id, "message": message}, timeout=15)
        r.raise_for_status()
        data = r.json()
        reply = data.get("reply", "")
        source = data.get("source", "")
        return reply or "(empty response)", source or "", session_id
    except requests.exceptions.RequestException as e:
        return f"❌ Error contacting backend: {e}", "error", session_id
    except Exception as e:
        return f"❌ Unexpected error: {e}", "error", session_id

def reset_backend_session(session_id: str):
    try:
        if not session_id:
            return False, "No session to reset."
        r = requests.post(RESET_URL, json={"session_id": session_id}, timeout=10)
        if r.status_code == 200:
            return True, "Session history cleared."
        return False, r.text
    except Exception as e:
        return False, str(e)

def fetch_health_markdown():
    try:
        r = requests.get(HEALTH_URL, timeout=5)
        if r.status_code != 200:
            return "**Backend:** Unavailable"
        data = r.json()
        faq_count = data.get("services", {}).get("faq_system", {}).get("faq_count", "-")
        gemini_status = data.get("services", {}).get("gemini_ai", {}).get("status", "unavailable")
        status = data.get("status", "unhealthy")
        color = "#16a34a" if status == "healthy" else "#dc2626"
        return (
            f"<div style='display:flex;gap:12px;align-items:center'>"
            f"<div style='width:10px;height:10px;border-radius:50%;background:{color}'></div>"
            f"<b>Backend:</b> {status} • <b>FAQs:</b> {faq_count} • <b>AI:</b> {gemini_status}"
            f"</div>"
        )
    except Exception:
        return "**Backend:** Unavailable"

# --- UI event handlers ---
def handle_send(user_text, chat_history, session_id):
    user_text = (user_text or "").strip()
    if not user_text:
        return chat_history, "", session_id
    chat_history = chat_history or []
    chat_history.append((user_text, ""))
    reply, source, session_id = send_to_backend(user_text, session_id)
    if source and source not in ("", "error"):
        reply = f"{reply}\n\n— Source: {source}"
    chat_history[-1] = (user_text, reply)
    return chat_history, "", session_id

def new_session(_: str):
    return [], str(uuid.uuid4())

def clear_chat_only(_: str):
    return []

def do_reset_backend(session_id, chat_history):
    ok, msg = reset_backend_session(session_id)
    note = f"✅ {msg}" if ok else f"❌ {msg}"
    chat_history = chat_history or []
    chat_history.append(("(system)", note))
    return chat_history

def fill_prompt(prompt_text: str):
    return prompt_text

# --- Gradio UI ---
with gr.Blocks(theme='soft', title=BOT_TITLE, fill_height=True) as demo:
    session_id_state = gr.State(str(uuid.uuid4()))

    with gr.Row():
        gr.Markdown(f"# {BOT_TITLE}")

    with gr.Row():
        health_md = gr.Markdown(value=fetch_health_markdown())

    with gr.Row():
        with gr.Column(scale=8):
            chatbot = gr.Chatbot(height=420)
            with gr.Row():
                user_input = gr.Textbox(placeholder="Type your message...", lines=2, scale=8)
                send_btn = gr.Button("Send", variant="primary", scale=1)
                clear_btn = gr.Button("Clear", scale=1)
        with gr.Column(scale=4, min_width=280):
            gr.Markdown("### Quick prompts")
            with gr.Row():
                qp1 = gr.Button("Reset my password")
                qp2 = gr.Button("Business hours")
            with gr.Row():
                qp3 = gr.Button("Refund policy")
                qp4 = gr.Button("Talk to human agent")
            gr.Markdown("### Session")
            new_session_btn = gr.Button("New session")
            reset_backend_btn = gr.Button("Reset backend history")
            session_md = gr.Markdown(value="")

    # Events
    send_btn.click(handle_send, inputs=[user_input, chatbot, session_id_state], outputs=[chatbot, user_input, session_id_state])
    user_input.submit(handle_send, inputs=[user_input, chatbot, session_id_state], outputs=[chatbot, user_input, session_id_state])
    clear_btn.click(clear_chat_only, inputs=[session_id_state], outputs=[chatbot])
    new_session_btn.click(new_session, inputs=[session_id_state], outputs=[chatbot, session_id_state])
    reset_backend_btn.click(do_reset_backend, inputs=[session_id_state, chatbot], outputs=[chatbot])
    qp1.click(lambda: "How do I reset my password?", outputs=[user_input])
    qp2.click(lambda: "What are your business hours?", outputs=[user_input])
    qp3.click(lambda: "What is your refund policy?", outputs=[user_input])
    qp4.click(lambda: "I want to talk to a human agent.", outputs=[user_input])
    session_id_state.change(lambda s: f"Session: `{s}`", inputs=session_id_state, outputs=session_md)

# --- Launch the App ---
if __name__ == "__main__":
    print("🚀 Launching Gradio Frontend...")
    print("Please ensure the Flask backend (app.py) is running in a separate terminal.")
    demo.launch(server_name="127.0.0.1", server_port=7860, show_api=False)