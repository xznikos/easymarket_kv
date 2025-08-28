# Importações do Kivy para criar a interface
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout  # Layout em forma de caixa vertical ou horizontal
from kivy.uix.textinput import TextInput  # Campo de texto para digitar itens
from kivy.uix.label import Label          # Exibe textos
from kivy.uix.scrollview import ScrollView  # Permite scroll vertical da lista
from kivy.uix.gridlayout import GridLayout  # Layout em grade para organizar itens da lista
from kivy.uix.image import Image          # Para mostrar logo ou imagens
from kivy.graphics import Color, RoundedRectangle  # Para desenhar botões arredondados e fundos
from kivy.uix.widget import Widget        # Widget genérico
from kivy.uix.behaviors import ButtonBehavior  # Para criar botões customizados

# ----------- Configurações de estilo ------------
COR_FUNDO = (0.05, 0.05, 0.05, 1)           # Cor de fundo da janela (preto escuro)
COR_TEXTO = (1, 1, 1, 1)                    # Cor do texto principal (branco)
COR_SUBTITULO = (0.7, 0.7, 0.7, 1)          # Cor do subtítulo (cinza claro)
COR_TEXTO_DESCRICAO = (0.85, 0.85, 0.85, 1)# Cor do texto descritivo
COR_BOTAO_ADICIONAR = (0.2, 0.6, 0.3, 1)   # Cor do botão "Adicionar" (verde)
COR_BOTAO_CONCLUIDO = (0.3, 0.4, 0.8, 1)   # Cor do botão "Concluído" (azul)
COR_BOTAO_APAGAR = (0.8, 0.2, 0.2, 1)      # Cor do botão "Apagar" e "Limpar Lista" (vermelho)
COR_ITEM_CONCLUIDO = (0.2, 0.6, 0.2, 1)    # Cor do texto de item concluído
RAIO_BOTAO = [15]                           # Raio para arredondar os botões

# Configurações da janela
Window.title = "EasyMarket - Sua Lista Inteligente"  # Título da janela
Window.clearcolor = COR_FUNDO                        # Cor de fundo da janela

# -------- Botão arredondado customizado --------
class BotaoArredondado(ButtonBehavior, Widget):
    """
    Botão customizado com cantos arredondados usando RoundedRectangle.
    Herdamos ButtonBehavior para comportar-se como botão e Widget para desenhar.
    """
    def __init__(self, text="", font_size=16, color=(1,1,1,1), background_color=(1,1,1,1), **kwargs):
        super().__init__(**kwargs)  # Inicializa widget base
        self.text = text                     # Texto do botão
        self.font_size = font_size           # Tamanho da fonte
        self.text_color = color              # Cor do texto
        self.background_color = background_color  # Cor de fundo do botão
        self.size_hint = kwargs.get("size_hint", (None, None))  # Sem redimensionamento automático
        self.width = kwargs.get("width", 150)  # Largura do botão
        self.height = kwargs.get("height", 50) # Altura do botão

        # Desenha o botão arredondado
        with self.canvas:
            Color(*self.background_color)                  # Define cor do botão
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=RAIO_BOTAO)  # Desenha retângulo arredondado

        # Atualiza posição e tamanho do retângulo quando o botão muda
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Label do texto dentro do botão
        self.label = Label(text=self.text, font_size=self.font_size, color=self.text_color,
                           halign="center", valign="middle")
        self.add_widget(self.label)                        # Adiciona label ao botão
        self.label.bind(size=self.label.setter("text_size"))  # Ajusta texto ao tamanho do botão

    # Atualiza a posição e tamanho do retângulo e label quando o botão muda de tamanho
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size

# --------- App EasyMarket -----------------------
class EasyMarketApp(App):
    def build(self):
        self.itens = []  # Lista para armazenar os itens adicionados

        # Layout principal da aplicação (vertical)
        layout = BoxLayout(orientation="vertical", padding=[20,20,20,20], spacing=15)

        # ---------- Cabeçalho ----------
        header_layout = BoxLayout(size_hint_y=None, height=200, orientation="vertical", spacing=5, padding=[0,20,0,0])
        
        header_layout.add_widget(Widget(size_hint_y=None, height=20))  # Espaço no topo

        # Tenta adicionar imagem da logo
        try:
            header_layout.add_widget(Image(source="imagens/jpeg.jpeg", size_hint_y=None, height=160,
                                           allow_stretch=True, keep_ratio=True))
        except:
            # Caso não exista imagem, exibe título e subtítulo
            titulo = Label(text="EasyMarket",
                           font_size=32,
                           bold=True,
                           color=COR_TEXTO,
                           size_hint_y=None, height=60)
            subtitulo = Label(text="Sua Lista Inteligente",
                              font_size=18,
                              color=COR_SUBTITULO,
                              size_hint_y=None, height=30)
            header_layout.add_widget(titulo)
            header_layout.add_widget(subtitulo)

        # ---------- Texto descritivo abaixo da logo ----------
        descricao = Label(
            text="Easy Market, seu App para criar listas para a sua compra em mercados de forma rápida e organizada.",
            font_size=16,
            color=COR_TEXTO_DESCRICAO,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=50
        )
        descricao.bind(size=descricao.setter("text_size"))  # Ajusta o texto à largura do label
        header_layout.add_widget(descricao)

        layout.add_widget(header_layout)  # Adiciona cabeçalho ao layout principal

        # ---------- Área de entrada ----------
        entrada_layout = BoxLayout(size_hint_y=None, height=55, spacing=10)

        # Campo para digitar novo item
        self.text_input = TextInput(hint_text="Adicionar novo item...",
                                    multiline=False,
                                    font_size=18,
                                    background_color=(0.1,0.1,0.1,1),
                                    foreground_color=COR_TEXTO,
                                    padding_y=(12,12))
        self.text_input.focus = True  # Foco automático

        # Botão para adicionar item
        botao_adicionar = BotaoArredondado(text="Adicionar",
                                           width=130,
                                           height=50,
                                           background_color=COR_BOTAO_ADICIONAR,
                                           color=COR_TEXTO)
        botao_adicionar.bind(on_press=self.adicionar_item)  # Liga função ao botão

        entrada_layout.add_widget(self.text_input)
        entrada_layout.add_widget(botao_adicionar)

        # ---------- Lista com scroll ----------
        self.scroll = ScrollView(size_hint=(1,1))
        self.lista_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=5)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter('height'))  # Ajusta altura automaticamente
        self.scroll.add_widget(self.lista_layout)

        # ---------- Botão limpar lista ----------
        botao_limpar = BotaoArredondado(text="Limpar Lista",
                                        width=150,
                                        height=50,
                                        background_color=COR_BOTAO_APAGAR,
                                        color=COR_TEXTO)
        botao_limpar.bind(on_press=self.limpar_lista)  # Liga função ao botão

        # Adiciona todos os widgets ao layout principal
        layout.add_widget(entrada_layout)
        layout.add_widget(self.scroll)
        layout.add_widget(botao_limpar)

        return layout

    # ---------- Funções dos botões ----------
    def adicionar_item(self, instance):
        """
        Adiciona item à lista com botões Concluído e Apagar.
        Cada item é um BoxLayout com Label + 2 Botões.
        """
        item = self.text_input.text.strip()
        if item:
            item_layout = BoxLayout(size_hint_y=None, height=50, spacing=5, padding=[5,0])
            
            # Fundo do item (caixa arredondada)
            with item_layout.canvas.before:
                Color(0.15,0.15,0.15,1)
                from kivy.graphics import RoundedRectangle
                rect = RoundedRectangle(pos=item_layout.pos, size=item_layout.size, radius=[10])
                item_layout.bind(pos=lambda inst, val: setattr(rect, 'pos', val))
                item_layout.bind(size=lambda inst, val: setattr(rect, 'size', val))

            # Label do item
            label_item = Label(text=item, halign="left", valign="middle", font_size=20, color=COR_TEXTO)
            label_item.bind(size=label_item.setter('text_size'))

            # Botão concluir
            botao_concluido = BotaoArredondado(text="Concluído", width=110, height=40,
                                               background_color=COR_BOTAO_CONCLUIDO, color=COR_TEXTO, font_size=14)
            botao_concluido.bind(on_press=lambda btn, lbl=label_item: self.marcar_item(lbl))

            # Botão apagar
            botao_apagar = BotaoArredondado(text="Apagar", width=80, height=40,
                                            background_color=COR_BOTAO_APAGAR, color=COR_TEXTO, font_size=14)
            botao_apagar.bind(on_press=lambda btn, layout=item_layout: self.apagar_item(layout))

            # Adiciona label e botões ao layout do item
            item_layout.add_widget(label_item)
            item_layout.add_widget(botao_concluido)
            item_layout.add_widget(botao_apagar)

            # Adiciona item à lista
            self.lista_layout.add_widget(item_layout)
            self.itens.append(item)
            self.text_input.text = ""  # Limpa campo de texto
            self.text_input.focus = True  # Mantém foco

    def marcar_item(self, label):
        """Marca ou desmarca um item como concluído"""
        if "(Concluído)" in label.text:
            label.text = label.text.replace(" (Concluído)","")
            label.color = COR_TEXTO
        else:
            label.text += " (Concluído)"
            label.color = COR_ITEM_CONCLUIDO

    def apagar_item(self, item_layout):
        """Remove um item da lista"""
        self.lista_layout.remove_widget(item_layout)

    def limpar_lista(self, instance):
        """Limpa todos os itens da lista"""
        self.lista_layout.clear_widgets()
        self.itens = []

# ---------- Executa o app ----------
if __name__ == "__main__":
    EasyMarketApp().run()
