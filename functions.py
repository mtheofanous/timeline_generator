import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import io

def event_timeline(df_,bar_color, bar_width, dot_color, dot_size, opacity, 
                   visualize, height=300, width=900, background_color=None,
                   grid_width=0.1, grid_color="black", letter_color="#BBBBBB", letter_size=18):
    """
    Generates a timeline visualization for events over a 3-day period.

    Args:
    df_ (DataFrame): The input data containing event details.

    Returns:
    None: Displays the timeline chart in the Streamlit app.
    """
    
    fig_timeline = px.timeline(
        data_frame=df_,
        x_start="starting_time",
        x_end="finishing_time",
        y=visualize,
        color="event_title",
        template="plotly_dark",
        width= width,
        height= height,
        color_discrete_sequence= [bar_color]
    )

    fig_timeline.update_traces(
        marker=dict(line=dict(width=grid_width, color=grid_color)),
        width = bar_width,
        opacity=opacity
    )
    fig_timeline.update_layout(
        showlegend=False,
        margin=dict(t=10, l=5, r=10, b=5),
        xaxis=dict(showgrid=True, zeroline=True, showticklabels=True, tickfont=dict(size=letter_size, weight='bold',color=letter_color), tickmode="auto"),
        yaxis=dict(showgrid=True, zeroline=True, showticklabels=True, tickfont=dict(size=letter_size, weight='bold',color=letter_color), tickmode="auto", 
                   griddash="dot", categoryorder="category ascending") ,paper_bgcolor=background_color if background_color else None, plot_bgcolor=background_color if background_color else None
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
# if you want to add dots to the timeline
    # for _, row in df_.iterrows():
    #     fig_timeline.add_trace(go.Scatter(
    #         x=[row["starting_time"], row["finishing_time"]],
    #         y=[row[visualize], row[visualize]],
    #         mode="markers",
    #         marker=dict(
    #             color= dot_color,
    #             symbol="circle", size= dot_size, opacity=opacity
    #         ),
    #         showlegend=False
    #     ))

    # st.plotly_chart(fig_timeline) 
    return fig_timeline
    # display the png image
    # st.image(simulate_instagram_display(fig_timeline.to_image(format="png"), mockup_type="story"), use_column_width=True)
  
    
def simulate_instagram_display(fig_timeline_or_image, mockup_type="story"):
    """
    Simulates how a figure or image will look in Instagram's mobile app story or post view.

    :param fig_timeline_or_image: Either a Matplotlib/Plotly figure or a PIL Image object.
    :param mockup_type: "story" or "post" to choose Instagram mockup type.
    :return: PIL Image with Instagram mockup applied.
    """
    # Define dimensions for Instagram story and post
    mockup_sizes = {
        "story": (1080, 1920),  # Instagram story resolution
        "post": (1080, 1080)   # Instagram post resolution
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
    mockup = Image.new("RGB", mockup_sizes[mockup_type], (0, 0, 0))  # Black background as placeholder

    # Resize the user image to fit within the mockup
    user_image = user_image.convert("RGBA")
    user_image.thumbnail(mockup_sizes[mockup_type])  # Scale to fit within the mockup

    # Calculate position to center the image
    x_offset = (mockup.width - user_image.width) // 2
    y_offset = (mockup.height - user_image.height) // 2

    # Paste the user image onto the mockup (supports transparency)
    mockup.paste(user_image, (x_offset, y_offset), user_image)

    return mockup