"""
AI Enhancement Module

This module provides functionality to generate missing docstrings
for Python code using OpenAI's language models.
"""

import os
import time
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

try:
    import openai
    from openai import OpenAI
except ImportError:
    raise ImportError(
        "OpenAI library not installed. Install it with: pip install openai"
    )

# Load environment variables
load_dotenv()

# Initialize OpenAI client
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    print("AI enhancement features will not work without a valid API key.")
    client = None
else:
    client = OpenAI(api_key=API_KEY)

# Configuration
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def get_ai_docstring(
    code: str,
    code_type: str = "function",
    model: str = DEFAULT_MODEL,
    max_retries: int = MAX_RETRIES
) -> str:
    """
    Generate a docstring for a Python function, method, or class using an LLM.
    
    Args:
        code: The source code to generate a docstring for
        code_type: Type of code ('function', 'method', or 'class')
        model: OpenAI model to use (default: gpt-4o-mini)
        max_retries: Maximum number of retry attempts on failure
        
    Returns:
        str: Generated docstring text (without triple quotes)
        
    Raises:
        Exception: If API call fails after all retries
    """
    if not client:
        return "AI generation unavailable: OpenAI API key not configured."
    
    # Customize prompt based on code type
    code_type_instruction = {
        "function": "Python function",
        "method": "Python method",
        "class": "Python class"
    }.get(code_type, "Python code")
    
    prompt = f"""You are an expert Python developer writing Google-style docstrings.
Generate a professional, comprehensive docstring for the following {code_type_instruction}.

Requirements:
1. Use Google-style docstring format
2. Include a brief description
3. Document all parameters with their types
4. Document return values with types
5. Include any relevant examples if the code is complex
6. Mention any exceptions that might be raised
7. Be concise but informative

Only return the docstring text itself (without the triple quotes).
Do not include any other text, explanation, or the code itself.

Code:
{code}
"""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python documentation expert specializing in writing clear, comprehensive docstrings."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=500
            )
            
            docstring = response.choices[0].message.content.strip()
            
            # Clean up the response
            # Remove triple quotes if present
            if docstring.startswith('"""') and docstring.endswith('"""'):
                docstring = docstring[3:-3].strip()
            elif docstring.startswith("'''") and docstring.endswith("'''"):
                docstring = docstring[3:-3].strip()
            
            return docstring
            
        except openai.RateLimitError:
            if attempt < max_retries - 1:
                wait_time = RETRY_DELAY * (attempt + 1)
                print(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                return "AI generation failed: Rate limit exceeded."
                
        except openai.APIError as e:
            if attempt < max_retries - 1:
                print(f"API error: {e}. Retrying...")
                time.sleep(RETRY_DELAY)
            else:
                return f"AI generation failed: {str(e)}"
                
        except Exception as e:
            print(f"Error generating docstring: {e}")
            return f"AI generation failed: {str(e)}"
    
    return "AI generation failed after all retries."


def enhance_function_with_ai(func_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance a function dictionary with AI-generated docstring if missing.
    
    Args:
        func_info: Function information dictionary from parser
        
    Returns:
        dict: Updated function information with docstring
    """
    if not func_info.get('docstring'):
        print(f"  Generating docstring for function: {func_info['name']}...")
        func_info['docstring'] = get_ai_docstring(
            func_info['code'],
            code_type='function'
        )
    return func_info


def enhance_method_with_ai(method_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance a method dictionary with AI-generated docstring if missing.
    
    Args:
        method_info: Method information dictionary from parser
        
    Returns:
        dict: Updated method information with docstring
    """
    if not method_info.get('docstring'):
        print(f"    Generating docstring for method: {method_info['name']}...")
        method_info['docstring'] = get_ai_docstring(
            method_info['code'],
            code_type='method'
        )
    return method_info


def enhance_class_with_ai(class_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance a class dictionary with AI-generated docstrings if missing.
    
    Generates docstrings for the class itself and all its methods.
    
    Args:
        class_info: Class information dictionary from parser
        
    Returns:
        dict: Updated class information with docstrings
    """
    # Generate class docstring if missing
    if not class_info.get('docstring'):
        print(f"  Generating docstring for class: {class_info['name']}...")
        class_info['docstring'] = get_ai_docstring(
            class_info['code'],
            code_type='class'
        )
    
    # Generate method docstrings if missing
    for i, method in enumerate(class_info.get('methods', [])):
        class_info['methods'][i] = enhance_method_with_ai(method)
    
    return class_info


def enhance_structure_with_ai(
    structure: Dict[str, List[Dict[str, Any]]],
    verbose: bool = True
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Iterate over the parsed structure and fill in missing docstrings using AI.
    
    This function processes all classes, methods, and functions in the structure,
    generating docstrings for any that are missing.
    
    Args:
        structure: Parsed structure dictionary from parser.parse_python_file()
        verbose: Whether to print progress messages
        
    Returns:
        dict: Enhanced structure with AI-generated docstrings
        
    Example:
        >>> structure = parse_python_file('my_module.py')
        >>> enhanced = enhance_structure_with_ai(structure)
        >>> # Now all missing docstrings are filled in
    """
    if not client:
        if verbose:
            print("Warning: OpenAI client not initialized. Skipping AI enhancement.")
        return structure
    
    if verbose:
        print("\n🤖 Enhancing structure with AI-generated docstrings...")
    
    # Enhance functions
    for i, func in enumerate(structure.get('functions', [])):
        structure['functions'][i] = enhance_function_with_ai(func)
    
    # Enhance classes and their methods
    for i, class_obj in enumerate(structure.get('classes', [])):
        structure['classes'][i] = enhance_class_with_ai(class_obj)
    
    if verbose:
        print("✅ AI enhancement complete!\n")
    
    return structure


def test_api_connection() -> bool:
    """
    Test if the OpenAI API connection is working.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    if not client:
        print("❌ OpenAI client not initialized. Check your API key.")
        return False
    
    try:
        # Make a simple test request
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print(f"✅ OpenAI API connection successful! Using model: {DEFAULT_MODEL}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test the API connection
    print("Testing OpenAI API connection...")
    test_api_connection()
