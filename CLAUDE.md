# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python education repository containing lecture materials for both Python basics and machine learning. The repository is structured into two main educational tracks with supporting tools.

## Architecture & Structure

### Educational Content
- `lecture-basic/`: Jupyter notebooks covering Python fundamentals (lists, I/O, conditionals, tuples, loops)
- `lecture-ml/`: Machine learning tutorials (linear/polynomial regression, SVM, KNN, decision trees, clustering)

### Problem Renderer Tool
- `lecture-basic/problem-renderer/`: HTML-based exercise generation system
  - Generates randomized problem sets from XML data for A4 printing
  - Uses Python HTTP server for local development
  - XML configuration system for problem management

## Common Development Commands

### Problem Renderer Development
```bash
# Start the problem renderer (from lecture-basic/problem-renderer/)
start.bat
# Or manually:
python -m http.server 8000
# Then navigate to http://localhost:8000
```

### Working with Jupyter Notebooks
```bash
# Install Jupyter if needed
pip install jupyter

# Start Jupyter server
jupyter notebook

# Or use Jupyter Lab
jupyter lab
```

## Key Files & Configuration

### Problem Renderer System
- `problem-xmls/config.xml`: Document structure and section configuration
- `problem-xmls/problems-*.xml`: Problem data with CDATA for code blocks
- `index.html`, `style.css`, `script.js`: Frontend problem rendering system

### Educational Materials
- Jupyter notebooks contain both Korean and English content
- ML notebooks include visualization and practical examples
- PDF exercise files complement the interactive content

## License & Usage Constraints

**Important**: This repository uses Creative Commons Attribution-NonCommercial 4.0 + Permission Required license:
- Non-commercial use only
- Permission required before use (contact via GitHub Issues)
- Educational purposes allowed with prior authorization

## Development Notes

- All educational content is bilingual (Korean/English)
- Problem renderer uses XML with CDATA sections for safe code block handling
- ML notebooks include practical datasets and visualization examples
- The repository focuses on educational delivery rather than software development