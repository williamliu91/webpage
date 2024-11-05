import streamlit as st

# Set the layout to wide
st.set_page_config(layout="wide")

# Load the CSS file
with open("styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# Define 20 color palettes with high contrast text colors
color_palettes = {
    "Ocean Breeze": {"button_color": "#008CBA", "sidebar_bg_color": "#E0F7FA", "main_bg_color": "#B2EBF2", "text_color": "#003B2E", "top_bar_color": "#006B8A"},
    "Forest Green": {"button_color": "#4CAF50", "sidebar_bg_color": "#E8F5E9", "main_bg_color": "#C8E6C9", "text_color": "#1B5E20", "top_bar_color": "#3E8E41"},
    "Sunset Glow": {"button_color": "#FF5722", "sidebar_bg_color": "#FFF3E0", "main_bg_color": "#FFE0B2", "text_color": "#6A2C20", "top_bar_color": "#E64A19"},
    "Midnight Blue": {"button_color": "#1A237E", "sidebar_bg_color": "#E8EAF6", "main_bg_color": "#C5CAE9", "text_color": "#0D47A1", "top_bar_color": "#283593"},
    "Cherry Blossom": {"button_color": "#E91E63", "sidebar_bg_color": "#FCE4EC", "main_bg_color": "#F8BBD0", "text_color": "#880E4F", "top_bar_color": "#C2185B"},
    "Citrus Splash": {"button_color": "#FFEB3B", "sidebar_bg_color": "#FFFDE7", "main_bg_color": "#FFF59D", "text_color": "#F57F17", "top_bar_color": "#FBC02D"},
    "Royal Purple": {"button_color": "#9C27B0", "sidebar_bg_color": "#F3E5F5", "main_bg_color": "#E1BEE7", "text_color": "#4A148C", "top_bar_color": "#7B1FA2"},
    "Coral Reef": {"button_color": "#FF7043", "sidebar_bg_color": "#FBE9E7", "main_bg_color": "#FFCCBC", "text_color": "#BF360C", "top_bar_color": "#D84315"},
    "Cool Gray": {"button_color": "#607D8B", "sidebar_bg_color": "#ECEFF1", "main_bg_color": "#CFD8DC", "text_color": "#37474F", "top_bar_color": "#455A64"},
    "Golden Sand": {"button_color": "#FFD54F", "sidebar_bg_color": "#FFF8E1", "main_bg_color": "#FFE082", "text_color": "#FF6F00", "top_bar_color": "#FFA000"},
    "Mystic Lavender": {"button_color": "#BA68C8", "sidebar_bg_color": "#F3E5F5", "main_bg_color": "#E1BEE7", "text_color": "#4A148C", "top_bar_color": "#8E24AA"},
    "Teal Dream": {"button_color": "#009688", "sidebar_bg_color": "#E0F2F1", "main_bg_color": "#B2DFDB", "text_color": "#004D40", "top_bar_color": "#00796B"},
    "Amber Glow": {"button_color": "#FFC107", "sidebar_bg_color": "#FFF8E1", "main_bg_color": "#FFECB3", "text_color": "#FF6F00", "top_bar_color": "#FFA000"},
    "Slate Blue": {"button_color": "#3F51B5", "sidebar_bg_color": "#E8EAF6", "main_bg_color": "#C5CAE9", "text_color": "#1A237E", "top_bar_color": "#303F9F"},
    "Spring Meadow": {"button_color": "#8BC34A", "sidebar_bg_color": "#F1F8E9", "main_bg_color": "#DCEDC8", "text_color": "#33691E", "top_bar_color": "#689F38"},
    "Rosewood": {"button_color": "#880E4F", "sidebar_bg_color": "#FCE4EC", "main_bg_color": "#F8BBD0", "text_color": "#4A148C", "top_bar_color": "#D81B60"},
    "Sandstone": {"button_color": "#A1887F", "sidebar_bg_color": "#EFEBE9", "main_bg_color": "#D7CCC8", "text_color": "#5D4037", "top_bar_color": "#8D6E63"},
    "Ruby Red": {"button_color": "#D32F2F", "sidebar_bg_color": "#FFEBEE", "main_bg_color": "#FFCDD2", "text_color": "#B71C1C", "top_bar_color": "#C62828"},
    "Mossy Green": {"button_color": "#689F38", "sidebar_bg_color": "#F1F8E9", "main_bg_color": "#DCEDC8", "text_color": "#33691E", "top_bar_color": "#558B2F"},
    "Cobalt Blue": {"button_color": "#0D47A1", "sidebar_bg_color": "#E3F2FD", "main_bg_color": "#BBDEFB", "text_color": "#0D47A1", "top_bar_color": "#1976D2"},
}

# Sidebar for color palette selection
st.sidebar.title("Choose a Color Palette")
selected_palette_name = st.sidebar.selectbox("Select Palette", list(color_palettes.keys()))

# Set the default palette and update CSS variables
selected_palette = color_palettes[selected_palette_name]

# Inject the selected palette colors into the CSS variables
st.markdown(
    f"""
    <style>
    :root {{
        --top-bar-color: {selected_palette["top_bar_color"]};
        --sidebar-bg-color: {selected_palette["sidebar_bg_color"]};
        --main-bg-color: {selected_palette["main_bg_color"]};
        --button-color: {selected_palette["button_color"]};
        --text-color: {selected_palette["text_color"]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sample button to demonstrate the color change
st.button("Sample Button")

# Additional elements
st.write("This is a sample text with dynamic color palette.")
