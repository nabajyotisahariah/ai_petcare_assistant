from crewai import Crew, Task, Process
from app.agents.agents import (
    create_orchestrator_agent, create_clinic_agent, create_appointment_agent,
    create_pet_agent, create_prescription_agent, create_commerce_agent
)

def build_assistant_crew(user_message: str, conversation_context: str) -> Crew:
    orchestrator = create_orchestrator_agent()
    
    # Task 1: The orchestrator analyzes the message and responds
    task_analyze_and_respond = Task(
        description=f"""
        User Message: '{user_message}'
        Conversation Context: '{conversation_context}'
        
        1. Analyze the user message to determine what information is needed.
        2. Use your available tools to retrieve the specific facts requested.
        3. Compile the facts into a helpful, natural language response.
        4. If the user wants to BOOK an appointment or REFILL a prescription, explain the options found, and ask for explicit confirmation (e.g., 'Would you like me to book the 10:30 AM slot?'). DO NOT book it yourself.
        """,
        expected_output="A natural language response answering the user's request with facts retrieved from tools.",
        agent=orchestrator
    )
    
    crew = Crew(
        agents=[orchestrator],
        tasks=[task_analyze_and_respond],
        process=Process.sequential,
        verbose=True
    )
    
    return crew






