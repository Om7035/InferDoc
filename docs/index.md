# Welcome to InferDoc

**InferDoc** is an AI-powered GitHub Action that automatically generates and updates comprehensive documentation for your Python projects.

## 🚀 Features

- **Automatic Documentation Generation**: Parses your Python codebase and generates beautiful documentation
- **AI-Powered Docstrings**: Uses GPT-4o-mini to generate missing docstrings automatically
- **Git History Integration**: Analyzes commit history to provide "Recent Changes" summaries
- **Beautiful UI**: Generates modern, searchable documentation using MkDocs Material theme
- **GitHub Actions Integration**: Automatically updates documentation on every push
- **Zero Configuration**: Works out of the box with sensible defaults

## 🎯 How It Works

1. **Parse**: InferDoc analyzes your Python files using AST (Abstract Syntax Tree)
2. **Enhance**: Missing docstrings are automatically generated using AI
3. **Analyze**: Git commit history is summarized for each file
4. **Generate**: Beautiful Markdown documentation is created
5. **Deploy**: Documentation is automatically deployed to GitHub Pages

## 📚 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Om7035/InferDoc.git
cd InferDoc

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

2. Run locally on a single file:
```bash
python run_local.py
```

3. Preview the documentation:
```bash
mkdocs serve
```

Visit `http://127.0.0.1:8000` to see your documentation!

## 🔧 Components

InferDoc consists of four main components:

- **Parser** (`parser.py`): Extracts structure from Python files using AST
- **Generator** (`generator.py`): Transforms parsed data into Markdown using Jinja2
- **AI Enhancer** (`ai_enhancer.py`): Generates missing docstrings using OpenAI
- **Git Analyzer** (`git_analyzer.py`): Summarizes commit history for each file

## 📖 Documentation

Explore the API reference to learn more about each component:

- [Parser Documentation](parser.md)
- [Generator Documentation](generator.md)
- [AI Enhancer Documentation](ai_enhancer.md)
- [Git Analyzer Documentation](git_analyzer.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌟 Acknowledgments

Built with:
- [MkDocs](https://www.mkdocs.org/) - Documentation generator
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) - Beautiful theme
- [OpenAI](https://openai.com/) - AI-powered docstring generation
- [GitPython](https://gitpython.readthedocs.io/) - Git integration

---

**Made with ❤️ by the InferDoc Team**
