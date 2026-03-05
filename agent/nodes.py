import json
from agent.state import ResearchState
from agent.react_agent import react_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def research_node(state):
    logs = list(state.get("logs", []))
    errors = list(state.get("errors", []))
    try:
        logs.append("[Research] Starting")
        msg = "Research " + state["company_name"] + " with: " + json.dumps(state["research_bundle"])
        result = react_agent.invoke({"messages": [HumanMessage(content=msg)]})
        findings = {"full_analysis": result["messages"][-1].content}
        logs.append("[Research] Completed")
        return {"react_findings": findings, "logs": logs, "errors": errors}
    except Exception as e:
        errors.append("[Research] ERROR: " + str(e))
        return {"react_findings": {}, "logs": logs, "errors": errors}

def rag_node(state):
    logs = list(state.get("logs", []))
    errors = list(state.get("errors", []))
    try:
        logs.append("[RAG] Starting")
        from rag.retriever import retrieve
        chunks = retrieve(state["company_name"] + " competitive analysis")
        logs.append("[RAG] Retrieved " + str(len(chunks)) + " chunks")
        return {"retrieved_guidance": chunks, "logs": logs, "errors": errors}
    except Exception as e:
        errors.append("[RAG] ERROR: " + str(e))
        return {"retrieved_guidance": [], "logs": logs, "errors": errors}

def synthesis_node(state):
    logs = list(state.get("logs", []))
    errors = list(state.get("errors", []))
    try:
        logs.append("[Synthesis] Starting")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        findings = state.get("react_findings", {})
        guidance = state.get("retrieved_guidance", [])
        prompt = "Synthesize this research: " + json.dumps(findings) + " Guidance: " + " ".join(guidance)
        result = llm.invoke(prompt)
        logs.append("[Synthesis] Completed")
        return {"react_findings": {**findings, "synthesis": result.content}, "logs": logs, "errors": errors}
    except Exception as e:
        errors.append("[Synthesis] ERROR: " + str(e))
        return {"logs": logs, "errors": errors}

def report_node(state):
    logs = list(state.get("logs", []))
    errors = list(state.get("errors", []))
    try:
        logs.append("[Report] Starting")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        company = state["company_name"]
        findings = state.get("react_findings", {})
        bundle = state.get("research_bundle", {})
        prompt = "You are a professional financial analyst. Create a detailed Markdown report for " + company + ". Use ONLY the real data provided. REAL API DATA: " + json.dumps(bundle) + " AGENT ANALYSIS: " + json.dumps(findings) + " Write with sections: ## Executive Summary ## Financial Overview ## Recent News & Sentiment ## Competitive Landscape ## Market Position ## Strategic Assessment. Include key risks and strategic recommendations."
        result = llm.invoke(prompt)
        logs.append("[Report] Completed")
        return {"draft_report": result.content, "logs": logs, "errors": errors}
    except Exception as e:
        errors.append("[Report] ERROR: " + str(e))
        return {"draft_report": "", "logs": logs, "errors": errors}

def validation_node(state):
    logs = list(state.get("logs", []))
    errors = list(state.get("errors", []))
    try:
        logs.append("[Validation] Starting")
        report = state.get("draft_report", "")
        required = ["## Executive Summary", "## Financial Overview", "## Recent News & Sentiment", "## Competitive Landscape", "## Market Position", "## Strategic Assessment"]
        missing = [s for s in required if s not in report]
        if missing or len(report.split()) < 300:
            logs.append("[Validation] FAIL")
            return {"validation_flag": False, "retry_count": state.get("retry_count", 0) + 1, "logs": logs, "errors": errors}
        logs.append("[Validation] PASS")
        return {"validation_flag": True, "logs": logs, "errors": errors}
    except Exception as e:
        errors.append("[Validation] ERROR: " + str(e))
        return {"validation_flag": False, "logs": logs, "errors": errors}
