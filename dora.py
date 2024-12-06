import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
from functions import *
import io
from matplotlib.colors import to_rgba

def main():
    
    # page config for mobile
    
    st.set_page_config(
        page_title="Event Timeline Visualization",
        page_icon="📅",
        layout="centered", # wide or centered
        initial_sidebar_state="auto" # auto or expanded or collapsed
        
    )
    # Streamlit app
    st.title("Event Timeline Visualization")

    st.sidebar.header("Event Details")

    # Initialize session states
    if "events_df" not in st.session_state:
        st.session_state["events_df"] = pd.DataFrame(columns=["event_title", "place", "starting_time",
                                                              "finishing_time"])

    if "event_inputs" not in st.session_state:
        st.session_state["event_inputs"] = {
            "event_title": "",
            "place": "",
            "starting_date": datetime.now().date(),
            "starting_time": datetime.now().time(),
            "finishing_date": datetime.now().date(),
            "finishing_time": datetime.now().time()
        }

    # Event details input
    event_title = st.sidebar.text_input("Event Title", value=st.session_state["event_inputs"]["event_title"])
    place = st.sidebar.text_input("Place", value=st.session_state["event_inputs"]["place"])
    starting_date = st.sidebar.date_input("Starting Date", value=st.session_state["event_inputs"]["starting_date"])
    starting_time = st.sidebar.time_input("Starting Time", value=st.session_state["event_inputs"]["starting_time"])
    finishing_date = st.sidebar.date_input("Finishing Date", value=st.session_state["event_inputs"]["finishing_date"])
    finishing_time = st.sidebar.time_input("Finishing Time", value=st.session_state["event_inputs"]["finishing_time"])

    # Combine date and time inputs into datetime objects
    starting_datetime = datetime.combine(starting_date, starting_time)
    finishing_datetime = datetime.combine(finishing_date, finishing_time)


    if st.sidebar.button("Add Event"):
    
        new_event = {
            "event_title": event_title,
            "place": place,
            "starting_time": starting_datetime,
            "finishing_time": finishing_datetime
        }
        st.session_state["events_df"] = pd.concat([st.session_state["events_df"], pd.DataFrame([new_event])], ignore_index=True)
        st.sidebar.success("Event added successfully!")

        # Reset input fields
        st.session_state["event_inputs"] = {
            "event_title": "",
            "place": "",
            "starting_date": datetime.now().date(),
            "starting_time": datetime.now().time(),
            "finishing_date": datetime.now().date(),
            "finishing_time": datetime.now().time()
        }
        
        # Display the events
    # st.subheader("Events Data")
    if not st.session_state["events_df"].empty:
        # st.dataframe(st.session_state["events_df"])

        # Select a row to delete
        event_to_delete = st.sidebar.selectbox(
            "Select an event to delete:", 
            st.session_state["events_df"].index, 
            format_func=lambda x: st.session_state["events_df"].iloc[x]["event_title"]
        )

        if st.sidebar.button("Delete Selected Event"):
            st.session_state["events_df"].drop(index=event_to_delete, inplace=True)
            st.session_state["events_df"].reset_index(drop=True, inplace=True)
            st.success("Event deleted successfully!")

    
        if st.sidebar.button("Delete All Events"):
            st.session_state["events_df"] = pd.DataFrame(columns=["event_title", "place", "starting_time", "finishing_time"])
            st.success("All events deleted successfully!")
            
    # Initialize session states
    if "bar_color" not in st.session_state:
        st.session_state["bar_color"] = "#8FA2B7"
    if "opacity" not in st.session_state:
        st.session_state["opacity"] = 0.65
    if "bar_width" not in st.session_state:
        st.session_state["bar_width"] = 0.65
    if "height" not in st.session_state:
        st.session_state["height"] = 800
    if "width" not in st.session_state:
        st.session_state["width"] = 1050
    if "background_color" not in st.session_state:
        st.session_state["background_color"] = '#DAE1E4'
    if "background_image" not in st.session_state:
        st.session_state["background_image"] = None
    if "background_image_opacity" not in st.session_state:
        st.session_state["background_image_opacity"] = 0.5
    if "grid_width" not in st.session_state:
        st.session_state["grid_width"] = 1.2
    if "grid_color" not in st.session_state:
        st.session_state["grid_color"] = "black"
    if "letter_color" not in st.session_state:
        st.session_state["letter_color"] = "#E8E2E2"
    if "time_letter_size" not in st.session_state:
        st.session_state["time_letter_size"] = 25
    if "event_letter_size" not in st.session_state:
        st.session_state["event_letter_size"] = 40
    if "letter_style" not in st.session_state:
        st.session_state["letter_style"] = "Lato, sans-serif"
    if "visualize" not in st.session_state:
        st.session_state["visualize"] = "event_title"

    
    with st.expander("Styling Options", expanded=False):
    
        col1, col2 = st.columns([1,2])
        
        with col1:
            options = st.selectbox("**Select**", ["Bars", "Letters","Grid","Timeline Size", "Background"])
            if options == "Bars":
                color_options = st.selectbox("Select a color option", ["Single Color", "Color Palette"])
                if color_options == "Single Color":
                    bar_color = st.color_picker("Pick a color for bars", "#8FA2B7")
                else:
                    
                    bar_color = None
                st.session_state["bar_color"] = bar_color
                
                opacity = st.slider("Bar opacity", 0.1, 1.0, 1.0)
                st.session_state["opacity"] = opacity
                bar_width = st.slider("Bar width", 0.1, 1.0, st.session_state.get("bar_width", 0.5))
                st.session_state["bar_width"] = bar_width
                if st.button("Reset"):
                    bar_color = st.session_state.get("bar_color", "#8FA2B7")
                    opacity = 0.7
                    bar_width = 0.5
                    st.success("Bars styling options have been reset.")
                
    
            if options == "Letters":
                font_families = ["Lato, sans-serif", "Courier New, monospace", "Times New Roman, serif", "Comic Sans MS, cursive"]
                st.header("Letters")
                letter_color = st.color_picker("Pick a color for letters", st.session_state.get("letter_color", "#E8E2E2"))
                st.session_state["letter_color"] = letter_color
                
                event_letter_size = st.slider("Letter size", 1, 50, 45)
                st.session_state["event_letter_size"] = event_letter_size
                
                time_letter_size = st.slider("Time size", 1, 50, 25)
                st.session_state["time_letter_size"] = time_letter_size
                
                letter_style = st.selectbox("Select a font family", font_families)
                st.session_state["letter_style"] = letter_style
                
                if st.button("Reset"):
                    letter_color = "#E8E2E2"
                    event_letter_size = 45
                    time_letter_size = 25
                    letter_style = "Lato, sans-serif"
                    st.success("Letters styling options have been reset.")
                st.session_state["letter_color"] = letter_color
                st.session_state["event_letter_size"] = event_letter_size
                st.session_state["time_letter_size"] = time_letter_size

                    
            if options == "Grid":
                st.header("Grid")
                grid_width = st.slider("Grid width", 0.1, 20.0, 1.0)
                base_grid_color  = st.color_picker("Pick a color for grid", "#020202")
                grid_opacity = st.slider("Grid opacity", 0.1, 1.0, 0.5)
                
                rgba_color = to_rgba(base_grid_color)  # Convert hex to RGBA
                grid_color = f"rgba({int(rgba_color[0]*255)}, {int(rgba_color[1]*255)}, {int(rgba_color[2]*255)}, {grid_opacity})"
                if st.button("Reset"):
                    grid_width = 0.1
                    grid_color = "black"
                    st.success("Grid styling options have been reset.")
                st.session_state["grid_width"] = grid_width
                st.session_state["grid_color"] = grid_color

  
            if options == "Background":
                st.header("Background")
                
                bg_option = st.selectbox("Select Background Option", ["Color", "Image"])
                
                if bg_option == "Color":
                    background_color = st.color_picker("Pick a color for background", st.session_state.get("background_color", "#DAE1E4"))
                    st.session_state["background_color"] = background_color
                
                if bg_option == "Image":
                    uploaded_image = st.file_uploader("Upload a background image", type=["jpg", "jpeg", "png"])
                    if uploaded_image is not None:
                        background_image = encode_image(uploaded_image)
                        st.session_state["background_image"] = background_image
                        st.session_state["background_image_opacity"] = st.slider("Background Image Opacity", 0.0, 1.0, 0.5)
                
                if st.button("Reset Background Options"):
                    st.session_state["background_color"] = "#DAE1E4"
                    st.session_state["background_image"] = None
                    st.session_state["background_image_opacity"] = 0.5
                    st.success("Background options have been reset.")
                    

          
            if options == "Timeline Size":
                st.header("Timeline Size")
                height = st.slider("Height", 100, 2000, 800)
                width = st.slider("Width", 100, 2000, 1050)
                if st.button("Reset"):
                    height = 800
                    width = 1050
                    st.success("Timeline size options have been reset.")
                st.session_state["height"] = height
                st.session_state["width"] = width
                
            visualize = st.selectbox("Visualize events or place", ["event_title", "place"]) 

            st.session_state["visualize"] = visualize
    
    
            if st.button("Reset All Styling Options"):
                # Add your reset styling logic here

                st.session_state["bar_color"] = "#8FA2B7"
                st.session_state["opacity"] = 1.0
                st.session_state["bar_width"] = 0.65
                st.session_state["height"] = 800
                st.session_state["width"] = 1050
                st.session_state["background_color"] = '#DAE1E4'
                st.session_state["background_image"] = None
                st.session_state["background_image_opacity"] = 0.5
                st.session_state["grid_width"] = 1.2
                st.session_state["grid_color"] = "black"
                st.session_state["letter_color"] = "#E8E2E2"
                st.session_state["letter_style"] = "Lato, sans-serif"
                st.session_state["event_letter_size"] = 40
                st.session_state["time_letter_size"] = 25
                st.success("Styling options reset successfully!")


        

    # Generate the timeline
        try:
            if st.session_state["events_df"].empty:
                st.warning("No events to display on the timeline.")
            else: # st.session_state["dot_color"], st.session_state["dot_size"]
                timeline_obj = event_timeline(st.session_state["events_df"], st.session_state["bar_color"], st.session_state["bar_width"],
                                st.session_state["opacity"], st.session_state["visualize"], st.session_state["height"],
                                st.session_state["width"], st.session_state["background_color"], st.session_state["background_image"], st.session_state["background_image_opacity"],
                                st.session_state["grid_width"], st.session_state["grid_color"],
                                st.session_state["letter_color"],st.session_state["event_letter_size"], 
                                st.session_state["time_letter_size"], st.session_state["letter_style"])
                buf = io.BytesIO()
                timeline_obj.write_image(buf, format="png")
                buf.seek(0)
                
                mockup_type = st.selectbox("Select a mockup type", ["Story", "Square post", "Vertical post", "Horizontal post"])
            with col2:    
                mockup_image = simulate_instagram_display(Image.open(buf), mockup_type= mockup_type, new_height=st.session_state["height"], new_width= st.session_state["width"])
                st.image(mockup_image, use_container_width=True)
                                # Create a download button
                st.download_button(
                    label="Download Mockup as PNG",
                    data=buf,
                    file_name=f"instagram_mockup_{mockup_type}.png",
                    mime="image/png"
                )
        except ValueError as e:
            st.write(e)
            st.warning("Please select Styling Options.")


    # Display the app
    st.sidebar.markdown(
        """
        **Note:** This is a simple event timeline visualization app. 
        """
    )
    if st.sidebar.checkbox("Instructions", False):
        st.sidebar.markdown(
            """
            # Event Timeline Visualization App

            This app enables users to visualize and manage events in a timeline format with customizable styling options. The app includes the following features:

            ## Features

            ### **1. Add Events**
            - Users can input event details like:
            - **Event Title**
            - **Place**
            - **Starting Date & Time**
            - **Finishing Date & Time**
            - Events are stored in a dynamic DataFrame.

            ### **2. Manage Events**
            - View all added events in a table format.
            - Options to:
            - Delete a single event.
            - Clear all events.
            - Reset all styling configurations.

            ### **3. Styling Options**
            Customize the appearance of the timeline:
            - **Bars**
            - Adjust bar colors, width, and opacity.
            - **Letters**
            - Choose font size and color for axis labels.
            - **Grid**
            - Customize grid line width and color.
            - **Dots**
            - Set the color and size of markers on the timeline.
            - **Timeline Size**
            - Adjust the height and width of the timeline.

            ### **4. Visualization**
            - Generate a timeline using **Plotly**, displaying events in a clean and interactive manner.
            - Choose to visualize events by **Event Title** or **Place**.

            ### **5. Sidebar**
            The sidebar serves as the main control panel:
            - Toggle between **Event Details** and **Styling Options**.
            - Reset individual styling settings or all settings at once.

            ### **6. Error Handling**
            - Provides warnings for incomplete or missing event data.
            - Ensures smooth user experience with appropriate feedback.

            ---

            ## How to Use
            1. Navigate to the **Event Details** section in the sidebar.
            2. Input event details and click **Add Event** to save the event.
            3. Switch to the **Styling Options** section to customize the timeline's appearance.
            4. View and interact with the timeline generated in the main display area.

            ---

            ## Notes
            - The app is ideal for visualizing events over a short period (e.g., 3 days).
            - Reset buttons are available for convenience.

            Feel free to explore and experiment with the visualization options!
            """
        )

if __name__ == "__main__":
    main()