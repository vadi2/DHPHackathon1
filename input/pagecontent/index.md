# Welcome to DHP Connectathon 1

### Overview

Welcome to the first Digital Health Platform (DHP) Connectathon! This event focuses on testing and integrating with two core components of the Uzbekistan health information system:

- **MSM (Metadata and Security Management)**: Understanding server capabilities and terminology services
- **MDM (Master Data Management)**: Working with healthcare master data including organizations, patients, and practitioners

Future connectathons will expand to additional DHP components as they become available for integration.

### What is FHIR?

FHIR (Fast Healthcare Interoperability Resources) is an international standard for exchanging healthcare information electronically. Think of it as a common language that allows different healthcare systems to communicate with each other.

Key concepts:
- **Resources**: Standardized data structures (Patient, Organization, Practitioner, etc.)
- **RESTful API**: Use standard HTTP methods (GET, POST, PUT, DELETE) to interact with data
- **Profiles**: Customizations of base FHIR resources for specific use cases (like uz-core profiles for Uzbekistan)
- **Terminology**: Standardized code systems and value sets for consistent data representation

Base URL for testing: `https://playground.dhp.uz/fhir`
- Note: This is a temporary URL that will be replaced closer to the connectathon

### What you'll learn

This connectathon will help you:

1. Register patients - Handle patient records with duplicate detection and matching
1. Manage organizations - Create, read, update, delete, and search healthcare organizations
1. Manage practitioners - Work with healthcare providers and their roles in organizations
1. Discover capabilities - Query what the server supports using CapabilityStatement
1. Use terminology services - Search and validate codes using CodeSystem, ValueSet, and ConceptMap

### Scenarios

We've prepared detailed scenarios to guide you through each integration task. Choose the order that best fits your application's needs:

#### [Patient Registration](patient-registration.html)
Handle patient records with proper identifiers (PINFL), duplicate detection, and matching logic.

Skills: Patient search and matching, duplicate detection, data quality

#### [Organization Management](organization-management.html)
Manage healthcare organizations and departments.

Skills: CRUD operations, search, references, identifiers, hierarchies

#### [Practitioner and PractitionerRole Management](practitioner-practitionerrole-management.html)
Work with healthcare providers and understand multi-resource relationships.

Skills: Managing related resources, organizational relationships, qualifications

#### [Discovering Server Capabilities](capability-discovery.html)
Learn how to query what the FHIR server supports.

Skills: Understanding CapabilityStatement, checking supported resources and operations

#### [Terminology Basics](terminology-basics.html)
Learn to work with medical coding systems and terminology services.

Skills: CodeSystem, ValueSet, ConceptMap, $expand, $validate-code, $lookup operations

### Prerequisites

Technical requirements:
- HTTP client or programming language of your choice (we provide examples in cURL, Python, JavaScript, Java, C#, and Go)
- JSON knowledge
- Basic understanding of RESTful APIs

No prior FHIR experience required - our scenarios are designed for beginners!

### What's next

This is the first of many connectathons. As the Digital Health Platform grows, future events will cover:
- Clinical data management (encounters, observations, diagnostic reports)
- Medication management
- Scheduling and appointments
- Laboratory and imaging integration
- Public health reporting
- And more...

Stay tuned for announcements as new components become available!

### Feedback and support

Your feedback is essential for improving DHP! Please share your experience:

- **Feedback form:** [Share your experience, issues, and successes](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing)
- Report issues, ask questions, and celebrate your integration successes

### Getting started

Ready to begin?

1. Choose the scenario most relevant to your integration needs from the list above
2. Test and integrate - use the playground server to test your implementation
3. Share feedback - help us improve for future connectathons!

### Useful links

- [FHIR R5 Documentation](http://hl7.org/fhir/R5/) - Official FHIR specification
- [uz-core Implementation Guide](https://dhp.uz/fhir/core/en/) - Uzbekistan-specific profiles and terminology
- [DHP Capability Statement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html) - What the server supports

Happy integrating!
