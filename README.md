# 📚 InferDoc

**AI-Powered Documentation Generator for Python Projects**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991.svg)](https://openai.com/)

InferDoc automatically generates and maintains comprehensive documentation for your Python projects. It combines code parsing, AI-powered docstring generation, and git history analysis to create beautiful, up-to-date documentation websites.

---

## 🎯 The Problem

- **Writing documentation is tedious** and time-consuming
- **Documentation becomes stale** as code evolves
- **Manual docstring updates** are often forgotten or incomplete
- **Tracking changes** across commits is difficult

## ✨ The Solution

InferDoc automates the entire documentation process:

1. **📖 Parses** your Python codebase using AST (Abstract Syntax Tree)
2. **🤖 Generates** missing docstrings using AI (GPT-4o-mini)
3. **📊 Analyzes** git commit history for "Recent Changes" summaries
4. **🏗️ Builds** beautiful, searchable documentation with MkDocs
5. **🚀 Deploys** automatically to GitHub Pages on every push

---

## 🚀 Features

### Core Features
- ✅ **Automatic Code Parsing** - Extracts classes, functions, methods, and their metadata
- ✅ **AI-Powered Docstrings** - Generates Google-style docstrings for undocumented code
- ✅ **Git History Integration** - Summarizes recent changes from commit messages
- ✅ **Beautiful Documentation** - Modern, responsive UI with MkDocs Material theme
- ✅ **GitHub Actions Integration** - Automatic deployment on every push
- ✅ **Zero Configuration** - Works out of the box with sensible defaults

### Advanced Features
- 🎨 **Customizable Templates** - Jinja2 templates for full control over output
- 🔍 **Full-Text Search** - Built-in search functionality
- 📱 **Mobile Responsive** - Works perfectly on all devices
- 🌙 **Dark Mode** - Automatic light/dark theme switching
- 📦 **Batch Processing** - Document entire projects at once
- ⚡ **Fast & Efficient** - Minimal API calls, smart caching

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Git (for commit history analysis)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Om7035/InferDoc.git
cd InferDoc

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

---

## 🎮 Usage

### Local Testing (Single File)

Test InferDoc on a single Python file:

```bash
python run_local.py inferdoc/parser.py
```

**Options:**
```bash
python run_local.py <file_path>           # Document specific file
python run_local.py --skip-ai             # Skip AI enhancement
python run_local.py --skip-git            # Skip git analysis
```

### Batch Processing (Entire Project)

Generate documentation for all Python files:

```bash
python main.py
```

**Options:**
```bash
python main.py --source-dir inferdoc    # Source directory
python main.py --output-dir docs          # Output directory
python main.py --skip-ai                  # Skip AI enhancement
python main.py --skip-git                 # Skip git analysis
python main.py --project-name "My Project" # Custom project name
```

### Preview Documentation

```bash
mkdocs serve
```

Visit `http://127.0.0.1:8000` to see your documentation!

### Build Static Site

```bash
mkdocs build
```

The static site will be generated in the `site/` directory.

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-api-key-here

# Optional: Customize AI model (default: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini
```

### MkDocs Configuration

Customize `mkdocs.yml` to change:
- Site name and description
- Theme colors and features
- Navigation structure
- Plugins and extensions

### Template Customization

Edit `templates/module.md.j2` to customize:
- Documentation layout
- Section headers
- Formatting style
- Additional metadata

---

## 🤖 GitHub Actions Setup

### Step 1: Add Repository Secret

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `OPENAI_API_KEY`
5. Value: Your OpenAI API key
6. Click **Add secret**

### Step 2: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** / **root**
4. Click **Save**

### Step 3: Push to Main Branch

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

The GitHub Action will automatically:
- Run CodeScribe on all Python files
- Generate documentation
- Deploy to GitHub Pages

Your documentation will be available at:
`https://Om7035.github.io/InferDoc/`

---

## 📁 Project Structure

```
InferDoc/
├── .github/
│   └── workflows/
│       └── docs.yml              # GitHub Actions workflow
├── inferdoc/
│   ├── __init__.py               # Package initialization
│   ├── parser.py                 # AST-based Python parser
│   ├── generator.py              # Markdown generator
│   ├── ai_enhancer.py            # AI docstring generator
│   └── git_analyzer.py           # Git history analyzer
├── docs/
│   └── index.md                  # Documentation homepage
├── templates/
│   └── module.md.j2              # Jinja2 template
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── mkdocs.yml                    # MkDocs configuration
├── requirements.txt              # Python dependencies
├── run_local.py                  # Local testing script
├── main.py                       # Production batch processor
├── README.md                     # This file
├── LICENSE                       # MIT License
└── PROJECT_GUIDE.md              # Implementation guide
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **Code Parsing** | `ast` module |
| **Git Analysis** | `GitPython` |
| **AI Integration** | `openai` library (GPT-4o-mini) |
| **Templating** | `Jinja2` |
| **Doc Generator** | `MkDocs` |
| **Theme** | `mkdocs-material` |
| **Automation** | GitHub Actions |
| **Deployment** | GitHub Pages |

---

## 📖 How It Works

### 1. Code Parsing
InferDoc uses Python's built-in `ast` module to parse your code and extract:
- Classes and their methods
- Functions and their parameters
- Existing docstrings
- Decorators and inheritance
- Line numbers and source code

### 2. AI Enhancement
For any missing docstrings, InferDoc:
- Sends the function/class code to GPT-4o-mini
- Requests a Google-style docstring
- Includes parameter types, return values, and examples
- Handles rate limits and errors gracefully

### 3. Git Analysis
InferDoc analyzes your git history:
- Extracts the last N commits for each file
- Uses AI to summarize changes in plain English
- Creates a "Recent Changes" section in documentation

### 4. Documentation Generation
Using Jinja2 templates, InferDoc:
- Generates clean, formatted Markdown
- Organizes content by classes and functions
- Includes metadata like line numbers and decorators
- Creates an index page linking all modules

### 5. Deployment
GitHub Actions automatically:
- Runs on every push to main
- Processes all Python files
- Builds the MkDocs site
- Deploys to GitHub Pages

---

## 🎨 Customization Examples

### Custom Docstring Style

Edit `inferdoc/ai_enhancer.py` to change the prompt:

```python
prompt = f"""Generate a NumPy-style docstring for:
{code}
"""
```

### Custom Template

Create a new template in `templates/`:

```jinja
# {{ module_name }}

{% for func in structure.functions %}
## {{ func.name }}
{{ func.docstring }}
{% endfor %}
```

### Custom Theme

Edit `mkdocs.yml`:

```yaml
theme:
  name: material
  palette:
    primary: deep purple
    accent: amber
```

---

## 🧪 Testing

### Test Individual Components

```bash
# Test parser
python -m inferdoc.parser inferdoc/parser.py

# Test generator
python -m inferdoc.generator inferdoc/parser.py

# Test AI connection
python -m inferdoc.ai_enhancer

# Test git analyzer
python -m inferdoc.git_analyzer inferdoc/parser.py
```

### Test Complete Pipeline

```bash
python run_local.py inferdoc/parser.py
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/InferDoc.git
cd InferDoc

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Make your changes and test
python run_local.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Repository

**GitHub**: [https://github.com/Om7035/InferDoc](https://github.com/Om7035/InferDoc)

---

## 🙏 Acknowledgments

Built with amazing open-source tools:

- [MkDocs](https://www.mkdocs.org/) - Documentation generator
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) - Beautiful theme
- [OpenAI](https://openai.com/) - AI-powered docstring generation
- [GitPython](https://gitpython.readthedocs.io/) - Git integration
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Om7035/InferDoc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Om7035/InferDoc/discussions)
- **Documentation**: [Project Guide](PROJECT_GUIDE.md)

---

## 🗺️ Roadmap

- [ ] Support for more programming languages (JavaScript, TypeScript, etc.)
- [ ] Integration with other documentation tools (Sphinx, Docusaurus)
- [ ] Custom AI model support (local LLMs, other providers)
- [ ] Interactive API documentation
- [ ] Code examples extraction from tests
- [ ] Automatic changelog generation
- [ ] PyPI package distribution

---

## ⭐ Star History

If you find InferDoc useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the InferDoc Team**

*Automate your documentation, focus on your code.*
