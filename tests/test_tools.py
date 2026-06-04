"""
Test script for Jemma v2 tools and agent loop.
Uses mocked inference (no real API calls).
"""

import sys
import os
import json
import logging
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the project root to the path so we can import jemma
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent_loop.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    filemode="w",
)

from jemma.tools.registry import TOOL_SCHEMAS, TOOL_FUNCTIONS
from jemma.tools.file_operations.read_file import read_file_lines
from jemma.tools.file_operations.write_to_file import replace_lines_in_file, write_new_file
from jemma.tools.search_tools.grep_search import search_in_files
from jemma.services.tool_service import ToolOrchestrator
from jemma.agent.loop import AgentLoop
from jemma.message_enum import MessageType
from jemma.agentic_response import AgentResponse
from jemma.response_enums import ResponseType
from jemma.exceptions.file_operation_exceptions import FileOperationError, FileNonExistentException
from jemma.exceptions.tool_call_exceptions import ToolCallException, InvalidToolArguments

# ── Test Helpers ─────────────────────────────────────────────────────────────

def green(text): return f"\033[92m{text}\033[0m"
def red(text): return f"\033[91m{text}\033[0m"

def assert_true(condition, msg):
    if not condition:
        raise AssertionError(msg)

def test(name):
    print(f"\n🧪 {name}")

# ── Tests ──────────────────────────────────────────────────────────────────

def test_tool_registry():
    test("Tool Registry")
    
    # All expected tools should be registered
    expected_tools = {"read_file", "write_to_file", "write_new_file", "grep_search"}
    registered_tools = set(TOOL_FUNCTIONS.keys())
    assert_true(registered_tools == expected_tools, 
                f"Expected tools {expected_tools}, got {registered_tools}")
    print(green("  ✓ All 4 tools registered in TOOL_FUNCTIONS"))
    
    # Schema names should match
    schema_names = {schema["function"]["name"] for schema in TOOL_SCHEMAS}
    assert_true(schema_names == expected_tools,
                f"Schema mismatch: expected {expected_tools}, got {schema_names}")
    print(green("  ✓ All 4 schemas registered"))
    
    # All functions should be callable
    for name, func in TOOL_FUNCTIONS.items():
        assert_true(callable(func), f"{name} is not callable")
    print(green("  ✓ All registered tools are callable"))

def test_read_file():
    test("Read File Tool")
    
    # Create a temp file
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, "test.txt")
    content = "line 1\nline 2\nline 3\nline 4\nline 5\n"
    with open(test_file, "w") as f:
        f.write(content)
    
    try:
        # Test 1: Read entire file (default start_line=1, no end_line)
        result = read_file_lines(test_file)
        assert_true(result == content, f"Expected full content, got: {repr(result)}")
        print(green("  ✓ Read entire file"))
        
        # Test 2: Read with line range
        result = read_file_lines(test_file, start_line=2, end_line=4)
        expected = "line 2\nline 3\nline 4\n"
        assert_true(result == expected, f"Expected {repr(expected)}, got: {repr(result)}")
        print(green("  ✓ Read with line range"))
        
        # Test 3: Read from start_line to end of file
        result = read_file_lines(test_file, start_line=3)
        expected = "line 3\nline 4\nline 5\n"
        assert_true(result == expected, f"Expected {repr(expected)}, got: {repr(result)}")
        print(green("  ✓ Read from line to end"))
        
        # Test 4: File does not exist
        try:
            read_file_lines("/nonexistent/path/file.txt")
            assert_true(False, "Should have raised FileNonExistentException")
        except FileNonExistentException as e:
            assert_true("File not found" in str(e), f"Unexpected error: {e}")
            print(green("  ✓ FileNotFound handled correctly"))
        
        # Test 5: Invalid line range (end < start)
        try:
            read_file_lines(test_file, start_line=4, end_line=2)
            assert_true(False, "Should have raised FileOperationError")
        except FileOperationError as e:
            assert_true("Invalid file read range" in e.model_error_feedback, 
                       f"Unexpected error: {e.model_error_feedback}")
            print(green("  ✓ Invalid line range handled correctly"))
        
        # Test 6: start_line < 1
        try:
            read_file_lines(test_file, start_line=0)
            assert_true(False, "Should have raised FileOperationError")
        except FileOperationError as e:
            assert_true("start at least from the first line" in e.model_error_feedback,
                       f"Unexpected error: {e.model_error_feedback}")
            print(green("  ✓ Invalid start_line handled correctly"))
        
    finally:
        shutil.rmtree(tmpdir)

def test_write_to_file():
    test("Write to File Tool")
    
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, "test.txt")
    original = "line 1\nline 2\nline 3\nline 4\nline 5\n"
    with open(test_file, "w") as f:
        f.write(original)
    
    try:
        # Test 1: Replace middle lines
        replace_lines_in_file(test_file, start_line=2, end_line=3, new_content="new line 2\nnew line 3")
        with open(test_file, "r") as f:
            result = f.read()
        expected = "line 1\nnew line 2\nnew line 3\nline 4\nline 5\n"
        assert_true(result == expected, f"Expected {repr(expected)}, got: {repr(result)}")
        print(green("  ✓ Replace middle lines"))
        
        # Test 2: Replace single line
        replace_lines_in_file(test_file, start_line=1, end_line=1, new_content="new line 1")
        with open(test_file, "r") as f:
            result = f.read()
        expected = "new line 1\nnew line 2\nnew line 3\nline 4\nline 5\n"
        assert_true(result == expected, f"Expected {repr(expected)}, got: {repr(result)}")
        print(green("  ✓ Replace single line"))
        
        # Test 3: Invalid range (start > end)
        try:
            replace_lines_in_file(test_file, start_line=5, end_line=2, new_content="bad")
            assert_true(False, "Should have raised ValueError")
        except ValueError as e:
            assert_true("Invalid line range" in str(e), f"Unexpected error: {e}")
            print(green("  ✓ Invalid range handled correctly"))
        
    finally:
        shutil.rmtree(tmpdir)

def test_write_new_file():
    test("Write New File Tool")
    
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, "new_file.txt")
    
    try:
        content = "Hello, World!\nThis is a new file.\n"
        write_new_file(test_file, content)
        
        with open(test_file, "r") as f:
            result = f.read()
        assert_true(result == content, f"Expected {repr(content)}, got: {repr(result)}")
        print(green("  ✓ Write new file"))
        
        # Verify it can overwrite (current behavior)
        new_content = "Overwritten!\n"
        write_new_file(test_file, new_content)
        with open(test_file, "r") as f:
            result = f.read()
        assert_true(result == new_content, f"Expected {repr(new_content)}, got: {repr(result)}")
        print(green("  ✓ Overwrite existing file (current behavior)"))
        
    finally:
        shutil.rmtree(tmpdir)

def test_grep_search():
    test("Grep Search Tool")
    
    tmpdir = tempfile.mkdtemp()
    
    # Create test files
    file1 = os.path.join(tmpdir, "file1.py")
    file2 = os.path.join(tmpdir, "file2.py")
    file3 = os.path.join(tmpdir, "file3.txt")
    
    with open(file1, "w") as f:
        f.write("def hello():\n    print('hello')\n")
    with open(file2, "w") as f:
        f.write("def hello_world():\n    print('hello world')\n")
    with open(file3, "w") as f:
        f.write("just some text\n")
    
    try:
        # Test 1: Search for "hello" in directory
        result = search_in_files(search_term="hello", path=tmpdir, file_type=None)
        result_list = json.loads(result)
        assert_true(len(result_list) > 0, "Expected matches for 'hello'")
        assert_true(any("hello" in match["content"].lower() for match in result_list),
                   "Expected 'hello' in match content")
        print(green("  ✓ Search for pattern in directory"))
        
        # Test 2: Search with file type filter
        result = search_in_files(search_term="hello", path=tmpdir, file_type="py")
        result_list = json.loads(result)
        assert_true(len(result_list) > 0, "Expected matches in .py files")
        print(green("  ✓ Search with file type filter"))
        
        # Test 3: Search for non-existent pattern
        result = search_in_files(search_term="xyznonexistent", path=tmpdir, file_type=None)
        assert_true("no matches found" in result.lower(), 
                   f"Expected 'no matches found', got: {result}")
        print(green("  ✓ No matches found handled correctly"))
        
    finally:
        shutil.rmtree(tmpdir)

def test_tool_orchestrator():
    test("Tool Orchestrator")
    
    orchestrator = ToolOrchestrator()
    
    # Test 1: Execute read_file tool call
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, "test.txt")
    with open(test_file, "w") as f:
        f.write("hello world\nline 2\n")
    
    try:
        tool_calls = {
            0: {
                "id": "call_1",
                "name": "read_file",
                "arguments": json.dumps({"file_path": test_file, "start_line": 1})
            }
        }
        
        results = orchestrator.execute_tool_calls(tool_calls)
        assert_true(len(results) == 1, f"Expected 1 result, got {len(results)}")
        assert_true(results[0]["role"] == "tool", "Expected role='tool'")
        assert_true(results[0]["tool_call_id"] == "call_1", "Expected tool_call_id='call_1'")
        assert_true("hello world" in results[0]["tool_result"], 
                   f"Expected 'hello world' in result, got: {results[0]['tool_result']}")
        print(green("  ✓ Execute read_file tool call"))
        
        # Test 2: Invalid tool name
        try:
            bad_calls = {
                0: {
                    "id": "call_2",
                    "name": "nonexistent_tool",
                    "arguments": "{}"
                }
            }
            orchestrator.execute_tool_calls(bad_calls)
            assert_true(False, "Should have raised ToolCallException")
        except ToolCallException as e:
            assert_true("does not exist" in e.model_error_feedback,
                       f"Unexpected error: {e.model_error_feedback}")
            print(green("  ✓ Invalid tool name handled correctly"))
        
        # Test 3: Invalid JSON arguments
        try:
            bad_calls = {
                0: {
                    "id": "call_3",
                    "name": "read_file",
                    "arguments": "not valid json"
                }
            }
            orchestrator.execute_tool_calls(bad_calls)
            assert_true(False, "Should have raised InvalidToolArguments")
        except InvalidToolArguments as e:
            assert_true("Invalid arguments" in e.model_error_feedback,
                       f"Unexpected error: {e.model_error_feedback}")
            print(green("  ✓ Invalid JSON arguments handled correctly"))
        
    finally:
        shutil.rmtree(tmpdir)

def test_agent_loop():
    test("Agent Loop")
    
    agent = AgentLoop()
    
    # Mock the inference layer to return a text-only response
    def mock_get_model_response(messages, model_id):
        # Simulate a streaming response with just text
        delta1 = MagicMock()
        delta1.content = "Hello! "
        delta1.tool_calls = None
        
        delta2 = MagicMock()
        delta2.content = "How can I help?"
        delta2.tool_calls = None
        
        return [delta1, delta2]
    
    with patch("jemma.agent.loop.get_model_response", side_effect=mock_get_model_response):
        responses = list(agent.start_loop(
            new_message="Hi there",
            conversation_history=None,
            model_id="test-model",
            message_type=MessageType.USER
        ))
        
        assert_true(len(responses) == 2, f"Expected 2 responses, got {len(responses)}")
        assert_true(all(isinstance(r, AgentResponse) for r in responses),
                   "All responses should be AgentResponse instances")
        assert_true(responses[0].type == ResponseType.TEXT, "First response should be TEXT")
        assert_true(responses[0].content == "Hello! ", f"Expected 'Hello! ', got {responses[0].content}")
        assert_true(responses[1].content == "How can I help?", 
                   f"Expected 'How can I help?', got {responses[1].content}")
        print(green("  ✓ Text-only streaming response"))
    
    # Test 2: Tool call response
    agent2 = AgentLoop()
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, "test.txt")
    with open(test_file, "w") as f:
        f.write("file content here\n")
    
    try:
        tool_call_delta = MagicMock()
        tool_call_delta.content = None
        tool_call = MagicMock()
        tool_call.index = 0
        tool_call.id = "call_123"
        tool_call.function.name = "read_file"
        tool_call.function.arguments = json.dumps({"file_path": test_file, "start_line": 1})
        tool_call_delta.tool_calls = [tool_call]
        
        # Second delta: end of stream
        end_delta = MagicMock()
        end_delta.content = None
        end_delta.tool_calls = None
        
        call_count = [0]

        def mock_tool_response(messages, model_id):
            if call_count[0] == 0:
                call_count[0] += 1
                return [tool_call_delta, end_delta]
            else:
                text_delta = MagicMock()
                text_delta.content = "Here is the file content."
                text_delta.tool_calls = None
                return [text_delta]
        
        with patch("jemma.agent.loop.get_model_response", side_effect=mock_tool_response):
            responses = list(agent2.start_loop(
                new_message="Read the file",
                conversation_history=None,
                model_id="test-model",
                message_type=MessageType.USER
            ))
            
            # Should have at least a TOOL_CALL response
            tool_call_responses = [r for r in responses if r.type == ResponseType.TOOL_CALL]
            assert_true(len(tool_call_responses) > 0, 
                       f"Expected TOOL_CALL responses, got: {responses}")
            assert_true(tool_call_responses[0].content == "read_file",
                       f"Expected tool name 'read_file', got {tool_call_responses[0].content}")
            print(green("  ✓ Tool call streaming response"))
            
    finally:
        shutil.rmtree(tmpdir)

# ── Main ───────────────────────────────────────────────────────────────────

def run_all_tests():
    print("=" * 60)
    print("Jemma v2 Tool Validation Suite")
    print("=" * 60)
    
    tests = [
        test_tool_registry,
        test_read_file,
        test_write_to_file,
        test_write_new_file,
        test_grep_search,
        test_tool_orchestrator,
        test_agent_loop,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(red(f"  ✗ FAILED: {e}"))
            failed += 1
        except Exception as e:
            print(red(f"  ✗ ERROR: {type(e).__name__}: {e}"))
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {green(f'{passed} passed')}, {red(f'{failed} failed')}")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
