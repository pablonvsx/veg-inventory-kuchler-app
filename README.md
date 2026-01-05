# KuchlerApp - Inventário Fitofisionômico

## Sobre o Projeto

KuchlerApp é um aplicativo mobile desenvolvido para facilitar o levantamento e classificação fisionômica da vegetação utilizando o método de Küchler (1988) e adaptado por Cavalcanti (2024). O app permite registrar características estruturais da vegetação em campo de forma prática e sistemática, gerando automaticamente fórmulas fisionômicas padronizadas conforme a proposta.

## Objetivo

Fornecer uma ferramenta digital para biólogos, ecólogos e pesquisadores realizarem inventários fitofisionômicos, substituindo cadernetas de campo tradicionais por um sistema integrado que:

- Registra dados de parcelas com coordenadas GPS e altitude
- Documenta a estrutura vertical da vegetação através de matriz fisionômica
- Gera automaticamente fórmulas de Küchler e descrições textuais da fisionomia vegetal
- Exporta dados para análises posteriores (formato CSV)
- Mantém histórico organizado por projetos

![GIF KuchlerApp](https://github.com/user-attachments/assets/b9f75360-b64d-4af9-b500-617887f4171b)

## Sobre August Wilhelm Küchler

August Wilhelm Küchler (1907-1999) foi um geógrafo e biogeógrafo alemão-americano, pioneiro no desenvolvimento de métodos sistemáticos para mapeamento e classificação fisionômica da vegetação. Professor emérito da Universidade do Kansas, Küchler dedicou sua carreira ao estudo da geografia da vegetação e ao desenvolvimento de sistemas de classificação que pudessem ser aplicados universalmente.

Uma de suas grandes contribuições foi a criação de um sistema de notação fisionômica que permite descrever de forma concisa e padronizada a estrutura tridimensional da vegetação, independentemente de sua composição florística, baseando-se na fisionomia das plantas. Este método, publicado em 1988, tornou-se referência mundial para estudos biogeográficos e ecológicos, sendo amplamente utilizado em inventários e mapeamentos de vegetação.

## Matriz Fisionômica

### O que é a Matriz Fisionômica?

A matriz fisionômica é uma ferramenta de registro que captura a estrutura tridimensional da vegetação através de duas dimensões principais:

1. **Formas de Vida** (colunas): 16 categorias morfológicas que descrevem o tipo de planta
2. **Classes de Altura** (linhas): 8 estratos verticais que variam de 0,1m até mais de 35m

Cada célula da matriz recebe uma classe de cobertura que indica a densidade da vegetação naquele estrato específico. Esta abordagem permite representar de forma objetiva e quantitativa a estrutura vertical e horizontal de qualquer formação vegetal.

### Orientação de Uso

**Importante:** Busque uma área de homogeneidade da vegetação antes de iniciar o registro. A parcela deve representar uma unidade fisionômica uniforme, evitando áreas de transição ou com variação significativa na composição estrutural.

### Formas de Vida

As formas de vida representam as diferentes categorias morfológicas da vegetação, organizadas em três grupos principais:

#### Lenhosas
- **B** - Folhas sempreverdes (Broad-leaved evergreen)
- **D** - Folhas decíduas (Deciduous)
- **E** - Acículas sempreverdes (Evergreen needleleaf)
- **N** - Acículas decíduas (Needleleaf deciduous)
- **O** - Áfilas (Aphyllous)
- **S** - Semidecíduas (Semi-deciduous, combinação B+D)
- **M** - Mistas (Mixed, combinação E+D)

#### Herbáceas
- **G** - Graminoides (Graminoids)
- **H** - Ervas comuns (Herbs)
- **L** - Musgos e líquens (Lichens and mosses)

#### Especiais
- **C** - Lianas e cipós (Climbers)
- **K** - Caule suculento (Succulents)
- **T** - Plantas tufadas e palmeiras (Tuft plants)
- **V** - Bambus (Bamboo)
- **X** - Epífitas (Epiphytes)
- **F** - Folhas especiais (Special leaf forms)

### Classes de Altura

As classes de altura dividem o perfil vertical da vegetação em oito estratos:

| Classe | Estrato | Faixa |
|--------|---------|-------|
| 8 | Emergente | Acima de 35m |
| 7 | Dossel superior | 20-35m |
| 6 | Dossel médio | 10-20m |
| 5 | Subdossel | 5-10m |
| 4 | Arbustivo alto | 2-5m |
| 3 | Arbustivo baixo | 0,5-2m |
| 2 | Herbáceo | 0,1-0,5m |
| 1 | Rasteiro | Menor que 0,1m |

### Classes de Cobertura

As classes de cobertura indicam a densidade da vegetação em cada estrato, representadas por letras minúsculas:

| Código | Nome | Cobertura | Descrição |
|--------|------|-----------|-----------|
| **c** | Contínua | Maior que 75% | Estrato praticamente fechado |
| **i** | Interrompida | 51-75% | Cobertura com pequenas aberturas |
| **p** | Porosa | 26-50% | Cobertura em manchas ou parques |
| **r** | Rara | 6-25% | Indivíduos dispersos |
| **b** | Baixa | 1-5% | Presença esporádica |
| **a** | Ausente | Menor que 1% | Ocorrência raríssima |

## Lógica das Fórmulas de Küchler

### Princípios de Construção

A fórmula fisionômica de Küchler é uma notação concisa que representa a estrutura vertical da vegetação através de regras específicas de sintaxe:

#### 1. Ordem de Importância
O estrato vegetal mais expressivo ou dominante deve ser escrito primeiro na fórmula. Normalmente, corresponde ao estrato mais alto ou com maior cobertura.

#### 2. Agrupamento de Alturas
Quando uma forma de crescimento aparece em várias alturas, a letra não se repete. Os números das alturas são escritos em sequência, da maior para a menor.

**Exemplo:** `D432` indica lenhosas decíduas nos estratos 4 (2-5m), 3 (0,5-2m) e 2 (0,1-0,5m).

#### 3. Omissão da Cobertura Contínua
O símbolo 'c' (contínuo, maior que 75%) é omitido por padrão quando representa a única classe de cobertura presente. Ele só deve aparecer quando necessário contrastar com outro estrato.

**Exemplos:**
- `D4` indica cobertura contínua em 2-5m
- `D4c3p` indica cobertura contínua em 2-5m e porosa em 0,5-2m

#### 4. Representação de Coberturas Variadas
Quando uma mesma forma de vida possui diferentes classes de cobertura em diferentes alturas, os números são agrupados por classe de cobertura.

**Exemplo:** `D4p32i` indica:
- Altura 4 com cobertura porosa (p)
- Alturas 3 e 2 com cobertura interrompida (i)

#### 5. Regras Especiais para Lianas e Epífitas
Lianas (C) e Epífitas (X) são registradas apenas na classe de altura mais elevada onde ocorrem, independentemente de sua distribuição vertical real.

### Exemplo Prático

Considere uma vegetação com as seguintes características:

**Dados da matriz:**
- Lenhosa Decídua (D) na altura 4 (2-5m) com cobertura porosa (p)
- Lenhosa Decídua (D) nas alturas 3 e 2 (0,5-2m e 0,1-0,5m) com cobertura interrompida (i)
- Caule Suculento (K) na altura 3 (0,5-2m) com cobertura porosa (p)

**Fórmula resultante:** `D4p32iK3p`

**Interpretação:**
- Vegetação em 3 estratos
- Estrato dominante: Lenhosas decíduas entre 2-5m com cobertura porosa (26-50%)
- Estrato intermediário/inferior: Lenhosas decíduas entre 0,5-2m e 0,1-0,5m com cobertura interrompida (51-75%)
- Componente suculento: Caules suculentos entre 0,5-2m com cobertura porosa (26-50%)

### Características Foliares (Opcional)

Quando necessário detalhar características foliares, utiliza-se letras minúsculas entre a forma de vida e a altura:

- **h** - Hard (folhas duras/esclerófilas)
- **w** - Waxy (folhas cerosas)
- **k** - succulent (folhas suculentas)
- **l** - Large (folhas grandes)
- **s** - Small (folhas pequenas)

**Exemplo:** `Bh4` indica lenhosas sempreverdes com folhas duras no estrato de 2-5m.

### Descrição Textual Automática

O aplicativo gera automaticamente uma descrição textual da fórmula, facilitando a compreensão da estrutura:

**Exemplo de descrição:**
"Vegetação em 3 estratos. Folhas decíduas entre 2-5m com cobertura porosa e entre 0,5-2m, entre 0,1-0,5m com cobertura interrompida; Caule suculento entre 0,5-2m com cobertura porosa."

## Funcionalidades

### Gerenciamento de Projetos
- Criar múltiplos projetos de inventário
- Visualizar lista de projetos salvos
- Exportar dados completos em formato CSV
- Excluir projetos obsoletos

### Registro de Parcelas
- **Etapa 1:** Coordenadas geográficas (latitude/longitude) e altitude
- **Etapa 2:** Preenchimento interativo da matriz fisionômica
- Timestamp automático de cada registro
- Geração automática de fórmula e descrição textual

### Visualização
- Lista detalhada de parcelas por projeto
- Exibição de fórmula Küchler para cada parcela
- Descrição textual completa da fisionomia
- Informações de localização geográfica e temporal

### Configurações
- Alternância entre tema claro e escuro
- Seis opções de cor primária (Blue, Green, Purple, Red, Orange, Pink)
- Persistência de preferências do usuário

## Estrutura de Dados

### Projeto
```json
{
  "name": "Nome do Projeto",
  "plots": [...]
}
```

### Parcela
```json
{
  "latitude": -23.5505,
  "longitude": -46.6333,
  "altitude": 760.0,
  "data_registro": "04/01/2026",
  "horario_registro": "14:30:45",
  "matriz_fisionomica": {
    "D4": "p",
    "D3": "i",
    "K3": "p"
  },
  "formula_kuchler": "D4p32iK3p",
  "descricao_fisionomia": "Vegetação em 3 estratos..."
}
```

## Tecnologias Utilizadas

- **Python 3.10+:** Linguagem de programação base
- **KivyMD 1.x:** Framework para interfaces Material Design
- **Kivy:** Framework multiplataforma para aplicações móveis
- **JSON:** Armazenamento local de dados
- **CSV:** Formato de exportação de dados

## Estrutura do Projeto

```
inventario-vegetal-kuchler/
├── main.py                      # Aplicação principal (Python 3.10+)
├── interface.kv                 # Interface (KivyMD)
├── setup.py                     # Configuração de instalação
├── requirements.txt             # Dependências do projeto
├── LICENSE                      # Licença GPL-3.0
├── README.md                    # Este arquivo
├── modules/
│   ├── __init__.py             # Inicialização dos módulos
│   ├── data_manager.py         # Gerenciamento de dados JSON
│   └── kuchler_calculator.py   # Geração de fórmulas Küchler
├── exports/                     # Arquivos CSV exportados
```

## Como Usar

### Requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/pablonvsx/veg-inventory-kuchler-app.git
cd veg-inventory-kuchler-app
```

2. Verifique a versão do Python (deve ser 3.10+):
```bash
python --version
```

3. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute o aplicativo:
```bash
python main.py
```

### Fluxo de Trabalho

1. **Criar Projeto:** Acesse Menu → Meus Projetos → Botão (+) Novo Projeto
2. **Adicionar Parcela:** Selecione o projeto → Botão (+) Nova Parcela
3. **Preencher Dados:**
   - Etapa 1: Insira latitude, longitude e altitude
   - Etapa 2: Preencha a matriz fisionômica clicando nas células
4. **Visualizar Resultado:** A fórmula e descrição aparecem automaticamente na lista
5. **Exportar Dados:** Acesse o menu do projeto → Exportar para CSV

## Caderneta de Campo Original

Este aplicativo é baseado na caderneta de campo para inventário fisionômico adaptada por Cavalcanti (2024).

## Referências Bibliográficas

CAVALCANTI, L.C.S. **Caderneta de campo para inventário fisionômico**. PAISAGEO/UFPE: Recife. 2024. 13p. Disponível em: https://www.even3.com.br/anais/biogeografia-icbb-iiicib-xiiiceb/870211-caderneta-de-campo-para-inventario-fisionomico/. Acesso em: 04 jan. 2026.

KÜCHLER, A. W. Physiognomic vegetation classification systems. In: KÜCHLER, A. W.; ZONNEVELD, I. S. (eds.). *Vegetation mapping*. Handbook of vegetation science, vol. 10. Dordrecht: Kluwer Academic Publishers, 1988. p. 65-84.

## Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

