from crewai import Crew, Task, Process
from app.agents.agents import (
    #create_orchestrator_agent,
    create_clinic_agent,
    create_appointment_agent,
    create_pet_agent,
    create_prescription_agent,
    create_commerce_agent
)

def build_assistant_crew(user_message: str, conversation_context: str) -> Crew:

    #orchestrator = create_orchestrator_agent()
    
    clinic_agent = create_clinic_agent()
    appointment_agent = create_appointment_agent()
    pet_agent = create_pet_agent()
    prescription_agent = create_prescription_agent()
    commerce_agent = create_commerce_agent()
    
    # Define tasks for specialized agents
    clinic_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking about clinics, hours, or doctors, use your tools to retrieve this information. If not, indicate it is not applicable.",
        expected_output="Details about clinics, hours, or doctors if requested. Otherwise, indicate no clinic info was needed.",
        agent=clinic_agent
    )
    
    appointment_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking to find available appointment slots, use your tools to get the slots. If not, indicate it is not applicable.",
        expected_output="List of available appointment slots if requested. Otherwise, indicate no appointment info was needed.",
        agent=appointment_agent
    )
    
    pet_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking about their pet's profile or visit history, use your tools to retrieve it. If not, indicate it is not applicable.",
        expected_output="Pet profile and visit history if requested. Otherwise, indicate no pet info was needed.",
        agent=pet_agent
    )
    
    prescription_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking about prescription history or refill eligibility, use your tools to fetch it. If not, indicate it is not applicable.",
        expected_output="Prescription history and refill status if requested. Otherwise, indicate no prescription info was needed.",
        agent=prescription_agent
    )
    
    commerce_task = Task(
        description=f"Analyze the User Message: '{user_message}' and Context: '{conversation_context}'. If the user is asking for pet products or recommendations, use your tools to search for products. If not, indicate it is not applicable.",
        expected_output="Product details and recommendations if requested. Otherwise, indicate no commerce info was needed.",
        agent=commerce_agent
    )

    # Task: The orchestrator synthesizes the results
    # task_analyze_and_respond = Task(
    #     description=f"""
    #     User Message: '{user_message}'
    #     Conversation Context: '{conversation_context}'
        
    #     1. Review the information retrieved by the specialized agents (clinic, appointment, pet, prescription, commerce).
    #     2. Compile the relevant facts into a helpful, natural language response.
    #     3. If the user wants to BOOK an appointment or REFILL a prescription, explain the options found, and ask for explicit confirmation (e.g., 'Would you like me to book the 10:30 AM slot?'). DO NOT book it yourself.
    #     """,
    #     expected_output="A natural language response answering the user's request in 100 words with facts retrieved by the specialized agents.",
    #     agent=orchestrator
    # )

    #Process.hierarchical, Dynamic Execution
    # crew = Crew(
    #     agents=[
    #         clinic_agent, 
    #         appointment_agent, 
    #         pet_agent, 
    #         prescription_agent, 
    #         commerce_agent
    #     ],
    #     tasks=[task_analyze_and_respond],
    #     manager_agent=orchestrator,
    #     process=Process.hierarchical,
    #     verbose=True
    # )

    #Process.hierarchical, Sequential Execution
    crew = Crew(
        agents=[
            clinic_agent,
            appointment_agent,
            pet_agent,
            prescription_agent,
            commerce_agent,
            #orchestrator
        ],
        tasks=[
            clinic_task,
            appointment_task,
            pet_task,
            prescription_task,
            commerce_task,
            #task_analyze_and_respond
        ],
        process=Process.sequential,
        verbose=True
    )
    return crew







