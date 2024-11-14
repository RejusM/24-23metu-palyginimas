import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://timingapp.lt/nidos-puses-maratono-begimas-2024"
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table', {'class': 'table'})
rows = table.find_all('tr')

vardai_2024 = []
for row in rows[1:]:
    cols = row.find_all('td')
    vardas = cols[2].text.strip()
    vardai_2024.append(vardas)

file_path = 'nidos-pusmaratonis-2023-puse-maratono-20240925092047.xlsx'
df_2023 = pd.read_excel(file_path)

df_filtered = df_2023[['Vardas', 'Laikas']]

tavo_vardas = "Jonas Markevičius"
tavo_laikas = df_filtered[df_filtered['Vardas'] == tavo_vardas]['Laikas'].values[0]


greitesni_2023 = df_filtered[df_filtered['Laikas'] < tavo_laikas]


greitesni_2024 = []
for vardas in greitesni_2023['Vardas']:
    if vardas in vardai_2024:
        laikas = df_filtered[df_filtered['Vardas'] == vardas]['Laikas'].values[0]
        greitesni_2024.append((vardas, laikas))


tavo_indeksas = df_filtered[df_filtered['Vardas'] == tavo_vardas].index[0]
po_taves = df_filtered.iloc[tavo_indeksas+1:tavo_indeksas+15]

po_taves_2024 = []
for vardas in po_taves['Vardas']:
    if vardas in vardai_2024:
         laikas = df_filtered[df_filtered['Vardas'] == vardas]['Laikas'].values[0]
         po_taves_2024.append((vardas, laikas))

# print(f'Tavo laikas: {tavo_laikas}')

# print("2023 metais tave lenkę ir 2024 užsiregistravę dalyviai:")
# for vardas, laikas in greitesni_2024:
#     print(f"{vardas}: {laikas}")

# print("\n2023 metais po tavęs buvę dalyviai ir 2024 užsiregistravę dalyviai:")
# for vardas, laikas in po_taves_2024:
#     print(f"{vardas}: {laikas}")


dalyviai_2023 = df_filtered['Vardas'].tolist()

nebego_2023 = [vardas for vardas in vardai_2024 if vardas not in dalyviai_2023]

# print("\nDalyviai, kurie nebėgo 2023 metais, bet užsiregistravo 2024:")
# for vardas in nebego_2023:
#     print(vardas)

results = {
    "Tavo laikas": [tavo_laikas],
    "Greitesni 2024": [f"{vardas}: {laikas}" for vardas, laikas in greitesni_2024],
    "Po tavęs 2024": [f"{vardas}: {laikas}" for vardas, laikas in po_taves_2024],
    "Nebėgo 2023": nebego_2023
}

results_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in results.items()]))

output_file_path = 'rezultatai_nidos_pusmaratonis.xlsx'
results_df.to_excel(output_file_path, index=False)

print(f"Rezultatai išsaugoti į: {output_file_path}")