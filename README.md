# Legal Lens
An AI-powered tool for automatic contract analysis, extracting key clauses, highlighting risks, and streamlining legal document review.

## 🚀 Features  
- **Extracts key legal clauses** (salaries, penalties, fees, liability, dispute resolution, etc.).  
- **Uses OpenAI GPT-4** to identify risky clauses.  
- **Highlights text physically in the PDF** using an orange marker.  
- **Processes PDFs page by page** to avoid API limits. 

## 📌 Installation  
### **1. Clone this repository**  
```sh
git clone https://github.com/juliuspleunes4/legallens.git
cd legallens
```
### **2. Install dependencies**
```sh
pip install -r requirements.txt
```
### **3. Set up environment variables**
Create a `.env` file in the root directory with the following text: 
```
OPENAI_API_KEY=YOUR_API_KEY_HERE
```

## 📄 Usage

1. Place the PDF file you want to analyze in the root directory.
2. Name it `input.pdf`.
3. Run the script:
    ```sh
    python main.py
    ```
4. The output PDF with highlighted clauses will be saved as `legallens.pdf`.

## 🛠️ Troubleshooting

### ⚠️ OpenAI Rate Limit Error
- The script will automatically switch to `gpt-3.5-turbo` if `gpt-4` exceeds its token limit.
- If API calls still fail, try reducing the PDF size or splitting it into smaller sections.

### ⚠️ Incorrect Highlighting (single letters instead of full sentences)
- Ensure your PDF contains selectable text rather than scanned images.

### ⚠️ Missing Dependencies
- Run `pip install -r requirements.txt` again to ensure all necessary packages are installed.

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.

## 👤 Author
Developed by Julius Pleunes  
GitHub: [juliuspleunes4](https://github.com/juliuspleunes4)

🚀 Happy Contract Scanning!