import google.generativeai as genai
import os
import random
import sys
from dotenv import load_dotenv, find_dotenv
from pylatexenc.latex2text import LatexNodes2Text
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

import re

def add_newline_after_long_line(text, max_length):
    # This regex finds lines longer than max_length and adds a newline after the max_length character
    pattern = re.compile(r'(.{'+str(max_length)+r'})(\s|$)')
    return pattern.sub(r'\1\n', text)

#text = "This is a very long line that needs to be broken into multiple lines for better readability in a mind map."
#max_length = 40  # Set the maximum length for a line

#formatted_text = add_newline_after_long_line(text, max_length)
#print(formatted_text)
def init():
    genai.configure(api_key=os.environ["GENERATIVE_AI_KEY"])

    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 0,
        "response_mime_type": "text/plain"
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        safety_settings=safety_settings,
        generation_config=generation_config
    )

    chat_session = model.start_chat(history=[])
    return chat_session
def latex_to_unicode(latex_str):
    return LatexNodes2Text().latex_to_text(latex_str)
def map(query):
    env_path = find_dotenv()
    if env_path == "":
        with open('.env', 'w') as f:
            pass
        env_path = find_dotenv()

    load_dotenv(find_dotenv(), override=True)

    # Check if API key is in environment variables
    api_key = os.getenv('GENERATIVE_AI_KEY')

    if api_key is None:
        # If API key is not set, ask the user for it
        api_key = input('Please enter your API key from https://ai.google.dev: ')

        # Store the API key in the .env file
        with open(find_dotenv(), 'a') as f:
            f.write(f'GENERATIVE_AI_KEY={api_key}\n')

        print("API key stored successfully!")
    load_dotenv()
    genai.configure(api_key=os.environ["GENERATIVE_AI_KEY"])

    topic= query  # Or use dot.view() to display directly


    prompt = f"make a mindmap of {topic} using * for headings and spaced text (without *) for definitions format."
    #response = genai.chat(model="models/chat-bison-001", messages=prompt, temperature=0.7)
    chat=init()
    response=chat.send_message(prompt)
    resp=response.text
    resp=re.sub(r'\*\*',"",resp)
    # Remove the leading and trailing whitespaces
    text = resp.strip()

    # Split the text into lines
    lines = text.split("\n")
    #print(lines)
    rest={}
    prev=""
    mhead=""
    newl=[]
    def invalid():
        for line in lines:
            mhead=re.match(r"\s+\* *", line) if not 'None' else topic
            if line == "":
                continue
            if re.match(r"\*\s.*", line) or re.match(r".*", line) or re.match(r"\s+\*\s.*", line):
                rest.update({line:[]})
                prev=line
                newl.clear()
            elif re.match(r"\s+\*\s.*", line) or re.match(r"\s .*", line) or re.match(r"\*\s .*", line):
                newl=rest[prev]
                newl.append(line)
                rest.update({prev:newl})
            else:
                print(f"Error in line: {line}")

    for line in lines:
        # Check if the line matches the regular expressions
        if re.match(r"^\*\s.*", line):
            rest[line] = []
            prev = line
        elif re.match(r"^\s+\*\s.*", line) and prev:
            line = add_newline_after_long_line(line, 30)
            rest[prev].append(line)
    print(rest)
    cont=input("DO you want to CONTINUE (Y/N)")
    if cont.lower() != 'y':
        exit(0)
    nodes_by_type = {"topic": [], "key": [], "sub": []}

    # Fill the dictionary with your nodes
    for key, value in rest.items():
        key= re.sub(r"\*\s+","", key)
        nodes_by_type["topic"].append(f"{topic}")
        nodes_by_type["key"].append(f"{key}")
        for subn in value:
            subn = re.sub(r"\*\s+", "", subn)
            nodes_by_type["sub"].append(f"{subn}")
    G = nx.DiGraph()
    for key, value in rest.items():
        key = re.sub(r"\*\s+", "", key)
        G.add_edge(f"{topic}", f"{key}")
        for subn in value:
            subn = re.sub(r"\*\s+", "", subn)
            G.add_edge(f"{key}", f"{subn}")

    # Position layout for the nodes
    pos = nx.shell_layout(G)#, k=0.5)
    # Create a list of small changes to be used for positions
    changes = [0, 0.02, 0.03, 0.05,0.07,0.09]

    # Update positions with a small random change
    for node in pos:
        pos[node] = (pos[node][0] + random.choice(changes), pos[node][1] + random.choice(changes))
    #print(pos)
    #exit(0)
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(40, 40))
    nx.draw_networkx_edges(G, pos, ax=ax)

    # Draw the edges with varied styles based on hierarchy
    #edge_styles = {"topic-key": "solid", "key-sub": "dotted"}
    #nx.draw_networkx_edges(G, pos, ax=ax,
                           #edge_color=[edge_styles.get(edge_type) for edge_type in edge_styles])

    # Draw each node with different shapes and colors based on their types
    node_colors = {"topic": "gold", "key": "lightblue", "sub": "lightgreen"}
    #node_shapes = {"topic": 's', "key": 'o', "sub": '^'}
    font_sizes = {"topic": 20, "key": 15, "sub": 10}
    for node_type in ["topic", "key", "sub"]:
        for node in nodes_by_type[node_type]:
            x, y = pos[node]
            text = ax.text(x, y, node, va='center', ha='center', fontsize=font_sizes[node_type])
            text.set_bbox(dict(facecolor=node_colors[node_type], edgecolor='black', boxstyle='round,pad=0.5'))

    plt.savefig(f"{topic} mindmap.jpg")
    return f"{topic} mindmap.jpg"
    #plt.show()
if __name__ =="__main__":
    map(input("Enter topic:"))
