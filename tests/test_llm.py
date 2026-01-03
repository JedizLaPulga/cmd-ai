from unittest.mock import MagicMock, patch
import sys
import types

# Mock llama_cpp module if not installed
module_name = 'llama_cpp'
if module_name not in sys.modules:
    mock_module = types.ModuleType(module_name)
    mock_module.Llama = MagicMock()
    sys.modules[module_name] = mock_module

import pytest
from cmd_ai.llm import CommandGenerator

@pytest.fixture
def mock_llama():
    with patch("cmd_ai.llm.Llama") as mock:
        yield mock

def test_initialization(mock_llama):
    """Test that the generator initializes the model correctly."""
    _ = CommandGenerator(model_path="dummy.gguf")
    mock_llama.assert_called_once_with(
        model_path="dummy.gguf", 
        n_ctx=2048, 
        verbose=False
    )

def test_generate_command(mock_llama):
    """Test that generate() calls the model with correct prompt and returns striped text."""
    # Setup mock return value
    instance = mock_llama.return_value
    instance.return_value = {
        'choices': [
            {'text': '  ls -la  '}
        ]
    }
    
    generator = CommandGenerator(model_path="dummy.gguf")
    result = generator.generate("list files", "linux")
    
    assert result == "ls -la"
    
    # Verify the call to the model
    call_args = instance.call_args
    assert call_args is not None
    prompt_arg = call_args[0][0]
    
    # Check that prompt contains key parts
    assert "<|im_start|>system" in prompt_arg
    assert "expert Linux Bash assistant" in prompt_arg
    assert "list files" in prompt_arg
