# InferDoc - Project Implementation Guide

## 🎯 Project Overview

**InferDoc** is an AI-powered GitHub Action that automatically generates and updates documentation websites for Python projects on every `git push`.

### Core Problem
- Writing and maintaining documentation is tedious
- Documentation becomes stale as code evolves
- Manual docstring updates are often forgotten

### Solution
InferDoc automatically:
1. Parses Python codebase structure using AST
2. Generates missing docstrings using LLM (GPT-4o-mini)
3. Analyzes git commit history for "Recent Changes" summaries
4. Builds and deploys beautiful MkDocs documentation website

---

## 📁 Complete Project Structure

```
InferDoc/
├── .github/
│   └── workflows/
│       └── docs.yml                 # GitHub Actions workflow
├── codescribe/
│   ├── __init__.py                  # Package initialization
│   ├── parser.py                    # AST-based Python parser
│   ├── generator.py                 # Markdown generator
│   ├── ai_enhancer.py               # AI docstring generator
│   └── git_analyzer.py              # Git history analyzer
├── docs/
│   └── index.md                     # MkDocs homepage
├── templates/
│   └── module.md.j2                 # Jinja2 template for docs
├── .env                             # Environment variables (API keys)
├── .gitignore                       # Git ignore rules
├── mkdocs.yml                       # MkDocs configuration
├── requirements.txt                 # Python dependencies
├── run_local.py                     # Local testing script
├── main.py                          # Production batch processor
├── README.md                        # Project documentation
├── LICENSE                          # MIT License
└── PROJECT_GUIDE.md                 # This file
```

---

## 🔧 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.10+ | Core implementation |
| **Code Parsing** | `ast` module | Extract Python structure |
| **Git Analysis** | `GitPython` | Read commit history |
| **AI Integration** | `openai` library | Generate docstrings (GPT-4o-mini) |
| **Templating** | `Jinja2` | Markdown template rendering |
| **Doc Generator** | `MkDocs` | Static site generation |
| **Theme** | `mkdocs-material` | Beautiful documentation theme |
| **Automation** | GitHub Actions | CI/CD pipeline |
| **Deployment** | GitHub Pages | Free hosting |

---

## 📦 Dependencies

```txt
mkdocs>=1.5.0
mkdocs-material>=9.0.0
GitPython>=3.1.0
openai>=1.0.0
python-dotenv>=1.0.0
Jinja2>=3.1.0
```

---

## 🏗️ Implementation Phases

### Phase 0: Foundation Setup ✅
**Goal:** Create project structure and configuration

**Tasks:**
- [x] Create directory structure
- [x] Setup `.gitignore`
- [x] Create `requirements.txt`
- [x] Setup `.env` template
- [x] Configure `mkdocs.yml`
- [x] Create `__init__.py` files

**Files Created:**
- `.gitignore`
- `requirements.txt`
- `.env.example`
- `mkdocs.yml`
- `codescribe/__init__.py`
- `docs/index.md`

---

### Phase 1: Core Parser
**Goal:** Extract Python file structure using AST

**Key Functions:**
- `parse_python_file(file_path)` → Returns structure dict
- `get_source_segment(source_lines, node)` → Extract node source code

**Output Structure:**
```python
{
    'classes': [
        {
            'name': 'ClassName',
            'docstring': 'Class docstring or None',
            'code': 'Full source code',
            'methods': [
                {
                    'name': 'method_name',
                    'args': ['self', 'arg1', 'arg2'],
                    'docstring': 'Method docstring or None',
                    'code': 'Full method source'
                }
            ]
        }
    ],
    'functions': [
        {
            'name': 'function_name',
            'args': ['arg1', 'arg2'],
            'docstring': 'Function docstring or None',
            'code': 'Full function source'
        }
    ]
}
```

**File:** `codescribe/parser.py`

---

### Phase 2: Documentation Generator
**Goal:** Transform parsed structure into Markdown

**Key Components:**
1. **Jinja2 Template** (`templates/module.md.j2`)
   - Module header with name
   - Recent Changes section (from git)
   - Classes with methods
   - Standalone functions
   - Docstring formatting

2. **Generator Function** (`codescribe/generator.py`)
   - `generate_markdown(structure, template_dir, template_name, module_name, summary)`
   - Renders Jinja2 template with data
   - Returns formatted Markdown string

**Files:**
- `templates/module.md.j2`
- `codescribe/generator.py`

---

### Phase 3: AI Enhancement Layer
**Goal:** Generate missing docstrings using OpenAI

**Key Functions:**
- `get_ai_docstring(function_code)` → Generate single docstring
- `enhance_structure_with_ai(structure)` → Fill all missing docstrings

**AI Prompt Strategy:**
- Use GPT-4o-mini (cost-effective)
- Google-style docstrings
- Context: full function/class code
- Clean response parsing

**Environment:**
- Requires `OPENAI_API_KEY` in `.env`
- Error handling for API failures
- Fallback messages

**File:** `codescribe/ai_enhancer.py`

---

### Phase 4: Git Analysis
**Goal:** Summarize commit history for each file

**Key Functions:**
- `get_commit_history(repo_path, file_path, limit=5)` → List of commit messages
- `summarize_commits_with_ai(commit_messages)` → AI-generated summary

**Features:**
- Extract last N commits for specific file
- Use AI to create readable "Recent Changes" summary
- Handle repositories without git history
- Error handling for git operations

**File:** `codescribe/git_analyzer.py`

---

### Phase 5: Main Integration
**Goal:** Tie all components together

**Scripts:**

1. **`run_local.py`** - Local testing
   - Test on single file
   - Full pipeline: parse → enhance → analyze → generate
   - Output to `docs/` folder
   - Run `mkdocs serve` to preview

2. **`main.py`** - Production batch processor
   - Discover all `.py` files in project
   - Process each file through pipeline
   - Generate individual `.md` files
   - Update MkDocs navigation
   - Command-line arguments support

**Files:**
- `run_local.py`
- `main.py`

---

### Phase 6: GitHub Actions Automation
**Goal:** Automatic documentation deployment

**Workflow:** `.github/workflows/docs.yml`

**Triggers:**
- Push to `main` branch

**Steps:**
1. Checkout code (with full git history)
2. Setup Python 3.10
3. Install dependencies
4. Run CodeScribe on all Python files
5. Build MkDocs site
6. Deploy to GitHub Pages

**Required Secrets:**
- `OPENAI_API_KEY` - Set in GitHub repository secrets
- `GITHUB_TOKEN` - Automatically provided

**Permissions:**
- `contents: write` - For gh-pages deployment

**File:** `.github/workflows/docs.yml`

---

### Phase 7: Polish & Documentation
**Goal:** Professional project presentation

**README.md Sections:**
1. Project logo/banner
2. Badges (build status, license)
3. Problem statement
4. Features list
5. Installation instructions
6. Usage guide (how to add to your repo)
7. Configuration options
8. Screenshots/GIFs
9. Contributing guidelines
10. License information

**Additional Files:**
- `LICENSE` - MIT License
- Enhanced `docs/index.md` - Documentation homepage
- Example documentation output

**Optional:**
- PyPI package setup (`setup.py`)
- CLI tool with `argparse`
- Unit tests

---

## 🔑 Environment Variables

Create `.env` file:
```env
OPENAI_API_KEY=sk-your-api-key-here
```

**Security:**
- Never commit `.env` to git
- Use GitHub Secrets for CI/CD
- Provide `.env.example` template

---

## 🚀 Usage Workflow

### Local Development
```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Test on single file
python run_local.py

# 4. Preview documentation
mkdocs serve
# Visit http://127.0.0.1:8000

# 5. Process all files
python main.py

# 6. Build static site
mkdocs build
```

### GitHub Actions (Automatic)
1. Push code to `main` branch
2. GitHub Actions triggers workflow
3. CodeScribe processes all Python files
4. Documentation deploys to GitHub Pages
5. Visit `https://username.github.io/codescribe/`

---

## 🎨 Customization Options

### MkDocs Theme
```yaml
# mkdocs.yml
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.instant
    - navigation.tracking
    - search.suggest
```

### Template Customization
Edit `templates/module.md.j2` to change:
- Section headers
- Formatting style
- Additional metadata
- Code block styling

### AI Prompts
Modify prompts in `ai_enhancer.py` and `git_analyzer.py` for:
- Different docstring styles (NumPy, Sphinx)
- More detailed summaries
- Different tone/formality

---

## 🧪 Testing Strategy

### Manual Testing
1. Test parser on various Python files
2. Verify AI-generated docstrings quality
3. Check git history summaries
4. Preview generated Markdown
5. Test MkDocs build

### Edge Cases
- Files without docstrings
- Files without git history
- Nested classes
- Complex function signatures
- Large codebases

---

## 📊 Success Metrics

✅ **Functional Requirements:**
- Parse any valid Python file
- Generate accurate docstrings
- Summarize git history
- Build valid MkDocs site
- Deploy to GitHub Pages

✅ **Quality Requirements:**
- Clean, readable code
- Proper error handling
- Comprehensive documentation
- Professional README
- MIT License

✅ **Performance:**
- Process files efficiently
- Minimize API calls
- Fast documentation builds

---

## 🔄 Development Workflow

1. **Start Phase** → Update PROJECT_GUIDE.md status
2. **Implement** → Write code following guide
3. **Test** → Verify functionality locally
4. **Document** → Add comments and docstrings
5. **Commit** → Clear commit messages
6. **Next Phase** → Move to next section

---

## 🐛 Common Issues & Solutions

### Issue: OpenAI API Rate Limits
**Solution:** Add retry logic with exponential backoff

### Issue: Large files timeout
**Solution:** Process files in batches, add progress indicators

### Issue: Git history not available
**Solution:** Graceful fallback, skip git analysis

### Issue: MkDocs build fails
**Solution:** Validate Markdown syntax, check mkdocs.yml

---

## 📚 Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [GitPython Documentation](https://gitpython.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jinja2 Template Designer](https://jinja.palletsprojects.com/)

---

## 🎯 Current Status

**Phase:** All Phases Complete
**Status:** Production Ready
**Next Steps:** Push to GitHub and deploy

---

## 📝 Notes

- Use GPT-4o-mini for cost efficiency
- Keep API calls minimal
- Cache results when possible
- Follow PEP 8 style guide
- Add type hints where beneficial
- Write defensive code with error handling

---

**Last Updated:** 2025-10-23
**Version:** 1.0.0
