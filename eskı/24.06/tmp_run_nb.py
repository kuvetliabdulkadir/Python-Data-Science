import re
import nbformat
from nbclient import NotebookClient

nb = nbformat.read('main_final.ipynb', as_version=4)
client = NotebookClient(nb, timeout=1200, kernel_name='python3', allow_errors=True)
client.execute()
for i, cell in enumerate(nb.cells):
    if cell.cell_type != 'code':
        continue
    for output in cell.get('outputs', []):
        if output.get('output_type') == 'stream':
            text = output.get('text', '')
            if re.search(r'KAZANAN MODEL|AUC-ROC Skoru|Standart %50 Eşik Maliyeti|Optimal %|NET TASARRUF|classification report|Karmaşıklık Matrisi|TN|FP|FN|TP|accuracy|macro avg|weighted avg|rf_f1|xgb_f1', text, re.I):
                print('CELL', i, 'OUTPUT:')
                print(text)
        elif output.get('output_type') in ('execute_result', 'display_data'):
            data = output.get('data', {})
            if 'text/plain' in data:
                text = data['text/plain']
                if re.search(r'KAZANAN MODEL|AUC-ROC Skoru|Standart %50 Eşik Maliyeti|Optimal %|NET TASARRUF|classification report|Karmaşıklık Matrisi|TN|FP|FN|TP|accuracy|macro avg|weighted avg|rf_f1|xgb_f1', text, re.I):
                    print('CELL', i, 'OUTPUT:')
                    print(text)
print('EXECUTION FINISHED')
