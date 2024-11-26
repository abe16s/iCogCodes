# 1. Daily Motivation Bot

This simple Python app uses the Google Gemini API to generate motivational messages based on the user's mood. The app prompts the user to enter their mood (e.g., "happy", "stressed", "unmotivated"), and then it sends a request to the Gemini API by using LangChain framework, which responds with a customized motivational message. 


# 2. Legal Review App

The Legal Document Review App provides a convenient way to analyze legal documents (e.g., Terms and Conditions, Privacy Policies, Contracts) using advanced natural language processing (NLP) techniques. By leveraging Google Gemini's generative capabilities, the app can extract and summarize key clauses related to privacy, liability, payment, and other crucial terms. It can also highlight risky clauses, such as automatic renewals or arbitration terms, that are often overlooked by users when agreeing to legal documents.

The application utilizes LangChain, a powerful framework for building applications with large language models (LLMs), to streamline the process of document analysis. With LangChain's flexibility, the app is able to integrate various LLMs (like Google Gemini) into workflows for efficient clause extraction, summarization, and risk detection. LangChain helps manage the document processing pipeline.

* Document Upload: Allows users to upload legal documents in PDF, DOCX, or text format.
* Clause Extraction: Automatically identifies and summarizes key clauses related to privacy, liability, payment, and other important legal aspects.
* Risk Clause Detection: Detects potentially risky clauses (e.g., automatic renewal, data collection, arbitration clauses) to help users make more informed decisions.
* Gemini-Powered Analysis: Utilizes Google Gemini's generative language model to extract relevant clauses and generate summaries from legal text.
* Simple UI Integration: A simple Flask web interface for uploading documents, viewing analysis, and interacting with the results.

***Change Your API Key***: Before running the app, don't forget to replace your_gemini_api_key with your actual Gemini API key in the script. Create a .env file in the root LangChain directory GEMINI_API_KEY=your_key