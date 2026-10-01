import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def analisar_espectro(caminho_imagem):
    img = cv2.imread(caminho_imagem)
    if img is None:
        print("Erro: Imagem não encontrada.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    intensidade = np.sum(gray, axis=0)
    
    intensidade = intensidade / np.max(intensidade)

    picos, _ = find_peaks(intensidade, height=0.2, distance=20)

    def pixel_para_nm(pixel):
        m = 0.5  # nm por pixel
        b = 380  # nm inicial
        return m * pixel + b

    comprimentos_onda = pixel_para_nm(picos)
    
    banco_dados = {
        'Hidrogênio': [410.2, 434.0, 486.1, 656.3], #Série de Balmer
        'Hélio': [447.1, 501.6, 587.6, 667.8],
        'Sódio': [589.0, 589.6], # Dubleto famoso
        'Mercúrio': [435.8, 546.1, 577.0, 579.1]
    }

    print("\n--- Análise ---")
    print(f"Picos detectados (pixels): {picos}")
    print(f"Comprimentos de onda estimados (nm): {np.round(comprimentos_onda, 2)}")
    
    tolerancia = 10.0
    elementos_candidatos = {}

    for elemento, linhas_conhecidas in banco_dados.items():
        matches = 0
        for lambda_calc in comprimentos_onda:
            if any(abs(lambda_calc - l_ref) < tolerancia for l_ref in linhas_conhecidas):
                matches += 1
        
        if matches > 0:
            elementos_candidatos[elemento] = matches

    print("\n Elementos possíveis:")
    if not elementos_candidatos:
        print("Nenhum elemento identificado com clareza")
    else:
        for el, score in elementos_candidatos.items():
            print(f"{el}: {score} linhas coincidentes")

    plt.figure(figsize=(10, 6))
    plt.plot(intensidade, color='black', label='Espectro Capturado')
    plt.plot(picos, intensidade[picos], "x", color='red', label='Picos Detectados')
    plt.title("Perfil Espectral")
    plt.xlabel("Pixel (Posição)")
    plt.ylabel("Intensidade Normalizada")
    plt.legend()
    plt.show()

analisar_espectro('./Data/helio.png')
