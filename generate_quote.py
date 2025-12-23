import requests
import os
import json

def get_random_quote():
    """Rastgele bir programlama sözü getirir"""
    try:
        response = requests.get('https://api.quotable.io/random?tags=technology')
        if response.status_code == 200:
            data = response.json()
            return data['content'], data['author']
        else:
            # Yedek sözler
            quotes = [
                ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
                ("First, solve the problem. Then, write the code.", "John Johnson"),
                ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
                ("In order to be irreplaceable, one must always be different.", "Coco Chanel"),
                ("Knowledge is power.", "Francis Bacon"),
                ("Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.", "Antoine de Saint-Exupery"),
                ("The best way to predict the future is to invent it.", "Alan Kay"),
                ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler")
            ]
            import random
            quote, author = random.choice(quotes)
            return quote, author
    except Exception as e:
        print(f"Error: {e}")
        return "Code is poetry.", "Unknown"

def wrap_text(text, max_width=60):
    """Metni belirli bir genişlikte böler"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= max_width:
            current_line.append(word)
            current_length += len(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def generate_svg(quote, author):
    """SVG dosyası oluşturur"""
    lines = wrap_text(quote, max_width=50)
    
    # SVG boyutlarını hesapla
    line_height = 30
    padding = 40
    quote_height = len(lines) * line_height
    total_height = quote_height + 100  # Author için ekstra alan
    width = 800
    
    svg_content = f'''<svg width="{width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="100%" height="100%" fill="url(#bg-gradient)" rx="15"/>
    
    <!-- Border -->
    <rect x="2" y="2" width="{width-4}" height="{total_height-4}" 
          fill="none" stroke="#e94560" stroke-width="2" rx="15"/>
    
    <!-- Quote Icon -->
    <text x="40" y="50" font-family="Arial, sans-serif" font-size="40" fill="#e94560" opacity="0.3">❝</text>
    
    <!-- Quote Text -->'''
    
    y_position = 80
    for i, line in enumerate(lines):
        svg_content += f'''
    <text x="50%" y="{y_position + i * line_height}" 
          font-family="'Segoe UI', Arial, sans-serif" 
          font-size="20" 
          fill="#ffffff" 
          text-anchor="middle">{line}</text>'''
    
    # Author
    author_y = y_position + len(lines) * line_height + 40
    svg_content += f'''
    
    <!-- Author -->
    <text x="50%" y="{author_y}" 
          font-family="'Segoe UI', Arial, sans-serif" 
          font-size="18" 
          fill="#e94560" 
          text-anchor="middle"
          font-style="italic">— {author}</text>
    
    <!-- Decorative Line -->
    <line x1="30%" y1="{author_y - 15}" x2="70%" y2="{author_y - 15}" 
          stroke="#e94560" stroke-width="1" opacity="0.5"/>
          
</svg>'''
    
    return svg_content

def main():
    # Output klasörünü oluştur
    os.makedirs('output', exist_ok=True)
    
    # Quote'u al
    quote, author = get_random_quote()
    print(f"Quote: {quote}")
    print(f"Author: {author}")
    
    # SVG oluştur
    svg = generate_svg(quote, author)
    
    # Dosyaya kaydet
    with open('output/quote.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    
    print("Quote SVG successfully generated!")

if __name__ == "__main__":
    main()
