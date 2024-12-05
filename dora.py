import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
from functions import *
import io

def main():
    
    # page config for mobile
    
    st.set_page_config(
        page_title="Event Timeline Visualization",
        page_icon="📅",
        layout="wide",
        initial_sidebar_state="auto" # auto or expanded or collapsed
        
    )
    # Streamlit app
    st.title("Event Timeline Visualization")

    # Sidebar for event details
    # sidebar = st.selectbox("**Select**", ["Event Details", "Styling Options"])
    # if sidebar == "Event Details":
    st.sidebar.header("Event Details")

    # Initialize session states
    if "events_df" not in st.session_state:
        st.session_state["events_df"] = pd.DataFrame(columns=["event_title", "place", "starting_time", "finishing_time"])

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

    # elif sidebar == "Styling Options":
    #     # Initialize session states
    if "bar_color" not in st.session_state:
        st.session_state["bar_color"] = "#BBBBBB"
    if "opacity" not in st.session_state:
        st.session_state["opacity"] = 0.7
    if "bar_width" not in st.session_state:
        st.session_state["bar_width"] = 0.5
    # if "dot_color" not in st.session_state:
    #     st.session_state["dot_color"] = "#BBBBBB"
    # if "dot_size" not in st.session_state:
    #     st.session_state["dot_size"] = 10
    if "height" not in st.session_state:
        st.session_state["height"] = 900
    if "width" not in st.session_state:
        st.session_state["width"] = 900
    if "background_color" not in st.session_state:
        st.session_state["background_color"] = None
    if "background_image" not in st.session_state:
        st.session_state["background_image"] = None
    if "grid_width" not in st.session_state:
        st.session_state["grid_width"] = 0.1
    if "grid_color" not in st.session_state:
        st.session_state["grid_color"] = "black"
    if "letter_color" not in st.session_state:
        st.session_state["letter_color"] = "#BBBBBB"
    if "letter_size" not in st.session_state:
        st.session_state["letter_size"] = 18
        
# Sidebar for styling options
    height = 300
    width = 900
    bar_color = "#BBBBBB"
    opacity = 0.7
    bar_width = 0.5
    # dot_color = "#BBBBBB"
    # dot_size = 10
    background_color = None
    background_image = None
    grid_width = 0.1
    grid_color = "black"
    letter_color = "#BBBBBB"
    letter_size = 18
    
    st.header("Styling Options")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # options = st.selectbox("**Select**", ["Bars", "Letters","Grid","Timeline Size", "Background"])
    with col1:
        if st.button("Bars"):
            bar_color = st.color_picker("Pick a color for bars", "#BBBBBB")
            opacity = st.slider("Bar opacity", 0.1, 1.0, 1.0)
            bar_width = st.slider("Bar width", 0.1, 1.0, 0.2)
            if st.button("Reset"):
                bar_color = "#BBBBBB"
                opacity = 0.7
                bar_width = 0.5
                st.success("Bars styling options have been reset.")
    with col2:
        if st.button("Letters"):
            st.header("Letters")
            letter_color = st.color_picker("Pick a color for letters", "#BBBBBB")
            letter_size = st.slider("Letter size", 1, 40, 18)
            if st.button("Reset"):
                letter_color = "#BBBBBB"
                letter_size = 18
                st.success("Letters styling options have been reset.")
    with col3:
        if st.button("Grid"):
            st.header("Grid")
            grid_width = st.slider("Grid width", 0.1, 2.0, 0.2)
            grid_color = st.color_picker("Pick a color for grid", "#020202")
            if st.button("Reset"):
                grid_width = 0.1
                grid_color = "black"
                st.success("Grid styling options have been reset.")
    with col4:
        if st.button("Background"):
            st.header("Background")
            background_color = st.color_picker("Pick a color for background", "#FFFFFF")
            background_image = st.file_uploader("Upload a background image", type=["png", "jpg", "jpeg"])
            if st.button("Reset"):
                background_color = None
                background_image = None
                st.success("Background styling options have been reset.")
        # ask if user wants to use dots
        # if options == "Dots":
        #     dot_color = st.sidebar.color_picker("Pick a color for dots", "#BBBBBB")
        #     dot_size = st.sidebar.slider("Dot size", 1, 40, 18)
        #     if st.sidebar.button("Reset"):
        #         dot_color = "#BBBBBB"
        #         dot_size = 10
        #         st.success("Dots styling options have been reset.")
    with col5:
        if st.button("Timeline Size"):
            st.header("Timeline Size")
            height = st.slider("Height", 100, 2000, 300)
            width = st.slider("Width", 100, 2000, 900)
            if st.button("Reset"):
                height = 300
                width = 900
                st.success("Timeline size options have been reset.")
    
    # SAVE THE SESSION STATE
    st.session_state["bar_color"] = bar_color
    st.session_state["opacity"] = opacity
    st.session_state["bar_width"] = bar_width
    # st.session_state["dot_color"] = dot_color
    # st.session_state["dot_size"] = dot_size
    st.session_state["height"] = height
    st.session_state["width"] = width
    st.session_state["background_color"] = background_color
    st.session_state["background_image"] = background_image
    st.session_state["grid_width"] = grid_width
    st.session_state["grid_color"] = grid_color
    st.session_state["letter_color"] = letter_color
    st.session_state["letter_size"] = letter_size
    

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
        # Create columns for horizontal alignment
        # col1, col2, col3 = st.columns(3)
        # # Place buttons in separate columns
        # with col1:
        if st.sidebar.button("Delete Selected Event"):
            st.session_state["events_df"].drop(index=event_to_delete, inplace=True)
            st.session_state["events_df"].reset_index(drop=True, inplace=True)
            st.success("Event deleted successfully!")

    
        if st.sidebar.button("Delete All Events"):
            st.session_state["events_df"] = pd.DataFrame(columns=["event_title", "place", "starting_time", "finishing_time"])
            st.success("All events deleted successfully!")
            
        col1, col2, col3 = st.columns(3)
        with col1:

            if st.button("Reset All Styling Options"):
                # Add your reset styling logic here

                st.session_state["bar_color"] = "#BBBBBB"
                st.session_state["opacity"] = 0.7
                st.session_state["bar_width"] = 0.5
                # st.session_state["dot_color"] = "#BBBBBB"
                # st.session_state["dot_size"] = 10
                st.session_state["height"] = 300
                st.session_state["width"] = 600
                st.session_state["background_color"] = None
                st.session_state["background_image"] = None
                st.session_state["grid_width"] = 0.1
                st.session_state["grid_color"] = "black"
                st.session_state["letter_color"] = "#BBBBBB"
                st.session_state["letter_size"] = 18
                st.success("Styling options reset successfully!")
        with col2:
            
            visualize = st.selectbox("Visualize events or place", ["event_title", "place"]) 

            st.session_state["visualize"] = visualize
        

    # Generate the timeline
    try:
        if st.session_state["events_df"].empty:
            st.warning("No events to display on the timeline.")
        else: # st.session_state["dot_color"], st.session_state["dot_size"]
            timeline_obj = event_timeline(st.session_state["events_df"], st.session_state["bar_color"], st.session_state["bar_width"],
                            st.session_state["opacity"], st.session_state["visualize"], st.session_state["height"],
                            st.session_state["width"], st.session_state["background_color"], st.session_state["background_image"] ,st.session_state["grid_width"], st.session_state["grid_color"], st.session_state["letter_color"], st.session_state["letter_size"])
            buf = io.BytesIO()
            timeline_obj.write_image(buf, format="png")
            buf.seek(0)
            
            with col3:
            
                mockup_type = st.selectbox("Select a mockup type", ["story", "post"])
            
            mockup_image = simulate_instagram_display(Image.open(buf), mockup_type= mockup_type)
            st.image(mockup_image, use_container_width=True)
            
            # download the image as png
            # Create a download button
            st.download_button(
                label="Download Mockup as PNG",
                data=buf,
                file_name=f"instagram_mockup_{mockup_type}.png",
                mime="image/png"
            )
    except:
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