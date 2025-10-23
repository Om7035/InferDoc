# 🚀 InferDoc Setup Guide

Complete guide to set up and deploy InferDoc for your project.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.10+** installed
- ✅ **Git** installed and configured
- ✅ **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- ✅ **GitHub Account** (for deployment)

---

## 🛠️ Local Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Om7035/InferDoc.git
cd InferDoc
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-api-key-here
```

**Get your OpenAI API Key:**
1. Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in your `.env` file

### Step 5: Test the Installation

```bash
# Test on a single file
python run_local.py inferdoc/parser.py

# Preview the documentation
mkdocs serve
```

Visit `http://127.0.0.1:8000` to see your documentation!

---

## 🌐 GitHub Deployment Setup

### Step 1: Fork or Use This Repository

If you want to use InferDoc for your own project:

1. Fork this repository
2. Clone your fork
3. Or create a new repository and copy the files

### Step 2: Add OpenAI API Key to GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `OPENAI_API_KEY`
5. Value: Your OpenAI API key
6. Click **Add secret**

### Step 3: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - **Deploy from a branch**
   - Branch: **gh-pages**
   - Folder: **/ (root)**
3. Click **Save**

### Step 4: Push Your Code

```bash
git add .
git commit -m "Setup InferDoc"
git push origin main
```

### Step 5: Wait for Deployment

1. Go to **Actions** tab in your repository
2. Watch the workflow run
3. Once complete, your documentation will be available at:
   `https://yourusername.github.io/InferDoc/`

---

## 🎯 Using InferDoc for Your Project

### Option 1: Add InferDoc to Existing Project

1. Copy these files to your project:
   ```
   .github/workflows/docs.yml
   templates/module.md.j2
   mkdocs.yml
   run_local.py
   main.py
   ```

2. Install dependencies:
   ```bash
   pip install mkdocs mkdocs-material GitPython openai python-dotenv Jinja2
   ```

3. Copy the `inferdoc/` package to your project

4. Update `mkdocs.yml` with your project name

5. Run locally:
   ```bash
   python main.py --source-dir your_package_name
   mkdocs serve
   ```

### Option 2: Use as a Template

1. Click "Use this template" on GitHub
2. Create your new repository
3. Clone and customize for your needs

---

## ⚙️ Configuration

### Customize MkDocs Theme

Edit `mkdocs.yml`:

```yaml
theme:
  name: material
  palette:
    primary: indigo  # Change color
    accent: indigo
  features:
    - navigation.instant
    - search.suggest
```

### Customize Documentation Template

Edit `templates/module.md.j2` to change:
- Layout and structure
- Section headers
- Formatting style
- Additional metadata

### Customize AI Prompts

Edit `inferdoc/ai_enhancer.py`:

```python
# Change docstring style
prompt = f"""Generate a NumPy-style docstring for:
{code}
"""

# Change AI model
DEFAULT_MODEL = "gpt-4"  # More powerful but expensive
```

### Configure Git Analysis

Edit `inferdoc/git_analyzer.py`:

```python
# Change number of commits to analyze
def get_commit_history(repo_path, file_path, limit=10):  # Default: 5
    ...
```

---

## 🧪 Testing

### Test Individual Components

```bash
# Test parser
python -m inferdoc.parser inferdoc/parser.py

# Test AI enhancement
python -m inferdoc.ai_enhancer

# Test git analyzer
python -m inferdoc.git_analyzer inferdoc/parser.py

# Test generator
python -m inferdoc.generator inferdoc/parser.py
```

### Test Complete Pipeline

```bash
# Single file
python run_local.py inferdoc/parser.py

# Entire project
python main.py

# With options
python main.py --skip-ai --skip-git  # Skip AI and git
python main.py --source-dir my_package
```

---

## 🐛 Troubleshooting

### Issue: OpenAI API Error

**Solution:**
- Check your API key is correct in `.env`
- Ensure you have credits in your OpenAI account
- Check rate limits

### Issue: Git History Not Found

**Solution:**
- Ensure you're in a git repository
- Run `git init` if needed
- Check file has commit history: `git log -- filename.py`

### Issue: MkDocs Build Fails

**Solution:**
- Check `mkdocs.yml` syntax
- Ensure all referenced files exist
- Run `mkdocs build --verbose` for details

### Issue: GitHub Actions Fails

**Solution:**
- Check `OPENAI_API_KEY` secret is set
- Review workflow logs in Actions tab
- Ensure `gh-pages` branch exists

### Issue: Import Errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.10+
```

---

## 📊 Usage Examples

### Document a Single Module

```bash
python run_local.py path/to/module.py
```

### Document Entire Package

```bash
python main.py --source-dir my_package --output-dir docs
```

### Custom Project Name

```bash
python main.py --project-name "My Awesome Project"
```

### Skip AI Enhancement (Faster)

```bash
python main.py --skip-ai
```

### Skip Git Analysis

```bash
python main.py --skip-git
```

---

## 🔄 Updating Documentation

### Manual Update

```bash
# Run documentation generator
python main.py

# Build site
mkdocs build

# Serve locally to preview
mkdocs serve
```

### Automatic Update (GitHub Actions)

Just push to main branch:

```bash
git add .
git commit -m "Update code"
git push origin main
```

Documentation updates automatically!

---

## 💡 Best Practices

### 1. Write Good Commit Messages

InferDoc uses commit messages for summaries:

```bash
# Good
git commit -m "Add error handling to parser"

# Bad
git commit -m "fix"
```

### 2. Use Descriptive Function Names

Better function names = better AI-generated docstrings

### 3. Keep API Calls Minimal

- Use `--skip-ai` during development
- Only run full generation before deployment

### 4. Review AI-Generated Docstrings

- AI is good but not perfect
- Review and edit generated docstrings
- Add examples manually if needed

### 5. Customize Templates

- Adapt templates to your project style
- Add custom sections (examples, notes, warnings)

---

## 🎓 Advanced Usage

### Custom Docstring Styles

Support different docstring formats:

```python
# In ai_enhancer.py
DOCSTRING_STYLES = {
    'google': 'Google-style docstring',
    'numpy': 'NumPy-style docstring',
    'sphinx': 'Sphinx-style docstring'
}
```

### Multiple Documentation Versions

Generate docs for different versions:

```bash
# Version 1.0
git checkout v1.0
python main.py --output-dir docs/v1.0

# Version 2.0
git checkout v2.0
python main.py --output-dir docs/v2.0
```

### Integration with CI/CD

Add to your existing workflow:

```yaml
- name: Generate Documentation
  run: |
    pip install -r requirements.txt
    python main.py
    mkdocs build
```

---

## 📚 Additional Resources

- **MkDocs Documentation**: [https://www.mkdocs.org/](https://www.mkdocs.org/)
- **MkDocs Material**: [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
- **OpenAI API Docs**: [https://platform.openai.com/docs/](https://platform.openai.com/docs/)
- **GitPython Docs**: [https://gitpython.readthedocs.io/](https://gitpython.readthedocs.io/)
- **Jinja2 Docs**: [https://jinja.palletsprojects.com/](https://jinja.palletsprojects.com/)

---

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/Om7035/InferDoc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Om7035/InferDoc/discussions)
- **Documentation**: [Project Guide](PROJECT_GUIDE.md)

---

**Happy Documenting! 📚✨**
