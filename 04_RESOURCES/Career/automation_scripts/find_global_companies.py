#!/usr/bin/env python3
"""
Find global remote-first AI/robotics companies hiring ML engineers
Focus: companies that sponsor visas OR hire fully remote globally
Output: JSON with companies to add to automation
"""

import json

# Companies known to hire remote globally + sponsor visas
# Curated from known remote-first AI/robotics companies
GLOBAL_REMOTE_COMPANIES = [
    # US-based, remote-first, known sponsors
    {"name": "NVIDIA", "location": "Remote (US-based)", "domain": "nvidia.com", "type": "remote+sponsor", "notes": "Deep learning, robotics, simulation - Isaac Sim, Omniverse"},
    {"name": "Google DeepMind", "location": "Remote (UK/US/CA)", "domain": "deepmind.com", "type": "remote+sponsor", "notes": "World models, robotics, physics simulation"},
    {"name": "Meta AI (FAIR)", "location": "Remote (US/UK)", "domain": "meta.com", "type": "remote+sponsor", "notes": "Embodied AI, world models, simulation"},
    {"name": "OpenAI", "location": "Remote (US)", "domain": "openai.com", "type": "remote+sponsor", "notes": "Robotics, world models, video generation"},
    {"name": "Anthropic", "location": "Remote (US/UK)", "domain": "anthropic.com", "type": "remote+sponsor", "notes": "AI safety, interpretability - aligns with physics verification"},
    {"name": "Tesla AI", "location": "Remote (US)", "domain": "tesla.com", "type": "remote+sponsor", "notes": "FSD, Optimus, simulation infrastructure"},
    {"name": "Waymo", "location": "Remote (US)", "domain": "waymo.com", "type": "remote+sponsor", "notes": "Autonomous driving, simulation at scale"},
    {"name": "Cruise", "location": "Remote (US)", "domain": "getcruise.com", "type": "remote+sponsor", "notes": "AV simulation, world models"},
    {"name": "Zoox", "location": "Remote (US)", "domain": "zoox.com", "type": "remote+sponsor", "notes": "Robotaxi, simulation"},
    {"name": "Nuro", "location": "Remote (US)", "domain": "nuro.ai", "type": "remote+sponsor", "notes": "Delivery AV, simulation"},
    
    # Robotics companies with remote roles
    {"name": "Boston Dynamics", "location": "Remote (US)", "domain": "bostondynamics.com", "type": "remote+sponsor", "notes": "Atlas, Spot - simulation, control"},
    {"name": "Agility Robotics", "location": "Remote (US)", "domain": "agilityrobotics.com", "type": "remote+sponsor", "notes": "Digit humanoid, sim-to-real"},
    {"name": "Figure AI", "location": "Remote (US)", "domain": "figure.ai", "type": "remote+sponsor", "notes": "Humanoid, physics simulation"},
    {"name": "1X Technologies", "location": "Remote (Norway/US)", "domain": "1x.tech", "type": "remote+sponsor", "notes": "Humanoid, world models"},
    {"name": "Apptronik", "location": "Remote (US)", "domain": "apptronik.com", "type": "remote+sponsor", "notes": "Apollo humanoid, NASA Valkyrie heritage"},
    {"name": "Sanctuary AI", "location": "Remote (Canada)", "domain": "sanctuary.ai", "type": "remote+sponsor", "notes": "Phoenix humanoid, Carbon AI control system"},
    {"name": "Agibot", "location": "Remote (China/Singapore)", "domain": "agibot.com", "type": "remote+sponsor", "notes": "Humanoid robotics"},
    {"name": "Fourier Intelligence", "location": "Remote (Singapore/China)", "domain": "fourierintelligence.com", "type": "remote+sponsor", "notes": "GR-1 humanoid, rehab robotics"},
    
    # Simulation/Physics companies
    {"name": "NVIDIA Omniverse/Isaac", "location": "Remote (Global)", "domain": "nvidia.com", "type": "remote+sponsor", "notes": "Physics simulation, digital twins, robotics"},
    {"name": "Unity Technologies", "location": "Remote (Global)", "domain": "unity.com", "type": "remote+sponsor", "notes": "Robotics simulation, ML-Agents, physics"},
    {"name": "Mujoco (Google DeepMind)", "location": "Remote (Global)", "domain": "mujoco.org", "type": "remote+sponsor", "notes": "Physics engine core team"},
    {"name": "DeepMind Robotics", "location": "Remote (UK/US)", "domain": "deepmind.com", "type": "remote+sponsor", "notes": "Robotics, simulation, world models"},
    {"name": "Intrinsic (Alphabet)", "location": "Remote (US)", "domain": "intrinsic.ai", "type": "remote+sponsor", "notes": "Robotics software, simulation"},
    
    # AI Research Labs - remote friendly
    {"name": "Cohere", "location": "Remote (Canada/US/UK)", "domain": "cohere.com", "type": "remote+sponsor", "notes": "LLMs, enterprise AI"},
    {"name": "Hugging Face", "location": "Remote (Global)", "domain": "huggingface.co", "type": "remote-first", "notes": "Fully remote, open source, ML tools"},
    {"name": "Weights & Biases", "location": "Remote (Global)", "domain": "wandb.ai", "type": "remote-first", "notes": "MLOps, experiment tracking - fully remote"},
    {"name": "Modal Labs", "location": "Remote (US)", "domain": "modal.com", "type": "remote-first", "notes": "Serverless GPU, ML infrastructure"},
    {"name": "Replicate", "location": "Remote (US)", "domain": "replicate.com", "type": "remote-first", "notes": "Model deployment, API"},
    {"name": "Together AI", "location": "Remote (US)", "domain": "together.ai", "type": "remote-first", "notes": "GPU cloud, open models"},
    {"name": "Lambda Labs", "location": "Remote (US)", "domain": "lambdalabs.com", "type": "remote-first", "notes": "GPU cloud, ML workstations"},
    {"name": "RunPod", "location": "Remote (US)", "domain": "runpod.io", "type": "remote-first", "notes": "GPU cloud, serverless"},
    {"name": "Vast.ai", "location": "Remote (US)", "domain": "vast.ai", "type": "remote-first", "notes": "GPU marketplace"},
    
    # European remote-friendly
    {"name": "Aleph Alpha", "location": "Remote (Germany/EU)", "domain": "aleph-alpha.com", "type": "remote+sponsor", "notes": "Sovereign AI, European LLMs"},
    {"name": "Mistral AI", "location": "Remote (France/UK)", "domain": "mistral.ai", "type": "remote+sponsor", "notes": "Already in UK list - open models"},
    {"name": "Helsing", "location": "Remote (Germany/UK/France)", "domain": "helsing.ai", "type": "remote+sponsor", "notes": "Defense AI, simulation"},
    {"name": "DeepL", "location": "Remote (Germany/Poland)", "domain": "deepl.com", "type": "remote+sponsor", "notes": "Translation AI, remote-friendly"},
    
    # Simulation/Engineering software
    {"name": "ANSYS", "location": "Remote (Global)", "domain": "ansys.com", "type": "remote+sponsor", "notes": "CAE simulation, digital twins"},
    {"name": "Siemens Digital Industries", "location": "Remote (Global)", "domain": "siemens.com", "type": "remote+sponsor", "notes": "Simcenter, NX, simulation"},
    {"name": "Dassault Systèmes", "location": "Remote (Global)", "domain": "3ds.com", "type": "remote+sponsor", "notes": "SIMULIA, CATIA, 3DEXPERIENCE"},
    {"name": "Hexagon AB", "location": "Remote (Global)", "domain": "hexagon.com", "type": "remote+sponsor", "notes": "Manufacturing simulation, CAE"},
    
    # Autonomous vehicles / robotics - remote roles
    {"name": "Aurora Innovation", "location": "Remote (US)", "domain": "aurora.tech", "type": "remote+sponsor", "notes": "Self-driving truck, simulation"},
    {"name": "Kodiak Robotics", "location": "Remote (US)", "domain": "kodiakrobotics.com", "type": "remote+sponsor", "notes": "Autonomous trucking"},
    {"name": "Gatik AI", "location": "Remote (US/Canada)", "domain": "gatik.ai", "type": "remote+sponsor", "notes": "Middle-mile autonomous"},
    {"name": "Plus AI", "location": "Remote (US/China)", "domain": "plus.ai", "type": "remote+sponsor", "notes": "Autonomous trucking"},
    {"name": "Waabi", "location": "Remote (Canada/US)", "domain": "waabi.ai", "type": "remote+sponsor", "notes": "Generative AI for autonomy, Raquel Urtasun"},
    
    # Climate/Physical AI
    {"name": "Climeworks", "location": "Remote (Switzerland)", "domain": "climeworks.com", "type": "remote+sponsor", "notes": "Carbon capture, physics simulation"},
    {"name": "Carbon Engineering", "location": "Remote (Canada)", "domain": "carbonengineering.com", "type": "remote+sponsor", "notes": "Direct air capture"},
    {"name": "Commonwealth Fusion Systems", "location": "Remote (US)", "domain": "cfs.energy", "type": "remote+sponsor", "notes": "Fusion energy, plasma physics simulation"},
    {"name": "Helion Energy", "location": "Remote (US)", "domain": "helionenergy.com", "type": "remote+sponsor", "notes": "Fusion, plasma physics"},
    
    # Remote-first platforms that hire globally
    {"name": "Turing", "location": "Remote (Global)", "domain": "turing.com", "type": "remote-first", "notes": "AI-matched developer roles, global"},
    {"name": "Andela", "location": "Remote (Global)", "domain": "andela.com", "type": "remote-first", "notes": "Technical talent marketplace"},
    {"name": "Braintrust", "location": "Remote (Global)", "domain": "usebraintrust.com", "type": "remote-first", "notes": "Talent network, crypto-enabled"},
    {"name": "Gun.io", "location": "Remote (Global)", "domain": "gun.io", "type": "remote-first", "notes": "Freelance dev, some full-time"},
    
    # Pakistani/Regional remote-friendly (can hire you from Pakistan)
    {"name": "Systems Limited", "location": "Pakistan/Remote", "domain": "systemsltd.com", "type": "local+remote", "notes": "Largest IT export, AI practice growing"},
    {"name": "10Pearls", "location": "Pakistan/Remote", "domain": "10pearls.com", "type": "local+remote", "notes": "Digital, AI/ML services"},
    {"name": "Arbisoft", "location": "Pakistan/Remote", "domain": "arbisoft.com", "type": "local+remote", "notes": "Python, ML engineering"},
    {"name": "Techlogix", "location": "Pakistan/Remote", "domain": "techlogix.com", "type": "local+remote", "notes": "Data, AI services"},
    {"name": "Confiz", "location": "Pakistan/Remote", "domain": "confiz.com", "type": "local+remote", "notes": "Your former employer - data, AI"},
    {"name": "Folio3", "location": "Pakistan/Remote", "domain": "folio3.com", "type": "local+remote", "notes": "AI, ML, computer vision"},
]

# Save to file
output = {
    "generated_at": "2026-08-09",
    "total": len(GLOBAL_REMOTE_COMPANIES),
    "companies": GLOBAL_REMOTE_COMPANIES
}

with open("/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/global_remote_companies.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(GLOBAL_REMOTE_COMPANIES)} companies to global_remote_companies.json")

# Also create an extended PRIORITY_COMPANIES list for the automation script
extended = [
    # Original 17 UK companies
    {"name": "JBS Applied A.I & Robotics Research Ltd", "location": "London", "domain": "jbs-ai-robotics.com"},
    {"name": "Shadow Robot Company Ltd.", "location": "London", "domain": "shadowrobot.com"},
    {"name": "Apollo Research AI Ltd", "location": "London", "domain": "apolloresearch.ai"},
    {"name": "CGA Simulation Ltd", "location": "Liverpool", "domain": "cga-simulation.com"},
    {"name": "HPi Verification Services Ltd", "location": "Wallingford", "domain": "hpi-verification.com"},
    {"name": "Fieldwork Robotics Limited", "location": "Cambridge", "domain": "fieldworkrobotics.com"},
    {"name": "Oxford Robotics Ltd", "location": "Reading", "domain": "oxfordrobotics.institute"},
    {"name": "Prosper Robotics Ltd", "location": "London", "domain": "prosper-robotics.com"},
    {"name": "Perceptual Robotics Limited", "location": "Bristol", "domain": "perceptualrobotics.com"},
    {"name": "Extend Robotics Limited", "location": "London", "domain": "extendrobotics.com"},
    {"name": "Human Digital Twin Limited", "location": "London", "domain": "humandigitaltwin.com"},
    {"name": "Mistral AI UK Limited", "location": "London", "domain": "mistral.ai"},
    {"name": "Stability AI Ltd", "location": "London", "domain": "stability.ai"},
    {"name": "Tecosim Technical Simulation Ltd.", "location": "Basildon", "domain": "tecosim.com"},
    {"name": "The Simulator Company Limited", "location": "London", "domain": "thesimulatorcompany.com"},
    {"name": "General Physics (UK) Ltd", "location": "London", "domain": "generalphysics.com"},
    {"name": "Innovative Physics Limited", "location": "Shanklin", "domain": "innovativephysics.co.uk"},
]

# Add high-priority global remote companies (top 30)
priority_global = [c for c in GLOBAL_REMOTE_COMPANIES if c["type"] in ("remote-first", "remote+sponsor")][:30]
for c in priority_global:
    extended.append({"name": c["name"], "location": c["location"], "domain": c["domain"]})

with open("/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/extended_priority_companies.json", "w") as f:
    json.dump({"companies": extended, "total": len(extended)}, f, indent=2)

print(f"Extended priority list: {len(extended)} companies")
