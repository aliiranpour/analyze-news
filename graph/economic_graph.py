from langgraph.graph import StateGraph, END
from models.news_types import NewsState
from graph.nodes.load_cache import load_cache
from graph.nodes.fetch_rss import fetch_rss
from graph.nodes.fetch_news import fetch_news
from graph.nodes.summarize import summarize
from graph.nodes.analyze import analyze_impact
from graph.nodes.print_cache import print_cache
from graph.nodes.save_cache import save_cache
from graph.nodes.fetch_symbols import fetch_symbols
from graph.nodes.filter_symbols import find_symbols

def run_pipeline_graph() -> NewsState:
    """
    ساخت و اجرای گراف پردازش اخبار اقتصادی
    """
    builder = StateGraph(dict)
    
    builder.add_node("FetchSymbols", fetch_symbols)
    builder.add_node("FilterSymbols", find_symbols)
    builder.add_node("LoadCache", load_cache)
    builder.add_node("FetchRSS", fetch_rss)
    builder.add_node("FetchNews", fetch_news)
    builder.add_node("Summarize", summarize)
    builder.add_node("Analyze", analyze_impact)
    builder.add_node("PrintCache", print_cache)
    builder.add_node("SaveCache", save_cache)

    builder.set_entry_point("FetchSymbols")
    builder.add_edge("FetchSymbols", "LoadCache")
    builder.add_edge("LoadCache", "FetchRSS")
    builder.add_edge("FetchRSS", "FetchNews")
    builder.add_edge("FetchNews", "Summarize")
    builder.add_edge("Summarize", "FilterSymbols")
    builder.add_edge("FilterSymbols", "Analyze")
    builder.add_edge("Analyze", "SaveCache")
    builder.add_edge("SaveCache", "PrintCache")
    builder.add_edge("PrintCache", END)

    # init_state: NewsState = {
    #     "symbols": [],
    #     "valid_symbol_names": [],
    #     "links": [],
    #     "articles": [],
    #     "summaries": [],
    #     "cache": {}
    # }

    init_state: NewsState = {
        "symbols": [],
        "valid_symbol_names": [],
        "links": [],
        "articles": [],
        "cache": {}
    }
    
    print("=== DEBUG: گراف آماده اجراست ===")

    final_state = builder.compile().invoke(init_state)
    
    print(">>> Final state keys:", final_state.keys())

    return final_state

