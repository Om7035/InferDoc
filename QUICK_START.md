# ⚡ InferDoc Quick Start

Get InferDoc running in 5 minutes!

---

## 🚀 Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/Om7035/InferDoc.git
cd InferDoc

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# OR (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Configuration (1 minute)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get key from: https://platform.openai.com/api-keys
```

**Your `.env` file should look like:**
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

---

## 🎯 Usage (2 minutes)

### Test on Single File

```bash
python run_local.py inferdoc/parser.py
```

### Generate Full Documentation

```bash
python main.py
```

### Preview Documentation

```bash
mkdocs serve
```

Then visit: **http://127.0.0.1:8000**

---

## 🎨 Common Commands

| Command | Description |
|---------|-------------|
| `python run_local.py <file>` | Document single file |
| `python main.py` | Document entire project |
| `python main.py --skip-ai` | Skip AI (faster, no API calls) |
| `python main.py --skip-git` | Skip git analysis |
| `mkdocs serve` | Preview documentation |
| `mkdocs build` | Build static site |

---

## 📁 Project Structure

```
InferDoc/
├── inferdoc/          # Core package
│   ├── parser.py      # Code parser
│   ├── generator.py   # Doc generator
│   ├── ai_enhancer.py # AI docstrings
│   └── git_analyzer.py# Git analysis
├── templates/         # Jinja2 templates
├── docs/             # Generated docs
├── run_local.py      # Test single file
└── main.py           # Batch processor
```

---

## 🔧 Customization

### Change AI Model

Edit `.env`:
```env
OPENAI_MODEL=gpt-4  # More powerful (but expensive)
```

### Change Theme Color

Edit `mkdocs.yml`:
```yaml
theme:
  palette:
    primary: deep purple  # Change this
```

### Customize Template

Edit `templates/module.md.j2` to change documentation layout.

---

## 🐛 Troubleshooting

### "OpenAI API key not found"
- Check `.env` file exists
- Verify API key is correct
- Restart terminal after editing `.env`

### "No module named 'inferdoc'"
- Ensure you're in the project directory
- Activate virtual environment
- Reinstall: `pip install -r requirements.txt`

### "Git repository not found"
- Run `git init` in your project
- Or use `--skip-git` flag

---

## 🌐 Deploy to GitHub Pages

### 1. Add Secret

Go to: **Settings → Secrets → Actions**

Add: `OPENAI_API_KEY` = your key

### 2. Enable Pages

Go to: **Settings → Pages**

Select: **gh-pages** branch

### 3. Push Code

```bash
git add .
git commit -m "Deploy InferDoc"
git push origin main
```

Your docs will be at: `https://yourusername.github.io/InferDoc/`

---

## 📚 Next Steps

- ✅ Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
- ✅ Check [IMPROVEMENTS.md](IMPROVEMENTS.md) for roadmap
- ✅ Review [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for architecture
- ✅ Customize templates for your project
- ✅ Star the repo! ⭐

---

## 💡 Pro Tips

1. **Use `--skip-ai` during development** to save API costs
2. **Review AI-generated docstrings** before committing
3. **Write good commit messages** for better git summaries
4. **Customize templates** to match your project style
5. **Enable GitHub Actions** for automatic updates

---

## 🆘 Need Help?

- **Issues**: [GitHub Issues](https://github.com/Om7035/InferDoc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Om7035/InferDoc/discussions)
- **Docs**: [Full Documentation](README.md)

---

**Happy Documenting! 🚀**
