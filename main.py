#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inventário Fitofisionômico - Método Küchler
Aplicativo mobile para levantamento e classificação fitofisionômica de vegetação.

Requer: Python 3.10+
Autor: Seu Nome
Licença: GPL-3.0
"""

# Verificação da versão do Python
import sys
if sys.version_info < (3, 10):
    print("Erro: Este aplicativo requer Python 3.10 ou superior.")
    print(f"Versão atual: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    sys.exit(1)

# Importações do Kivy e KivyMD
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import csv
import os
import webbrowser
from datetime import datetime

# Importações dos módulos personalizados
from modules import data_manager as data
from modules import kuchler_calculator

# Constantes
JSON_FILE = 'data.json'
WINDOW_SIZE = (540, 900)
EXPORTS_DIR = 'exports'

# Formas de vida e alturas da matriz fisionômica
LIFE_FORMS = ['B', 'D', 'E', 'N', 'O', 'S', 'M', 'G', 'H', 'L', 'C', 'K', 'T', 'V', 'X', 'F']
HEIGHT_CLASSES = ['1', '2', '3', '4', '5', '6', '7', '8']
COVERAGE_CLASSES = ['c', 'i', 'p', 'r', 'b', 'a']

# Classes de cobertura com descrições
COVERAGE_DESCRIPTIONS = {
    'c': 'contínua (>75%)',
    'i': 'interrompida (51-75%)',
    'p': 'porosa (26-50%)',
    'r': 'rara (6-25%)',
    'b': 'baixa (1-5%)',
    'a': 'ausente (<1%)'
}

# Carrega dados e configura janela
projects_data = data.load_data(JSON_FILE)
Window.size = WINDOW_SIZE

class KuchlerInventoryApp(MDApp):
    """Aplicativo de inventário fitofisionômico usando metodologia Küchler."""
    
    def build(self):
        """Inicializa o aplicativo e carrega configurações."""
        self.title = 'KuchlerApp'
        # Cores disponíveis para o tema
        self.colors = {
            'Blue': 'Blue',
            'Green': 'Green',
            'Purple': 'Purple',
            'Red': 'Red',
            'Orange': 'Orange',
            'Pink': 'Pink'
        }
        
        # Variáveis do projeto atual
        self.current_project = None
        self.current_project_index = None
        
        # Dados temporários da parcela em criação
        self.temp_plot_data = {}
        
        # Carrega configurações salvas
        self.load_settings()
        
        # Carrega interface
        return Builder.load_file('interface.kv')
    
    # ==================== NAVEGAÇÃO ====================
    
    def confirm_exit_app(self):
        """Exibe diálogo de confirmação para sair do aplicativo."""
        if not hasattr(self, 'exit_dialog') or not self.exit_dialog:
            self.exit_dialog = MDDialog(
                title='Sair do Aplicativo',
                text='Deseja realmente sair do aplicativo?',
                buttons=[
                    MDFlatButton(
                        text='CANCELAR',
                        on_release=lambda x: self.exit_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text='SAIR',
                        on_release=lambda x: self.stop()
                    ),
                ],
            )
        self.exit_dialog.open()
    
    def go_back(self):
        """Navega para a tela anterior baseado na tela atual."""
        current_screen = self.root.current

        back_navigation = {
            'my_projects_screen': 'menu_screen',
            'new_project_screen': 'my_projects_screen',
            'delete_project_screen': 'my_projects_screen',
            'view_project_screen': 'my_projects_screen',
            'delete_plot_screen': 'view_project_screen',
            'new_plot_screen1': 'view_project_screen',
            'new_plot_screen2': 'new_plot_screen1',
            'settings_screen': 'menu_screen',
            'about_app_screen': 'menu_screen',
        }
        
        self.root.current = back_navigation.get(current_screen, 'menu_screen')

    def go_to_screen(self, screen_name, dialog=None):
        """Navega para a tela especificada.
        
        Args:
            screen_name: Nome da tela de destino
            dialog: Diálogo opcional a ser fechado antes da navegação
        """
        if dialog:
            dialog.dismiss()
        self.root.current = screen_name
    
    # ==================== PROJETOS ====================
    
    def load_projects_list(self):
        """Carrega e exibe lista de projetos na tela principal."""
        projects_list_container = self.root.get_screen('my_projects_screen').ids.projects_list_container
        projects_list_container.clear_widgets()

        for index, project in enumerate(projects_data.get('projects', [])):
            project_card = MDCard(
                size_hint_y=None,
                height='80dp',
                elevation=0,
                ripple_behavior=True,
                md_bg_color=self.theme_cls.primary_color,
                radius=[15, 15, 15, 15],
                padding=dp(10)
            )
            
            project_card.bind(on_release=lambda x, idx=index: self.open_project(idx))

            project_label = MDLabel(
                text=project['name'],
                halign='center',
                valign='middle',
                font_style='H6',
                bold=True,
                theme_text_color='Custom',
                text_color=(1, 1, 1, 1),
            )

            project_card.add_widget(project_label)
            projects_list_container.add_widget(project_card)

    def save_new_project(self):
        """Salva um novo projeto no arquivo JSON."""
        project_name = self.root.get_screen('new_project_screen').ids.project_name_input.text.strip()

        if not project_name:
            # Mostra diálogo pedindo para inserir um nome
            self.show_info_dialog('Nome Obrigatório', 'Por favor, insira um nome para o projeto.')
            return

        new_project = {
            'name': project_name,
            'plots': []
        }

        projects_data.setdefault('projects', []).append(new_project)
        data.save_data(projects_data, JSON_FILE)

        # Limpa os campos de entrada
        self.root.get_screen('new_project_screen').ids.project_name_input.text = ''

        # Mostra diálogo de confirmação
        self.show_success_dialog('Projeto Criado', f'O projeto "{project_name}" foi criado com sucesso!')
        
        # Volta para a tela de Meus Projetos
        self.go_to_screen('my_projects_screen')
    
    # Funções da tela DeleteProjectScreen
    def go_to_delete_projects(self):
        """Navega para a tela de excluir projetos."""
        if not projects_data.get('projects', []):
            self.show_info_dialog('Sem Projetos', 'Não há projetos cadastrados para excluir.')
            return
        self.go_to_screen('delete_project_screen')
    
    def load_delete_projects_list(self):
        """Carrega a lista de projetos para exclusão."""
        projects_list_container = self.root.get_screen('delete_project_screen').ids.delete_projects_list_container
        projects_list_container.clear_widgets()

        projects = projects_data.get('projects', [])
        
        if not projects:
            no_projects_label = MDLabel(
                text='Nenhum projeto cadastrado',
                halign='center',
                font_style='Body1',
                size_hint_y=None,
                height=dp(40)
            )
            projects_list_container.add_widget(no_projects_label)
        else:
            for index, project in enumerate(projects):
                project_card = MDCard(
                    size_hint_y=None,
                    height='70dp',
                    elevation=0,
                    ripple_behavior=True,
                    radius=[10, 10, 10, 10],
                    padding=dp(10)
                )
                
                # Adiciona função de clique para confirmar exclusão
                project_card.bind(on_release=lambda x, idx=index, proj=project: self.confirm_delete_project(idx, proj))

                # Layout interno do card
                from kivymd.uix.boxlayout import MDBoxLayout
                card_layout = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(2)
                )
                
                project_name_label = MDLabel(
                    text=project['name'],
                    halign='left',
                    font_style='Subtitle1',
                    bold=True,
                    size_hint_y=None,
                    height=dp(25)
                )
                
                num_plots = len(project.get('plots', []))
                plot_count_text = f"{num_plots} parcela" if num_plots == 1 else f"{num_plots} parcelas"
                project_info_label = MDLabel(
                    text=plot_count_text,
                    halign='left',
                    font_style='Caption',
                    size_hint_y=None,
                    height=dp(18)
                )
                
                card_layout.add_widget(project_name_label)
                card_layout.add_widget(project_info_label)
                project_card.add_widget(card_layout)
                projects_list_container.add_widget(project_card)
    
    def confirm_delete_project(self, project_index, project):
        """Mostra diálogo de confirmação para excluir projeto."""
        project_name = project.get('name', 'este projeto')
        
        if not hasattr(self, 'delete_project_dialog') or not self.delete_project_dialog:
            self.delete_project_dialog = MDDialog(
                title='Excluir Projeto',
                text=f'Deseja realmente excluir o projeto "{project_name}"?\nTodos os dados serão perdidos.',
                buttons=[
                    MDFlatButton(
                        text='CANCELAR',
                        on_release=lambda x: self.delete_project_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text='EXCLUIR',
                        on_release=lambda x: self.delete_project(project_index, project_name)
                    ),
                ],
            )
        else:
            self.delete_project_dialog.text = f'Deseja realmente excluir o projeto "{project_name}"?\nTodos os dados serão perdidos.'
            # Atualiza o botão de excluir com o novo callback
            self.delete_project_dialog.buttons[1].unbind(on_release=self.delete_project_dialog.buttons[1].on_release)
            self.delete_project_dialog.buttons[1].bind(on_release=lambda x: self.delete_project(project_index, project_name))
        
        self.delete_project_dialog.open()
    
    def delete_project(self, project_index, project_name):
        """Executa a exclusão do projeto."""
        if self.delete_project_dialog:
            self.delete_project_dialog.dismiss()
        
        # Remove o projeto da lista
        if 0 <= project_index < len(projects_data.get('projects', [])):
            projects_data['projects'].pop(project_index)
            data.save_data(projects_data, JSON_FILE)
            
            self.show_success_dialog('Projeto Excluído', f'O projeto "{project_name}" foi excluído com sucesso!')
            self.go_to_screen('my_projects_screen')
    
    # ==================== DIÁLOGOS UTILITÁRIOS ====================
    
    def show_info_dialog(self, title, message):
        """Exibe diálogo informativo simples."""
        info_dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text='OK',
                    on_release=lambda x: info_dialog.dismiss()
                ),
            ],
        )
        info_dialog.open()
    
    def show_success_dialog(self, title, message):
        """Exibe diálogo de sucesso."""
        self.show_info_dialog(title, message)
    
    def open_url(self, url):
        """Abre uma URL no navegador padrão."""
        webbrowser.open(url)
    
    # ==================== VISUALIZAÇÃO DE PROJETOS ====================
    
    def open_project(self, project_index):
        """Abre projeto específico para visualização."""
        self.current_project_index = project_index
        self.current_project = projects_data.get('projects', [])[project_index]
        self.go_to_screen('view_project_screen')
    
    def load_project_details(self):
        """Carrega os detalhes do projeto atual na tela."""
        if not self.current_project:
            return
        
        screen = self.root.get_screen('view_project_screen')
        
        # Atualiza as informações do projeto
        screen.ids.project_name_label.text = self.current_project.get('name', '')
        
        # Carrega a lista de parcelas
        self.load_plots_list()
    
    def load_plots_list(self):
        """Carrega a lista de parcelas do projeto atual."""
        if not self.current_project:
            return
        
        plots_list = self.root.get_screen('view_project_screen').ids.plots_list_container
        plots_list.clear_widgets()
        
        plots = self.current_project.get('plots', [])
        
        if not plots:
            no_plots_label = MDLabel(
                text='Nenhuma parcela adicionada ainda',
                halign='center',
                font_style='Body1',
                size_hint_y=None,
                height=dp(40)
            )
            plots_list.add_widget(no_plots_label)
        else:
            for index, plot in enumerate(plots):
                # Layout interno do card
                from kivymd.uix.boxlayout import MDBoxLayout
                card_layout = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(4),
                    size_hint_y=None,
                    padding=0
                )
                card_layout.bind(minimum_height=card_layout.setter('height'))
                
                # Título da parcela
                plot_title = MDLabel(
                    text=f"Parcela {index + 1}",
                    halign='left',
                    font_style='Subtitle1',
                    bold=True,
                    size_hint_y=None
                )
                plot_title.bind(
                    width=lambda instance, value: setattr(instance, 'text_size', (value, None))
                )
                plot_title.bind(
                    texture_size=lambda instance, value: setattr(instance, 'height', value[1] + dp(4))
                )
                
                # Coordenadas e fórmula
                plot_coords = ''
                if 'latitude' in plot and 'longitude' in plot:
                    plot_coords = f"Lat: {plot['latitude']}, Long: {plot['longitude']}"
                    # Adicionar fórmula se disponível
                    if 'formula_kuchler' in plot and plot['formula_kuchler']:
                        plot_coords += f" | Fórmula: {plot['formula_kuchler']}"
                else:
                    plot_coords = 'Sem coordenadas'
                
                plot_coords_label = MDLabel(
                    text=plot_coords,
                    halign='left',
                    font_style='Caption',
                    size_hint_y=None
                )
                # Permitir quebra de linha para coordenadas/fórmula
                plot_coords_label.bind(
                    width=lambda instance, value: setattr(instance, 'text_size', (value, None))
                )
                plot_coords_label.bind(
                    texture_size=lambda instance, value: setattr(instance, 'height', value[1] + dp(4))
                )
                
                # Data e horário de registro
                datetime_text = ''
                if 'data_registro' in plot and 'horario_registro' in plot:
                    datetime_text = f"Registrado em: {plot['data_registro']} às {plot['horario_registro']}"
                elif 'data_registro' in plot:
                    datetime_text = f"Registrado em: {plot['data_registro']}"
                else:
                    datetime_text = 'Data de registro não disponível'
                
                plot_datetime_label = MDLabel(
                    text=datetime_text,
                    halign='left',
                    font_style='Caption',
                    size_hint_y=None
                )
                # Permitir quebra de linha para data/hora
                plot_datetime_label.bind(
                    width=lambda instance, value: setattr(instance, 'text_size', (value, None))
                )
                plot_datetime_label.bind(
                    texture_size=lambda instance, value: setattr(instance, 'height', value[1] + dp(4))
                )
                
                # Adicionar widgets ao layout
                card_layout.add_widget(plot_title)
                card_layout.add_widget(plot_coords_label)
                card_layout.add_widget(plot_datetime_label)
                
                # Descrição fisionômica (com altura adaptativa)
                if 'descricao_fisionomia' in plot and plot['descricao_fisionomia']:
                    plot_description_label = MDLabel(
                        text=plot['descricao_fisionomia'],
                        halign='left',
                        font_style='Caption',
                        size_hint_y=None,
                        markup=True
                    )
                    # Permitir quebra de linha e ajustar altura automaticamente
                    plot_description_label.bind(
                        width=lambda instance, value: setattr(instance, 'text_size', (value, None))
                    )
                    plot_description_label.bind(
                        texture_size=lambda instance, value: setattr(instance, 'height', value[1] + dp(4))
                    )
                    card_layout.add_widget(plot_description_label)
                
                # Criar o card com altura adaptativa
                plot_card = MDCard(
                    size_hint_y=None,
                    elevation=0,
                    ripple_behavior=True,
                    radius=[10, 10, 10, 10],
                    padding=dp(10),
                    line_color=(0.7, 0.7, 0.7, 1),
                    style="outlined"
                )
                plot_card.add_widget(card_layout)
                
                # Ajustar altura do card baseado no conteúdo (usando factory para evitar closure)
                def make_update_func(card, layout):
                    def update_height(instance, value):
                        card.height = layout.height + dp(20)
                    return update_height
                
                card_layout.bind(height=make_update_func(plot_card, card_layout))
                
                plots_list.add_widget(plot_card)
    
    def go_to_new_plot(self):
        """Navega para a tela de adicionar nova parcela."""
        if self.current_project:
            self.go_to_screen('new_plot_screen1')
    
    def validate_and_save_plot_step1(self):
        """Valida e salva dados da etapa 1 (coordenadas e altitude)."""
        screen = self.root.get_screen('new_plot_screen1')
        latitude_text = screen.ids.latitude_input.text.strip()
        longitude_text = screen.ids.longitude_input.text.strip()
        altitude_text = screen.ids.altitude_input.text.strip()
        
        # Validação de campos vazios
        if not latitude_text or not longitude_text or not altitude_text:
            self.show_info_dialog('Campos Obrigatórios', 'Por favor, preencha todos os campos.')
            return
        
        # Validação de valores numéricos
        try:
            latitude = float(latitude_text)
            longitude = float(longitude_text)
            altitude = float(altitude_text)
        except ValueError:
            self.show_info_dialog('Valores Inválidos', 'Por favor, insira valores numéricos válidos.')
            return
        
        # Validação de intervalos
        if not (-90 <= latitude <= 90):
            self.show_info_dialog('Latitude Inválida', 'A latitude deve estar entre -90 e 90 graus.')
            return
        
        if not (-180 <= longitude <= 180):
            self.show_info_dialog('Longitude Inválida', 'A longitude deve estar entre -180 e 180 graus.')
            return
        
        if altitude < 0:
            self.show_info_dialog('Altitude Inválida', 'A altitude deve ser maior ou igual a zero.')
            return
        
        # Armazena os dados temporariamente
        if not hasattr(self, 'temp_plot_data'):
            self.temp_plot_data = {'matriz_fisionomica': {}}
        
        if 'matriz_fisionomica' not in self.temp_plot_data:
            self.temp_plot_data['matriz_fisionomica'] = {}
        
        self.temp_plot_data['latitude'] = latitude
        self.temp_plot_data['longitude'] = longitude
        self.temp_plot_data['altitude'] = altitude
        
        # Limpa os campos
        screen.ids.latitude_input.text = ''
        screen.ids.longitude_input.text = ''
        screen.ids.altitude_input.text = ''
        
        # Limpa a matriz antes de navegar
        self.clear_matriz_interface()
        
        # Navega para a próxima tela
        self.go_to_screen('new_plot_screen2')
    
    def show_matriz_help(self):
        """Mostra diálogo com guia rápido de uso da matriz."""
        help_text = (
            "ORIENTAÇÃO INICIAL:\n"
            "Busque uma área de HOMOGENEIDADE da vegetação para realizar o registro. "
            "A parcela deve representar uma unidade fisionômica uniforme.\n\n"
            "GUIA RÁPIDO: INVENTÁRIO FISIONÔMICO\n\n"
            "1. Registro: Comece pela altura mais elevada.\n"
            "2. Cobertura: Insira os códigos (c, i, p, r, b, a).\n"
            "Consulte a caderneta para mais detalhes."
        )
        
        help_dialog = MDDialog(
            title='Guia de Uso',
            text=help_text,
            size_hint=(0.9, None),
            height=dp(400),
            buttons=[
                MDFlatButton(
                    text='ENTENDI',
                    on_release=lambda x: help_dialog.dismiss()
                ),
            ],
        )
        help_dialog.open()
    
    def clear_matriz_interface(self):
        """Limpa todas as células da matriz fisionômica na interface."""
        try:
            screen = self.root.get_screen('new_plot_screen2')
            if not hasattr(screen, 'ids'):
                return
            
            # Limpa todas as células usando constantes globais
            for form in LIFE_FORMS:
                for height in HEIGHT_CLASSES:
                    cell_id = f"cell_{form}{height}"
                    if cell_id in screen.ids:
                        screen.ids[cell_id].text = ""
        except Exception as e:
            print(f"Erro ao limpar interface da matriz: {e}")
    
    def select_matriz_cell(self, forma, altura):
        """Exibe diálogo para selecionar classe de cobertura de uma célula."""
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.button import MDRaisedButton
        
        # Cria layout para os botões
        content = MDBoxLayout(
            orientation='vertical',
            spacing="12dp",
            size_hint_y=None,
            height="360dp",
            padding="20dp"
        )
        
        # Classes de cobertura
        coberturas = [
            ('c', 'contínua (>75%)'),
            ('i', 'interrompida (51-75%)'),
            ('p', 'porosa (26-50%)'),
            ('r', 'rara (6-25%)'),
            ('b', 'baixa (1-5%)'),
            ('a', 'ausente (<1%)')
        ]
        
        for cob, desc in coberturas:
            btn = MDRaisedButton(
                text=f"{cob} - {desc}",
                size_hint_x=1,
                on_release=lambda x, c=cob: self.set_cobertura_cell(forma, altura, c)
            )
            content.add_widget(btn)
        
        self.cobertura_dialog = MDDialog(
            title=f"{forma}{altura} - {self.get_altura_range(altura)}",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text='Limpar célula',
                    on_release=lambda x: self.clear_matriz_cell(forma, altura)
                ),
                MDFlatButton(
                    text='Cancelar',
                    on_release=lambda x: self.cobertura_dialog.dismiss()
                ),
            ],
        )
        self.cobertura_dialog.open()
    
    def get_altura_range(self, altura):
        """Retorna o range de altura em texto."""
        ranges = {
            '8': '>35m',
            '7': '20-35m',
            '6': '10-20m',
            '5': '5-10m',
            '4': '2-5m',
            '3': '0.5-2m',
            '2': '0.1-0.5m',
            '1': '<0.1m'
        }
        return ranges.get(altura, '')
    
    def set_cobertura_cell(self, forma, altura, cobertura):
        """Salva a combinação forma-altura-cobertura na célula."""
        key = f"{forma}{altura}"
        self.temp_plot_data['matriz_fisionomica'][key] = cobertura
        self.cobertura_dialog.dismiss()
        self.update_matriz_cell_display(forma, altura)
    
    def clear_matriz_cell(self, forma, altura):
        """Limpa uma célula da matriz."""
        key = f"{forma}{altura}"
        if key in self.temp_plot_data['matriz_fisionomica']:
            del self.temp_plot_data['matriz_fisionomica'][key]
        self.cobertura_dialog.dismiss()
        self.update_matriz_cell_display(forma, altura)
    
    def update_matriz_cell_display(self, forma, altura):
        """Atualiza a exibição de uma célula específica da matriz."""
        try:
            key = f"{forma}{altura}"
            screen = self.root.get_screen('new_plot_screen2')
            cell_id = f"cell_{forma}{altura}"
            
            if hasattr(screen, 'ids') and cell_id in screen.ids:
                if key in self.temp_plot_data['matriz_fisionomica']:
                    cobertura = self.temp_plot_data['matriz_fisionomica'][key]
                    screen.ids[cell_id].text = cobertura.lower()
                else:
                    screen.ids[cell_id].text = ""
        except Exception as e:
            print(f"Erro ao atualizar célula {forma}{altura}: {e}")
    
    def select_folha_cell(self, altura):
        """Mostra diálogo para selecionar características de folhas."""
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.button import MDRaisedButton
        
        # Cria layout para os botões
        content = MDBoxLayout(
            orientation='vertical',
            spacing="12dp",
            size_hint_y=None,
            height="300dp",
            padding="20dp"
        )
        
        # Características de folhas
        folhas = [
            ('h', 'h - rígida (esclerófila)'),
            ('w', 'w - maleável'),
            ('k', 'k - suculenta'),
            ('l', 'l - grande (>400 cm²)'),
            ('s', 's - pequena (<4 cm²)')
        ]
        
        for fol, desc in folhas:
            btn = MDRaisedButton(
                text=desc,
                size_hint_x=1,
                on_release=lambda x, f=fol: self.set_folha_cell(altura, f)
            )
            content.add_widget(btn)
        
        self.folha_dialog = MDDialog(
            title=f"Folhas - Altura {altura}",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text='Limpar célula',
                    on_release=lambda x: self.clear_folha_cell(altura)
                ),
                MDFlatButton(
                    text='Cancelar',
                    on_release=lambda x: self.folha_dialog.dismiss()
                ),
            ],
        )
        self.folha_dialog.open()
    
    def set_folha_cell(self, altura, folha):
        """Salva a característica de folha."""
        key = f"F{altura}"
        self.temp_plot_data['matriz_fisionomica'][key] = folha
        self.folha_dialog.dismiss()
        self.update_folha_cell_display(altura)
    
    def clear_folha_cell(self, altura):
        """Limpa uma célula de folha."""
        key = f"F{altura}"
        if key in self.temp_plot_data['matriz_fisionomica']:
            del self.temp_plot_data['matriz_fisionomica'][key]
        self.folha_dialog.dismiss()
        self.update_folha_cell_display(altura)
    
    def update_folha_cell_display(self, altura):
        """Atualiza a exibição de uma célula de folha."""
        try:
            key = f"F{altura}"
            screen = self.root.get_screen('new_plot_screen2')
            cell_id = f"cell_F{altura}"
            
            if hasattr(screen, 'ids') and cell_id in screen.ids:
                if key in self.temp_plot_data['matriz_fisionomica']:
                    folha = self.temp_plot_data['matriz_fisionomica'][key]
                    screen.ids[cell_id].text = folha.lower()
                else:
                    screen.ids[cell_id].text = ""
        except Exception as e:
            print(f"Erro ao atualizar célula de folha {altura}: {e}")
    
    def finalize_and_save_plot(self):
        """Finaliza e salva a parcela completa."""
        if not self.current_project:
            self.show_info_dialog('Erro', 'Nenhum projeto selecionado.')
            return
        
        # Verifica se há dados da matriz
        if not self.temp_plot_data.get('matriz_fisionomica'):
            self.show_info_dialog('Matriz Vazia', 'Por favor, preencha pelo menos uma célula da matriz fisionômica.')
            return
        
        # Obtém data e horário atual
        now = datetime.now()
        data_registro = now.strftime('%d/%m/%Y')
        horario_registro = now.strftime('%H:%M:%S')
        
        # Gera a fórmula de Küchler e a descrição
        matriz_data = self.temp_plot_data.get('matriz_fisionomica', {})
        formula_kuchler = kuchler_calculator.generate_kuchler_formula(matriz_data)
        descricao_fisionomia = kuchler_calculator.generate_formula_description(matriz_data)
        
        # Cria a nova parcela
        new_plot = {
            'latitude': self.temp_plot_data.get('latitude', 0),
            'longitude': self.temp_plot_data.get('longitude', 0),
            'altitude': self.temp_plot_data.get('altitude', 0),
            'matriz_fisionomica': self.temp_plot_data.get('matriz_fisionomica', {}),
            'data_registro': data_registro,
            'horario_registro': horario_registro,
            'formula_kuchler': formula_kuchler,
            'descricao_fisionomia': descricao_fisionomia
        }
        
        # Adiciona a parcela ao projeto atual
        if 'plots' not in self.current_project:
            self.current_project['plots'] = []
        
        self.current_project['plots'].append(new_plot)
        
        # Salva os dados atualizados
        data.save_data(projects_data, JSON_FILE)
        
        # Limpa os dados temporários
        self.temp_plot_data = {'matriz_fisionomica': {}}
        
        # Mostra diálogo de confirmação com opções
        self.show_plot_saved_confirmation()
    
    def show_plot_saved_confirmation(self):
        """Mostra diálogo de confirmação após salvar parcela."""
        project_name = self.current_project.get('name', 'Sem nome')
        num_plots = len(self.current_project.get('plots', []))
        
        dialog = MDDialog(
            title='Parcela Salva com Sucesso!',
            text=f'A parcela foi adicionada ao projeto "{project_name}".\nTotal de parcelas: {num_plots}',
            buttons=[
                MDFlatButton(
                    text='Ver Parcelas do Projeto',
                    on_release=lambda x: self.go_to_screen('view_project_screen', dialog)
                ),
                MDFlatButton(
                    text='Criar Nova Parcela',
                    on_release=lambda x: self.go_to_screen('new_plot_screen1', dialog)
                ),
            ],
        )
        dialog.open()
    
    def go_to_delete_plots(self):
        """Navega para a tela de excluir parcelas."""
        if not self.current_project or not self.current_project.get('plots', []):
            self.show_info_dialog('Sem Parcelas', 'Este projeto ainda não possui parcelas para excluir.')
            return
        self.go_to_screen('delete_plot_screen')
    
    def load_delete_plots_list(self):
        """Carrega a lista de parcelas para exclusão."""
        if not self.current_project:
            return
        
        plots_list_container = self.root.get_screen('delete_plot_screen').ids.delete_plots_list_container
        plots_list_container.clear_widgets()

        plots = self.current_project.get('plots', [])
        
        if not plots:
            no_plots_label = MDLabel(
                text='Nenhuma parcela cadastrada',
                halign='center',
                font_style='Body1',
                size_hint_y=None,
                height=dp(40)
            )
            plots_list_container.add_widget(no_plots_label)
        else:
            for index, plot in enumerate(plots):
                plot_card = MDCard(
                    size_hint_y=None,
                    height='85dp',
                    elevation=0,
                    ripple_behavior=True,
                    radius=[10, 10, 10, 10],
                    padding=dp(10)
                )
                
                # Adiciona função de clique para confirmar exclusão
                plot_card.bind(on_release=lambda x, idx=index, plt=plot: self.confirm_delete_single_plot(idx, plt))

                # Layout interno do card
                from kivymd.uix.boxlayout import MDBoxLayout
                card_layout = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(2)
                )
                
                plot_name_label = MDLabel(
                    text=f'Parcela {index + 1}',
                    halign='left',
                    font_style='Subtitle1',
                    bold=True,
                    size_hint_y=None,
                    height=dp(25)
                )
                
                plot_info_text = ''
                if 'latitude' in plot and 'longitude' in plot:
                    plot_info_text = f"Lat: {plot['latitude']}, Long: {plot['longitude']}"
                    # Adicionar fórmula se disponível
                    if 'formula_kuchler' in plot and plot['formula_kuchler']:
                        plot_info_text += f" | Fórmula: {plot['formula_kuchler']}"
                elif 'location' in plot:
                    plot_info_text = f"Localização: {plot['location']}"
                else:
                    plot_info_text = 'Dados da parcela'
                    
                plot_info_label = MDLabel(
                    text=plot_info_text,
                    halign='left',
                    font_style='Caption',
                    size_hint_y=None,
                    height=dp(18)
                )
                
                # Data e horário de registro
                datetime_text = ''
                if 'data_registro' in plot and 'horario_registro' in plot:
                    datetime_text = f"Registrado: {plot['data_registro']} às {plot['horario_registro']}"
                elif 'data_registro' in plot:
                    datetime_text = f"Registrado: {plot['data_registro']}"
                else:
                    datetime_text = 'Sem data de registro'
                
                plot_datetime_label = MDLabel(
                    text=datetime_text,
                    halign='left',
                    font_style='Caption',
                    size_hint_y=None,
                    height=dp(18)
                )
                
                card_layout.add_widget(plot_name_label)
                card_layout.add_widget(plot_info_label)
                card_layout.add_widget(plot_datetime_label)
                plot_card.add_widget(card_layout)
                plots_list_container.add_widget(plot_card)
    
    def confirm_delete_single_plot(self, plot_index, plot):
        """Mostra diálogo de confirmação para excluir parcela."""
        if not hasattr(self, 'delete_single_plot_dialog') or not self.delete_single_plot_dialog:
            self.delete_single_plot_dialog = MDDialog(
                title='Excluir Parcela',
                text=f'Deseja realmente excluir a Parcela {plot_index + 1}?\nTodos os dados serão perdidos.',
                buttons=[
                    MDFlatButton(
                        text='CANCELAR',
                        on_release=lambda x: self.delete_single_plot_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text='EXCLUIR',
                        on_release=lambda x: self.delete_single_plot(plot_index)
                    ),
                ],
            )
        else:
            self.delete_single_plot_dialog.text = f'Deseja realmente excluir a Parcela {plot_index + 1}?\nTodos os dados serão perdidos.'
            # Atualiza o botão de excluir com o novo callback
            self.delete_single_plot_dialog.buttons[1].unbind(on_release=self.delete_single_plot_dialog.buttons[1].on_release)
            self.delete_single_plot_dialog.buttons[1].bind(on_release=lambda x: self.delete_single_plot(plot_index))
        
        self.delete_single_plot_dialog.open()
    
    def delete_single_plot(self, plot_index):
        """Executa a exclusão da parcela."""
        if self.delete_single_plot_dialog:
            self.delete_single_plot_dialog.dismiss()
        
        # Remove a parcela da lista
        if self.current_project and 0 <= plot_index < len(self.current_project.get('plots', [])):
            self.current_project['plots'].pop(plot_index)
            
            # Atualiza os dados no arquivo
            projects_data['projects'][self.current_project_index] = self.current_project
            data.save_data(projects_data, JSON_FILE)
            
            # Mostra diálogo de confirmação
            self.show_success_dialog('Parcela Excluída', f'A Parcela {plot_index + 1} foi excluída com sucesso!')
            
            # Volta para a tela de detalhes do projeto
            self.go_to_screen('view_project_screen')
    
    def export_project_to_csv(self):
        """Exporta o projeto atual para um arquivo CSV."""
        if not self.current_project:
            return
        
        plots = self.current_project.get('plots', [])
        
        if not plots:
            # Mostra diálogo se não houver parcelas
            self.show_info_dialog('Sem Parcelas', 'Este projeto ainda não possui parcelas para exportar.')
            return
        
        # Cria a pasta exports se não existir
        exports_dir = 'exports'
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)
        
        # Nome do arquivo com timestamp
        project_name = self.current_project.get('name', 'projeto')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{project_name}_{timestamp}.csv"
        filepath = os.path.join(exports_dir, filename)
        
        # Coleta todas as chaves possíveis das parcelas
        all_keys = set()
        for plot in plots:
            all_keys.update(plot.keys())
        
        # Ordena as chaves para manter consistência
        # Garante que descricao_fisionomia seja o último campo
        fieldnames = sorted(list(all_keys))
        if 'descricao_fisionomia' in fieldnames:
            fieldnames.remove('descricao_fisionomia')
            fieldnames.append('descricao_fisionomia')
        
        # Escreve o arquivo CSV
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(plots)
            
            # Mostra confirmação
            self.show_export_success(filename)
        except Exception as e:
            print(f"Erro ao exportar CSV: {e}")
    
    def show_export_success(self, filename):
        """Mostra diálogo de sucesso após exportar."""
        success_dialog = MDDialog(
            title='Exportação Concluída',
            text=f'Projeto exportado com sucesso!\nArquivo: {filename}',
            buttons=[
                MDFlatButton(
                    text='OK',
                    on_release=lambda x: success_dialog.dismiss()
                ),
            ],
        )
        success_dialog.open()
    
    # Funções de configuração do tema
    def load_settings(self):
        """Carrega as configurações salvas do arquivo JSON."""
        settings = projects_data.get('settings', {})
        
        # Aplica o tema
        theme_style = settings.get('theme_style', 'Light')
        self.theme_cls.theme_style = theme_style
        
        # Aplica a cor primária
        primary_color = settings.get('primary_color', 'Blue')
        if primary_color in self.colors:
            self.theme_cls.primary_palette = self.colors[primary_color]
    
    def save_settings(self):
        """Salva as configurações atuais no arquivo JSON."""
        projects_data['settings'] = {
            'theme_style': self.theme_cls.theme_style,
            'primary_color': self.theme_cls.primary_palette
        }
        data.save_data(projects_data, JSON_FILE)
    
    def toggle_theme_and_save(self):
        """Alterna entre tema claro e escuro e salva."""
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.theme_style = 'Dark'
        else:
            self.theme_cls.theme_style = 'Light'
        self.save_settings()
    
    def change_color_and_save(self, color_name):
        """Muda a cor primária do aplicativo e salva."""
        if color_name in self.colors:
            self.theme_cls.primary_palette = self.colors[color_name]
            self.save_settings()
    


class MenuScreen(Screen):
    pass

class MyProjectsScreen(Screen):
    pass

class NewProjectScreen(Screen):
    pass

class DeleteProjectScreen(Screen):
    pass

class ViewProjectScreen(Screen):
    pass

class DeletePlotScreen(Screen):
    pass

class NewPlotScreen1(Screen):
    pass

class NewPlotScreen2(Screen):
    pass

class SettingsScreen(Screen):
    pass

class AboutAppScreen(Screen):
    pass


# Execução do aplicativo
if __name__ == '__main__':
    KuchlerInventoryApp().run()