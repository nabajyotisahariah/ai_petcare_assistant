from crewai import Crew, Task, Process
from app.agents.agents import (
    create_orchestrator_agent, create_clinic_agent, create_appointment_agent,
    create_pet_agent, create_prescription_agent, create_commerce_agent
)

def build_assistant_crew(user_message: str, conversation_context: str) -> Crew:
    orchestrator = create_orchestrator_agent()
    clinic_agent = create_clinic_agent()
    appointment_agent = create_appointment_agent()
    pet_agent = create_pet_agent()
    prescription_agent = create_prescription_agent()
    commerce_agent = create_commerce_agent()
    
    # Task 1: The orchestrator analyzes the message and delegates to the right agent
    task_analyze_and_respond = Task(
        description=f"""
        User Message: '{user_message}'
        Conversation Context: '{conversation_context}'
        
        1. Analyze the user message and identify the intent.
        2. Delegate tasks to the specific specialized agents (Clinic, Appointment, Pet, Prescription, Commerce) using your tools.
        3. Compile their findings into a helpful, natural language response for the user.
        4. If the user wants to BOOK an appointment or REFILL a prescription, explain the options found, and ask for explicit confirmation (e.g., 'Would you like me to book the 10:30 AM slot?'). DO NOT book it yourself.
        """,
        expected_output="A natural language response answering the user's request, gathering facts from agents, and asking for confirmation if a transactional action is implied.",
        agent=orchestrator
    )
    
    crew = Crew(
        agents=[orchestrator, clinic_agent, appointment_agent, pet_agent, prescription_agent, commerce_agent],
        tasks=[task_analyze_and_respond],
        process=Process.hierarchical,
        manager_agent=orchestrator, # Use orchestrator as manager in hierarchical process
        verbose=True
    )
    
    return crew
