#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random
from .utils import log, cargar_json, guardar_json
from .config import FUENTES_NOTICIAS, PAGINAS_REFERENCIA

class AnalizadorEstilo:
    def __init__(self):
        self.estilo_path = 'data/estilo_referencias.json'
        self.estilo = cargar_json(self.estilo_path, {
            'temas_populares': [],
            'formatos_exitosos': [],
            'palabras_clave': []
        })
    
    def obtener_noticias_frescas(self):
        """Obtiene noticias reales de fuentes confiables"""
        import feedparser
        
        noticias = []
        categoria = random.choice(list(FUENTES_NOTICIAS.keys()))
        feeds = FUENTES_NOTICIAS[categoria]
        
        log(f"Buscando noticias en categoría: {categoria}", 'info')
        
        for feed_url in random.sample(feeds, min(2, len(feeds))):
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:3]:
                    noticia = {
                        'titulo': entry.get('title', ''),
                        'resumen': entry.get('summary', entry.get('description', '')),
                        'link': entry.get('link', ''),
                        'categoria': categoria,
                        'fecha': entry.get('published', ''),
                        'fuente': feed.feed.get('title', 'Desconocida')
                    }
                    if noticia['titulo'] and len(noticia['titulo']) > 10:
                        noticias.append(noticia)
            except Exception as e:
                log(f"Error feed {feed_url}: {e}", 'advertencia')
        
        return noticias
    
    def analizar_tendencias(self):
        """Analiza qué tipo de contenido funciona según las referencias"""
        # Simula análisis de las páginas de referencia
        # En producción, esto podría usar datos históricos de engagement
        
        patrones = {
            'horarios_pic': ['08:00', '12:00', '18:00', '21:00'],
            'longitud_ideal': random.randint(100, 280),
            'emojis_top': ['🔥', '🚨', '😱', '⚠️', '💥', '👀', '🤯', '🛑'],
            'temas_virales': [
                'política_controversial', 'tecnología_impacto', 
                'misterios_conspiraciones', 'humor_negro', 'alertas_sociales'
            ]
        }
        return patrones

class GeneradorContenidoViral:
    def __init__(self):
        self.analizador = AnalizadorEstilo()
        self.templates = cargar_json('data/templates_virales.json')
    
    def seleccionar_mejor_noticia(self, noticias):
        """Selecciona la noticia con mayor potencial viral"""
        if not noticias:
            return None
        
        # Puntaje basado en palabras de alto impacto
        palabras_virales = ['crisis', 'polémica', 'escándalo', 'revelan', 'urgente', 
                           'histórico', 'impactante', 'increíble', 'shock', 'alerta']
        
        noticias_puntuadas = []
        for n in noticias:
            texto = f"{n['titulo']} {n['resumen']}".lower()
            puntaje = sum(2 for p in palabras_virales if p in texto)
            puntaje += len([e for e in ['🔥', '🚨', '⚠️'] if e in n['titulo']]) * 3
            noticias_puntuadas.append((puntaje, n))
        
        noticias_puntuadas.sort(reverse=True)
        return noticias_puntuadas[0][1] if noticias_puntuadas else noticias[0]
    
    def crear_variante_viral(self, noticia_original):
        """Transforma una noticia aburrida en contenido viral"""
        from .config import TEMPLATES_ENGAGEMENT
        
        titulo_original = noticia_original['titulo']
        categoria = noticia_original.get('categoria', 'general')
        
        # Seleccionar estilo según categoría
        if categoria == 'tecnologia':
            estilo = 'ironico'
        elif categoria == 'politica':
            estilo = 'critico'
        elif categoria == 'internacional':
            estilo = 'urgente'
        else:
            estilo = random.choice(['urgente', 'intrigante', 'critico'])
        
        # Crear hook inicial
        hook = random.choice(TEMPLATES_ENGAGEMENT['hook_inicial']).format(
            titulo=titulo_original
        )
        
        # Crear cuerpo
        cuerpo_template = random.choice(TEMPLATES_ENGAGEMENT['cuerpo_estilos'][estilo])
        resumen_limpio = self._simplificar_contenido(noticia_original['resumen'])
        cuerpo = cuerpo_template.format(contenido=resumen_limpio)
        
        # Añadir contexto viral
        contexto = self._generar_contexto_engagement(noticia_original)
        
        # Llamada a la acción
        cta = random.choice(TEMPLATES_ENGAGEMENT['llamada_accion'])
        
        # Combinar todo
        texto_completo = f"{hook}\n\n{cuerpo}\n\n{contexto}{cta}"
        
        return {
            'titulo_original': titulo_original,
            'texto_viral': texto_completo,
            'categoria': categoria,
            'estilo': estilo,
            'fuente': noticia_original['fuente'],
            'link_original': noticia_original['link'],
            'hashtags': self._generar_hashtags(categoria, titulo_original)
        }
    
    def _simplificar_contenido(self, texto, max_chars=200):
        """Simplifica el contenido para lectura rápida"""
        import re
        texto = re.sub(r'<[^>]+>', '', texto)
        oraciones = texto.split('.')
        resultado = []
        chars = 0
        
        for oracion in oraciones:
            oracion = oracion.strip()
            if len(oracion) > 20:
                resultado.append(oracion)
                chars += len(oracion)
                if chars > max_chars:
                    break
        
        return '. '.join(resultado) + ('...' if len(texto) > max_chars else '')
    
    def _generar_contexto_engagement(self, noticia):
        """Genera frases que generan curiosidad"""
        frases = [
            f"📍 Fuente: {noticia['fuente']}",
            "⏰ Información actualizada",
            "🔍 Esto cambia todo...",
            "💡 Dato clave que nadie menciona",
        ]
        return random.choice(frases)
    
    def _generar_hashtags(self, categoria, titulo):
        """Genera hashtags relevantes y virales"""
        base = {
            'tecnologia': ['#Tecnología', '#Innovación', '#Futuro'],
            'politica': ['#Política', '#Actualidad', '#Gobierno'],
            'internacional': ['#Internacional', '#Mundo', '#Global'],
            'viral': ['#Viral', '#Tendencia', '#Noticias']
        }
        
        hashtags = base.get(categoria, ['#Noticias', '#Actualidad'])
        hashtags.extend(['#VerdadAhora', '#InformaciónLibre', '#Comparte'])
        
        return ' '.join(hashtags)
