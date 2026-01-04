"""
Módulo de cálculo de fórmulas fisionômicas segundo Küchler (1988).
Gera fórmulas e descrições textuais a partir de dados de matriz fisionômica.
"""


def generate_kuchler_formula(physiognomic_matrix):
    """
    Gera a fórmula fisionômica de Küchler a partir dos dados da matriz.
    
    Args:
        physiognomic_matrix (dict): Dicionário com chaves no formato 'FormaN' (ex: 'B8', 'D4', 'F3')
                                     e valores com classes de cobertura ('c', 'i', 'p', 'r', 'b', 'a')
                                     ou características foliares ('h', 'w', 'k', 'l', 's')
    
    Returns:
        str: Fórmula fisionômica formatada segundo Küchler (1988)
    
    Exemplo:
        >>> generate_kuchler_formula({'D4': 'p', 'D3': 'i', 'D2': 'i', 'K3': 'p'})
        'D4p32iK3p'
    """
    if not physiognomic_matrix:
        return ''
    
    # Dicionários de mapeamento
    forms_order = ['B', 'D', 'E', 'N', 'O', 'S', 'M', 'G', 'H', 'L', 'C', 'K', 'T', 'V', 'X', 'F']
    heights = ['8', '7', '6', '5', '4', '3', '2', '1']
    
    # Organizar dados por forma de crescimento
    data_by_form = {}
    
    for key, coverage in physiognomic_matrix.items():
        # Extrair forma e altura
        form = key[0]  # Primeira letra
        height = key[1]  # Número da altura
        
        # Características foliares (F) são tratadas separadamente
        if form == 'F':
            leaf_characteristic = coverage
            # F está associado a uma altura, precisamos associar à forma principal
            # Por enquanto, vamos ignorar F na fórmula principal
            continue
        
        if form not in data_by_form:
            data_by_form[form] = {}
        
        data_by_form[form][height] = coverage
    
    # Ordenar formas por importância (ordem definida)
    present_forms = [f for f in forms_order if f in data_by_form]
    
    # Construir a fórmula
    formula_parts = []
    
    for form in present_forms:
        present_heights = data_by_form[form]
        
        # Agrupar alturas com mesma cobertura
        coverage_groups = {}
        for hgt, cov in present_heights.items():
            if cov not in coverage_groups:
                coverage_groups[cov] = []
            coverage_groups[cov].append(hgt)
        
        # Ordenar alturas dentro de cada grupo (da maior para a menor)
        for cov in coverage_groups:
            coverage_groups[cov].sort(key=lambda x: heights.index(x))
        
        # Construir string para esta forma
        # Primeiro, verificar se há apenas um tipo de cobertura
        if len(coverage_groups) == 1:
            single_coverage = list(coverage_groups.keys())[0]
            heights_str = ''.join(coverage_groups[single_coverage])
            
            # Omitir 'c' se for a única cobertura e for 'c'
            if single_coverage == 'c':
                formula_parts.append(f"{form}{heights_str}")
            else:
                formula_parts.append(f"{form}{heights_str}{single_coverage}")
        else:
            # Múltiplas coberturas: escrever cada grupo separadamente
            # Ordenar grupos por altura mais alta primeiro
            sorted_groups = sorted(coverage_groups.items(), 
                                  key=lambda x: heights.index(x[1][0]))
            
            first_part = True
            for cov, hgts in sorted_groups:
                heights_str = ''.join(hgts)
                
                if first_part:
                    # Primeira parte: incluir forma
                    if cov == 'c':
                        formula_parts.append(f"{form}{heights_str}")
                    else:
                        formula_parts.append(f"{form}{heights_str}{cov}")
                    first_part = False
                else:
                    # Partes subsequentes: sem repetir a forma
                    formula_parts.append(f"{heights_str}{cov}")
    
    return ''.join(formula_parts)


def generate_formula_description(physiognomic_matrix):
    """
    Gera a descrição textual por extenso da fórmula fisionômica.
    
    Args:
        physiognomic_matrix (dict): Dicionário com dados da matriz
    
    Returns:
        str: Descrição textual da fisionomia
    """
    if not physiognomic_matrix:
        return 'Sem dados fisionômicos'
    
    # Dicionários de descrição
    forms_desc = {
        'B': 'folhas sempreverdes',
        'D': 'folhas decíduas',
        'E': 'acículas sempreverdes',
        'N': 'acículas decíduas',
        'O': 'áfilas',
        'S': 'semidecíduas',
        'M': 'mistas',
        'G': 'graminoides',
        'H': 'ervas comuns',
        'L': 'musgos e líquens',
        'C': 'lianas',
        'K': 'caule suculento',
        'T': 'plantas tufadas',
        'V': 'bambus',
        'X': 'epífitas',
        'F': 'folhas especiais'
    }
    
    heights_desc = {
        '8': 'acima de 35m',
        '7': 'entre 20-35m',
        '6': 'entre 10-20m',
        '5': 'entre 5-10m',
        '4': 'entre 2-5m',
        '3': 'entre 0,5-2m',
        '2': 'entre 0,1-0,5m',
        '1': 'abaixo de 0,1m'
    }
    
    coverage_desc = {
        'c': 'contínua (>75%)',
        'i': 'interrompida (51-75%)',
        'p': 'porosa (26-50%)',
        'r': 'rara (6-25%)',
        'b': 'baixa (1-5%)',
        'a': 'ausente (<1%)'
    }
    
    # Organizar dados
    forms_order = ['B', 'D', 'E', 'N', 'O', 'S', 'M', 'G', 'H', 'L', 'C', 'K', 'T', 'V', 'X']
    data_by_form = {}
    all_heights = set()  # Para contar estratos únicos
    
    for key, coverage in physiognomic_matrix.items():
        if len(key) >= 2:
            form = key[0]
            height = key[1]
            
            if form == 'F':
                continue
            
            all_heights.add(height)  # Adicionar altura ao conjunto
            
            if form not in data_by_form:
                data_by_form[form] = []
            
            data_by_form[form].append({
                'height': height,
                'coverage': coverage,
                'height_desc': heights_desc.get(height, height),
                'coverage_desc': coverage_desc.get(coverage, coverage)
            })
    
    # Contar número de estratos
    num_estratos = len(all_heights)
    estrato_text = 'estrato' if num_estratos == 1 else 'estratos'
    
    # Construir descrição
    descriptions = []
    
    for form in forms_order:
        if form in data_by_form:
            form_name = forms_desc.get(form, form)
            records = data_by_form[form]
            
            # Agrupar por cobertura
            by_coverage = {}
            for rec in records:
                cov = rec['coverage']
                if cov not in by_coverage:
                    by_coverage[cov] = []
                by_coverage[cov].append(rec['height_desc'])
            
            # Criar descrições para cada cobertura
            form_parts = []
            for cov, hgts in by_coverage.items():
                heights_text = ', '.join(hgts)
                cov_text = coverage_desc.get(cov, cov)
                # Remover a descrição entre parênteses (ex: "(>75%)")
                cov_text_clean = cov_text.split(' (')[0]
                form_parts.append(f"{heights_text} com cobertura {cov_text_clean}")
            
            full_desc = f"{form_name.capitalize()} {' e '.join(form_parts)}"
            descriptions.append(full_desc)
    
    if descriptions:
        # Adicionar informação sobre estratos no início
        final_description = f"Vegetação em {num_estratos} {estrato_text}. " + '; '.join(descriptions) + '.'
        return final_description
    else:
        return 'Sem dados fisionômicos.'
