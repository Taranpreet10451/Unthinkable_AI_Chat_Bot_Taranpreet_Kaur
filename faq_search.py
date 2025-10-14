import pandas as pd
import re
from config import FAQ_DATASET_PATH, FAQ_SEARCH_THRESHOLD, FAQ_DATASET_ENCODING

class FAQSearch:
    """
    FAQ search functionality to find relevant answers from the dataset.
    """
    
    def __init__(self):
        """Initialize FAQ search by loading the dataset."""
        self.faq_data = self.load_faq_data()
    
    def load_faq_data(self):
        """
        Load FAQ data from CSV file.
        
        Returns:
            pandas.DataFrame: FAQ dataset
        """
        try:
            df = pd.read_csv(FAQ_DATASET_PATH, encoding=FAQ_DATASET_ENCODING)
            print(f"Loaded {len(df)} FAQs from {FAQ_DATASET_PATH}")
            return df
        except FileNotFoundError:
            print(f"FAQ dataset not found at {FAQ_DATASET_PATH}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading FAQ data: {e}")
            return pd.DataFrame()
    
    def search_faq(self, query):
        """
        Search for relevant FAQ based on user query.
        
        Args:
            query (str): User's question/query
            
        Returns:
            str: FAQ answer if found, empty string otherwise
        """
        if self.faq_data.empty:
            return ""

        query_lower = (query or "").lower().strip()

        # Intent shortcut: requests to talk to a human/agent/representative
        human_terms = {"human", "agent", "representative", "person", "someone"}
        wants_human = any(t in query_lower for t in [
            "talk to a human",
            "human agent",
            "talk to human",
            "human support",
            "human representative",
            "real person",
            "speak to a person",
            "speak to someone",
        ]) or ("human" in query_lower and ("agent" in query_lower or "person" in query_lower or "representative" in query_lower))

        if wants_human:
            # Prefer explicit contact FAQs
            for _, row in self.faq_data.iterrows():
                q = str(row.get('question', '')).lower()
                if ("contact" in q and ("support" in q or "customer service" in q)) or ("technical support" in q):
                    return row.get('answer', '')
            # Fallback: return any customer service or support contact answer
            for _, row in self.faq_data.iterrows():
                q = str(row.get('question', '')).lower()
                if "support" in q or "customer service" in q:
                    return row.get('answer', '')
            return "You can reach technical support by emailing tech@unthinkable.com or calling our support line at 1-800-SUPPORT."

        # Tokenize utility
        def tokenize(text):
            return set(re.findall(r"[a-z0-9]+", str(text).lower()))

        query_tokens = tokenize(query_lower)
        best_match = None
        best_score = 0.0

        for _, row in self.faq_data.iterrows():
            question_tokens = tokenize(row.get('question', ''))
            keywords_tokens = tokenize(row.get('keywords', '')) if 'keywords' in row else set()

            # Score exact token overlaps; avoid substring-based scoring to reduce false positives
            question_overlap = len(query_tokens & question_tokens)
            keywords_overlap = len(query_tokens & keywords_tokens)

            score = question_overlap * 3.0 + keywords_overlap * 2.0

            if score > best_score:
                best_score = score
                best_match = row

        try:
            threshold = float(FAQ_SEARCH_THRESHOLD)
        except Exception:
            threshold = 3.0

        if best_match is not None and best_score >= threshold:
            return best_match.get('answer', '')

        return ""
    
    def get_all_faqs(self):
        """
        Get all FAQ entries.
        
        Returns:
            list: List of FAQ dictionaries
        """
        if self.faq_data.empty:
            return []
        
        return self.faq_data.to_dict('records')
