Plan: Integrated RAG Chatbot
The Plan structures the implementation, decomposing the complex RAG system into traceable, sequential milestones (M) and discrete tasks (T). This plan ensures that the critical requirement of Constrained QA (answering questions using only user-selected text) is addressed by architecting distinct handling paths within the Agent orchestration logic (T2.3, T2.4).   

I. Project Milestones and Task Decomposition
Milestone	Description	Key Tasks (T)	Traceability
M1: Core Backend & Data Layer	Establish secure, scalable infrastructure, persistent storage, and the offline indexing utility.	
T1.1: Configure FastAPI (Poetry, Uvicorn) and basic API structure (e.g., /health).  T1.2: Implement SQLModel schema for Session/Metadata in Neon Postgres using psycopg[binary].  T1.3: Configure database engine with pooled connection, sslmode=require, and pool_recycle=300 seconds.  T1.4: Develop Qdrant Indexing Utility: Chunk textbook content, generate embeddings (OpenAI), and ingest into Qdrant using payload filtering metadata (document_id).  T1.5: Configure serverless secrets integration: Create SSM Parameter Store secret for the Neon connection string and reference its ARN in apprunner.yaml. 

Constitution 3.1, 3.2, 3.3, 3.4
M2: Agent Orchestration & Logic	Implement the core RAG logic using the OpenAI Agents SDK, defining tools and prompt strategies for both General and Constrained QA.	
T2.1: Define Agent core configuration, including the global system prompt enforcing zero-hallucination.  T2.2: Implement General_Retrieval_Tool: Tool that queries Qdrant, dynamically applying document_id payload filter for search, and returns top-K results.  T2.3: Implement Strict_Context_Tool: Tool that receives raw user-selected text and passes it directly to the LLM as context, bypassing Qdrant search.  T2.4: Implement Agent conditional logic to prioritize and select the Strict_Context_Tool if a selected_context payload is received via the API request.  T2.5: Design and implement two primary FastAPI endpoints: /api/qa/general and /api/qa/constrained, mapping each to the appropriate Agent tool execution. 

Constitution 1.1, 1.2, 2.1, 3.1
M3: Frontend Integration & Deployment	Develop the custom Docusaurus component, implement client-side capture logic, and finalize secure serverless deployment.	
T3.1: Create custom React component (<RAGChatbot>) and embed it into Docusaurus MDX files using JSX syntax.  T3.2: Implement client-side getSelectionText() function using window.getSelection().toString().  T3.3: Integrate selection capture logic using document.onmouseup or document.onselectionchange listeners.  T3.4: Wrap the custom component in Docusaurus <BrowserOnly> to ensure execution only in the client browser environment.  T3.5: Implement secure asynchronous POST request from the Docusaurus component to the FastAPI /api/qa/constrained endpoint, transmitting the query and selected text.  T3.6: Finalize AWS App Runner deployment configuration using the apprunner.yaml and the dedicated IAM role for SSM access. 

Constitution 3.5, 3.6, 2.1
  
II. Detailed Task Breakdown: Critical Path
A. T1.3: Neon Connection Management
The database engine must be configured to handle the serverless environment lifecycle, directly addressing Principle 3.2 from the Constitution.

Action: When initializing the SQLAlchemy engine (via SQLModel), the following parameters must be strictly applied to the connection URL (using postgresql+psycopg driver):

connect_args={"sslmode": "require"}: Ensures secure connection.

pool_recycle=300: Forces connection recycling every 5 minutes (300 seconds), preempting connection failures caused by Neon's default compute auto-suspend feature.   

B. T2.4 & T2.5: Agent Orchestration for Dual QA Modes
The Agent SDK must be the central router, ensuring that the Constrained QA requirement is handled without involving the latency-inducing retrieval step.

QA Mode	FastAPI Endpoint	Agent Action	Tool Selection	Prompt Strategy
General RAG	/api/qa/general	Standard execution path.	General_Retrieval_Tool (Qdrant Search)	Standard RAG Prompt: Context is retrieved text.
Constrained QA	/api/qa/constrained	Execution path triggered by selected text.	Prioritized: Strict_Context_Tool	
Constraint-Based Prompt: Context is only the user-selected text; instruction mandates strict adherence. 

  
C. T3.4: Docusaurus Browser Integration
The client-side React component must be correctly packaged to function within the static site generator's environment.

Action: The <RAGChatbot> component and its event listeners (document.onmouseup, window.getSelection()) must be nested within the Docusaurus <BrowserOnly> component. This ensures that browser-specific JavaScript APIs are only accessed after the React application has hydrated on the client, preventing Node.js-based build failures.   

