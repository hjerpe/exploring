import base64
import json
import os
import warnings

import altair as alt
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
import umap
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)
warnings.simplefilter("ignore", category=NumbaPendingDeprecationWarning)


def authenticate():
    return "DALI-credentials", "DLAI-PROJECT"
    # Load .env
    load_dotenv()

    # Decode key and store in .JSON
    SERVICE_ACCOUNT_KEY_STRING_B64 = os.getenv("SERVICE_ACCOUNT_KEY")
    SERVICE_ACCOUNT_KEY_BYTES_B64 = SERVICE_ACCOUNT_KEY_STRING_B64.encode("ascii")
    SERVICE_ACCOUNT_KEY_STRING_BYTES = base64.b64decode(SERVICE_ACCOUNT_KEY_BYTES_B64)
    SERVICE_ACCOUNT_KEY_STRING = SERVICE_ACCOUNT_KEY_STRING_BYTES.decode("ascii")

    SERVICE_ACCOUNT_KEY = json.loads(SERVICE_ACCOUNT_KEY_STRING)

    # Create credentials based on key from service account
    # Make sure your account has the roles listed in the Google Cloud Setup section
    credentials = Credentials.from_service_account_info(
        SERVICE_ACCOUNT_KEY, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    if credentials.expired:
        credentials.refresh(Request())

    # Set project ID accoridng to environment variable
    PROJECT_ID = os.getenv("PROJECT_ID")

    return credentials, PROJECT_ID


def plot_heatmap(data, x_labels=None, y_labels=None, title=None):
    fig, ax = plt.subplots(figsize=(50, 3))
    heatmap = ax.pcolor(data, cmap="coolwarm", edgecolors="k", linewidths=0.1)

    # Add color bar to the right of the heatmap
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.remove()

    # Set labels for each axis
    if x_labels:
        ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
    if y_labels:
        ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
        ax.set_yticklabels(y_labels, va="center")

    # Set title
    if title:
        ax.set_title(title)

    plt.tight_layout()

    # Show the plot
    plt.show()


def plot_2D(x_values, y_values, labels):

    # Create scatter plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(x_values, y_values, alpha=0.5, edgecolors="k", s=40)

    # Create a mplcursors object to manage the data point interaction
    cursor = mplcursors.cursor(scatter, hover=True)

    # aes
    ax.set_title("Embedding visualization in 2D")  # Add a title
    ax.set_xlabel("X_1")  # Add x-axis label
    ax.set_ylabel("X_2")  # Add y-axis label

    # Define how each annotation should look
    @cursor.connect("add")
    def on_add(sel):
        sel.annotation.set_text(labels[sel.target.index])
        sel.annotation.get_bbox_patch().set(
            facecolor="white", alpha=0.5
        )  # Set annotation's background color
        sel.annotation.set_fontsize(12)

    plt.show()


def umap_plot(emb, text):

    cols = list(text.columns)
    # UMAP reduces the dimensions from 1024 to 2 dimensions that we can plot
    reducer = umap.UMAP(n_neighbors=2)
    umap_embeds = reducer.fit_transform(emb)
    # Prepare the data to plot and interactive visualization
    # using Altair
    # df_explore = pd.DataFrame(data={'text': qa['text']})
    # print(df_explore)

    # df_explore = pd.DataFrame(data={'text': qa_df[0]})
    df_explore = text.copy()
    df_explore["x"] = umap_embeds[:, 0]
    df_explore["y"] = umap_embeds[:, 1]

    # Plot
    chart = (
        alt.Chart(df_explore)
        .mark_circle(size=60)
        .encode(
            x=alt.X("x", scale=alt.Scale(zero=False)),  #'x',
            y=alt.Y("y", scale=alt.Scale(zero=False)),
            tooltip=cols,
        )
        .properties(width=700, height=400)
    )
    return chart


def umap_plot_big(text, emb):

    cols = list(text.columns)
    # UMAP reduces the dimensions from 1024 to 2 dimensions that we can plot
    reducer = umap.UMAP(n_neighbors=100)
    umap_embeds = reducer.fit_transform(emb)
    # Prepare the data to plot and interactive visualization
    # using Altair
    # df_explore = pd.DataFrame(data={'text': qa['text']})
    # print(df_explore)

    # df_explore = pd.DataFrame(data={'text': qa_df[0]})
    df_explore = text.copy()
    df_explore["x"] = umap_embeds[:, 0]
    df_explore["y"] = umap_embeds[:, 1]

    # Plot
    chart = (
        alt.Chart(df_explore)
        .mark_circle(size=60)
        .encode(
            x=alt.X("x", scale=alt.Scale(zero=False)),  #'x',
            y=alt.Y("y", scale=alt.Scale(zero=False)),
            tooltip=cols
            # tooltip=['text']
        )
        .properties(width=700, height=400)
    )
    return chart


def umap_plot_old(sentences, emb):
    # UMAP reduces the dimensions from 1024 to 2 dimensions that we can plot
    reducer = umap.UMAP(n_neighbors=2)
    umap_embeds = reducer.fit_transform(emb)
    # Prepare the data to plot and interactive visualization
    # using Altair
    # df_explore = pd.DataFrame(data={'text': qa['text']})
    # print(df_explore)

    # df_explore = pd.DataFrame(data={'text': qa_df[0]})
    df_explore = sentences
    df_explore["x"] = umap_embeds[:, 0]
    df_explore["y"] = umap_embeds[:, 1]

    # Plot
    chart = (
        alt.Chart(df_explore)
        .mark_circle(size=60)
        .encode(
            x=alt.X("x", scale=alt.Scale(zero=False)),  #'x',
            y=alt.Y("y", scale=alt.Scale(zero=False)),
            tooltip=["text"],
        )
        .properties(width=700, height=400)
    )
    return chart
