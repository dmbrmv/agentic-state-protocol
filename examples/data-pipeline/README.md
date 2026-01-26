# Example: Earth Science Data Pipeline

This example shows how to set up a geospatial data processing pipeline with the Agentic State Protocol.

## Project Type
- **Architecture**: Data Pipeline for Earth Science
- **Tech Stack**: Python (Earth Science / Geospatial)
- **Use Case**: Geospatial processing, watershed analysis, climate data, remote sensing

## Initialization

```bash
# From the agentic-state-protocol root directory
python init_project.py

# When prompted:
# - Project name: "Watershed Pipeline"
# - Tech stack: Python (1)
# - Architecture: Data Pipeline (2)
```

## Resulting Structure

```
watershed_pipeline/
├── docs/                          # Protocol documentation
├── src/watershed_pipeline/        # Main package
│   ├── __init__.py
│   ├── ingestion/                 # Data acquisition (add)
│   │   ├── __init__.py
│   │   ├── dem_loader.py          # DEM download/extraction
│   │   ├── climate_loader.py      # Climate data (ERA5, CHIRPS)
│   │   └── remote_sensing.py      # Satellite imagery (Landsat, MODIS)
│   ├── processing/                # Geospatial transformations (add)
│   │   ├── __init__.py
│   │   ├── terrain.py             # Slope, aspect, flow direction
│   │   ├── watershed.py           # Delineation, subbasin extraction
│   │   └── reproject.py           # CRS transformations, resampling
│   ├── storage/                   # Data persistence (add)
│   │   ├── __init__.py
│   │   └── catalog.py             # Data catalog and metadata
│   └── serving/                   # Output generation (add)
│       ├── __init__.py
│       └── export.py              # GeoTIFF, NetCDF, GeoPackage export
├── tests/
├── scripts/
├── configs/
│   └── pipeline.yaml              # Pipeline configuration (add)
├── data/                          # Data directory (add, gitignored)
│   ├── raw/                       # Original downloaded data
│   ├── processed/                 # Intermediate products
│   └── output/                    # Final analysis results
├── .claude/
├── CLAUDE.md
├── pyproject.toml                 # Add this
└── README.md                      # Add this
```

## Recommended pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "watershed-pipeline"
version = "0.1.0"
description = "Geospatial data pipeline for watershed analysis"
requires-python = ">=3.10"
dependencies = [
    "rasterio>=1.3.0",
    "xarray>=2023.1.0",
    "rioxarray>=0.14.0",
    "geopandas>=0.13.0",
    "shapely>=2.0.0",
    "numpy>=1.24.0",
    "netcdf4>=1.6.0",
    "pyyaml>=6.0.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "pyright>=1.1.0",
]

[project.scripts]
watershed = "watershed_pipeline.cli:app"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "basic"
```

## Sample Pipeline Code

```python
# src/watershed_pipeline/processing/terrain.py
from pathlib import Path

import numpy as np
import rasterio
import xarray as xr
from rasterio.transform import from_bounds


def compute_slope(dem_path: Path, output_path: Path) -> Path:
    """Compute slope from a DEM raster.

    Args:
        dem_path: Path to input DEM GeoTIFF.
        output_path: Path to write slope raster.

    Returns:
        Path to the output slope raster.
    """
    with rasterio.open(dem_path) as src:
        dem = src.read(1).astype(np.float32)
        transform = src.transform
        crs = src.crs
        nodata = src.nodata

        # Compute cell size from transform
        cell_size_x = abs(transform.a)
        cell_size_y = abs(transform.e)

        # Gradient in x and y directions
        dy, dx = np.gradient(dem, cell_size_y, cell_size_x)

        # Slope in degrees
        slope = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))

        # Mask nodata regions
        if nodata is not None:
            slope[dem == nodata] = nodata

        # Write output
        profile = src.profile.copy()
        profile.update(dtype="float32")

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(slope, 1)

    return output_path


def load_climate_dataset(nc_path: Path, variable: str) -> xr.DataArray:
    """Load a climate variable from a NetCDF file.

    Args:
        nc_path: Path to NetCDF file (ERA5, CHIRPS, etc.).
        variable: Climate variable name (e.g., 'tp', 't2m', 'precip').

    Returns:
        xarray DataArray with the requested variable.
    """
    ds = xr.open_dataset(nc_path)
    if variable not in ds:
        available = list(ds.data_vars)
        raise ValueError(
            f"Variable '{variable}' not found. Available: {available}"
        )
    return ds[variable]
```

## Sample Config

```yaml
# configs/pipeline.yaml
project:
  name: "Syr Darya Watershed"
  crs: "EPSG:32642"  # UTM Zone 42N

sources:
  dem:
    type: geotiff
    path: data/raw/srtm_30m.tif
    resolution: 30  # meters
  climate:
    type: netcdf
    path: data/raw/era5_daily_2000_2020.nc
    variables: [tp, t2m, ssrd]
  landuse:
    type: geotiff
    path: data/raw/esa_worldcover_2021.tif

processing:
  terrain:
    - compute_slope
    - compute_aspect
    - compute_flow_direction
  watershed:
    - delineate_watershed
    - extract_subbasins
    threshold: 500  # cells

output:
  format: geopackage
  path: data/output/watershed_analysis.gpkg
```

## Workflow Example

```bash
# Start session
/boot

# Add new processing stage
/feature add-watershed-delineation

# After implementing
/done

# Run pipeline test
pytest tests/ -v

# Save and commit
/save
```

## Architecture Notes

The Earth Science Data Pipeline follows this flow:

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Acquire   │ - │  Process   │ - │  Analyze   │ - │  Export    │
│            │   │            │   │            │   │            │
│ - DEM      │   │ - Reproject│   │ - Watershed│   │ - GeoTIFF  │
│ - Climate  │   │ - Resample │   │ - Terrain  │   │ - NetCDF   │
│ - Landuse  │   │ - Clip/Mask│   │ - Stats    │   │ - GeoPackage│
│ - Satellite│   │ - Merge    │   │ - Classify │   │ - CSV/JSON │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
```

Each stage is independent and can be tested/run separately. Data flows through
`data/raw/ -> data/processed/ -> data/output/` with full provenance tracking.
