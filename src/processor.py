import json
import os

def load_raw_data(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def simple_text_splitter(text, chunk_size=1000, chunk_overlap=100):
    """
    A simple manual text splitter that breaks text into chunks of specified size
    with overlap, trying to break at sentence boundaries if possible.
    """
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        if end >= text_len:
            chunks.append(text[start:])
            break
            
        # Try to find a good break point (period followed by space)
        break_point = text.rfind(". ", start, end)
        if break_point != -1 and break_point > start + (chunk_size // 2):
            end = break_point + 1 # Include the period
            
        chunks.append(text[start:end])
        start = end - chunk_overlap
        
    return chunks

def process_data(raw_data):
    processed_chunks = []
    for entry in raw_data:
        source_url = entry.get("source")
        title = entry.get("title")
        content = entry.get("content", "")
        
        # Use our simple manual splitter instead of LangChain
        chunks = simple_text_splitter(content)
        
        for i, chunk in enumerate(chunks):
            processed_chunks.append({
                "chunk_id": f"{source_url}_{i}",
                "text": chunk.strip(),
                "metadata": {
                    "source": source_url,
                    "title": title
                }
            })
    return processed_chunks

def main():
    raw_file = "data/raw_data.json"
    output_file = "data/processed_chunks.json"
    
    print(f"Loading raw data from {raw_file}...")
    raw_data = load_raw_data(raw_file)
    
    if not raw_data:
        print("No data to process.")
        return
        
    print(f"Processing {len(raw_data)} documents into chunks...")
    chunks = process_data(raw_data)
    
    if not os.path.exists("data"):
        os.makedirs("data")
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)
    print(f"Finished processing. Created {len(chunks)} chunks in {output_file}")

if __name__ == "__main__":
    main()
