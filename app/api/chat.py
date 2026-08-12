from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import uuid
from app.schemas.schemas import ChatRequest, ChatResponse
from app.crews.assistant_crew import build_assistant_crew
from app.utils.state import state_manager
from app.services.services import AppointmentService

router = APIRouter()
appointment_svc = AppointmentService()

# In a real app, this would be an LLM call to classify intent strictly.
def simple_intent_parser(message: str) -> str:
    msg = message.lower()
    if "book" in msg or "appointment" in msg:
        return "APPOINTMENT_BOOKING"
    if "refill" in msg or "prescription" in msg:
        return "RX_REFILL"
    return "GENERAL"

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the PetCare AI Assistant",
    description="Send a message to the AI pet care assistant to retrieve pet profiles, search clinics, check available appointment slots, or ask for product recommendations.",
    response_description="The AI's generated response to the user query, alongside metadata such as intent and required confirmations."
)
async def chat_endpoint(request: ChatRequest):
    # Session handling (simple for MVP)
    session_id = request.user_id # In real app, separate user_id and conversation_id
    current_state = state_manager.get_state(session_id)
    
    user_msg_lower = request.message.lower()
    
    # 1. Check if we are waiting for a confirmation
    if current_state.get("requires_confirmation"):
        if "yes" in user_msg_lower or "confirm" in user_msg_lower:
            action = current_state.get("pending_action")
            params = current_state.get("action_parameters", {})
            
            response_msg = "Action confirmed."
            
            # Execute deterministic mutation
            if action == "BOOK_APPOINTMENT":
                try:
                    appt = appointment_svc.book_appointment(
                        pet_id=params.get("pet_id", "PET-1001"), # Mocking context
                        clinic_id=params.get("clinic_id", "CLINIC-1001"),
                        doctor_id=params.get("doctor_id", "DOC-1001"),
                        slot_id=params.get("slot_id")
                    )
                    response_msg = f"Successfully booked appointment! Your reference is {appt['id']}."
                except Exception as e:
                    response_msg = f"Failed to book appointment: {e}"
            
            elif action == "RX_REFILL":
                response_msg = "Successfully requested prescription refill."
            
            # Clear state
            state_manager.clear_pending_action(session_id)
            return ChatResponse(
                conversation_id=session_id,
                message=response_msg,
                intent="CONFIRMATION_PROCESSED"
            )
        elif "no" in user_msg_lower or "cancel" in user_msg_lower:
            state_manager.clear_pending_action(session_id)
            return ChatResponse(
                conversation_id=session_id,
                message="Okay, I have cancelled that action. What else can I help you with?",
                intent="CONFIRMATION_CANCELLED"
            )

    # 2. Not a confirmation, so route to CrewAI
    intent = simple_intent_parser(request.message)
    context_str = str(current_state)
    
    try:
        # Build and run the crew
        crew = build_assistant_crew(request.message, context_str)
        result = await crew.kickoff_async()
        response_text = result.raw if hasattr(result, 'raw') else str(result)
        
        # 3. Post-process Crew response to detect if we need to enter confirmation state
        # (This is a simplified mock. A real system would use Structured Tool Outputs from the Orchestrator)
        requires_confirm = False
        if "Would you like me to book" in response_text or intent == "APPOINTMENT_BOOKING" and "available" in response_text.lower():
            # Mock extracting the slot id for the demo
            state_manager.set_pending_action(session_id, "BOOK_APPOINTMENT", {"slot_id": "SLOT-123"})
            requires_confirm = True

        return ChatResponse(
            conversation_id=session_id,
            message=response_text,
            intent=intent,
            agents_used=["orchestrator"], # Simplified
            requires_confirmation=requires_confirm,
            pending_action="BOOK_APPOINTMENT" if requires_confirm else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))