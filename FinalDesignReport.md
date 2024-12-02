# Final Design Report

## Our Team

| Contributor | Major | Email |
| -------- | ------- | --------- |
| Alex Gribble | BME | alexander.g.gribble@gmail.com |
| Grant Guernsey | CS | guernsgd@mail.uc.edu |
| Kyle Woods | EET | woods2ky@mail.uc.edu |
| Ricky Roberts | CS | roberrf@mail.uc.edu |
| Thaviska Gamage | CS | gamagetd@gmail.ud.edu |

| Advisor   | Email |
| -------- | ------- |
| Dr. Privetera (BME) | marybeth.privitera@uc.edu |

## Project Abstract

The Integrated Therapy Software aims to combat the global challenge of depression, affecting 280 million people. This innovative solution combines Cognitive Behavioral Therapy (CBT) techniques with guidance for building positive social connections. Our software features a four-stage growth model: Trust, Support, Connection, and Accountability, facilitating holistic treatment. By leveraging existing large language models through APIs, we enhance accessibility while addressing the critical need for social support in mental health treatment. This project highlights the potential of multi-disciplinary collaboration to develop effective solutions that empower individuals in their mental health journeys.

## User Stories and Design Diagrams

### User stories

1. As a person experiencing depressive symptoms, I want to build trust through communication with the therapy device, so that I may feel safe sharing my thoughts and feelings while trying to find judgement-free support.

2. As a user with depression, I want to receive guidance to additional help and resources, so I can attempt to find the method to help improve my mental health that best suits me and my current situation.

3. As a user wanting to better my mental health, I want to learn cognitive behavioral therapy techniques, so that I can identify my negative thought patterns and change them into positive ones.

4. As a frequent therapy device user, I want to keep track of improvements in my mental health or emotional state, so that I can feel motivated to continue improving my mental state by recognizing my progress.As a socially isolated user, I want to receive guidance on building healthy relationships, so that I can learn to develop supportive social connections and reduce my feelings of isolation.

5. As a socially isolated user, I want to receive guidance on building healthy relationships, so that I can learn to develop supportive social connections and reduce my feelings of isolation.

### Design Diagrams

Please **[CLICK HERE](https://github.com/thavishkagamage/Integrated-Therapy-Software/blob/main/Capstone%20Assignments/Assignment%20%234%20-%20Design%20Diagrams.pdf)** to view our design diagrams.

## Project Tasks and Timeline

### Front End Tasklist

| All Tasks | Responsibility |
| ----- | -------------- |
| Refine our product purpose and description to display on the homepage/landing page for user to understand the purpose of the product | Alex | 
| Research and define information about our target/potential user regarding behaviors, characteristics, peferences, and what they would benefit from most when using our product | Ricky, Alex |
| Research and Specify the front end framework to be used as the foundation of our web app | Ricky |
| Specify coding standards, rules and conventions to be used when developing the front end of the product | Ricky |
| Specify layout and architecture choices for front end components and overall UI/UX | Ricky, Grant |
| Create basic design mocks for the various pages and user states of our web app, using user research ad user stories when applicable | Ricky, Grant | 
| Develop seperate UI pages with ability to create and add components based on design mocks | Ricky, Grant | 
| Develop connections between front end and back end/database for profile, information, and LLM chat message transfer and retrieval | Ricky, Grant | 
| Develop user flows for a user to sign in/sign up and fetch data from back end or database | Ricky, Grant | 
| Research and develop the user chat interface that interacts with the LLM, including sending messages to the LLM, recievig responses from the LLM, and displaying previous messages and chat history | Ricky, Grant | 
| Research how to publicly host the site and make it indexable by Google | Grant | 


### Back End Taskist

| All Tasks | Responsibility |
| ----- | -------------- |
| **First**                                                                                |                                        |
| Decide a language (Python makes the most sense)                                          | Grant |
| Decide high level architecture and create class and relationship diagrams               | Grant |
| Communication with Frontend (receiving user data, sending LLM responses)                 |Grant, Ricky  |
| **LLM Tasks**                                                                            |                                        |
| Build the core conversational agent that will interact with users, providing responses based on cognitive behavioral therapy (CBT) techniques. This agent will guide users through therapeutic exercises and respond to inputs based on a pre-defined system of prompts. |Grant, Ricky|
| Create structured prompts for the LLM to follow during conversations with users, ensuring they align with therapeutic principles and the flow of therapy sessions. These prompts will guide the LLM's behavior to keep conversations on track with therapy goals. |Grant, Ricky, Alex|
| Implement RAG to provide more informed responses by fetching relevant information from a database of therapy-related materials. This will allow the chatbot to retrieve external content to enrich its answers with accurate and helpful therapy advice. | Grant, Ricky |
| Store users' previous interactions with the chatbot in a database, allowing the system to retrieve and reference past conversations. This enables the chatbot to remember user preferences, goals, and therapy progress for personalized sessions.| Ricky |
| **Non LLM Tasks**                                                                        |                                        |
| Preprocess user inputs to handle typos, ambiguous language, and inappropriate content. This may involve filtering, normalizing, or restructuring user messages to ensure they align with the LLM’s expected input format and improve response quality. | Grant, Ricky |
| Develop a safety evaluator to ensure that the chatbot's responses are aligned with ethical and therapeutic standards. This will involve defining rules that ensure the chatbot gives appropriate and safe advice, especially for sensitive topics in therapy. | Grant, Ricky |
| Implement a decision tree to track the user’s progress through the stages of Cognitive Behavioral Therapy (CBT). This system will help decide which therapy stage (e.g., identifying cognitive distortions, setting goals) the user is in and adjust the chatbot's responses accordingly. | Grant, Ricky |
| Allow users to set personal therapy goals (e.g., reducing anxiety, improving sleep), which will be integrated into the LLM’s decision-making process. This will make the therapy more personalized and goal-driven by allowing the LLM to tailor responses according to the user's progress. | Grant, Ricky |
| **Evaluation**                                                                           |                                        |
| Develop a system to evaluate the chatbot's effectiveness and user satisfaction. This will involve setting up key performance metrics, such as user feedback, progress tracking (towards CBT goals), and response accuracy, to measure how well the chatbot supports therapy sessions.  | Grant, Ricky, Alex  |

### Project Milestones
- **Collaboration Infrastructure Setup** (8/19 - 9/20)
- **Team Formation** (8/26 - 9/16)
- **Team Onboarding** (9/5 - 9/22)
- **Project Planning** (9/16 - 9/29)
- **Research** (9/16 - 11/1)
- **Requirements** (9/23 - 11/1)
- **System Architecture** (9/30 - 3/31)
- **User Interface** (9/30 - 3/31)
- **CBT System** (9/30 - 3/31)
- **Relationship Support System** (9/30 - 3/31)
- **Integration** (10/14 - 3/31)
- **Testing** (10/7 - 3/31)
- **Documentation** (9/2 - 1/3)
- **Administration** (9/9 - 4/30)

### Important Deadlines
- **Collaboration Infrastructure Setup** (8/19 - 9/20)
- **Team Onboarding** (9/5 - 9/22)
- **Research** (9/16 - 11/1)
- **Requirements** (9/23 - 11/1)
- **Integration** (10/14 - 3/31)

### Effort Matrix

| Task                           | Thavishka Gamage   | Alex Gribble   | Grant Guernsey   | Richard Roberts   | Kyle Woods     | Total Effort     | Primary Responsibility   |
|:-------------------------------|:-------------------|:---------------|:-----------------|:------------------|:---------------|:-----------------|:-------------------------|
| Requirements Gathering         | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Thavishka Gamage         |
| System Architecture Design     | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Alex Gribble             |
| Front-End UI Design            | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Grant Guernsey           |
| Back-End Development           | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Richard Roberts          |
| Data Integration & API Setup   | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Kyle Woods               |
| Testing & Debugging            | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Grant Guernsey           |
| Documentation & Report Writing | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Thavishka Gamage         |
| Presentation Preparation       | 20% (or 3 hrs)     | 20% (or 3 hrs) | 20% (or 3 hrs)   | 20% (or 3 hrs)    | 20% (or 3 hrs) | 15 hrs (or 100%) | Richard Roberts          |
| Ethical Decision Making        | 20% (or 3 hrs)     | 20% (or 3 hrs) | 20% (or 3 hrs)   | 20% (or 3 hrs)    | 20% (or 3 hrs) | 15 hrs (or 100%) | Alex Gribble             |
| Prototype Iteration & Testing  | 20% (or 5 hrs)     | 20% (or 5 hrs) | 20% (or 5 hrs)   | 20% (or 5 hrs)    | 20% (or 5 hrs) | 25 hrs (or 100%) | Kyle Woods               |

## ABET Concerns

### Security

One major constraint of our project is security due to the private information that our users will share with the LLM used in our product. This will require us to include more security measures into our product to ensure that the user’s private information cannot be seen or accessed by anyone else. We will need to create a secure sign-in for the user, including two factor authentication to verify a user’s identity before allowing them to view previous messages or information. We will also need to verify that our database is set up correctly to ensure our user’s information and our product is not at risk of viruses or attacks like SQL injections. 

### Ethical

Another constraint of our product will be the ethical aspects of our products responses to the user. Since our project will use an LLM, we need to be certain that there is no possibility that the model’s response can contain words that promote unhealthy thoughts, self-harm, or other sentences that could negatively affect the user. We will need to take significant amounts of time to tailor and add guiderails to the LLM so that its responses will have positive words and messages. We will do extensive testing as well as likely include response feedback options that can allow our users to help filter out potentially negative or harmful responses. 

### Professional

Another constraint of our product is the specialized knowledge of cognitive behavioral therapy and LLMs. Our finalized product will be able to take a user through the many stages of CBT effectively using a mix of static forms and conversation with the LLM. We will need to first do extensive documented research of the CBT process and how we can best implement its individual stages, as well as research and experimentation with the LLM that will successfully take a use that CBT process. We may need to reach out to professionals with experience in either of these areas to help the implementations of these two components work correctly. 

## Fall Design Presentation

Please **[CLICK HERE](https://docs.google.com/presentation/d/1cSRtU_0y11EwSb63RB_woNr8MLVxLAPDgQR824egSgI/edit#slide=id.g3015c05c7d6_0_58)** to view our Fall Design Presentation

## Self Assessment Essays
- **[Ricky Roberts](https://github.com/thavishkagamage/Integrated-Therapy-Software/blob/main/Capstone%20Assignments/Individual_Capstone_Assessment_Richard_Roberts.pdf)**
- **[Grant Guernsey](https://github.com/thavishkagamage/Integrated-Therapy-Software/blob/main/Capstone%20Assignments/Individual%20Capstone%20Assessment%20Grant%20Guernsey.docx)**
-  **[Thavishka Gamage - Self Assessment](https://github.com/thavishkagamage/Integrated-Therapy-Software/blob/main/Capstone%20Assignments/Thavishka%20Gamage%20Resume.md)**

## Professional Bibliographies

- **[Ricky Roberts](https://github.com/thavishkagamage/Integrated-Therapy-Software/blob/main/Capstone%20Assignments/roberrf.md)**
- **[Grant Guernsey](https://github.com/thavishkagamage/Integrated-Therapy-Software/blob/main/Capstone%20Assignments/professionalBibGrantGuernsey.md)**
- - **[Thavishka Gamage - Self Assessment](https://github.com/thavishkagamage/Integrated-Therapy-Software/blob/main/Capstone%20Assignments/Thavishka%20Gamage%20Individual%20Capstone%20Assessment.pdf)**
## Budget

| Expense   | Cost To-Date |
| -------- | ------- |
| OpenAI API Key | $5 |

## Appendix

- Visit our [project root](https://github.com/thavishkagamage/Integrated-Therapy-Software/tree/main/cbt_chatbot) to learn how to locally run and test our project

- View our [team Miro board](https://miro.com/app/board/uXjVKmxq8sQ=/?share_link_id=588768285443) to see various diagrams, planning, and prototypes

- This is each of our team members' predicted weekly commitment (based on the beginning of the semester) and our actual commitment hours. These hours can be justified for everyone other than Alex within the Miro board and the git repo.
-  ![image](https://github.com/user-attachments/assets/d7d08d2b-dfef-45b8-a140-85c48eff8205)

- Add Coda Links Here
