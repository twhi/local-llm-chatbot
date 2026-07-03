import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Local AI Chat", layout="centered")
st.title("Local LLM Chat")


@st.cache_resource
def get_openai_client():
    return OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="placeholder")


client = get_openai_client()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant.",
            "reasoning": None,
        }
    ]

# Render chat history with expanders for past reasoning
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            if message.get("reasoning"):
                with st.expander("💭 Thinking Process"):
                    st.markdown(message["reasoning"])
            st.markdown(message["content"])

if user_input := st.chat_input("Type your message here..."):
    # Store user input
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "reasoning": None}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # Strip out the 'reasoning' key before sending to the model to save context window
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        stream = client.chat.completions.create(
            model="default",
            messages=api_messages,
            stream=True,
        )

        reasoning_text = ""
        content_text = ""

        reasoning_placeholder = None
        content_placeholder = None
        expander = None

        for chunk in stream:
            delta = chunk.choices[0].delta
            reasoning = getattr(delta, "reasoning_content", None)
            content = getattr(delta, "content", None)

            if reasoning:
                # Create the expander the first time we see reasoning tokens
                if expander is None:
                    expander = st.expander("💭 Thinking Process", expanded=False)
                    reasoning_placeholder = expander.empty()

                reasoning_text += reasoning
                reasoning_placeholder.markdown(
                    reasoning_text + "▌"  # ▌ adds a visual cursor
                )

            if content:
                # Clean up the reasoning cursor once final content begins
                if reasoning_placeholder and expander:
                    reasoning_placeholder.markdown(reasoning_text)

                # Create the content placeholder for the first content tokens
                if content_placeholder is None:
                    content_placeholder = st.empty()

                content_text += content
                content_placeholder.markdown(content_text + "▌")

        # Clean up the final cursor when generation stops
        if content_placeholder:
            content_placeholder.markdown(content_text)
        elif reasoning_placeholder:
            reasoning_placeholder.markdown(reasoning_text)

    # Save both outputs to state
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": content_text,
            "reasoning": reasoning_text if reasoning_text else None,
        }
    )
