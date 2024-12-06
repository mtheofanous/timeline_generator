import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import io
import base64

def encode_image(image_file):
    """Convert image file to base64 string."""
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_image}"

def event_timeline(df_,bar_color=None, bar_width=1, opacity=1-0, 
                   visualize="place", height=300, width=900, background_color=None, 
                   background_image=None, background_image_opacity=0.5,
                   grid_width=0.1, grid_color="rgba(0,0,0,0)",letter_color="#BBBBBB", 
                   event_letter_size=25, time_letter_size=15, letter_style="Lato, sans-serif"): # dot_color, dot_size,
    """
    Generates a timeline visualization for events over a 3-day period.

    Args:
    df_ (DataFrame): The input data containing event details.

    Returns:
    None: Displays the timeline chart in the Streamlit app.
    """
    
        # Set the color scheme
    if  bar_color:
        color_sequence = [bar_color]  # Use the single color for all bars
    else:
        color_sequence = None  # Use dynamic coloring based on the 'place' column
    # Create a timeline visualization    
    fig_timeline = px.timeline(
        data_frame=df_,
        x_start="starting_time",
        x_end="finishing_time",
        y=visualize,
        color="event_title" if visualize == "place" else "place",
        template="plotly_dark",
        width= width,
        height= height,
        color_discrete_sequence= color_sequence
        
    )

    fig_timeline.update_traces(
        marker=dict(line=dict(width=grid_width, color=grid_color)),
        # selector=dict(mode="markers+lines"),# other options: "markers", "lines" or "markers+lines"  
        width = bar_width, opacity=opacity
        
    )
    
    # Style gridlines and text
    fig_timeline.update_layout(
        plot_bgcolor=background_color or "rgba(0,0,0,0)",# Default to transparent if no color
        xaxis=dict(
            showgrid=True,
            zeroline=False,
            gridcolor=grid_color,
            gridwidth=grid_width,
            tickfont=dict(
                family=letter_style,
                size=time_letter_size,
                color=letter_color,
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            gridcolor=grid_color,
            gridwidth=grid_width,
            tickfont=dict(
                family=letter_style,
                size=event_letter_size,
                color=letter_color,
            ),       
            
        ),
            legend=dict(
                title=dict(text=""),  # Set the legend title
                orientation="h",  # Horizontal layout
                x=1,  # Position to the top-right
                xanchor="right",
                y=1,  # Position at the top
                yanchor="bottom",
                font=dict(
                    family=letter_style,
                    size=event_letter_size,
                    color=letter_color
                
                ),
            ),
    )
    
    # Apply background image if provided
    if background_image:
        fig_timeline.update_layout(
            images=[
                dict(
                    source=background_image,
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=1,
                    sizex=1,
                    sizey=1,
                    xanchor="left",
                    yanchor="top",
                    opacity=background_image_opacity,
                    layer="below",
                )
            ]
        )


    fig_timeline.update_yaxes(
        title_text='', 
        showgrid=True, 
        categoryorder="total ascending"
    )
    fig_timeline.update_xaxes(
        title_text='', 
        showgrid=True
    )

    return fig_timeline
    
def simulate_instagram_display(fig_timeline_or_image, mockup_type="story",new_width=1050, new_height=800):
    """
    Simulates how a figure or image will look in Instagram's mobile app story or post view.

    :param fig_timeline_or_image: Either a Matplotlib/Plotly figure or a PIL Image object.
    :param mockup_type: "story" or "post" to choose Instagram mockup type.
    :return: PIL Image with Instagram mockup applied.
    """
    # Define dimensions for Instagram story and post
    mockup_sizes = {
        "Story": (1080, 1920),  # Instagram story resolution
        "Square post": (1080, 1080), # Instagram post resolution
        "Vertical post": (1080, 1350), # Instagram vertical post resolution
        "Horizontal post": (1080, 566) # Instagram horizontal post resolution
    }

    if mockup_type not in mockup_sizes:
        raise ValueError("Invalid mockup_type. Choose 'story' or 'post'.")

    # Check if input is a figure or an image
    if hasattr(fig_timeline_or_image, "savefig"):  # It's a Matplotlib/Plotly figure
        buf = io.BytesIO()
        fig_timeline_or_image.savefig(buf, format="png", bbox_inches="tight", dpi=300)
        buf.seek(0)
        user_image = Image.open(buf)
    elif isinstance(fig_timeline_or_image, Image.Image):  # It's already a PIL Image
        user_image = fig_timeline_or_image
    else:
        raise TypeError("Input must be a Matplotlib/Plotly figure or a PIL Image.")
    

    # Create a blank background mockup
    mockup = Image.new("RGB", mockup_sizes[mockup_type], (0, 0, 0))  # Black background as placeholder or white (255, 255, 255)

    # Resize the user image to fit within the mockup
    user_image = user_image.convert("RGBA")
    user_image.thumbnail((new_width, new_height))  # Scale to fit within the mockup
    user_image = user_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    


    # Calculate position to center the image
    x_offset = (mockup.width - user_image.width) // 2
    y_offset = (mockup.height - user_image.height) // 2

    # Paste the user image onto the mockup (supports transparency)
    mockup.paste(user_image, (x_offset, y_offset), user_image)

    return mockup

