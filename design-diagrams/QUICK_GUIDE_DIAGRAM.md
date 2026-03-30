# Quick Guide: Generating the System Design Diagram

This guide will help you install the required tools and generate the architecture diagram for your project using the Python diagrams library.

## 1. Install System Dependencies

- **Graphviz** is required for rendering diagrams.
- On macOS, run:
  ```sh
  brew install graphviz
  ```
- On Ubuntu/Debian, run:
  ```sh
  sudo apt-get install graphviz
  ```

## 2. Set Up Python Environment

- (Optional but recommended) Create a virtual environment:
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

## 3. Install Python Packages

- Install the diagrams library:
  ```sh
  pip install diagrams
  ```

## 4. Add the React Logo

- Download a React logo PNG (transparent background recommended).
- Save it as `react.png` in the project root (same directory as `system_design_diagram.py`).

## 5. Generate the Diagram

- Run the script:
  ```sh
  python system_design_diagram.py
  ```
- This will create `system_design.png` in your project directory.

## 6. Add the Diagram to Documentation

- Reference the PNG in your `SYSTEM_DESIGN.md`:
  ```markdown
  ![System Design Diagram](system_design.png)
  ```

---

If you encounter any issues, ensure Graphviz is installed and available in your PATH. For more details, see: https://diagrams.mingrammer.com/docs/getting-started/installation
