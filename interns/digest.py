"""
Digest and compression module for intern research
Takes raw web results and compresses them into useful context
"""


def digest_web_results(results, max_findings=3):
    """
    Compress web search results into digestible findings
    
    Args:
        results: List of search results from web search
        max_findings: Maximum number of findings to return
    
    Returns:
        List of compressed, useful findings
    """
    findings = []
    
    for result in results[:max_findings]:
        title = result.get('title', '')
        snippet = result.get('body', '')
        url = result.get('href', '')
        
        if title and snippet:
            # Compress: Take title + first 150 chars of snippet
            compressed = {
                "title": title,
                "snippet": snippet[:150] + "..." if len(snippet) > 150 else snippet,
                "url": url,
                "relevance": "high"  # Could add relevance scoring later
            }
            findings.append(compressed)
    
    return findings


def format_findings_for_host(findings, intern_name, topic):
    """
    Format digested findings into a brief for the host
    
    Args:
        findings: List of digested findings
        intern_name: Name of the intern
        topic: Topic being researched
    
    Returns:
        Formatted string for host consumption
    """
    if not findings:
        return [f"No substantial information found on '{topic}'"]
    
    formatted = []
    
    for i, finding in enumerate(findings, 1):
        title = finding.get('title', 'Unknown')
        snippet = finding.get('snippet', '')
        
        # Create compact, informative finding
        formatted_finding = f"{title}: {snippet}"
        formatted.append(formatted_finding)
    
    return formatted


def extract_key_facts(text, max_facts=3):
    """
    Extract key facts from text
    This is a simple version - could be enhanced with NLP
    
    Args:
        text: Text to extract facts from
        max_facts: Maximum number of facts to extract
    
    Returns:
        List of key facts
    """
    # Simple sentence splitting for now
    sentences = text.split('.')
    facts = []
    
    for sentence in sentences[:max_facts]:
        sentence = sentence.strip()
        if len(sentence) > 20:  # Skip very short fragments
            facts.append(sentence)
    
    return facts
