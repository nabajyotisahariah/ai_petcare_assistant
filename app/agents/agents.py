import os
import logging
from pathlib import Path
from crewai import Agent, LLM
from app.tools.crew_tools import (
    find_nearby_clinics, is_clinic_open, get_clinic_doctors,
    get_available_slots, get_pet_profile, get_pet_visits, get_latest_prescription,
    check_refill_eligibility, search_products, search_faq
)
from app.config import settings, BASE_DIR
from app.models.model import llm

# llm = LLM(
#     model="openai/gpt-5-mini"
# )

logger = logging.getLogger(__name__)

def load_prompt(filename: str) -> str:
    path = Path(BASE_DIR) / "app" / "prompts" / filename
    logger.debug(f"load_prompt... filename {filename}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def create_orchestrator_agent() -> Agent:
    logger.debug("create_orchestrator_agent...")
    return Agent(
        role="AI PetCare Assistant Orchestrator",
        goal="Understand user intent, manage context, and coordinate other agents to fulfill pet care requests.",
        backstory=load_prompt("orchestrator.txt"),
        llm=llm,
        allow_delegation=True,
        max_iter=3,
        verbose=False
    )

def create_clinic_agent() -> Agent:
    logger.debug("create_clinic_agent...")
    return Agent(
        role="Clinic Agent",
        goal="Provide accurate information about clinics, their hours, and doctors.",
        backstory=load_prompt("clinic_agent.txt"),
        tools=[find_nearby_clinics, is_clinic_open, get_clinic_doctors],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=False
    )

def create_appointment_agent() -> Agent:
    logger.debug("create_appointment_agent...")
    return Agent(
        role="Appointment Agent",
        goal="Find available appointment slots for users.",
        backstory=load_prompt("appointment_agent.txt"),
        tools=[get_available_slots],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=False
    )

def create_pet_agent() -> Agent:
    logger.debug("create_pet_agent...")
    return Agent(
        role="Pet Agent",
        goal="Retrieve accurate profile and context information about the user's pet.",
        backstory=load_prompt("pet_agent.txt"),
        tools=[get_pet_profile, get_pet_visits],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=False
    )

def create_prescription_agent() -> Agent:
    logger.debug("create_prescription_agent...")
    return Agent(
        role="Prescription Agent",
        goal="Retrieve prescription history and check refill eligibility.",
        backstory=load_prompt("prescription_agent.txt"),
        tools=[get_latest_prescription, check_refill_eligibility],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=False
    )

def create_faq_agent() -> Agent:
    logger.debug("create_faq_agent...")
    return Agent(
        role="FAQ Agent",
        goal="Answer general clinic and policy questions using the FAQ knowledge base.",
        backstory=load_prompt("faq_agent.txt"),
        tools=[search_faq],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=False
    )

def create_commerce_agent() -> Agent:
    logger.debug("create_commerce_agent...")
    return Agent(
        role="Commerce Agent",
        goal="Find and recommend pet products based on constraints.",
        backstory=load_prompt("commerce_agent.txt"),
        tools=[search_products],
        llm=llm,
        allow_delegation=False,
        max_iter=1,
        verbose=False
    )