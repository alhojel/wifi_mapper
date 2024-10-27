# WiFi Mapper 🗺️ 📡

Map your WiFi network performance by combining GPS tracking with network measurements. This tool creates beautiful signal strength visualizations using Ordinary Kriging interpolation to transform sparse measurements into comprehensive coverage maps.

## Overview

WiFi Mapper consists of two main components:
1. A network performance logger that collects ping and speed test data
2. An analysis notebook that combines GPS tracks with network measurements to create interpolated coverage maps

## Requirements

```
python >= 3.8
gpxpy
pandas
matplotlib
seaborn
contextily
geopandas
pyproj
speedtest-cli
```

## Quick Start

1. Download GPX Tracker from the App Store on your mobile device
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Start GPS tracking in GPX Tracker app
4. Run the network logger:
   ```bash
   python logger.py
   ```
5. Walk around your area of interest while the script collects data
6. Export the GPX file from GPX Tracker and place it in the project directory
7. Run the analysis notebook to generate visualizations

## Project Structure

```
wifi_mapper/
├── logger.py           # Network performance data collection script
├── analysis.ipynb      # Jupyter notebook for data analysis and visualization
├── requirements.txt    # Python dependencies
```

## Logger Features

The `logger.py` script collects:
- Ping statistics (min/avg/max/packet loss) every 5 seconds
- Speed test measurements (download/upload/ping) every 5 minutes
- Automatic CSV logging with timestamps

## Analysis Features

The analysis notebook (`analysis.ipynb`) provides:
- GPS track visualization
- Network performance heatmaps
- Kriging interpolation for coverage estimation

## Data Collection Tips

1. Start GPS tracking before running the logger script
2. Walk at a steady pace to ensure even sampling
3. Cover the area in a grid pattern when possible
4. Make sure to visit areas where you expect different signal strengths
5. Let the script run for at least a few minutes in each location
6. Keep your device at a consistent height during collection

## Visualization Examples

The analysis notebook generates several types of visualizations:
- Raw measurement points overlaid on a map
- Interpolated coverage heatmaps
- Uncertainty heatmaps

## Contributing

Feel free to open issues or submit pull requests! Some areas for potential improvement:
- Additional network metrics collection
- More sophisticated interpolation methods
- Real-time visualization