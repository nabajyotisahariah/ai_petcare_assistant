import os
from pathlib import Path
from crewai import Agent
from app.tools.crew_tools import (
    find_nearby_clinics, is_clinic_open, get_clinic_doctors,
    get_available_slots, get_pet_profile, get_latest_prescription,
    check_refill_eligibility, search_products
)
from app.config import settings, BASE_DIR

def load_prompt(filename: str) -> str:
    path = Path(BASE_DIR) / "app" / "prompts" / filename
    print("load_prompt... filename ",filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def create_orchestrator_agent() -> Agent:
    print("create_orchestrator_agent...")
    return Agent(
        role="AI PetCare Assistant Orchestrator",
        goal="Understand user intent, manage context, and coordinate other agents to fulfill pet care requests.",
        backstory=load_prompt("orchestrator.txt"),
        allow_delegation=True,
        verbose=True
    )

def create_clinic_agent() -> Agent:
    print("create_clinic_agent...")
    return Agent(
        role="Clinic Agent",
        goal="Provide accurate information about clinics, their hours, and doctors.",
        backstory=load_prompt("clinic_agent.txt"),
        tools=[find_nearby_clinics, is_clinic_open, get_clinic_doctors],
        allow_delegation=False,
        verbose=True
    )

def create_appointment_agent() -> Agent:
    print("create_appointment_agent...")
    return Agent(
        role="Appointment Agent",
        goal="Find available appointment slots for users.",
        backstory=load_prompt("appointment_agent.txt"),
        tools=[get_available_slots],
        allow_delegation=False,
        verbose=True
    )

def create_pet_agent() -> Agent:
    print("create_pet_agent...",load_prompt("pet_agent.txt"))
    return Agent(
        role="Pet Agent",
        goal="Retrieve accurate profile and context information about the user's pet.",
        backstory=load_prompt("pet_agent.txt"),
        tools=[get_pet_profile],
        allow_delegation=False,
        verbose=True
    )

def create_prescription_agent() -> Agent:
    print("create_prescription_agent...")
    return Agent(
        role="Prescription Agent",
        goal="Retrieve prescription history and check refill eligibility.",
        backstory=load_prompt("prescription_agent.txt"),
        tools=[get_latest_prescription, check_refill_eligibility],
        allow_delegation=False,
        verbose=True
    )

def create_commerce_agent() -> Agent:
    print("create_commerce_agent...")
    return Agent(
        role="Commerce Agent",
        goal="Find and recommend pet products based on constraints.",
        backstory=load_prompt("commerce_agent.txt"),
        tools=[search_products],
        allow_delegation=False,
        verbose=True
    )