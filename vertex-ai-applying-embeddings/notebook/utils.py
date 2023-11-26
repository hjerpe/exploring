import functools
import math
import time
from concurrent.futures import ThreadPoolExecutor

import altair as alt
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
import scann
import umap
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
from tqdm.auto import tqdm
from vertexai.language_models import TextEmbeddingModel


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


def generate_batches(sentences, batch_size=5):
    for i in range(0, len(sentences), batch_size):
        yield sentences[i : i + batch_size]


def encode_texts_to_embeddings(sentences):
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    try:
        embeddings = model.get_embeddings(sentences)
        return [embedding.values for embedding in embeddings]
    except Exception:
        return [None for _ in range(len(sentences))]


def encode_text_to_embedding_batched(
    sentences, api_calls_per_second=0.33, batch_size=5
):
    # Generates batches and calls embedding API

    embeddings_list = []

    # Prepare the batches using a generator
    batches = generate_batches(sentences, batch_size)

    seconds_per_job = 1 / api_calls_per_second

    with ThreadPoolExecutor() as executor:
        futures = []
        for batch in tqdm(
            batches, total=math.ceil(len(sentences) / batch_size), position=0
        ):
            futures.append(
                executor.submit(functools.partial(encode_texts_to_embeddings), batch)
            )
            time.sleep(seconds_per_job)

        for future in futures:
            embeddings_list.extend(future.result())

    is_successful = [
        embedding is not None for sentence, embedding in zip(sentences, embeddings_list)
    ]
    embeddings_list_successful = np.squeeze(
        np.stack([embedding for embedding in embeddings_list if embedding is not None])
    )
    return embeddings_list_successful


def clusters_2D(x_values, y_values, labels, kmeans_labels):
    fig, ax = plt.subplots()
    scatter = ax.scatter(
        x_values,
        y_values,
        c=kmeans_labels,
        cmap="Set1",
        alpha=0.5,
        edgecolors="k",
        s=40,
    )  # Change the denominator as per n_clusters

    # Create a mplcursors object to manage the data point interaction
    cursor = mplcursors.cursor(scatter, hover=True)

    # axes
    ax.set_title("Embedding clusters visualization in 2D")  # Add a title
    ax.set_xlabel("X_1")  # Add x-axis label
    ax.set_ylabel("X_2")  # Add y-axis label

    # Define how each annotation should look
    @cursor.connect("add")
    def on_add(sel):
        sel.annotation.set_text(labels.category[sel.target.index])
        sel.annotation.get_bbox_patch().set(
            facecolor="white", alpha=0.95
        )  # Set annotation's background color
        sel.annotation.set_fontsize(14)

    plt.show()


# configure ScaNN as a tree - asymmetric hash hybrid with reordering
# anisotropic quantization as described in the paper; see README


def create_index(
    embedded_dataset, num_leaves, num_leaves_to_search, training_sample_size
):

    # normalize data to use cosine sim as explained in the paper
    normalized_dataset = (
        embedded_dataset / np.linalg.norm(embedded_dataset, axis=1)[:, np.newaxis]
    )

    searcher = (
        scann.scann_ops_pybind.builder(normalized_dataset, 10, "dot_product")
        .tree(
            num_leaves=num_leaves,
            num_leaves_to_search=num_leaves_to_search,
            training_sample_size=training_sample_size,
        )
        .score_ah(2, anisotropic_quantization_threshold=0.2)
        .reorder(100)
        .build()
    )
    return searcher
