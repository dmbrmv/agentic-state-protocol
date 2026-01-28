# Example: Spatial Web Application

This example shows how to set up a spatial data visualization web app with the Agentic State Protocol.

## Project Type
- **Architecture**: Spatial Web Application
- **Tech Stack**: Python (Spatial Web App)
- **Use Case**: Interactive maps, spatial data dashboards, research data exploration

## Initialization

```bash
# From the agentic-state-protocol root directory
python init_project.py

# When prompted:
# - Project name: "Watershed Explorer"
# - Tech stack: Python (1)
# - Architecture: Monolithic Application (1)
```

## Resulting Structure

```
watershed_explorer/
├── docs/                          # Protocol documentation
├── src/watershed_explorer/        # Main package
│   ├── __init__.py
│   ├── app.py                     # Streamlit app entry point
│   ├── pages/                     # Multi-page app (add)
│   │   ├── 01_overview.py         # Basin overview map
│   │   ├── 02_timeseries.py       # Streamflow/climate time series
│   │   └── 03_comparison.py       # Multi-basin comparison
│   ├── components/                # Reusable UI components (add)
│   │   ├── __init__.py
│   │   ├── map_viewer.py          # Interactive map widget
│   │   ├── charts.py              # Time series and scatter plots
│   │   └── filters.py             # Date/basin/variable selectors
│   ├── data/                      # Data access layer (add)
│   │   ├── __init__.py
│   │   ├── loader.py              # GeoPackage/GeoJSON loader
│   │   └── cache.py               # Data caching utilities
│   └── utils/                     # Shared utilities (add)
│       ├── __init__.py
│       └── spatial.py             # CRS transforms, bbox helpers
├── tests/
├── scripts/
├── configs/
│   └── app.yaml                   # App configuration (add)
├── data/                          # Sample data (add)
│   └── sample/
│       ├── basins.geojson
│       └── stations.csv
├── .claude/
├── CLAUDE.md
├── pyproject.toml
└── README.md
```

## Recommended pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "watershed-explorer"
version = "0.1.0"
description = "Interactive spatial dashboard for watershed data exploration"
requires-python = ">=3.10"
dependencies = [
    "streamlit>=1.30.0",
    "geopandas>=0.13.0",
    "folium>=0.15.0",
    "streamlit-folium>=0.18.0",
    "leafmap>=0.30.0",
    "plotly>=5.18.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "pyyaml>=6.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "pyright>=1.1.0",
]

[project.scripts]
explorer = "watershed_explorer.cli:app"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "basic"
```

## Sample App Code

```python
# src/watershed_explorer/app.py
"""Watershed Explorer - Interactive spatial data dashboard."""

from pathlib import Path

import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Watershed Explorer",
    page_icon="🌊",
    layout="wide",
)


@st.cache_data
def load_basins(path: str) -> gpd.GeoDataFrame:
    """Load basin boundaries from GeoJSON or GeoPackage."""
    return gpd.read_file(path)


@st.cache_data
def load_stations(path: str) -> pd.DataFrame:
    """Load monitoring station data."""
    return pd.read_csv(path)


def create_basin_map(
    basins: gpd.GeoDataFrame,
    stations: pd.DataFrame,
) -> folium.Map:
    """Create an interactive map with basin boundaries and stations."""
    # Center map on basin centroids
    centroid = basins.geometry.union_all().centroid
    m = folium.Map(
        location=[centroid.y, centroid.x],
        zoom_start=8,
        tiles="CartoDB positron",
    )

    # Add basin polygons
    folium.GeoJson(
        basins,
        name="Basins",
        style_function=lambda _: {
            "fillColor": "#3388ff",
            "color": "#1a5599",
            "weight": 2,
            "fillOpacity": 0.3,
        },
        tooltip=folium.GeoJsonTooltip(fields=["name", "area_km2"]),
    ).add_to(m)

    # Add station markers
    for _, row in stations.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            popup=f"{row['name']}<br>Elevation: {row['elevation_m']}m",
            color="#e74c3c",
            fill=True,
            fill_opacity=0.8,
        ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


def main() -> None:
    """Main app entry point."""
    st.title("Watershed Explorer")
    st.markdown("Interactive visualization of watershed spatial data.")

    # Sidebar controls
    with st.sidebar:
        st.header("Data Sources")
        basins_path = st.text_input(
            "Basin boundaries",
            value="data/sample/basins.geojson",
        )
        stations_path = st.text_input(
            "Station data",
            value="data/sample/stations.csv",
        )

    # Load data
    basins_file = Path(basins_path)
    stations_file = Path(stations_path)

    if not basins_file.exists():
        st.error(f"Basin file not found: {basins_path}")
        return
    if not stations_file.exists():
        st.error(f"Station file not found: {stations_path}")
        return

    basins = load_basins(str(basins_file))
    stations = load_stations(str(stations_file))

    # Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Basin Map")
        basin_map = create_basin_map(basins, stations)
        st_folium(basin_map, width=700, height=500)

    with col2:
        st.subheader("Basin Statistics")
        st.dataframe(
            basins[["name", "area_km2"]].sort_values("area_km2", ascending=False),
            use_container_width=True,
        )

        st.subheader("Stations")
        st.metric("Total stations", len(stations))
        st.dataframe(
            stations[["name", "elevation_m", "lat", "lon"]],
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
```

## Running the App

```bash
# Development mode with auto-reload
streamlit run src/watershed_explorer/app.py

# With custom config
streamlit run src/watershed_explorer/app.py -- --config configs/app.yaml
```

## Sample Config

```yaml
# configs/app.yaml
app:
  title: "Watershed Explorer"
  default_crs: "EPSG:4326"
  map_tiles: "CartoDB positron"

data:
  basins: data/sample/basins.geojson
  stations: data/sample/stations.csv

display:
  map_zoom: 8
  color_scheme: "viridis"
```

## Workflow Example

```bash
# Start session
/boot

# Add a new page
/feature add-timeseries-page

# After implementing
/done

# Test locally
streamlit run src/watershed_explorer/app.py

# Save and commit
/save
```

## Architecture Notes

The Spatial Web Application follows this pattern:

```
┌──────────────────────────────────────────────────────┐
│                  Streamlit App                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │  Pages  │  │  Pages  │  │  Pages  │  ...          │
│  │Overview │  │Timeseries│ │Compare │              │
│  └────┬────┘  └────┬────┘  └────┬────┘              │
│       │            │            │                    │
│  ┌────┴────────────┴────────────┴────┐               │
│  │          Components               │               │
│  │  Map Viewer | Charts | Filters    │               │
│  └────────────────┬──────────────────┘               │
│                   │                                  │
│  ┌────────────────┴──────────────────┐               │
│  │          Data Layer               │               │
│  │  Loader | Cache | Spatial Utils   │               │
│  └───────────────────────────────────┘               │
└──────────────────────────────────────────────────────┘
```

Key principles:
- **Pages**: Each page is a self-contained view with its own data needs
- **Components**: Reusable widgets shared across pages
- **Data layer**: Centralized data access with caching for performance
- **Spatial-first**: All data operations preserve CRS and spatial metadata
