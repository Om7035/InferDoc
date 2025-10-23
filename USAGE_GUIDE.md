# 📖 InferDoc Usage Guide

Complete guide on how to use InferDoc for your projects.

---

## ✅ Testing Completed Successfully!

### What We Tested:
1. ✅ **Single file documentation** - `python run_local.py`
2. ✅ **Full project documentation** - `python main.py`
3. ✅ **MkDocs preview server** - Running at http://127.0.0.1:8000/InferDoc/
4. ✅ **Generated 5 documentation files** for all InferDoc modules

---

## 🎯 How to Use InferDoc

### 1. **Document a Single Python File**

```bash
# Basic usage
python run_local.py path/to/your_file.py

# Skip AI enhancement (faster, no API costs)
python run_local.py path/to/your_file.py --skip-ai

# Skip git analysis
python run_local.py path/to/your_file.py --skip-git

# Skip both
python run_local.py path/to/your_file.py --skip-ai --skip-git
```

**Example:**
```bash
python run_local.py inferdoc/parser.py --skip-ai
```

**Output:** Creates `docs/parser.md`

---

### 2. **Document Entire Project**

```bash
# Basic usage (documents all Python files)
python main.py

# Specify source directory
python main.py --source-dir your_package_name

# Specify output directory
python main.py --output-dir documentation

# Skip AI (recommended for testing)
python main.py --skip-ai

# Full example
python main.py --source-dir inferdoc --output-dir docs --skip-ai --skip-git
```

**What it does:**
- Finds all `.py` files in source directory
- Generates documentation for each file
- Creates an index page linking all modules
- Saves everything to the output directory

---

### 3. **Preview Documentation Locally**

```bash
# Start MkDocs development server
python -m mkdocs serve

# Or specify port
python -m mkdocs serve --dev-addr 127.0.0.1:8080
```

**Then visit:** http://127.0.0.1:8000/InferDoc/

**Features:**
- ✅ Live reload on file changes
- ✅ Search functionality
- ✅ Dark/light mode
- ✅ Mobile responsive
- ✅ Beautiful Material Design theme

---

### 4. **Build Static Documentation Site**

```bash
# Build production-ready site
python -m mkdocs build

# Build with verbose output
python -m mkdocs build --verbose

# Clean and rebuild
python -m mkdocs build --clean
```

**Output:** Creates `site/` directory with static HTML files

---

## 🚀 Deployment Options

### Option 1: GitHub Pages (Automatic)

**Setup:**
1. Add `OPENAI_API_KEY` to GitHub Secrets
2. Enable GitHub Pages (Settings → Pages → gh-pages branch)
3. Push to main branch

**Workflow automatically:**
- Runs InferDoc on all Python files
- Builds MkDocs site
- Deploys to GitHub Pages

**Your docs will be at:** `https://Om7035.github.io/InferDoc/`

---

### Option 2: Manual Deployment

```bash
# Build the site
python -m mkdocs build

# Deploy to GitHub Pages manually
python -m mkdocs gh-deploy

# Or deploy the site/ folder to any web server
```

---

### Option 3: Other Platforms

**Netlify:**
```bash
# Build command
python -m mkdocs build

# Publish directory
site/
```

**Vercel:**
```bash
# Build command
pip install -r requirements.txt && mkdocs build

# Output directory
site
```

---

## 🎨 Customization

### 1. **Change Theme Colors**

Edit `mkdocs.yml`:
```yaml
theme:
  palette:
    primary: deep purple  # Change this
    accent: amber         # And this
```

**Available colors:** red, pink, purple, deep purple, indigo, blue, light blue, cyan, teal, green, light green, lime, yellow, amber, orange, deep orange

---

### 2. **Customize Documentation Template**

Edit `templates/module.md.j2`:

```jinja
# {{ module_name }}

> **Module Path:** `{{ file_path }}`

## 📋 Overview
{{ module_docstring or "No module docstring available." }}

## 📊 Statistics
- **Functions:** {{ structure.functions|length }}
- **Classes:** {{ structure.classes|length }}
- **Total Lines:** {{ total_lines }}

<!-- Add your custom sections here -->
```

---

### 3. **Change AI Model**

Edit `.env`:
```env
# Use more powerful model (costs more)
OPENAI_MODEL=gpt-4

# Or use cheaper model
OPENAI_MODEL=gpt-3.5-turbo

# Default (recommended)
OPENAI_MODEL=gpt-4o-mini
```

---

### 4. **Customize Project Name**

```bash
python main.py --project-name "My Awesome Project"
```

Or edit `mkdocs.yml`:
```yaml
site_name: My Awesome Project
site_description: My project description
```

---

## 📁 Using InferDoc for Your Own Project

### Step 1: Copy InferDoc Files

```bash
# Copy these files to your project:
.github/workflows/docs.yml  # GitHub Actions
templates/module.md.j2      # Documentation template
mkdocs.yml                  # MkDocs configuration
run_local.py               # Local testing script
main.py                    # Batch processor
requirements.txt           # Dependencies (add to yours)
```

### Step 2: Install Dependencies

```bash
pip install mkdocs mkdocs-material GitPython openai python-dotenv Jinja2
```

### Step 3: Copy InferDoc Package

```bash
# Copy the inferdoc/ directory to your project
cp -r inferdoc/ /path/to/your/project/
```

### Step 4: Generate Documentation

```bash
# Document your package
python main.py --source-dir your_package_name

# Preview
python -m mkdocs serve
```

### Step 5: Customize

- Update `mkdocs.yml` with your project name
- Customize `templates/module.md.j2` for your style
- Modify `.github/workflows/docs.yml` if needed

---

## 🔧 Command Reference

### run_local.py Options

| Flag | Description |
|------|-------------|
| `<file_path>` | Path to Python file to document |
| `--skip-ai` | Skip AI-powered docstring generation |
| `--skip-git` | Skip git history analysis |

### main.py Options

| Flag | Description | Default |
|------|-------------|---------|
| `--source-dir` | Source directory with Python files | `inferdoc` |
| `--output-dir` | Output directory for docs | `docs` |
| `--template-dir` | Template directory | `templates` |
| `--template-name` | Template file name | `module.md.j2` |
| `--skip-ai` | Skip AI enhancement | `False` |
| `--skip-git` | Skip git analysis | `False` |
| `--project-name` | Project name for index | `InferDoc Documentation` |

### mkdocs Commands

| Command | Description |
|---------|-------------|
| `mkdocs serve` | Start dev server |
| `mkdocs build` | Build static site |
| `mkdocs gh-deploy` | Deploy to GitHub Pages |
| `mkdocs --help` | Show all commands |

---

## 💡 Best Practices

### 1. **Development Workflow**

```bash
# During development (fast, no API costs)
python main.py --skip-ai --skip-git

# Before committing (with AI)
python main.py

# Preview changes
python -m mkdocs serve

# Commit and push (auto-deploys)
git add .
git commit -m "Update documentation"
git push
```

### 2. **Write Good Docstrings**

Even with AI, good docstrings help:

```python
def calculate_total(items: list, tax_rate: float = 0.1) -> float:
    """
    Calculate total price including tax.
    
    Args:
        items: List of item prices
        tax_rate: Tax rate as decimal (default: 0.1 for 10%)
    
    Returns:
        Total price with tax applied
    
    Example:
        >>> calculate_total([10, 20, 30], 0.1)
        66.0
    """
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

### 3. **Organize Your Code**

```
your_project/
├── your_package/       # Your main package
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/             # Tests (can document these too!)
├── docs/              # Generated documentation
├── inferdoc/          # InferDoc package
├── templates/         # Documentation templates
├── mkdocs.yml         # MkDocs config
└── main.py           # Documentation generator
```

### 4. **Git Commit Messages**

InferDoc uses commit messages for summaries:

```bash
# Good commits
git commit -m "Add user authentication module"
git commit -m "Fix bug in data parser"
git commit -m "Improve error handling in API client"

# Bad commits
git commit -m "update"
git commit -m "fix"
git commit -m "changes"
```

---

## 🐛 Troubleshooting

### Issue: "OpenAI API quota exceeded"

**Solution:**
```bash
# Use without AI
python main.py --skip-ai

# Or add credits to OpenAI account
# Visit: https://platform.openai.com/account/billing
```

### Issue: "Module not found"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install mkdocs mkdocs-material openai GitPython python-dotenv Jinja2
```

### Issue: "Git repository not found"

**Solution:**
```bash
# Initialize git if needed
git init

# Or skip git analysis
python main.py --skip-git
```

### Issue: "MkDocs build fails"

**Solution:**
```bash
# Check for missing files in mkdocs.yml
python -m mkdocs build --verbose

# Update navigation in mkdocs.yml to match generated files
```

---

## 📊 What Gets Generated

### File Structure After Running InferDoc:

```
docs/
├── index.md                    # Homepage
├── api_index.md               # API overview (generated)
├── inferdoc_parser.md         # Parser documentation
├── inferdoc_generator.md      # Generator documentation
├── inferdoc_ai_enhancer.md    # AI enhancer documentation
└── inferdoc_git_analyzer.md   # Git analyzer documentation

site/                          # Built static site (after mkdocs build)
├── index.html
├── api_index/
├── inferdoc_parser/
└── ... (all HTML files)
```

---

## 🎯 Next Steps After Testing

### 1. **Commit Your Changes**

```bash
git add .
git commit -m "Setup InferDoc and generate documentation"
git push origin main
```

### 2. **Configure GitHub Secrets**

1. Go to: https://github.com/Om7035/InferDoc/settings/secrets/actions
2. Add secret: `OPENAI_API_KEY` = your OpenAI API key
3. This enables automatic documentation updates

### 3. **Enable GitHub Pages**

1. Go to: https://github.com/Om7035/InferDoc/settings/pages
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** / **root**
4. Save

### 4. **Wait for Deployment**

- Check Actions tab for workflow progress
- Once complete, docs available at: `https://Om7035.github.io/InferDoc/`

### 5. **Share Your Project**

- Add badges to README
- Share on social media
- Post on Reddit (r/Python, r/programming)
- Write a blog post
- Create a demo video

---

## 🌟 Advanced Usage

### Document Multiple Projects

```bash
# Project 1
python main.py --source-dir project1 --output-dir docs/project1

# Project 2
python main.py --source-dir project2 --output-dir docs/project2
```

### Custom Docstring Styles

Edit `inferdoc/ai_enhancer.py`:

```python
# NumPy style
prompt = f"""Generate a NumPy-style docstring for:
{code}
"""

# Sphinx style
prompt = f"""Generate a Sphinx-style docstring for:
{code}
"""
```

### Integrate with Pre-commit

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: inferdoc
        name: Generate Documentation
        entry: python main.py --skip-ai
        language: system
        pass_filenames: false
```

---

## 📚 Additional Resources

- **MkDocs**: https://www.mkdocs.org/
- **MkDocs Material**: https://squidfunk.github.io/mkdocs-material/
- **OpenAI API**: https://platform.openai.com/docs/
- **GitPython**: https://gitpython.readthedocs.io/
- **Jinja2**: https://jinja.palletsprojects.com/

---

## 🆘 Getting Help

- **Issues**: https://github.com/Om7035/InferDoc/issues
- **Discussions**: https://github.com/Om7035/InferDoc/discussions
- **Documentation**: https://Om7035.github.io/InferDoc/

---

**Happy Documenting! 🚀📚**

*InferDoc - Automate your documentation, focus on your code.*
