import streamlit as st
import re

# Regular expressions to match headers and section headers
header_pattern = re.compile(r'^\[(.*?)\]$')  # Matches text wrapped in []
section_header_pattern = re.compile(r'^\{(.*?)\}$')  # Matches text wrapped in {}

# Streamlit app title
st.title("Customizable Header and Section Header Formatter")

# User input for text with a larger text area
user_input = st.text_area("Enter your text (wrap headers in [], section headers in {}, and write paragraphs as plain text):", height=300)

# Sidebar for user inputs for header customization
st.sidebar.header("Customize Appearance")

header_font_size = st.sidebar.selectbox("Select header font size:", ["20px", "24px", "28px", "32px"])
header_font_family = st.sidebar.selectbox("Select header font family:", ["Arial", "Courier New", "Georgia", "Times New Roman"])
header_font_color = st.sidebar.color_picker("Select header font color:", "#4CAF50")

# Sidebar for section header customization
section_header_font_size = st.sidebar.selectbox("Select section header font size:", ["18px", "22px", "26px", "30px"])
section_header_font_family = st.sidebar.selectbox("Select section header font family:", ["Arial", "Courier New", "Georgia", "Times New Roman"])
section_header_font_color = st.sidebar.color_picker("Select section header font color:", "#FF9800")

# Sidebar for paragraph customization
paragraph_font_size = st.sidebar.selectbox("Select paragraph font size:", ["14px", "16px", "18px", "20px"])
paragraph_font_family = st.sidebar.selectbox("Select paragraph font family:", ["Arial", "Courier New", "Georgia", "Times New Roman"])
paragraph_font_color = st.sidebar.color_picker("Select paragraph font color:", "#000000")

# Function to format the output
def format_output(text):
    formatted_lines = []
    for line in text.splitlines():
        # Check if the line matches the header pattern
        if header_pattern.match(line):
            header_text = header_pattern.match(line).group(1)  # Extract the text within brackets
            formatted_lines.append(f"<h1 style='color: {header_font_color}; font-family: {header_font_family}; font-size: {header_font_size};'>{header_text}</h1>")
        # Check if the line matches the section header pattern
        elif section_header_pattern.match(line):
            section_header_text = section_header_pattern.match(line).group(1)  # Extract the text within braces
            formatted_lines.append(f"<h2 style='color: {section_header_font_color}; font-family: {section_header_font_family}; font-size: {section_header_font_size};'>{section_header_text}</h2>")
        elif line.strip():  # Check if line is not empty
            formatted_lines.append(f"<p style='color: {paragraph_font_color}; font-family: {paragraph_font_family}; font-size: {paragraph_font_size};'>{line.strip()}</p>")  # Treat plain text as paragraph
    return "\n".join(formatted_lines)

# Display button to show formatted output
if st.button("Format Text"):
    # Format the input text
    formatted_text = format_output(user_input)
    
    # Display the formatted output in the Streamlit app
    st.markdown(formatted_text, unsafe_allow_html=True)
