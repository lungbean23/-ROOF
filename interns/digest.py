"""
Enhanced Digest and compression module for intern research
Takes raw web results and extracts USEFUL, CITABLE information

Philosophy:
- Hosts need FACTS they can cite, not just titles
- Extract claims, statistics, dates, names
- Attribute to sources properly
- Make it actionable
"""

import re


def digest_web_results(results, max_findings=3):
    """
    Enhanced digest that extracts actual useful information
    
    Args:
        results: List of search results from web search
        max_findings: Maximum number of findings to return
    
    Returns:
        List of enriched findings with actionable content
    """
    findings = []
    
    for result in results[:max_findings]:
        title = result.get('title', '')
        snippet = result.get('body', '')
        url = result.get('href', '')
        
        if title and snippet:
            # Extract enriched content
            enriched = _extract_key_information(title, snippet, url)
            
            if enriched:
                findings.append(enriched)
    
    return findings


def _extract_key_information(title, snippet, url):
    """
    Extract actionable information from title and snippet
    
    Looks for:
    - Statistics and numbers
    - Dates and timeframes
    - Claims and assertions
    - Proper nouns (people, places, organizations)
    - Key facts
    
    Returns enriched finding dict
    """
    # Extract statistics (percentages, large numbers)
    stats = _extract_statistics(snippet)
    
    # Extract dates/years
    dates = _extract_dates(snippet)
    
    # Extract proper nouns (potential sources/experts)
    sources = _extract_sources(title, snippet)
    
    # Build enriched snippet
    enriched_snippet = snippet[:200]
    
    # Enhance with extracted metadata
    metadata = []
    if stats:
        metadata.append(f"Data: {', '.join(stats[:2])}")
    if dates:
        metadata.append(f"Timeframe: {dates[0]}")
    if sources:
        metadata.append(f"Source: {sources[0]}")
    
    # Create source attribution
    source_name = _extract_source_name(url, title)
    
    return {
        "title": title,
        "snippet": enriched_snippet,
        "url": url,
        "source": source_name,
        "statistics": stats[:3],  # Top 3 stats
        "dates": dates[:2],       # Top 2 dates
        "has_data": bool(stats or dates),
        "relevance": "high"
    }


def _extract_statistics(text):
    """Extract percentages and numerical statistics from text"""
    stats = []
    
    # Find percentages
    percentages = re.findall(r'\b\d+(?:\.\d+)?%', text)
    stats.extend(percentages)
    
    # Find large numbers with context (millions, billions, thousands)
    large_numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand|trillion)', text, re.IGNORECASE)
    stats.extend(large_numbers)
    
    # Find dollar amounts
    dollar_amounts = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:million|billion|thousand|trillion))?', text, re.IGNORECASE)
    stats.extend(dollar_amounts)
    
    return stats[:5]  # Top 5 stats


def _extract_dates(text):
    """Extract years and dates from text"""
    dates = []
    
    # Find 4-digit years (2020-2030)
    years = re.findall(r'\b20[12]\d\b', text)
    dates.extend(years)
    
    # Find month-year combinations
    month_years = re.findall(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+20[12]\d\b', text, re.IGNORECASE)
    dates.extend(month_years)
    
    return dates[:3]  # Top 3 dates


def _extract_sources(title, snippet):
    """Extract potential source attributions (experts, organizations, studies)"""
    sources = []
    
    # Look for "according to X"
    according_to = re.findall(r'according to ([^,\.]+)', snippet, re.IGNORECASE)
    sources.extend(according_to)
    
    # Look for study/research mentions
    studies = re.findall(r'(?:study|research|report|survey|analysis)\s+(?:by|from)\s+([^,\.]+)', snippet, re.IGNORECASE)
    sources.extend(studies)
    
    # Look for expert quotes
    experts = re.findall(r'([A-Z][a-z]+\s+[A-Z][a-z]+),\s+(?:a|an|the)\s+(?:professor|researcher|expert|analyst|CEO|director)', snippet)
    sources.extend(experts)
    
    return sources[:2]  # Top 2 sources


def _extract_source_name(url, title):
    """Extract clean source name from URL or title"""
    # Try to get domain name
    domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if domain_match:
        domain = domain_match.group(1)
        # Clean up domain (remove .com, .org, etc)
        clean_domain = re.sub(r'\.(com|org|net|edu|gov|io|co\.uk)$', '', domain, flags=re.IGNORECASE)
        # Capitalize first letter of each word
        return clean_domain.replace('-', ' ').replace('_', ' ').title()
    
    # Fallback: extract from title
    if ':' in title:
        return title.split(':')[0].strip()
    
    return "Web Source"


def format_findings_for_host(findings, intern_name, topic):
    """
    Format digested findings into citable briefs for the host
    
    Focus on making findings:
    - Citable (clear source attribution)
    - Actionable (contains specific facts/data)
    - Contextual (when/where/who information)
    
    Args:
        findings: List of digested findings
        intern_name: Name of the intern
        topic: Topic being researched
    
    Returns:
        List of formatted strings ready for host consumption
    """
    if not findings:
        return [f"No substantial information found on '{topic}'"]
    
    formatted = []
    
    for finding in findings:
        # Build a rich, citable finding
        source = finding.get('source', 'Unknown')
        title = finding.get('title', '')
        snippet = finding.get('snippet', '')
        stats = finding.get('statistics', [])
        dates = finding.get('dates', [])
        
        # Create formatted finding with attribution and data
        parts = [source]
        
        # Add date context if available
        if dates:
            parts.append(f"({dates[0]})")
        
        # Add key stats if available
        if stats:
            parts.append(f"reports {stats[0]}")
        
        # Add snippet content
        if snippet:
            # Clean up snippet
            clean_snippet = snippet.strip()
            # Limit to first sentence or 150 chars
            if '.' in clean_snippet:
                clean_snippet = clean_snippet.split('.')[0] + '.'
            else:
                clean_snippet = clean_snippet[:150] + '...'
            
            parts.append(f"- {clean_snippet}")
        
        # Combine into formatted finding
        formatted_finding = ' '.join(parts)
        formatted.append(formatted_finding)
    
    return formatted


def extract_key_facts(text, max_facts=3):
    """
    Extract key facts from text
    Enhanced with pattern recognition
    
    Args:
        text: Text to extract facts from
        max_facts: Maximum number of facts to extract
    
    Returns:
        List of key facts
    """
    facts = []
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    
    # Prioritize sentences with:
    # - Numbers/statistics
    # - Dates
    # - "According to" attributions
    # - Superlatives (first, largest, best, most)
    
    scored_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:  # Skip very short fragments
            continue
        
        score = 0
        
        # Has numbers?
        if re.search(r'\d+', sentence):
            score += 2
        
        # Has dates?
        if re.search(r'\b20[12]\d\b', sentence):
            score += 2
        
        # Has attribution?
        if re.search(r'according to|study|research|report', sentence, re.IGNORECASE):
            score += 3
        
        # Has superlatives?
        if re.search(r'\b(?:first|largest|biggest|best|most|top|leading)\b', sentence, re.IGNORECASE):
            score += 1
        
        scored_sentences.append((score, sentence))
    
    # Sort by score and take top facts
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    facts = [sent for score, sent in scored_sentences[:max_facts] if score > 0]
    
    return facts
