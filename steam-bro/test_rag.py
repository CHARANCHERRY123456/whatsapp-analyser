import os
import sys
from datetime import datetime
from preprocessor import preprocess
from rag_src.main import RAG

# Debug logging helper
def log(step, message, data=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{step}] {message}")
    if data is not None:
        if isinstance(data, (list, tuple)):
            print(f"  └─ Count: {len(data)}")
            if len(data) > 0 and len(data) <= 5:
                print(f"  └─ Sample: {data[:3]}")
        elif isinstance(data, dict):
            print(f"  └─ Keys: {list(data.keys())}")
        else:
            print(f"  └─ Value: {data}")

CHAT_PATH = "../WhatsApp Chat with Insomniacs.txt"

def build_rag():
    log("INIT", "Starting RAG pipeline initialization...")
    
    # Step 1: Read file
    log("FILE", f"Reading chat file: {CHAT_PATH}")
    try:
        with open(CHAT_PATH, "r", encoding="utf-8") as f:
            raw = f.read()
        log("FILE", f"File read successfully", {"size_bytes": len(raw), "size_chars": len(raw)})
    except FileNotFoundError:
        log("ERROR", f"File not found: {CHAT_PATH}")
        log("ERROR", f"Current working directory: {os.getcwd()}")
        log("ERROR", f"Looking for file at: {os.path.abspath(CHAT_PATH)}")
        sys.exit(1)
    except Exception as e:
        log("ERROR", f"Error reading file: {e}")
        sys.exit(1)
    
    # Step 2: Preprocess
    log("PREPROCESS", "Starting preprocessing...")
    try:
        df = preprocess(raw)
        log("PREPROCESS", "Preprocessing completed", {
            "total_messages": len(df),
            "unique_users": df["user"].nunique(),
            "date_range": f"{df['date'].min()} to {df['date'].max()}"
        })
        log("PREPROCESS", f"Users found: {df['user'].unique().tolist()}")
    except Exception as e:
        log("ERROR", f"Error in preprocessing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 3: Prepare data for RAG
    log("DATA_PREP", "Preparing data tuples for RAG...")
    try:
        data = list(zip(df["user"].to_list(), df["message"].to_list(), df["date"].to_list()))
        log("DATA_PREP", f"Data prepared", {"total_tuples": len(data)})
        if len(data) > 0:
            log("DATA_PREP", f"Sample tuple: {data[0]}")
    except Exception as e:
        log("ERROR", f"Error preparing data: {e}")
        sys.exit(1)
    
    # Step 4: Initialize RAG
    log("RAG_INIT", "Initializing RAG system...")
    try:
        rag = RAG(data)
        log("RAG_INIT", "RAG initialization completed successfully!")
        return rag
    except Exception as e:
        log("ERROR", f"Error initializing RAG: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    print("=" * 60)
    print("WhatsApp Chat RAG Tester")
    print("=" * 60)
    
    rag = build_rag()
    
    print("\n" + "=" * 60)
    log("READY", "RAG system is ready!")
    log("READY", "Type your questions below (empty line to exit)")
    print("=" * 60 + "\n")
    
    query_count = 0
    while True:
        try:
            q = input("Q: ").strip()
            if not q:
                log("EXIT", "Exiting...")
                break
            
            query_count += 1
            log("QUERY", f"Processing query #{query_count}", {"query": q})
            
            start_time = datetime.now()
            ans = rag.ask_query(q)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            log("RESPONSE", f"Query completed in {duration:.2f}s")
            print("\n" + "─" * 60)
            print("A:", ans)
            print("─" * 60 + "\n")
            
        except KeyboardInterrupt:
            log("EXIT", "Interrupted by user")
            break
        except Exception as e:
            log("ERROR", f"Error processing query: {e}")
            import traceback
            traceback.print_exc()
            print()

if __name__ == "__main__":
    main()