[README.md](https://github.com/user-attachments/files/26729081/README.md)
# Hospital Simulation: Role-Based AI for Root Cause Analysis of Surgical Site Infections

## Overview

This project develops a role-based AI simulation to support root cause analysis of elevated Surgical Site Infection (SSI) rates at Naranja Hospital. The system models five key hospital personas—Nurse, Physician, Quality Assurance Specialist, Custodian, and Maintenance Technician—each with distinct knowledge, constraints, and biases.

The objective is to provide an interactive tool that allows users to interview simulated stakeholders and uncover underlying contributors to infection risk. The system is designed for use in a Lean Six Sigma (LSS) educational setting, specifically within the DMAIC framework.

## Background

Naranja Hospital is a 350-bed regional healthcare facility serving a diverse patient population, including approximately 25% Medicaid, 40% Medicare, and 10% uninsured patients. The hospital operates six surgical suites continuously on a 24-hour basis.

Hospital leadership identified a sustained increase in hospital-acquired infections (HAIs), particularly Surgical Site Infections (SSIs), which represent a significant risk to both patient safety and organizational performance.

## Problem

The hospital’s Standardized Infection Ratio (SIR) ranged from 0.68 to 1.34 between 2019 and 2024, indicating periods where infection rates exceeded expected benchmarks.

In 2024, a full audit of custodial cleaning checklists revealed 256 defective checklists across all operating suites, suggesting process inconsistency in sanitation procedures.

## Impact and Consequences

Elevated SSI rates have direct and measurable consequences:

- Increased patient morbidity and mortality  
- Extended length of stay and higher treatment costs  
- Greater strain on hospital capacity and staffing  
- Declining patient satisfaction scores  
- Reduced reimbursements from CMS under the HAC Reduction Program  
- Increased regulatory scrutiny and legal risk  

## Project Scope

This project focuses specifically on identifying process-driven contributors to elevated SSI rates within the six operating suites at Naranja Hospital.

### Included
- Pre-operative preparation procedures  
- Intra-operative sterility and workflow  
- Environmental cleaning and sanitation processes  
- Equipment and infrastructure conditions  
- Cross-functional communication and coordination  

### Excluded
- Patient-level risk factors (controlled within the SSI metric)  
- Non-surgical departments  
- Real-time clinical decision-making  

## Pipeline Design

```
Hospital Data Sources
        ↓
Knowledge Base / Data Storage
        ↓
Data Processing & Categorization
        ↓
Persona Configuration
        ↓
Prompt Generation
        ↓
AI Agent Initialization
        ↓
Gemini Model Execution
        ↓
User Interaction
        ↓
Persona Responses
        ↓
Student RCA Analysis
```

## Pedagogical Use

This project is designed for Lean Six Sigma coursework (LSS2), supporting students pursuing Yellow Belt certification.

Students apply DMAIC methodology and use the personas during the Analyze phase to conduct root cause analysis (RCA), refine Ishikawa diagrams, and build cause-and-effect tables.

## Responsible AI Considerations

- Personas include realistic bias to reflect real-world perspectives  
- Agents do not fabricate unknown information  
- Responses are constrained to role-specific knowledge  
- The system is for educational use only  

## What’s Next

- Expand personas to additional hospital roles  
- Add visualization dashboards  
- Build web-based interface  
- Improve evaluation of responses  

## Author List

- Harrison Abramsohn – https://github.com/habramsohn  
- A.J. Sexton – https://github.com/ajsexton23  
- Michelle Nggo – https://github.com/michellenggo  
- Elijah Booth – https://github.com/ElijahBooth  

## References

- Naranja Hospital Case Study  
- Rezaei, N. et al. (2025). Surgical Site Infections: A Comprehensive Review.  
- Shambhu, S. et al. (2024). SSI Burden Study  
- Haque, M. et al. (2020). HAI Prevention  
- CMS HAC Reduction Program  
- Nichols, R. (2004). SSI Prevention  

