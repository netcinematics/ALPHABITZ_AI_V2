
import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from alphabitz.GATHERSTATE_AGENT import GATHERSTATE_AGENT

@pytest.fixture
def gather_agent():
    # Patch Agent to prevent actual instantiation
    with patch("alphabitz.GATHERSTATE_AGENT.Agent") as MockAgent, \
         patch("alphabitz.GATHERSTATE_AGENT.InMemoryRunner") as MockRunner:
        
        # Setup Mock Agent (mostly ignored now since we use runner)
        mock_agent_instance = MockAgent.return_value
        
        # Setup Mock Runner (this is what's called now)
        mock_runner_instance = MockRunner.return_value
        
        # Mock run_debug instead of run
        mock_runner_instance.run_debug = AsyncMock()
        mock_runner_instance.run_debug.return_value = ["1. Mock Concept - Because it is a mock."]
        
        agent = GATHERSTATE_AGENT()
        
        yield agent

def test_gather_misnomer(gather_agent):
    result = asyncio.run(gather_agent.gather_misnomer_MECH())
    # Since GATHERSTATE_AGENT returns str(events), check if mock string is inside
    assert "Mock Concept" in result
    
    gather_agent.runner.run_debug.assert_called_once()
    args, _ = gather_agent.runner.run_debug.call_args
    assert "MISNOMERS" in args[0]

def test_gather_cliche(gather_agent):
    result = asyncio.run(gather_agent.gather_cliche_MECH())
    assert "Mock Concept" in result
    
    gather_agent.runner.run_debug.assert_called_once()
    args, _ = gather_agent.runner.run_debug.call_args
    assert "CLICHES" in args[0]
