"""Palmer Penguins Explorer - a Streamlit app that uses all 11 features
from the Streamlit Features for Beginners guide.

Dataset: Palmer Archipelago (Antarctica) penguin data, also on Kaggle as
"Palmer Archipelago (Antarctica) penguin data".
Columns: species, island, bill_length_mm, bill_depth_mm, flipper_length_mm,
         body_mass_g, sex, year

Run:
    pip install streamlit pandas numpy matplotlib seaborn
    streamlit run app.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
NUMERIC_COLS = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]


# ---------- 9. Cache data ----------
@st.cache_data
def load_data(url: str = DATA_URL) -> pd.DataFrame:
    return pd.read_csv(url)


# ---------- helpers (plain pandas, easy to test) ----------
def filter_data(df, species, island, sex, mass_range):
    out = df[df["species"].isin(species)]
    if island != "All":
        out = out[out["island"] == island]
    if sex != "All":
        out = out[out["sex"] == sex]
    low, high = mass_range
    out = out[out["body_mass_g"].between(low, high)]
    return out


def closest_species(df, flipper, mass):
    """Nearest-average match: which species has the closest typical flipper and mass?"""
    stats = df.groupby("species")[["flipper_length_mm", "body_mass_g"]].mean()
    spread = df[["flipper_length_mm", "body_mass_g"]].std()
    dist = (
                   ((stats["flipper_length_mm"] - flipper) / spread["flipper_length_mm"]) ** 2
                   + ((stats["body_mass_g"] - mass) / spread["body_mass_g"]) ** 2
           ) ** 0.5
    return dist.idxmin(), dist.sort_values()


def main():
    st.set_page_config(page_title="Penguins Explorer", page_icon="🐧", layout="wide")

    # ---------- 1. Text and headings ----------
    st.title("🐧 Palmer Penguins Explorer")
    st.header("Penguin measurements from Antarctica")
    st.write("Filter the data in the sidebar, explore the charts, and try the species finder.")
    st.markdown("Data: **Palmer Station LTER** (also available on *Kaggle*).")

    # ---------- Load data ----------
    try:
        df = load_data()
    except Exception as exc:  # no internet / URL blocked
        st.error(f"Could not load the dataset from the web: {exc}")
        uploaded = st.file_uploader("Upload penguins.csv from Kaggle instead", type="csv")
        if uploaded is None:
            st.stop()
        df = pd.read_csv(uploaded)

    # ---------- 5. Sidebar (with 3. input widgets) ----------
    st.sidebar.header("Filters")
    species = st.sidebar.multiselect(
        "Species", sorted(df["species"].unique()), default=sorted(df["species"].unique())
    )
    island = st.sidebar.selectbox("Island", ["All"] + sorted(df["island"].unique()))
    sex = st.sidebar.radio("Sex", ["All"] + sorted(df["sex"].dropna().unique()), horizontal=True)
    mass_min, mass_max = int(df["body_mass_g"].min()), int(df["body_mass_g"].max())
    mass_range = st.sidebar.slider("Body mass (g)", mass_min, mass_max, (mass_min, mass_max))
    show_raw = st.sidebar.checkbox("Show raw data table", value=True)

    filtered = filter_data(df, species, island, sex, mass_range)

    if filtered.empty:
        st.warning("No penguins match these filters. Try widening them.")
        st.stop()

    # ---------- 2. Numbers and messages + 7. Columns ----------
    st.subheader("Summary")
    st.success(f"Data loaded: {len(df)} penguins, {len(filtered)} match your filters.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Penguins", len(filtered))
    col2.metric("Avg body mass", f"{filtered['body_mass_g'].mean():,.0f} g")
    col3.metric("Avg flipper", f"{filtered['flipper_length_mm'].mean():.1f} mm")
    col4.metric("Avg bill length", f"{filtered['bill_length_mm'].mean():.1f} mm")

    missing_total = int(filtered.isna().sum().sum())
    if missing_total:
        st.warning(f"{missing_total} values are missing in the filtered data.")
    st.info("Explore the penguin dataset using the sidebar filters.")

    # ---------- 8. Expandable section ----------
    with st.expander("Show missing values"):
        missing = filtered.isna().sum()
        st.write(missing[missing > 0].to_frame("missing") if missing.any() else "No missing values.")

    # ---------- 4. Tables and dataframes ----------
    st.subheader("Dataset preview")
    if show_raw:
        st.dataframe(filtered)  # interactive
    st.write("Average measurements by species")
    st.table(filtered.groupby("species")[NUMERIC_COLS].mean().round(1))  # static
    st.write(filtered.head(3))

    # ---------- 6. Matplotlib and Seaborn charts (+ 7. Columns) ----------
    st.subheader("Charts")
    left, right = st.columns(2)

    with left:
        fig, ax = plt.subplots()
        sns.countplot(data=filtered, x="species", hue="species", ax=ax, legend=False)
        ax.set_title("Penguins per species")
        ax.set_xlabel("Species")
        ax.set_ylabel("Count")
        st.pyplot(fig)
        plt.close(fig)

    with right:
        fig, ax = plt.subplots()
        sns.scatterplot(
            data=filtered, x="flipper_length_mm", y="body_mass_g", hue="species", ax=ax
        )
        ax.set_title("Flipper length vs body mass")
        ax.set_xlabel("Flipper length (mm)")
        ax.set_ylabel("Body mass (g)")
        st.pyplot(fig)
        plt.close(fig)

    left2, right2 = st.columns(2)
    with left2:
        feature = st.selectbox("Feature for histogram", NUMERIC_COLS, index=3)
        fig, ax = plt.subplots()
        sns.histplot(data=filtered, x=feature, hue="species", kde=True, ax=ax)
        ax.set_title(f"Distribution of {feature}")
        st.pyplot(fig)
        plt.close(fig)

    with right2:
        st.write("Correlation between measurements")
        fig, ax = plt.subplots()
        sns.heatmap(filtered[NUMERIC_COLS].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation heatmap")
        st.pyplot(fig)
        plt.close(fig)

    # ---------- 3. Input widgets: text, number, button ----------
    st.subheader("Species finder")
    st.write("Enter a penguin's measurements and see which species it most resembles.")
    name = st.text_input("Name your penguin", value="Pingu")
    f_col, m_col = st.columns(2)
    flipper = f_col.number_input("Flipper length (mm)", min_value=150, max_value=250, value=200)
    mass = m_col.number_input("Body mass (g)", min_value=2000, max_value=7000, value=4000, step=50)

    if st.button("Find species"):
        best, distances = closest_species(df.dropna(subset=NUMERIC_COLS), flipper, mass)
        st.success(f"{name} looks most like an **{best}** penguin!")
        st.write("Distance to each species (smaller = closer):")
        st.write(distances.round(2).to_frame("distance"))

    # ---------- 10. Download a CSV ----------
    st.subheader("Download")
    csv = filtered.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="penguins_filtered.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()

