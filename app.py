import streamlit as st
import pandas as pd
import random
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
# import subprocess

# Configuration
st.set_page_config(page_title="Haiku Chain", layout="wide", initial_sidebar_state="collapsed")
EXCEL_FILE = "haiku_chains.xlsx"

# Initialize Groq LLM
llm = ChatGroq(temperature=0, 
              groq_api_key="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",  # Replace with your actual key
              model_name="llama-3.3-70b-versatile")

# Session State Initialization
if 'username' not in st.session_state:
    st.session_state.username = None
if 'chains' not in st.session_state:
    st.session_state.chains = []
if 'viewing_chain' not in st.session_state:
    st.session_state.viewing_chain = None
if 'word_counts' not in st.session_state:
    st.session_state.word_counts = {}

# Database Functions
def init_excel():
    """Create Excel file with required structure if missing"""
    if not os.path.exists(EXCEL_FILE):
        pd.DataFrame(columns=[
            'chain_id', 'line_number', 'text', 'user', 'thumbnail', 'rule'
        ]).to_excel(EXCEL_FILE, index=False)

def load_chains():
    """Load chains from Excel into session state"""
    init_excel()
    df = pd.read_excel(EXCEL_FILE)
    st.session_state.chains = []
    
    if not df.empty:
        for chain_id in df['chain_id'].unique():
            chain_df = df[df['chain_id'] == chain_id]
            st.session_state.chains.append({
                'id': chain_id,
                'thumbnail': chain_df.iloc[0]['thumbnail'],
                'rule': chain_df.iloc[0]['rule'],
                'lines': [{
                    'text': row['text'],
                    'user': row['user'],
                    'number': row['line_number']
                } for _, row in chain_df.iterrows()]
            })

def save_chain(chain):
    """Save a single chain to Excel"""
    init_excel()
    df = pd.read_excel(EXCEL_FILE)
    
    # Remove existing entries for this chain
    df = df[df['chain_id'] != chain['id']]
    
    # Add new entries
    new_rows = [{
        'chain_id': chain['id'],
        'line_number': line['number'],
        'text': line['text'],
        'user': line['user'],
        'thumbnail': chain['thumbnail'],
        'rule': chain['rule']
    } for line in chain['lines']]
    
    updated_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    updated_df.to_excel(EXCEL_FILE, index=False)
#     update_github_repo()  # Push the updated Excel file to GitHub

# # --- GitHub Update Function ---
# def update_github_repo():
#     """
#     Stage, commit, and push the Excel file to GitHub.
#     Ensure that Git is configured with proper credentials in your environment.
#     """
#     try:
#         # Stage the file
#         result = subprocess.run(["git", "add", EXCEL_FILE], capture_output=True, text=True)
#         if result.returncode != 0:
#             st.error(f"Git add failed: {result.stderr}")
#             return

#         # Commit the changes (if there are any)
#         commit_message = "Update haiku chains data"
#         result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
#         # If nothing to commit, result.stderr might include "nothing to commit"
#         if result.returncode != 0 and "nothing to commit" not in result.stderr:
#             st.error(f"Git commit failed: {result.stderr}")
#             return

#         # Push the changes
#         result = subprocess.run(["git", "push"], capture_output=True, text=True)
#         if result.returncode != 0:
#             st.error(f"Git push failed: {result.stderr}")
#         else:
#             st.success("Excel file updated in GitHub repo!")
#     except Exception as e:
#         st.error(f"Error during Git operations: {e}")

# Rule Generation Functions
def generate_chain_rule(chain):
    """Generate evolving rule for the chain using Groq"""
    prompt = ChatPromptTemplate.from_template(
        """Analyze this haiku chain and create a concise rule that describes its emerging pattern.
        Consider structure, themes, word choices, and any observable patterns.
        The rule should be 1-2 sentences and guide future contributions.
        
        Previous Rule: {current_rule}
        Current Lines: {lines}
        
        New Rule:"""
    )
    
    lines = "\n".join([f"{line['number']}. {line['text']} ({line['user']})" 
                      for line in chain['lines']])
    
    chain = prompt.format_messages(
        current_rule=chain.get('rule', 'No existing rule'),
        lines=lines
    )
    
    response = llm.invoke(chain)
    return response.content.strip()

# Helper Functions
def generate_thumbnail():
    """Create random image URL for chain card"""
    return f"https://picsum.photos/300/200?random={random.randint(1,1000)}"

def validate_line(text):
    """Check line meets requirements"""
    words = text.split()
    if len(words) == 0:
        return False, "Line cannot be empty"
    
    if any(len(word) > 15 for word in words):
        return False, "Words must be ≤15 characters"
    
    user_count = st.session_state.word_counts.get(st.session_state.username, 0)
    if user_count + len(words) > 150:
        return False, "Word limit exceeded (150 total)"
    
    return True, ""

# User Interface
def username_gate():
    """Username input before accessing app"""
    if not st.session_state.username:
        with st.container(border=True):
            username = st.text_input("Choose a username:", key="username_input")
            if username:
                st.session_state.username = username
                st.rerun()

def main_view():
    """Display all haiku chains"""
    st.title("Collaborative Haiku Chains")
    st.write('You have 150 words each max 15 charachter long. Enjow creating weird poems,fun conversations and free space.\n Last two writers cannot wtite new line to chain but you can always start a new one. \n HAPPY WRITING!!!')
    
    # Start new chain section
    with st.expander("Start New Chain", expanded=False):
        new_line = st.text_input("First line of new chain:", key="new_chain_input")
        if st.button("Create Chain"):
            valid, msg = validate_line(new_line)
            if valid:
                new_chain = {
                    'id': random.randint(1000, 9999),
                    'thumbnail': generate_thumbnail(),
                    'rule': "New chain - no rules yet!",
                    'lines': [{
                        'text': new_line,
                        'user': st.session_state.username,
                        'number': 1
                    }]
                }
                st.session_state.chains.append(new_chain)
                save_chain(new_chain)
                st.rerun()
            else:
                st.error(msg)
    
    # Display existing chains
    st.subheader("Existing Chains")
    cols = st.columns(3)
    for idx, chain in enumerate(st.session_state.chains):
        with cols[idx % 3]:
            st.image(chain['thumbnail'], use_container_width=True)
            st.caption(chain['lines'][0]['text'])
            st.write(f"**Rule:** {chain['rule'][:50]}...")
            if st.button("Open", key=f"open_{chain['id']}"):
                st.session_state.viewing_chain = chain['id']
                st.rerun()

def chain_view():
    """View and contribute to a single chain"""
    chain = next(c for c in st.session_state.chains if c['id'] == st.session_state.viewing_chain)
    
    st.title("Haiku Chain")
    st.button("← Back", on_click=lambda: st.session_state.update(viewing_chain=None), key="back_button")
    
    # Display current rule
    with st.container(border=True):
        st.subheader("Current Rule")
        st.write(chain['rule'])
        st.caption("This rule evolves with each contribution, guiding future additions to the chain")
    
    # Display all lines
    for line in chain['lines']:
        st.markdown(f"""
        <div style='padding: 1rem; margin: 1rem 0; border-left: 3px solid #ccc;'>
            <div style='font-size: 1.2rem;'>{line['text']}</div>
            <div style='color: #666; font-size: 0.8rem;'>— {line['user']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Contribution form
    last_users = [line['user'] for line in chain['lines'][-2:]]
    if st.session_state.username not in last_users:
        with st.form(key="add_line_form"):
            new_line = st.text_input("Add your line:")
            if st.form_submit_button("Contribute"):
                valid, msg = validate_line(new_line)
                if valid:
                    # Add new line
                    chain['lines'].append({
                        'text': new_line,
                        'user': st.session_state.username,
                        'number': len(chain['lines']) + 1
                    })
                    
                    # Update word count
                    st.session_state.word_counts[st.session_state.username] = \
                        st.session_state.word_counts.get(st.session_state.username, 0) + len(new_line.split())
                    
                    # Generate new rule
                    chain['rule'] = generate_chain_rule(chain)
                    
                    # Save changes
                    save_chain(chain)
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.info("You can't add consecutive lines. Let others contribute!")

# Main App Flow
load_chains()  # Initial load from Excel
username_gate()

if not st.session_state.username:
    st.stop()

if st.session_state.viewing_chain is not None:
    chain_view()
else:
    main_view()

st.divider()
st.caption(f"Logged in as: {st.session_state.username} | Words used: {st.session_state.word_counts.get(st.session_state.username, 0)}/150")
