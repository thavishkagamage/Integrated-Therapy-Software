
# Task List

## Front End Tasks

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


## Back End Tasks

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
