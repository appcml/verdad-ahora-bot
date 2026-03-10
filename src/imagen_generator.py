#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import os
from .utils import log, generar_hash
from .config import IMAGEN_CONFIG

class GeneradorImagenesViral:
    def __init__(self):
        self.width = IMAGEN_CONFIG['width']
        self.height = IMAGEN_CONFIG['height']
    
    def crear_imagen_viral(self, titulo, estilo='urgente'):
        """
        Crea imágenes optimizadas para alto engagement en Facebook
        """
        # Seleccionar paleta según estilo
        colores = self._seleccionar_paleta(estilo)
        
        # Crear imagen base con gradiente
        img = Image.new('RGB', (self.width, self.height), color=colores['fondo'])
        draw = ImageDraw.Draw(img)
        
        # Añadir elementos visuales llamativos
        self._dibujar_elementos_fondo(draw, colores, estilo)
        
        # Cargar fuentes
        try:
            font_titulo = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56
            )
            font_sub = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32
            )
        except:
            font_titulo = ImageFont.load_default()
            font_sub = ImageFont.load_default()
        
        # Preparar texto
        titulo_envuelto = self._envolver_texto(titulo, 25)
        
        # Calcular posición centrada
        bbox = draw.textbbox((0, 0), titulo_envuelto, font=font_titulo)
        altura_texto = bbox[3] - bbox[1]
        y_pos = (self.height - altura_texto) // 2 - 50
        
        # Dibujar caja de contraste
        padding = 40
        draw.rectangle(
            [50, y_pos - padding, self.width - 50, y_pos + altura_texto + padding],
            fill=(0, 0, 0, 180)
        )
        
        # Dibujar texto con borde para legibilidad
        self._dibujar_texto_con_borde(
            draw, titulo_envuelto, (self.width//2, y_pos), 
            font_titulo, colores['texto'], colores['borde']
        )
        
        # Añadir marca y elementos de urgencia
        self._añadir_marca_urgencia(draw, font_sub, colores)
        
        # Guardar
        filename = f'/tmp/verdadahora_{generar_hash(titulo)}.jpg'
        img.save(filename, 'JPEG', quality=90)
        log(f"Imagen viral creada: {filename}", 'exito')
        
        return filename
    
    def _seleccionar_paleta(self, estilo):
        """Selecciona colores según el estilo emocional"""
        paletas = {
            'urgente': {
                'fondo': '#DC143C',  # Rojo crimson
                'texto': '#FFFFFF',
                'borde': '#8B0000',
                'acento': '#FFD700'
            },
            'ironico': {
                'fondo': '#2C3E50',  # Azul oscuro
                'texto': '#ECF0F1',
                'borde': '#34495E',
                'acento': '#E74C3C'
            },
            'intrigante': {
                'fondo': '#1A1A2E',  # Negro azulado
                'texto': '#E94560',
                'borde': '#16213E',
                'acento': '#0F3460'
            },
            'critico': {
                'fondo': '#000000',  # Negro
                'texto': '#FFFFFF',
                'borde': '#434343',
                'acento': '#FF0000'
            }
        }
        return paletas.get(estilo, paletas['urgente'])
    
    def _dibujar_elementos_fondo(self, draw, colores, estilo):
        """Añade elementos gráficos llamativos"""
        import random
        
        # Líneas diagonales de urgencia
        for i in range(0, self.width, 100):
            draw.line([(i, 0), (i + 50, self.height)], 
                     fill=colores['acento'], width=3)
        
        # Bordes gruesos
        draw.rectangle([0, 0, self.width-1, self.height-1], 
                      outline=colores['acento'], width=10)
        
        # Esquinas destacadas
        tam_esquina = 80
        # Esquina superior izquierda
        draw.line([(0, tam_esquina), (0, 0), (tam_esquina, 0)], 
                 fill=colores['acento'], width=8)
        # Esquina inferior derecha
        draw.line([(self.width-tam_esquina, self.height), 
                  (self.width, self.height), 
                  (self.width, self.height-tam_esquina)], 
                 fill=colores['acento'], width=8)
    
    def _envolver_texto(self, texto, ancho):
        """Envuelve texto manteniendo palabras completas"""
        lineas = textwrap.wrap(texto.upper(), width=ancho)
        return '\n'.join(lineas)
    
    def _dibujar_texto_con_borde(self, draw, texto, pos, font, color, color_borde):
        """Dibuja texto con efecto de borde para mejor legibilidad"""
        x, y = pos[0], pos[1]
        
        # Dibujar borde
        for dx, dy in [(-2,-2), (-2,2), (2,-2), (2,2), (0,-2), (0,2), (-2,0), (2,0)]:
            draw.text((x + dx, y + dy), texto, font=font, fill=color_borde, anchor="mm")
        
        # Dibujar texto principal
        draw.text((x, y), texto, font=font, fill=color, anchor="mm")
    
    def _añadir_marca_urgencia(self, draw, font, colores):
        """Añade marca y elementos de 'breaking news'"""
        # Banner superior
        draw.rectangle([0, 0, self.width, 60], fill=colores['acento'])
        draw.text((self.width//2, 30), "🔴 VERDAD AHORA - ÚLTIMA HORA", 
                 font=font, fill='#000000', anchor="mm")
        
        # Footer
        draw.rectangle([0, self.height-40, self.width, self.height], 
                      fill=(0, 0, 0, 200))
        draw.text((self.width//2, self.height-20), 
                 "📢 Información sin censura | Comparte", 
                 font=font, fill='#FFFFFF', anchor="mm")
