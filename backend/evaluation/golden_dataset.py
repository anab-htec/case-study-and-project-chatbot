from deepeval.dataset import Golden

from app.models.constants import Intent

dataset = [
    Golden(
        input="Can you summarize case studies in the Healthcare sector, specifically regarding patient monitoring and data management?",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="How did we assist a client in the financial sector with predictive analytics? What were the challenges of implementing machine learning in this environment, and how did it improve decision-making?",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="Give me an overview of case studies that focus on how we've used data visualization and dashboards to improve business decision-making.",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="Can you explain how we optimized a manufacturing client’s alerting system to reduce downtime? What were the challenges related to syncing systems, and what was the measurable impact on operational efficiency?",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="Give me details on case studies that focus on our past experience in handling 'hybrid' environments where systems operate both locally (offline) and in the cloud.",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="Give me an overview of case stduies in the 'Utilities' and 'Logistics' industries, specifically regarding asset tracking and resource management.",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="What approach did we use to enhance customer engagement for a retail client? How did we address data inconsistencies and improve overall service delivery through automation and analytics?",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="I need information on platforms that use a Live Video Sdk and a Secure DB. The solution should have implemented Remote doctor visits, Prescription management, and Automated reminders through Telemedicine and Notification Automation services",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="Do we have an Energy grid remote control project that uses SCADA Software, IoT Gateways, and a Licensed Protocol? I am interested in Grid segment automation, Incident reporting systems, and Remote device management via Control Engineering services.",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="I'm searching for a Workforce scheduler that features a Scheduler Module and an HR API with Cloud Sync. It should offer Shift planning, Automated reminders, and Performance graphs as part of its HR Tools and Analytics services.",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="I am looking for a project which utilizes a Web Framework, SSL, and a Relational DB. We need to see evidence of solutions like Digital patient records, an Appointment handling system, and Health insights. This project should fall under our Web Development, Security Review, and Data Management services",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="Show all AI chatbot initiatives leveraging Deep Learning Models and NoSQL. The solution should cover Automated Customer Replies and Query Escalation Routing, and be part of Conversational Design, ML Training, and Customer Engagement services.",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="Can you show me examples of retail platforms using SQL and NoSQL databases for inventory monitoring and sales analytics?",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="Can you find a management platform built with a Javascript Framework and NoSQL data store? We specifically need a solution that offers Inventory monitoring dashboards, Customer pattern tracking, and Automated sales analytics, including Business Modeling services.",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="I am looking for frontend projects build with React",
         additional_metadata={"scenario": "no_results", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="Can you give me a list of all AI projects?",
        additional_metadata={"scenario": "no_results", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="Our experience with IoT solutions",
        additional_metadata={"scenario": "ambiguous_intent", "expected_intent": Intent.AMBIGUOUS}
    ),
    Golden(
        input="Cloud solutions in Finance?",
        additional_metadata={"scenario": "ambiguous_intent", "expected_intent": Intent.AMBIGUOUS}
    )
]