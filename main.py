import time
import tracemalloc
import functools
import folium

# =====================================================
# GRAFOS
# =====================================================

grafo_sp = {
    "Tucuruvi": [("Parada Inglesa", 3)],
    "Parada Inglesa": [("Tucuruvi", 3), ("Jardim São Paulo", 2)],
    "Jardim São Paulo": [("Parada Inglesa", 2), ("Santana", 3)],
    "Santana": [("Jardim São Paulo", 3), ("Carandiru", 2)],
    "Carandiru": [("Santana", 2), ("Portuguesa-Tietê", 2)],
    "Portuguesa-Tietê": [("Carandiru", 2), ("Armênia", 3)],
    "Armênia": [("Portuguesa-Tietê", 3), ("Tiradentes", 2)],
    "Tiradentes": [("Armênia", 2), ("Luz", 2)],
    "Luz": [("Tiradentes", 2), ("Sé", 4), ("Brás", 3)],
    "Brás": [("Luz", 3), ("Tamanduateí", 4)],
    "Tamanduateí": [("Brás", 4), ("Santo André", 5)],
    "Sé": [("Luz", 4), ("São Joaquim", 3)],
    "São Joaquim": [("Sé", 3), ("Vergueiro", 2)],
    "Vergueiro": [("São Joaquim", 2), ("Paraíso", 3)],
    "Paraíso": [("Vergueiro", 3), ("Ana Rosa", 2)],
    "Ana Rosa": [("Paraíso", 2), ("Chácara Klabin", 3)],
    "Chácara Klabin": [("Ana Rosa", 3), ("Santos-Imigrantes", 4)],
    "Santos-Imigrantes": [("Chácara Klabin", 4), ("Alto do Ipiranga", 3)],
    "Alto do Ipiranga": [("Santos-Imigrantes", 3), ("Capão Redondo", 6)],
    "Capão Redondo": []
}

grafo_beijing = {
    "Sihui East": [("Sihui", 2)],
    "Sihui": [("Sihui East", 2), ("Guomao", 3)],
    "Guomao": [("Sihui", 3), ("Yonganli", 2)],
    "Yonganli": [("Guomao", 2), ("Jianguomen", 3)],
    "Jianguomen": [("Yonganli", 3), ("Dongdan", 2)],
    "Dongdan": [("Jianguomen", 2), ("Wangfujing", 3)],
    "Wangfujing": [("Dongdan", 3), ("Tiananmen East", 2)],
    "Tiananmen East": [("Wangfujing", 2), ("Tiananmen West", 2)],
    "Tiananmen West": [("Tiananmen East", 2), ("Xidan", 3)],
    "Xidan": [("Tiananmen West", 3), ("Chegongzhuang", 4)],
    "Chegongzhuang": [("Xidan", 4), ("Xizhimen", 3)],
    "Xizhimen": []
}

grafo_sf = {
    "Dublin": [("Pleasanton", 2)],
    "Pleasanton": [("Dublin", 2), ("Castro Valley", 4)],
    "Castro Valley": [("Pleasanton", 4), ("Bay Fair", 3)],
    "Bay Fair": [("Castro Valley", 3), ("San Leandro", 3)],
    "San Leandro": [("Bay Fair", 3), ("Coliseum", 4)],
    "Coliseum": [("San Leandro", 4), ("Fruitvale", 3)],
    "Fruitvale": [("Coliseum", 3), ("Lake Merritt", 3)],
    "Lake Merritt": [("Fruitvale", 3), ("West Oakland", 5)],
    "West Oakland": [("Lake Merritt", 5), ("Embarcadero", 6)],
    "Embarcadero": [("West Oakland", 6), ("Montgomery", 2)],
    "Montgomery": [("Embarcadero", 2), ("Powell", 2)],
    "Powell": [("Montgomery", 2), ("Civic Center", 2)],
    "Civic Center": [("Powell", 2), ("Daly City", 5)],
    "Daly City": []
}

# =====================================================
# FATOR DE HORÁRIO
# =====================================================

def fator_horario(h):
    if 5 <= h < 7:
        return 0.6
    elif 7 <= h < 9:
        return 1.5
    elif 9 <= h < 17:
        return 1.0
    elif 17 <= h < 20:
        return 2.0
    return 1.2

# =====================================================
# MENOR CAMINHO (COM MEMOIZAÇÃO)
# =====================================================

@functools.lru_cache(maxsize=None)
def menor_custo(grafo_id, origem, destino, horario, visitados=frozenset()):
    grafos = {
        "sp": grafo_sp,
        "bj": grafo_beijing,
        "sf": grafo_sf
    }

    grafo = grafos[grafo_id]

    if origem == destino:
        return 0

    melhor = float('inf')

    for vizinho, peso in grafo.get(origem, []):
        if vizinho not in visitados:
            custo = (peso * fator_horario(horario)) + menor_custo(
                grafo_id, vizinho, destino, horario, visitados | {origem}
            )
            melhor = min(melhor, custo)

    return melhor

# =====================================================
# MAIOR CAMINHO (BACKTRACKING)
# =====================================================

def maior_caminho(grafo, origem, destino, visitados=None):
    if visitados is None:
        visitados = set()

    if origem == destino:
        return 0

    visitados.add(origem)
    maior = float('-inf')

    for vizinho, peso in grafo.get(origem, []):
        if vizinho not in visitados:
            custo = peso + maior_caminho(grafo, vizinho, destino, visitados)
            maior = max(maior, custo)

    visitados.remove(origem)
    return maior

# =====================================================
# TESTE + PERFORMANCE
# =====================================================

def testar(grafo_id, origem, destino, horario):
    tracemalloc.start()
    t0 = time.perf_counter()

    custo = menor_custo(grafo_id, origem, destino, horario)

    t1 = time.perf_counter()
    mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n==============================")
    print(f"Cidade: {grafo_id}")
    print(f"Origem: {origem} -> Destino: {destino}")
    print(f"Custo mínimo: {custo:.2f}")
    print(f"Tempo: {t1-t0:.6f}s")
    print(f"Memória: {mem[1]/1024:.2f} KB")

# =====================================================
# EXECUÇÃO
# =====================================================

if __name__ == "__main__":
    testar("sp", "Tucuruvi", "Capão Redondo", 18)
    testar("bj", "Sihui East", "Xizhimen", 10)
    testar("sf", "Dublin", "Daly City", 8)

    # Maior caminho (exemplo SP)
    print("\nMaior caminho SP:")
    print(maior_caminho(grafo_sp, "Tucuruvi", "Capão Redondo"))

    # =====================================================
    # MAPA (gera arquivo HTML)
    # =====================================================
    mapa = folium.Map(location=[-23.55, -46.63], zoom_start=11)

    folium.Marker([-23.48, -46.62], tooltip="Tucuruvi").add_to(mapa)
    folium.Marker([-23.60, -46.77], tooltip="Capão Redondo").add_to(mapa)

    mapa.save("mapa_sp.html")

    print("\nMapa gerado: abra 'mapa_sp.html'")