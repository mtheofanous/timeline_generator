import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
from functions import encode_image, event_timeline, simulate_instagram_display
import io
from matplotlib.colors import to_rgba

def initialize_session_states():
    """Initializes Streamlit session states."""
    default_states = {
        "events_df": pd.DataFrame(columns=["event_title", "place", "starting_time", "finishing_time"]),
        "event_inputs": {
            "event_title": "",
            "place": "",
            "starting_date": datetime.now().date(),
            "starting_time": datetime.now().time(),
            "finishing_date": datetime.now().date(),
            "finishing_time": datetime.now().time(),
        },
        "bar_color": "#8FA2B7",
        "opacity": 0.65,
        "bar_width": 0.65,
        "height": 800,
        "width": 1050,
        "background_color": '#DAE1E4',
        "background_image": None,
        "background_image_opacity": 0.5,
        "grid_width": 1.2,
        "grid_color": "black",
        "letter_color": "#E8E2E2",
        "time_letter_size": 25,
        "event_letter_size": 40,
        "letter_style": "Lato, sans-serif",
        "visualize": "event_title"
    }
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_styling_options():
    """Renders the styling options for the timeline."""
    with st.expander("Styling Options", expanded=False):
        options = st.selectbox("Select a Styling Option", ["Bars", "Letters", "Grid", "Background", "Timeline Size"])

        if options == "Bars":
            color_options = st.selectbox("Select a color option", ["Single Color", "Color Palette"])
            if color_options == "Single Color":
                bar_color = st.color_picker("Pick a color for bars", st.session_state["bar_color"])
                st.session_state["bar_color"] = bar_color
            opacity = st.slider("Bar opacity", 0.1, 1.0, st.session_state["opacity"])
            st.session_state["opacity"] = opacity
            bar_width = st.slider("Bar width", 0.1, 1.0, st.session_state["bar_width"])
            st.session_state["bar_width"] = bar_width

        elif options == "Letters":
            font_families = ["Lato, sans-serif", "Courier New, monospace", "Times New Roman, serif", "Comic Sans MS, cursive"]
            letter_color = st.color_picker("Pick a color for letters", st.session_state["letter_color"])
            st.session_state["letter_color"] = letter_color
            event_letter_size = st.slider("Letter size", 1, 50, st.session_state["event_letter_size"])
            st.session_state["event_letter_size"] = event_letter_size
            time_letter_size = st.slider("Time size", 1, 50, st.session_state["time_letter_size"])
            st.session_state["time_letter_size"] = time_letter_size
            letter_style = st.selectbox("Select a font family", font_families)
            st.session_state["letter_style"] = letter_style

        elif options == "Grid":
            grid_width = st.slider("Grid width", 0.1, 20.0, st.session_state["grid_width"])
            base_grid_color = st.color_picker("Pick a color for grid", st.session_state["grid_color"])
            grid_opacity = st.slider("Grid opacity", 0.1, 1.0, 0.5)
            rgba_color = to_rgba(base_grid_color)
            grid_color = f"rgba({int(rgba_color[0]*255)}, {int(rgba_color[1]*255)}, {int(rgba_color[2]*255)}, {grid_opacity})"
            st.session_state["grid_width"] = grid_width
            st.session_state["grid_color"] = grid_color

        elif options == "Background":
            bg_option = st.selectbox("Select Background Option", ["Color", "Image"])
            if bg_option == "Color":
                background_color = st.color_picker("Pick a color for background", st.session_state["background_color"])
                st.session_state["background_color"] = background_color
            elif bg_option == "Image":
                uploaded_image = st.file_uploader("Upload a background image", type=["jpg", "jpeg", "png"])
                if uploaded_image is not None:
                    background_image = encode_image(uploaded_image)
                    st.session_state["background_image"] = background_image
                    st.session_state["background_image_opacity"] = st.slider("Background Image Opacity", 0.0, 1.0, st.session_state["background_image_opacity"])

        elif options == "Timeline Size":
            height = st.slider("Height", 100, 2000, st.session_state["height"])
            st.session_state["height"] = height
            width = st.slider("Width", 100, 2000, st.session_state["width"])
            st.session_state["width"] = width

        if st.button("Reset All Styling Options"):
            initialize_session_states()
            st.success("Styling options have been reset to default.")

def reset_inputs():
    """Resets event input fields."""
    st.session_state["event_inputs"] = {
        "event_title": "",
        "place": "",
        "starting_date": datetime.now().date(),
        "starting_time": datetime.now().time(),
        "finishing_date": datetime.now().date(),
        "finishing_time": datetime.now().time(),
    }

def handle_event_addition():
    """Handles adding new events to the timeline."""
    inputs = st.session_state["event_inputs"]
    starting_datetime = datetime.combine(inputs["starting_date"], inputs["starting_time"])
    finishing_datetime = datetime.combine(inputs["finishing_date"], inputs["finishing_time"])
    new_event = {
        "event_title": inputs["event_title"],
        "place": inputs["place"],
        "starting_time": starting_datetime,
        "finishing_time": finishing_datetime
    }
    st.session_state["events_df"] = pd.concat(
        [st.session_state["events_df"], pd.DataFrame([new_event])], ignore_index=True
    )
    reset_inputs()
    st.sidebar.success("Event added successfully!")

def handle_event_deletion():
    """Handles deletion of selected or all events."""
    events_df = st.session_state["events_df"]
    event_to_delete = st.selectbox(
        "Select an event to delete:",
        events_df.index,
        format_func=lambda x: events_df.iloc[x]["event_title"]
    )
    if st.button("Delete Selected Event"):
        st.session_state["events_df"].drop(index=event_to_delete, inplace=True)
        st.session_state["events_df"].reset_index(drop=True, inplace=True)
        st.sidebar.success("Event deleted successfully!")
    if st.button("Delete All Events"):
        st.session_state["events_df"] = pd.DataFrame(columns=events_df.columns)
        st.success("All events deleted successfully!")

def render_timeline():
    """Renders the event timeline visualization."""
    if st.session_state["events_df"].empty:
        st.warning("No events to display on the timeline.")
        return
    fig = event_timeline(
        st.session_state["events_df"],
        bar_color=st.session_state["bar_color"],
        bar_width=st.session_state["bar_width"],
        opacity=st.session_state["opacity"],
        visualize=st.session_state["visualize"],
        height=st.session_state["height"],
        width=st.session_state["width"],
        background_color=st.session_state["background_color"],
        background_image=st.session_state["background_image"],
        background_image_opacity=st.session_state["background_image_opacity"],
        grid_width=st.session_state["grid_width"],
        grid_color=st.session_state["grid_color"],
        letter_color=st.session_state["letter_color"],
        event_letter_size=st.session_state["event_letter_size"],
        time_letter_size=st.session_state["time_letter_size"],
        letter_style=st.session_state["letter_style"],
    )
    buf = io.BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    mockup_type = st.selectbox("Select a mockup type", ["Story", "Square post", "Vertical post", "Horizontal post"])
    mockup_image = simulate_instagram_display(Image.open(buf), mockup_type, st.session_state["width"], st.session_state["height"])
    st.image(mockup_image, use_container_width=True)
    st.download_button(
        label="Download Mockup as PNG",
        data=buf,
        file_name=f"instagram_mockup_{mockup_type}.png",
        mime="image/png"
    )

def main():
    st.set_page_config(page_title="Event Timeline Visualization", page_icon="📅", layout="wide")
    st.title("Event Timeline Visualization")
    left_col, middle_col, right_col = st.columns([1, 4, 1]) 
    
    with left_col:
        
        initialize_session_states()

        # Sidebar inputs
        inputs = st.session_state["event_inputs"]
        inputs["event_title"] = st.text_input("Event Title", value=inputs["event_title"])
        inputs["place"] = st.text_input("Place", value=inputs["place"])
        inputs["starting_date"] = st.date_input("Starting Date", value=inputs["starting_date"])
        inputs["starting_time"] = st.time_input("Starting Time", value=inputs["starting_time"])
        inputs["finishing_date"] = st.date_input("Finishing Date", value=inputs["finishing_date"])
        inputs["finishing_time"] = st.time_input("Finishing Time", value=inputs["finishing_time"])
        
        if st.button("Add Event"):
            handle_event_addition()
            
        if not st.session_state["events_df"].empty:
            handle_event_deletion()
            
        if st.button("Reset Inputs"):
            reset_inputs()
            st.success("Inputs have been reset to default.")
        
    with middle_col:
        render_timeline()
        
    with right_col:
        render_styling_options()
        

        


    # render_timeline()

if __name__ == "__main__":
    main()
