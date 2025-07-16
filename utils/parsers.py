import re

def extract_section(text: str, section_header: str) -> str:
    pattern = r"{}:\s*(\[.*?\]|\S+)".format(re.escape(section_header))
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""

def parse_list(text: str) -> list:
    if not text:
        return []   
    text = re.sub(r'[\[\]]', '', text)
    return [item.strip() for item in re.split(r'[,،]|\s+و\s+', text) if item.strip()]

def parse_impact(text: str) -> str:
    if not text:
        return "خنثی"
    text = text.lower()
    if 'مثبت' in text: return 'مثبت'
    if 'منفی' in text: return 'منفی'
    return 'خنثی'


def parse_symbols(summary_output: str) -> list:
    for line in summary_output.split('\n'):
        if line.startswith("نمادها:"):
            symbols_str = line.split(":", 1)[1].strip()
            return [s.strip(" '\"[]") for s in symbols_str.split(",")]
    return []
def extract_impact_section(text: str) -> str:
    # به دنبال "تاثیر: مثبت" یا "تاثیر : منفی" در هر جای متن می‌گردد
    match = re.search(r"تأثیر\s*[:：]?\s*(مثبت|منفی|خنثی)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""