from deepeval.dataset import Golden

from app.models.constants import Intent

dataset = [
    Golden(
        input="Can you summarize case studies in the Healthcare sector, specifically regarding patient monitoring and data management?",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="Find case studies where we used 'IoT'",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="Give me an overview of case studies that focus on how we've used data visualization and dashboards to improve business decision-making.",
        additional_metadata={"scenario": "case_study_sum", "expected_intent": Intent.CASE_STUDY_RETRIEVAL}
    ),
    Golden(
        input="Summarize case studies that involve a mix of hardware design and custom software integration.",
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
        input="Summarize case studies that involve Power BI and dashboards.",
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
        input="Show me details about AI chatbot projects that use a Deep Learning Model and NoSQL. I need a solution that focuses on Automated customer replies and Query escalation routing, specifically involving Conversational Design, ML Training, and Customer Engagement services.",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="I am searching for a project that utilizes an Urban Sensor Array and a Data Broker connected to Secure Cloud Systems. The project must demonstrate capabilities in Traffic flow monitoring, Incident capture, and Resource allocation, while offering services such as Urban Analytics, Cloud Filing, and Incident Reporting",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="Can you find a management platform built with a Javascript Framework and NoSQL data store? We specifically need a solution that offers Inventory monitoring dashboards, Customer pattern tracking, and Automated sales analytics, including Business Modeling services.",
        additional_metadata={"scenario": "project_match", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="I am interested in frontend projects?",
         additional_metadata={"scenario": "no_results", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="I am looking for information on AI projects",
        additional_metadata={"scenario": "no_results", "expected_intent": Intent.PROJECT_MATCHING}
    ),
    Golden(
        input="I need to find engineers who are experts in Embedded Sensing and IoT Gateways for a new build.",
        additional_metadata={"scenario": "ambiguous_intent", "expected_intent": Intent.AMBIGUOUS}
    ),
    Golden(
        input="What can you tell me about your capabilities with Deep Learning Models and NoSQL data stores?",
        additional_metadata={"scenario": "ambiguous_intent", "expected_intent": Intent.AMBIGUOUS}
    )
]