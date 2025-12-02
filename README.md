# FastNavGenerator

![](asserts/1.png)
![](asserts/2.png)

## Project Overview

This project is a sophisticated static site generator written in Python. It reads configuration from an INI file (`FastNavGenerator.ini`) and generates a single-page, interactive HTML navigation website (`index.html`).

The key features include:
- **Configurable Link Categories:** Group links into different sections (e.g., "发版工具", "项目管理").
- **Multiple Layouts:** Supports both list and grid views for displaying links.
- **Tag-based Filtering:** Allows users to filter the displayed links by tags within each category.
- **Release Notes Timeline:** A dedicated section to display version release notes in a timeline format.
- **Interface Evolution Tracker:** A unique feature (`InterfaceRouteTable`) that visualizes the evolution of different API or software interfaces across versions and branches.
- **Local Folder Links:** Supports linking to local directories on the user's filesystem.
- **Self-Contained:** The HTML structure and CSS styles are embedded directly within the Python script, making it a single-file solution for generation logic.

## Building and Running

### Generating the Website

The primary way to generate the navigation website is to run the batch script:

```bash
FastNavGenerator.bat
```

This will execute the Python script with the correct parameters, reading from `FastNavGenerator.ini` and writing the output to `index.html`.

Alternatively, you can run the Python script directly:

```bash
python FastNavGenerator.py --config=FastNavGenerator.ini --output=index.html
```

### Creating a Standalone Executable

The `FastNavGenerator.sh` script is provided to package the Python script into a single standalone executable using `PyInstaller`.

```bash
./FastNavGenerator.sh
```

This will create a distributable file in the `dist/` directory.

## Development Conventions

- **Configuration:** All content, including links, categories, release notes, and interface route data, is managed in the `FastNavGenerator.ini` file. To add or change content, edit this file.
- **Styling:** All CSS is embedded within the `SoftNavGenerator` and `InterfaceRouteGenerator` classes in the `FastNavGenerator.py` script.
- **Dependencies:** The script relies on standard Python libraries (`configparser`, `argparse`, `sys`, `os`, `json`) and does not require any external packages for its core functionality. `PyInstaller` is an optional dependency for building an executable.
- **Management UI:** The `manage.html` file provides a basic static interface that directs the user to the command-line tools. It also references a potential Flask-based management server, but the implementation for that is not included in this project.
