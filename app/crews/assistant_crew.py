import logging
from crewai import Crew, Task, Process
from app.agents.agents import (
    create_orchestrator_agent,
    create_clinic_agent,
    create_appointment_agent,
    create_pet_agent,
    create_prescription_agent,
    create_commerce_agent
)

logger = logging.getLogger(__name__)

def build_assistant_crew(user_message: str, conversation_context: str, intent: str = "GENERAL") -> Crew:

    orchestrator = create_orchestrator_agent()
    
    clinic_agent = create_clinic_agent()
    appointment_agent = create_appointment_agent()
    pet_agent = create_pet_agent()
    prescription_agent = create_prescription_agent()
    commerce_agent = create_commerce_agent()
    
    # Define tasks for specialized agents
    clinic_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking about clinics, hours, or doctors, use your tools to retrieve this information. If not, indicate it is not applicable.",
        expected_output="Details about clinics, hours, or doctors if requested. Otherwise, indicate no clinic info was needed.",
        agent=clinic_agent,
        async_execution=True
    )
    
    appointment_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking to find available appointment slots, use your tools to get the slots. If not, indicate it is not applicable.",
        expected_output="List of available appointment slots if requested. Otherwise, indicate no appointment info was needed.",
        agent=appointment_agent,
        async_execution=True
    )
    
    pet_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking about their pet's profile or visit history, use your tools to retrieve it. If not, indicate it is not applicable.",
        expected_output="Pet profile and visit history if requested. Otherwise, indicate no pet info was needed.",
        agent=pet_agent,
        async_execution=True
    )
    
    prescription_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking about prescription history or refill eligibility, use your tools to fetch it. If not, indicate it is not applicable.",
        expected_output="Prescription history and refill status if requested. Otherwise, indicate no prescription info was needed.",
        agent=prescription_agent,
        async_execution=True
    )
    
    commerce_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking for pet products or recommendations, use your tools to search for products. If not, indicate it is not applicable.",
        expected_output="Product details and recommendations if requested. Otherwise, indicate no commerce info was needed.",
        agent=commerce_agent,
        async_execution=True
    )

    # Conditionally include agents and tasks based on intent to reduce execution time
    agents_list = []
    tasks_list = []

    if intent == "CLINIC":
        agents_list = [clinic_agent]
        tasks_list = [clinic_task]
    elif intent == "APPOINTMENT_BOOKING":
        # Often booking requires finding the clinic first, and pet info for context
        agents_list = [clinic_agent, appointment_agent, pet_agent]
        tasks_list = [clinic_task, appointment_task, pet_task]
    elif intent == "PET":
        agents_list = [pet_agent]
        tasks_list = [pet_task]
    elif intent == "RX_REFILL":
        agents_list = [pet_agent, prescription_agent]
        tasks_list = [pet_task, prescription_task]
    elif intent == "COMMERCE":
        agents_list = [commerce_agent]
        tasks_list = [commerce_task]
    else: # GENERAL
        agents_list = [pet_agent]
        tasks_list = [pet_task]

    # Task: The orchestrator synthesizes the results
    task_analyze_and_respond = Task(
        description=f"""
        User Message: '{user_message}'
        Conversation Context: '{conversation_context}'
        
        1. Review the information retrieved by the specialized agents.
        2. Compile the relevant facts into a helpful, natural language response.
        3. If the user wants to BOOK an appointment or REFILL a prescription, explain the options found, and ask for explicit confirmation (e.g., 'Would you like me to book the 10:30 AM slot?'). DO NOT book it yourself.
        """,
        expected_output="A JSON format response containing the requested information according to the prompt instructions.",
        agent=orchestrator,
        context=tasks_list
    )

    # Always append the orchestrator to synthesize the final response
    agents_list.append(orchestrator)
    tasks_list.append(task_analyze_and_respond)
    #logger.info(f"build_assistant_crew agents_list: {agents_list}, tasks_list: {tasks_list} intent {intent}")
            
    crew = Crew(
        agents=agents_list,
        tasks=tasks_list,
        process=Process.sequential,
        verbose=True
    )
    return crew







